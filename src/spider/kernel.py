from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from typing import Any

from .models import Mechanism, Observation, Resolution, ResolutionStatus
from .registry import MechanismRegistry


_PARAMETER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def _matches(required: dict[str, Any], actual: dict[str, Any]) -> bool:
    return all(actual.get(k) == v for k, v in required.items())


def _template_slots(value: Any) -> set[str]:
    if isinstance(value, str):
        return set(_PARAMETER.findall(value))
    if isinstance(value, dict):
        out: set[str] = set()
        for item in value.values():
            out.update(_template_slots(item))
        return out
    if isinstance(value, list):
        out: set[str] = set()
        for item in value:
            out.update(_template_slots(item))
        return out
    return set()


def _bind(value: Any, params: dict[str, Any]) -> Any:
    if isinstance(value, str):
        full = _PARAMETER.fullmatch(value)
        if full:
            return params[full.group(1)]

        def replace(match: re.Match[str]) -> str:
            return str(params[match.group(1)])

        return _PARAMETER.sub(replace, value)
    if isinstance(value, dict):
        return {k: _bind(v, params) for k, v in value.items()}
    if isinstance(value, list):
        return [_bind(v, params) for v in value]
    return value


# --------------------------------------------------------------------------- #
# Parameter induction
#
# Prereg EXP-PRODUCT-36293260887 section 5 requires that a URL *prefix* survive
# induction. The parent packet's defect was overwriting the entire path value
# with the slot placeholder, so every bound request issued a bare "${id}".
# Induction below therefore works at path-segment granularity: the common
# leading segments are pinned and only the genuinely varying segment positions
# become slots.
# --------------------------------------------------------------------------- #

#: Slot names are derived, not hardcoded, but must be stable for the tests.
_SLOT_BASENAME = "id"

#: Fields that name the RESOURCE rather than the operation. They are constant
#: within a distillation group but differ between resource A and resource B, so
#: retaining them in preconditions would block every cross-resource transfer.
#: This exclusion is hand-declared (as the intent namespace map is, prereg
#: section 12) and is recorded in each mechanism's failure_boundary.
DEFAULT_IDENTITY_FIELDS: tuple[str, ...] = ("collection", "resource")


def _segments(path: str) -> list[str]:
    return [s for s in path.split("/") if s != ""]


def _strip_common_prefix(paths: list[str]) -> str:
    """Longest common leading path SEGMENT prefix, as a URL prefix string.

    Segment granularity (not character granularity) is deliberate: given
    ``/api/v1/items/item-1`` and ``/api/v1/items/item-2`` a character-wise prefix
    would swallow ``item-`` and reduce the slot to the final character.
    """
    if not paths:
        return ""
    split = [_segments(p) for p in paths]
    shared: list[str] = []
    for column in zip(*split):
        if len(set(column)) != 1:
            break
        shared.append(column[0])
    return "/" + "/".join(shared) if shared else ""


def _strip_common_suffix(paths: list[str]) -> list[str]:
    """Trailing segments shared by every path, as a list of segment strings."""
    if not paths:
        return []
    split = [_segments(p) for p in paths]
    shared: list[str] = []
    for column in zip(*[list(reversed(s)) for s in split]):
        if len(set(column)) != 1:
            break
        shared.append(column[0])
    return list(reversed(shared))


def _varying_positions(paths: list[str]) -> list[int]:
    """Indices where the path segment actually differs across observations."""
    if not paths:
        return []
    split = [_segments(p) for p in paths]
    width = min(len(s) for s in split)
    return [i for i in range(width) if len({s[i] for s in split}) > 1]


def _slot_name(index: int) -> str:
    return _SLOT_BASENAME if index == 0 else f"{_SLOT_BASENAME}{index + 1}"


def _path_template(paths: list[str]) -> tuple[str, list[str]]:
    """Return (template_path, slot_names) with the prefix and suffix preserved.

    The head is every leading segment shared by all observations, the tail is the
    shared trailing segment run, and exactly the differing positions in between
    become slots. A slot therefore never absorbs a stable prefix of its own value.
    """
    if not paths:
        return "", []
    split = [_segments(p) for p in paths]
    width = min(len(s) for s in split)
    varying = [i for i in range(width) if len({s[i] for s in split}) > 1]

    head_len = varying[0] if varying else width
    # Shared trailing run, trimmed so it can never overlap a varying position.
    tail: list[str] = []
    limit = head_len
    for column in zip(*[list(reversed(s))[:limit] for s in split]):
        if len(set(column)) != 1:
            break
        tail.append(column[0])
    tail.reverse()

    slots = [_slot_name(i) for i in range(len(varying))]
    head = split[0][:head_len]
    parts = head + [f"${{{name}}}" for name in slots] + tail
    template = "/".join(parts)
    if paths[0].startswith("/"):
        template = "/" + template
    return template, slots


def _is_identifier_value(value: Any, slot_values: set[str]) -> bool:
    """True when a value is (or contains) an induced slot value.

    Postconditions and preconditions that mention a resource-A identifier cannot
    be required of a resource-B mechanism, because the identifiers are disjoint
    by construction. Dropping them is what makes verification transfer, and the
    dropped keys are recorded in the mechanism's failure_boundary.
    """
    if isinstance(value, str):
        return any(sv and sv in value for sv in slot_values)
    return False


def _transferable(
    fields: dict[str, Any], slot_values: set[str], identity_fields: tuple[str, ...]
) -> tuple[dict[str, Any], list[str]]:
    kept: dict[str, Any] = {}
    dropped: list[str] = []
    for key, value in fields.items():
        if key in identity_fields or _is_identifier_value(value, slot_values):
            dropped.append(key)
        else:
            kept[key] = value
    return kept, dropped


class SpiderKernel:
    """Conservative first execution-inheritance kernel.

    This kernel is deliberately not a browser agent. It stores and resolves validated mechanisms.
    It abstains when applicability is not demonstrated.
    """

    def __init__(
        self,
        registry: MechanismRegistry,
        min_confidence: float = 0.8,
        intent_namespace_map: dict[str, list[str]] | None = None,
    ):
        self.registry = registry
        self.min_confidence = min_confidence
        self.intent_namespace_map = intent_namespace_map or {}

    def observe(self, observation: Observation) -> str:
        raw = json.dumps({
            "intent": observation.intent,
            "state": observation.state,
            "action": observation.action,
            "next_state": observation.next_state,
            "success": observation.success,
            "provenance": observation.provenance,
        }, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(raw).hexdigest()

    def distill(self, observation: Observation) -> Mechanism | None:
        """Create only a literal candidate mechanism.

        Generalization/parameter induction is intentionally not guessed here; Research 2.0 must
        earn that capability through C-PARAM-INHERIT and related gates.
        """
        if not observation.success:
            return None
        oid = self.observe(observation)[:16]
        return Mechanism(
            mechanism_id=f"obs-{oid}",
            intent=observation.intent,
            preconditions=dict(observation.state),
            action_template=dict(observation.action),
            postconditions=dict(observation.next_state),
            evidence=[oid],
            confidence=0.5,
        )

    # -- section 5.5: group observations and locate the varying structure ----- #

    def align_parameters(self, observations: list[Observation]) -> dict[str, Any]:
        """Group observations by intent namespace and locate varying structure.

        Returns one alignment record per intent group. No mechanism is built
        here; this is the evidence layer that ``distill_parameterized`` scores.
        """
        groups: dict[str, list[Observation]] = defaultdict(list)
        for observation in observations:
            groups[observation.intent].append(observation)

        alignment: dict[str, Any] = {"intents": {}, "n_observations": len(observations)}
        for intent, members in sorted(groups.items()):
            successes = [o for o in members if o.success]
            paths = [o.action.get("path") for o in members if isinstance(o.action.get("path"), str)]
            varying = _varying_positions(paths) if paths else []
            prefix = _strip_common_prefix(paths)
            slot_values: set[str] = set()
            for observation in members:
                for index in varying:
                    parts = _segments(observation.action.get("path", ""))
                    if index < len(parts):
                        slot_values.add(parts[index])

            # Fields that vary across the group, ignoring the path (handled above).
            keys = {k for o in members for k in o.action if k != "path"}
            varying_body = sorted(
                k for k in keys
                if len({json.dumps(o.action.get(k), sort_keys=True) for o in members}) > 1
            )
            alignment["intents"][intent] = {
                "n": len(members),
                "n_success": len(successes),
                "support": (len(successes) / len(members)) if members else 0.0,
                "common_prefix": prefix,
                "n_prefix_segments": len(_segments(prefix)),
                "varying_segment_positions": varying,
                "n_varying_segments": len(varying),
                "varying_body_fields": varying_body,
                "slot_values": sorted(slot_values),
                "preconditions": _common_fields([o.state for o in members]),
                "postconditions": _common_fields([o.next_state for o in members]),
            }
        return alignment

    # -- section 5.3: build the template, prefix preserved -------------------- #

    def _build_action_template(
        self, observations: list[Observation], identity_fields: tuple[str, ...] = ()
    ) -> dict[str, Any]:
        """Build an action template that PRESERVES the common URL prefix.

        Section 5.4 requires ``_strip_common_prefix`` to be called here rather
        than left as dead code. The slot placeholder replaces only the varying
        segment position, never the whole path value.

        A group whose paths share no leading segment still yields its degenerate
        segment template (for example ``/${id}/${id2}``). It deliberately does
        NOT fall back to a literal first-observation path: silently reusing one
        concrete path would let an under-determined group look concrete, which
        is the failure mode this prereg exists to remove. Confidence and the
        under-determined cap in ``distill_parameterized`` are what stop it.

        When ``identity_fields`` is supplied, a leading path segment whose value
        equals the observation's value for one of those fields becomes a DECLARED
        slot named after the field. Preserving the version/root prefix while
        letting the resource identity be bound is the only way a mechanism
        distilled on one collection can act on another, and the frozen success
        pattern ``/api/v1/<collection>/<slot>`` describes exactly that shape.
        """
        if not observations:
            return {}
        paths = [
            o.action["path"] for o in observations
            if isinstance(o.action.get("path"), str)
        ]
        if not paths:
            return dict(observations[0].action)

        # Section 5.4: the prefix helper is called here, not merely defined.
        prefix = _strip_common_prefix(paths)
        template_path, slots = _path_template(paths)
        if not template_path:
            return dict(observations[0].action)

        declared = self._identity_segment_slots(observations, paths, identity_fields)
        for name, index in declared.items():
            template_path = self._replace_segment(template_path, index, f"${{{name}}}")
            slots = [name if s == index else s for s in slots]
        if declared:
            slots = sorted(set(slots) | set(declared), key=lambda n: template_path.find("${" + n + "}"))

        keys = {k for o in observations for k in o.action if k != "path"}
        template: dict[str, Any] = {}
        for key in sorted(keys):
            values = {json.dumps(o.action.get(key), sort_keys=True) for o in observations}
            if len(values) == 1:
                template[key] = observations[0].action.get(key)
            elif slots and key in {"id", "identifier"}:
                # The identifier slot is shared with the path slot of the same name.
                template[key] = f"${{{slots[0]}}}"
            else:
                template[key] = observations[0].action.get(key)
        template["path"] = template_path
        template["__slots__"] = slots
        template["__declared_slots__"] = sorted(declared)
        return template

    @staticmethod
    def _identity_segment_slots(
        observations: list[Observation], paths: list[str], identity_fields: tuple[str, ...]
    ) -> dict[str, int]:
        """Leading path segments that name the resource rather than the operation.

        Returns {field_name: segment_index} for identity fields that actually
        appear as a path segment. Only leading positions are considered, so a
        trailing identifier can never be mistaken for resource identity.
        """
        out: dict[str, int] = {}
        for field in identity_fields:
            values = {o.state.get(field) for o in observations if o.state.get(field) is not None}
            if len(values) != 1:
                continue
            value = next(iter(values))
            for index, parts in enumerate([_segments(p) for p in paths]):
                if index < len(parts) and parts[index] == str(value):
                    out.setdefault(field, index)
                    break
        return out

    @staticmethod
    def _forced_consistency(observations: list[Observation]) -> float:
        """Fraction of observations sharing the modal non-path action fields.

        Permuting intent labels also permutes the verbs behind them, so this is
        the factor that stops a null arm from manufacturing a confident
        mechanism out of a shuffled label set.
        """
        if not observations:
            return 0.0
        keys = {k for o in observations for k in o.action if k != "path"}
        if not keys:
            return 1.0
        agreeing = 0
        for observation in observations:
            modal = {}
            for key in keys:
                counts = Counter(json.dumps(o.action.get(key), sort_keys=True) for o in observations)
                modal[key] = counts.most_common(1)[0][0]
            if all(json.dumps(observation.action.get(k), sort_keys=True) == modal[k] for k in keys):
                agreeing += 1
        return agreeing / len(observations)

    # -- section 5.1: the parameterized distillation path --------------------- #

    @staticmethod
    def _replace_segment(template: str, index: int, value: str) -> str:
        parts = template.split("/")
        parts[index + 1] = value
        return "/".join(parts)

    def distill_parameterized(
        self,
        observations: list[Observation],
        mechanism_prefix: str = "param",
        intent_namespace_map: dict[str, list[str]] | None = None,
        identity_fields: tuple[str, ...] = DEFAULT_IDENTITY_FIELDS,
        induce_identity_slots: bool = False,
    ) -> list[Mechanism]:
        """Induce one mechanism per intent group, with calibrated confidence.

        Confidence is derived from three measured factors and never hardcoded:
        add-one empirical support over the group, the fraction of observations
        that conform to the induced template, and a structural multiplicity
        penalty for templates with several free positions. A template pinning no
        leading path segment with several free positions is under-determined and
        is capped below ``min_confidence`` so ``resolve`` abstains rather than
        emitting an under-determined request.
        """
        alignment = self.align_parameters(observations)
        built: list[Mechanism] = []
        nsmap = intent_namespace_map if intent_namespace_map is not None else self.intent_namespace_map

        for intent, info in alignment["intents"].items():
            if info["n"] == 0:
                continue
            members = [o for o in observations if o.intent == intent]
            slots_for_build = identity_fields if induce_identity_slots else ()
            template = self._build_action_template(members, slots_for_build)
            slots = list(template.pop("__slots__", []))
            declared_slots = set(template.pop("__declared_slots__", []))
            inferred_slots = [s for s in slots if s not in declared_slots]
            slot_values = set(info["slot_values"])

            conforming = 0
            for observation in members:
                path = observation.action.get("path", "")
                if re.match(_template_regex(template.get("path", ""), slots), path):
                    conforming += 1
            consistency = conforming / info["n"] if info["n"] else 0.0
            # The verb and any other non-path action field must also agree.
            consistency *= self._forced_consistency(members)
            # Add-one (Laplace) support: a mechanism supported by finitely many
            # observations is never scored at exactly 1.0, so confidence cannot
            # be a constant wearing a derived name.
            support = (info["n_success"] + 1.0) / (info["n"] + 1.0)
            # Structural specificity applies to INFERRED slots only. A declared
            # identity slot is supplied and checked by the caller, not guessed.
            multiplicity = 1.0 / (1.0 + 0.5 * (len(inferred_slots) - 1)) if inferred_slots else 1.0
            confidence = round(support * consistency * multiplicity, 4)
            # A template pinning NO leading segment while leaving several
            # INFERRED positions free is under-determined: it cannot determine a
            # resource and it cannot be trusted to determine one. That is
            # precisely the parent packet's defect, so it is capped below
            # min_confidence. Declared identity slots do not trigger this.
            pinned = info["n_prefix_segments"] > 0 or bool(declared_slots)
            underdetermined = (not pinned) and len(inferred_slots) > 1
            if underdetermined:
                confidence = min(confidence, 0.5)

            preconditions, dropped_pre = _transferable(info["preconditions"], slot_values, identity_fields)
            postconditions, dropped_post = _transferable(info["postconditions"], slot_values, identity_fields)
            dropped = sorted(set(dropped_pre) | set(dropped_post))

            digest = hashlib.sha256(
                json.dumps([intent, template, slots], sort_keys=True).encode()
            ).hexdigest()[:12]
            built.append(
                Mechanism(
                    mechanism_id=f"{mechanism_prefix}-{intent}-{digest}",
                    intent=intent,
                    preconditions=preconditions,
                    action_template=template,
                    postconditions=postconditions,
                    parameter_slots=slots,
                    auth_scope="bearer",
                    intent_namespace_map=list(nsmap.get(intent, [])) if nsmap else [],
                    freshness={
                        "strategy": "etag-revalidate",
                        "max_stale_requests": 0,
                        "revalidate_before_reuse": True,
                    },
                    applicability_guards={
                        k: v for k, v in info["preconditions"].items()
                        if k not in dropped_pre
                    },
                    verification_rule={
                        "type": "postcondition_match",
                        "postconditions": postconditions,
                    },
                    failure_boundary={
                        "excluded_identifier_keys": dropped,
                        "declared_identity_fields": list(identity_fields),
                        "declared_identity_slots": sorted(declared_slots),
                        "inferred_slots": inferred_slots,
                        "no_empty_prefix_template": not underdetermined,
                        "confidence": confidence,
                        "min_confidence": self.min_confidence,
                    },
                    repair_scope={
                        "rebind_slots": True,
                        "retryable_statuses": ["UNKNOWN", "EXPLORE"],
                    },
                    evidence=[self.observe(o)[:16] for o in members],
                    confidence=confidence,
                )
            )
        return built

    # -- resolution --------------------------------------------------------- #

    def _intent_matches(self, mechanism: Mechanism, intent: str) -> bool:
        """Exact equality, or an alias declared in either direction."""
        if mechanism.intent == intent:
            return True
        if intent in mechanism.intent_namespace_map:
            return True
        return intent in self.intent_namespace_map.get(mechanism.intent, [])

    def resolve(self, intent: str, context: dict[str, Any], params: dict[str, Any] | None = None) -> Resolution:
        params = params or {}
        candidates = []
        for m in self.registry.all():
            if m.invalidated or not self._intent_matches(m, intent):
                continue
            if not _matches(m.preconditions, context):
                continue
            if not _matches(m.applicability_guards, context):
                continue

            required_slots = set(m.parameter_slots) | _template_slots(m.action_template)
            if any(slot not in params for slot in required_slots):
                continue
            candidates.append(m)

        if not candidates:
            return Resolution(ResolutionStatus.UNKNOWN, None, "no applicable validated mechanism")

        candidates.sort(key=lambda m: m.confidence, reverse=True)
        best = candidates[0]
        if best.confidence < self.min_confidence:
            return Resolution(ResolutionStatus.EXPLORE, best.mechanism_id, "candidate exists but confidence is below execution threshold", confidence=best.confidence)

        return Resolution(
            ResolutionStatus.EXECUTABLE,
            best.mechanism_id,
            "applicability guards and confidence threshold passed",
            bound_action=_bind(best.action_template, params),
            confidence=best.confidence,
        )

    def force_resolve(self, intent: str, context: dict[str, Any], params: dict[str, Any] | None = None) -> Resolution:
        """Resolve ignoring min_confidence. Diagnostic only; never a decision path.

        This exists so the null control can separate genuine abstention from an
        arm that would have produced a wrong request anyway.
        """
        params = params or {}
        for m in self.registry.all():
            if m.invalidated or not self._intent_matches(m, intent):
                continue
            if not _matches(m.preconditions, context) or not _matches(m.applicability_guards, context):
                continue
            required_slots = set(m.parameter_slots) | _template_slots(m.action_template)
            if any(slot not in params for slot in required_slots):
                continue
            return Resolution(
                ResolutionStatus.EXECUTABLE,
                m.mechanism_id,
                "forced: confidence gate bypassed",
                bound_action=_bind(m.action_template, params),
                confidence=m.confidence,
            )
        return Resolution(ResolutionStatus.UNKNOWN, None, "no applicable mechanism")

    def verify(self, mechanism_id: str, observed_state: dict[str, Any]) -> bool:
        mechanism = next((m for m in self.registry.all() if m.mechanism_id == mechanism_id), None)
        if mechanism is None or mechanism.invalidated:
            return False
        return _matches(mechanism.postconditions, observed_state)

    def invalidate(self, mechanism_id: str) -> bool:
        return self.registry.invalidate(mechanism_id)


def _common_fields(states: list[dict[str, Any]]) -> dict[str, Any]:
    """Keys whose value is identical in every supplied state."""
    if not states:
        return {}
    out: dict[str, Any] = {}
    for key in {k for s in states for k in s}:
        values = [json.dumps(s.get(key), sort_keys=True) for s in states]
        if len(set(values)) == 1:
            out[key] = states[0].get(key)
    return out


def _template_regex(template: str, slots: list[str]) -> str:
    """Regex accepting any value in each slot position of ``template``."""
    if not template:
        return r"$^"
    out = ""
    remainder = template
    for name in slots:
        marker = "${" + name + "}"
        head, _, remainder = remainder.partition(marker)
        out += re.escape(head) + ".*"
    out += re.escape(remainder)
    return "^" + out

