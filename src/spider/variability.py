"""Variability-learned parameter induction and the strong null binders.

This module exists to answer one question with a measurement rather than with
an argument: is SPIDER's parameter binding a MECHANISM that learns each slot's
support from observed variability, or a STRING MATCHER that binds by string
shape against a hardcoded kernel vocabulary?

Nothing in this module consults a field name, a collection list, an identity
vocabulary or any other hand-written label. Every quantity a binder uses is
either (a) a property of the frozen request frame, which is identical for every
binder, or (b) a statistic computed from the training observations handed to it.

Three strong nulls are provided so that the mechanism is compared against
plausible learning-free engineering rather than against a straw man. Each null is
implemented in its strongest defensible form:

``lexical_overlap``
    Score every candidate value by overlap with the goal and intent string and
    assign in descending score. No training observations at all.

``positional_regex``
    Freeze the per-slot character class from ONE canonical observed path, then
    consume the request's values left to right in slot order, first match wins.
    This is what a practitioner writes who has seen exactly one example of the
    URL form: it generalises across collections for the SHAPE but not for the
    VALUE, and it has no notion of a value's support.

``most_frequent_value``
    Always bind the modal training value for each slot, ignoring the request.
    The only null permitted to look at the training distribution, and it does so
    only through the mode.

Abstention is a first-class outcome (``BINDER_ABSTAIN``), not an absence of one.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from typing import Any

from .models import (
    BINDER_ABSTAIN,
    BINDER_BOUND,
    BindOutcome,
    Mechanism,
    Observation,
)

#: A slot whose observed value set is at most this large is treated as a CLOSED
#: support set: a candidate outside it is outside the observed support and is
#: refused. Above it the support is a learned character-class shape, which admits
#: unseen values of the same form by construction.
SUPPORT_CLOSED_SET_MAX = 16

#: Leave-one-out confidence replay: number of held-out observations, and the
#: seed of the deterministic subsample drawn from the training group.
CONFIDENCE_LOO_SAMPLE = 60
CONFIDENCE_LOO_SEED = 42

# --------------------------------------------------------------------------- #
# The frozen request frame.
#
# Supplied identically to every binder so that goal parsing is never the thing
# under test. Two forms exist:
#   R ("raw")  -- the request names the identifier verbatim, e.g. product-217
#   B ("bare") -- the request names only the ordinal and the collection word,
#                 e.g. "217" in "products", so the identifier FORM has to be
#                 learned from observed variability in order to be rebuilt.
# --------------------------------------------------------------------------- #

_GOAL_FRAME = re.compile(
    r"^(?P<verb>[a-z]+) record (?P<target>\S+) in (?P<collection>[a-z]+) catalog$"
)


def parse_goal(goal: str) -> dict[str, str]:
    """Parse the frozen request frame. Identical for every binder."""
    match = _GOAL_FRAME.match(goal.strip())
    if not match:
        return {}
    out = match.groupdict()
    out["form"] = "B" if re.fullmatch(r"[0-9]+", out["target"]) else "R"
    return out


def make_goal(verb: str, target: str, collection: str) -> str:
    return f"{verb} record {target} in {collection} catalog"


# --------------------------------------------------------------------------- #
# Character-class shapes: a generalisation of observed values, not a literal.
# --------------------------------------------------------------------------- #


def shape_of(value: str) -> str:
    """Character-class shape of one observed value; item-151 -> [a-z]+\\-[0-9]+."""
    parts: list[str] = []
    prev: str | None = None
    count = 0

    def flush() -> None:
        nonlocal prev, count
        if prev is None:
            return
        parts.append(prev if count == 1 else f"{prev}+")

    for ch in value:
        if ch.isdigit():
            cls = "[0-9]"
        elif ch.islower():
            cls = "[a-z]"
        elif ch.isupper():
            cls = "[A-Z]"
        else:
            cls = re.escape(ch)
        if cls == prev:
            count += 1
        else:
            flush()
            prev = cls
            count = 1
    flush()
    return "".join(parts)


def learned_shape(values: list[str]) -> str:
    """Smallest character-class alternation covering every observed value."""
    shapes = sorted({shape_of(v) for v in values})
    if len(shapes) == 1:
        return shapes[0]
    return "(?:" + "|".join(shapes) + ")"


def alpha_prefix(value: str) -> str:
    out: list[str] = []
    for ch in value:
        if not ch.isalpha():
            break
        out.append(ch)
    return "".join(out)


def slot_support_for(values: list[str]) -> dict[str, Any]:
    """Learned support of one path position, from observed values only."""
    distinct = sorted(set(values))
    if len(distinct) <= SUPPORT_CLOSED_SET_MAX:
        return {
            "kind": "closed_set",
            "values": distinct,
            "cardinality": len(distinct),
            "n_observations": len(values),
        }
    return {
        "kind": "shape",
        "shape": learned_shape(values),
        "n_distinct": len(distinct),
        "n_observations": len(values),
        "prefixes": sorted({alpha_prefix(v) for v in distinct}),
    }


def template_regex(template: str, slots: list[str]) -> str:
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


def segments(path: str) -> list[str]:
    return [s for s in path.split("/") if s != ""]


def common_fields(states: list[dict[str, Any]]) -> dict[str, Any]:
    """Keys whose value is identical in every supplied state."""
    if not states:
        return {}
    out: dict[str, Any] = {}
    for key in {k for s in states for k in s}:
        values = [json.dumps(s.get(key), sort_keys=True) for s in states]
        if len(set(values)) == 1:
            out[key] = states[0].get(key)
    return out


def transferable(
    fields: dict[str, Any], slot_values: set[str], identity_fields: tuple[str, ...]
) -> tuple[dict[str, Any], list[str]]:
    """Drop identity keys and identifier-bearing values from state fields."""
    kept: dict[str, Any] = {}
    dropped: list[str] = []
    for key, value in fields.items():
        if key in identity_fields or (
            isinstance(value, str) and any(sv and sv in value for sv in slot_values)
        ):
            dropped.append(key)
        else:
            kept[key] = value
    return kept, dropped


class VariabilityBinders:
    """Mixin: variability induction plus the mechanism and the three nulls.

    Mixed into :class:`spider.kernel.SpiderKernel` so that the declared-vocabulary
    path and this path share one kernel, one confidence gate and one resolution
    contract.
    """

    min_confidence: float

    # -- shared action helpers ------------------------------------------------ #

    @staticmethod
    def _action_for(mechanism: Mechanism, path: str) -> dict[str, Any]:
        action = {k: v for k, v in mechanism.action_template.items() if k != "path"}
        action["path"] = path
        return action

    @staticmethod
    def _assemble(mechanism: Mechanism, slot_values: dict[str, str]) -> str:
        path = mechanism.action_template.get("path", "")
        for name, value in slot_values.items():
            path = path.replace("${" + name + "}", value)
        return path

    # -- the variability-learned induction path ------------------------------- #

    def distill_variability(
        self,
        observations: list[Observation],
        mechanism_prefix: str = "var",
        intent_namespace_map: dict[str, list[str]] | None = None,
        compute_confidence: bool = True,
    ) -> list[Mechanism]:
        """Induce slots and slot support FROM OBSERVED VARIABILITY alone.

        For each intent group:

        * a path position becomes a slot if and only if its value was observed to
          take more than one distinct value in that position;
        * each slot records the support it was actually observed under: the closed
          set of values when that set is small, otherwise the learned
          character-class shape and the learned identifier prefixes;
        * the relation between the leading path value and the identifier prefix is
          learned by co-occurrence, so a mechanism trained on one collection learns
          only that collection's relation and has no basis for any other.

        Confidence is a leave-one-out replay of this same binder over the training
        observations, so it is a measured correctness estimate and never a
        constant. The incumbent's own confidence formula is also recorded, for
        every mechanism, as ``incumbent_formula_confidence``.
        """
        groups: dict[str, list[Observation]] = defaultdict(list)
        for observation in observations:
            groups[observation.intent].append(observation)
        nsmap = intent_namespace_map if intent_namespace_map is not None else getattr(
            self, "intent_namespace_map", {}
        )

        built: list[Mechanism] = []
        for intent, members in sorted(groups.items()):
            paths = [o.action["path"] for o in members if isinstance(o.action.get("path"), str)]
            if not paths:
                continue
            split = [segments(p) for p in paths]
            width = min(len(s) for s in split)
            varying = [i for i in range(width) if len({s[i] for s in split}) > 1]
            slot_names = [f"s{i}" for i in varying]
            pinned = {i: split[0][i] for i in range(width) if i not in varying}

            parts: list[str] = []
            for i in range(width):
                if i in varying:
                    parts.append("${%s}" % slot_names[varying.index(i)])
                else:
                    parts.append(split[0][i])
            template_path = "/" + "/".join(parts)

            slot_support: dict[str, Any] = {}
            for name, index in zip(slot_names, varying):
                observed = [row[index] for row in split if index < len(row)]
                slot_support[name] = slot_support_for(observed)

            id_prefix_by_head: dict[str, Any] = {}
            if varying:
                id_index = varying[-1]
                # The head is the nearest informative segment BEFORE the
                # identifier: a varying position if the collection name itself
                # varied in training (A1), otherwise the pinned leading segment
                # (A2, where only the identifier varied). Either way the
                # head -> identifier-prefix relation is read off co-occurrence.
                earlier = [i for i in varying if i < id_index]
                head_index = earlier[-1] if earlier else max(
                    [i for i in pinned if i < id_index], default=0
                )
                buckets: dict[str, set[str]] = defaultdict(set)
                for row in split:
                    if id_index < len(row) and 0 <= head_index < len(row):
                        buckets[row[head_index]].add(alpha_prefix(row[id_index]))
                id_prefix_by_head = {
                    head: (next(iter(p)) if len(p) == 1 else None)
                    for head, p in sorted(buckets.items())
                }

            template: dict[str, Any] = {
                "method": members[0].action.get("method"),
                "path": template_path,
            }
            conforming = sum(
                1 for path in paths if re.fullmatch(template_regex(template_path, slot_names), path)
            )
            consistency = conforming / len(paths)

            pre_common = common_fields([o.state for o in members])
            post_common = common_fields([o.next_state for o in members])
            slot_values = set()
            for name, index in zip(slot_names, varying):
                spec = slot_support[name]
                if spec["kind"] == "closed_set":
                    slot_values.update(spec["values"])
                else:
                    slot_values.update(spec["prefixes"])
            preconditions, dropped_pre = transferable(pre_common, slot_values, ())
            postconditions, dropped_post = transferable(post_common, slot_values, ())
            dropped = sorted(set(dropped_pre) | set(dropped_post))

            loo = (
                self._variability_loo(members, mechanism_prefix, nsmap)
                if compute_confidence
                else {"accuracy": 0.0, "n": 0, "n_correct": 0, "method": "not_computed_nested"}
            )
            confidence = round(consistency * loo["accuracy"], 4) if compute_confidence else 0.0
            n_success = sum(1 for o in members if o.success)
            incumbent_formula = round(
                ((n_success + 1.0) / (len(members) + 1.0))
                * consistency
                * (1.0 / (1.0 + 0.5 * (len(slot_names) - 1)) if slot_names else 1.0),
                4,
            )
            digest = json.dumps(
                [intent, template, slot_names, slot_support], sort_keys=True
            ).encode()
            import hashlib

            built.append(
                Mechanism(
                    mechanism_id=f"{mechanism_prefix}-{intent}-{hashlib.sha256(digest).hexdigest()[:12]}",
                    intent=intent,
                    preconditions=preconditions,
                    action_template=template,
                    postconditions=postconditions,
                    parameter_slots=slot_names,
                    auth_scope="bearer",
                    intent_namespace_map=list(nsmap.get(intent, [])) if nsmap else [],
                    freshness={
                        "strategy": "etag-revalidate",
                        "max_stale_requests": 0,
                        "revalidate_before_reuse": True,
                    },
                    applicability_guards={
                        k: v for k, v in pre_common.items() if k not in dropped_pre
                    },
                    verification_rule={
                        "type": "postcondition_match",
                        "postconditions": postconditions,
                    },
                    failure_boundary={
                        "induction_basis": "observed_variability",
                        "declared_identity_fields": [],
                        "declared_identity_slots": [],
                        "inferred_slots": slot_names,
                        "pinned_segments": {str(k): v for k, v in sorted(pinned.items())},
                        "slot_support": slot_support,
                        "id_prefix_by_head": id_prefix_by_head,
                        "varying_segment_positions": varying,
                        "excluded_identifier_keys": dropped,
                        "conforming": conforming,
                        "n_observations": len(paths),
                        "loo_accuracy": loo["accuracy"],
                        "loo_n": loo["n"],
                        "loo_n_correct": loo["n_correct"],
                        "loo_method": loo["method"],
                        "confidence": confidence,
                        "incumbent_formula_confidence": incumbent_formula,
                        "min_confidence": self.min_confidence,
                    },
                    repair_scope={"rebind_slots": True, "retryable_statuses": ["UNKNOWN", "EXPLORE"]},
                    evidence=[],
                    confidence=confidence,
                )
            )
        return built

    def _variability_loo(
        self,
        members: list[Observation],
        mechanism_prefix: str,
        nsmap: dict[str, list[str]] | None,
    ) -> dict[str, Any]:
        """Leave-one-out replay of the variability binder over the training group."""
        import random

        if len(members) < 2:
            return {"accuracy": 0.0, "n": 0, "n_correct": 0, "method": "degenerate_group"}
        sample_size = min(CONFIDENCE_LOO_SAMPLE, len(members))
        rng = random.Random(CONFIDENCE_LOO_SEED)
        held_out = sorted(rng.sample(range(len(members)), sample_size))
        n_correct = 0
        for idx in held_out:
            fold = [o for j, o in enumerate(members) if j != idx]
            rebuilt = self.distill_variability(
                fold, mechanism_prefix, nsmap, compute_confidence=False
            )
            probe = members[idx]
            parsed = parse_goal(
                make_goal(
                    str(probe.action.get("method", "get")).lower(),
                    str(probe.state.get("resource", "")),
                    str(probe.state.get("collection", "")),
                )
            )
            for mech in rebuilt:
                if mech.intent != probe.intent:
                    continue
                outcome = self.bind_variability(mech, parsed)
                if (
                    outcome.status == BINDER_BOUND
                    and outcome.bound_action is not None
                    and outcome.bound_action.get("path") == probe.action.get("path")
                ):
                    n_correct += 1
                break
        return {
            "accuracy": n_correct / len(held_out),
            "n": len(held_out),
            "n_correct": n_correct,
            "method": f"leave_one_out_random_{CONFIDENCE_LOO_SEED}_n{len(held_out)}",
        }

    # -- the variability-learned binder --------------------------------------- #

    def bind_variability(
        self, mechanism: Mechanism, parsed: dict[str, str]
    ) -> BindOutcome:
        """Bind using ONLY the slot support learned from observed variability."""
        if not parsed:
            return BindOutcome(BINDER_ABSTAIN, None, 0.0, "request frame not recognised", {}, {})
        boundary = mechanism.failure_boundary or {}
        support = boundary.get("slot_support", {})
        pinned = {int(k): v for k, v in boundary.get("pinned_segments", {}).items()}
        id_prefix_by_head = boundary.get("id_prefix_by_head", {})
        slots = list(mechanism.parameter_slots)
        if not slots:
            return BindOutcome(
                BINDER_ABSTAIN, None, 0.0,
                "no path position was observed to vary in training", {}, support,
            )
        if boundary.get("induction_basis") != "observed_variability":
            return BindOutcome(
                BINDER_ABSTAIN, None, 0.0,
                "mechanism carries no observed-variability slot support", {}, support,
            )

        for index, literal in sorted(pinned.items()):
            if index == 0 and literal != parsed.get("collection"):
                return BindOutcome(
                    BINDER_ABSTAIN, None, 0.0,
                    f"pinned leading segment '{literal}' contradicts requested collection "
                    f"'{parsed.get('collection')}'; training carried no evidence that it varies",
                    {}, support,
                )

        closed = [n for n in slots if support.get(n, {}).get("kind") == "closed_set"]
        shaped = [n for n in slots if support.get(n, {}).get("kind") == "shape"]
        if len(closed) > 1 or len(shaped) > 1 or len(closed) + len(shaped) != len(slots):
            return BindOutcome(
                BINDER_ABSTAIN, None, 0.0,
                "learned slot layout is not one closed support slot plus one shape slot",
                {}, support,
            )

        slot_values: dict[str, str] = {}
        head = parsed.get("collection", "")
        if closed:
            name = closed[0]
            values = support[name].get("values", [])
            if head not in values:
                return BindOutcome(
                    BINDER_ABSTAIN, None, 0.0,
                    f"'{head}' lies outside the observed support {values} of slot {name}",
                    {}, support,
                )
            slot_values[name] = head

        if shaped:
            name = shaped[0]
            shape = support[name].get("shape", "")
            if parsed.get("form") == "B":
                prefix = id_prefix_by_head.get(head)
                if not prefix:
                    return BindOutcome(
                        BINDER_ABSTAIN, None, 0.0,
                        f"no learned identifier prefix for head '{head}'", {}, support,
                    )
                value = f"{prefix}-{parsed.get('target', '')}"
            else:
                value = parsed.get("target", "")
            if not re.fullmatch(shape, value):
                return BindOutcome(
                    BINDER_ABSTAIN, None, 0.0,
                    f"'{value}' does not match the learned shape {shape} of slot {name}",
                    {}, support,
                )
            slot_values[name] = value

        path = self._assemble(mechanism, slot_values)
        return BindOutcome(
            BINDER_BOUND, self._action_for(mechanism, path), mechanism.confidence,
            "bound from observed slot support", slot_values, support,
        )

    # -- strong null binders --------------------------------------------------- #

    @staticmethod
    def _lexical_overlap(candidate: str, haystack: str) -> float:
        cand = candidate.lower()
        if not cand:
            return 0.0
        token_hit = 1.0 if cand in haystack.split() else 0.0
        sub_hit = 1.0 if cand in haystack else 0.0
        grams_c = {cand[i:i + 3] for i in range(max(1, len(cand) - 2))}
        grams_h = {haystack[i:i + 3] for i in range(max(1, len(haystack) - 2))}
        trigram = len(grams_c & grams_h) / len(grams_c) if grams_c else 0.0
        return round(0.4 * token_hit + 0.2 * sub_hit + 0.4 * trigram, 6)

    def bind_lexical_overlap(
        self,
        mechanism: Mechanism,
        parsed: dict[str, str],
        pinned_values: dict[str, str] | None = None,
        tie_break: str = "longest_first",
    ) -> BindOutcome:
        """Null: choose the slot value whose tokens overlap the goal/intent string.

        No training observations are used. Candidate values are the request's own
        values plus the mechanism's pinned literals; each is scored by token and
        character-trigram overlap with the goal and intent string, and candidates
        are assigned to slots in descending score.

        The frozen definition underdetermines what happens when two candidates
        score identically, and on this request frame both candidates always do,
        because the goal string literally contains both slot values. Rather than
        let one arbitrary rule decide the experiment, ``tie_break`` selects the
        ordering and the caller runs the extreme in each direction, so the null
        can be scored at its best. Confidence is the winning margin over the
        runner-up, and is 0 whenever the ranking is tied.
        """
        if not parsed:
            return BindOutcome(BINDER_ABSTAIN, None, 0.0, "request frame not recognised", {}, {})
        pinned_values = pinned_values or {}
        haystack = " ".join(
            [parsed.get("verb", ""), parsed.get("target", ""), parsed.get("collection", ""), mechanism.intent]
        ).lower()
        candidates = [parsed.get("target", ""), parsed.get("collection", "")]
        candidates += [v for _, v in sorted(pinned_values.items())]
        candidates = [c for c in dict.fromkeys(candidates) if c]
        slots = list(mechanism.parameter_slots)
        if not slots or not candidates:
            return BindOutcome(BINDER_ABSTAIN, None, 0.0, "no slots or no candidates", {}, {})

        if tie_break == "shortest_first":
            key = lambda t: (-t[0], t[1], t[2])  # noqa: E731
        else:
            key = lambda t: (-t[0], -t[1], t[2])  # noqa: E731
        scored = sorted(
            ((self._lexical_overlap(c, haystack), len(c), c) for c in candidates), key=key
        )
        chosen = [c for _, _, c in scored[: len(slots)]]
        if len(chosen) < len(slots):
            return BindOutcome(BINDER_ABSTAIN, None, 0.0, "not enough candidate values", {}, {})
        top = scored[0][0]
        runner_up = scored[1][0] if len(scored) > 1 else 0.0
        margin = (top - runner_up) / top if top else 0.0
        slot_values = {slot: value for slot, value in zip(slots, chosen)}
        path = self._assemble(mechanism, slot_values)
        return BindOutcome(
            BINDER_BOUND, self._action_for(mechanism, path),
            round(margin * (len(chosen) / len(slots)), 4),
            f"lexical overlap between request values and the goal/intent string ({tie_break})",
            slot_values, {"tie_break": tie_break, "top_score": top, "runner_up_score": runner_up},
        )

    def bind_positional_regex(
        self,
        mechanism: Mechanism,
        parsed: dict[str, str],
        canonical_example: str | None = None,
    ) -> BindOutcome:
        """Null: fill slots from fixed URL positions using one frozen regex.

        The per-slot character class is frozen from ONE canonical observed path,
        then the request's values are consumed left to right in slot order, the
        first value whose frozen class matches being taken for that slot. This is
        the strongest learning-free binder available: it generalises across
        collections for the SHAPE of a value, and it has no notion of a value's
        support, so an unseen-but-well-formed collection is indistinguishable to
        it from a familiar one.
        """
        if not parsed:
            return BindOutcome(BINDER_ABSTAIN, None, 0.0, "request frame not recognised", {}, {})
        if not canonical_example:
            return BindOutcome(
                BINDER_ABSTAIN, None, 0.0, "no canonical observed path was supplied", {}, {}
            )
        slots = list(mechanism.parameter_slots)
        example = segments(canonical_example)
        template_parts = segments(mechanism.action_template.get("path", ""))
        if not slots or len(example) != len(template_parts):
            return BindOutcome(
                BINDER_ABSTAIN, None, 0.0, "canonical example does not fit the template", {}, {}
            )
        classes: list[str] = []
        for index, part in enumerate(template_parts):
            if part.startswith("${") and part.endswith("}"):
                classes.append(shape_of(example[index]))
            else:
                classes.append("")
        pool = [parsed.get("target", ""), parsed.get("collection", "")]
        pool = [p for p in pool if p]
        taken: dict[str, str] = {}
        cursor = 0
        for name, cls in zip(slots, classes):
            picked = ""
            for candidate in pool[cursor:]:
                if cls and re.fullmatch(cls, candidate):
                    picked = candidate
                    cursor = pool.index(candidate) + 1
                    break
            if not picked:
                return BindOutcome(
                    BINDER_ABSTAIN, None, 0.0,
                    f"no request value matches the frozen class {cls!r} of slot {name}",
                    {}, {"frozen_classes": dict(zip(slots, classes))},
                )
            taken[name] = picked
        path = self._assemble(mechanism, taken)
        return BindOutcome(
            BINDER_BOUND, self._action_for(mechanism, path), 1.0,
            "fixed URL positions filled with the first value matching the frozen class",
            taken, {"frozen_classes": dict(zip(slots, classes)), "canonical_example": canonical_example},
        )

    def bind_most_frequent_value(
        self,
        mechanism: Mechanism,
        parsed: dict[str, str],
        modal_values: dict[str, Any] | None = None,
    ) -> BindOutcome:
        """Null: always bind the most frequent training value for each slot.

        The request is ignored entirely. Confidence is the modal share of the
        bound value, which is the only honest estimate this binder can form, and
        it is far below any sane execution threshold for a high-cardinality slot.
        """
        modal_values = modal_values or {}
        slots = list(mechanism.parameter_slots)
        if not slots or not modal_values:
            return BindOutcome(
                BINDER_ABSTAIN, None, 0.0, "no modal training values supplied", {}, {}
            )
        slot_values: dict[str, str] = {}
        shares: dict[str, float] = {}
        for name in slots:
            entry = modal_values.get(name)
            if not isinstance(entry, dict) or not entry.get("value"):
                return BindOutcome(
                    BINDER_ABSTAIN, None, 0.0, f"no modal value recorded for slot {name}", {}, {}
                )
            slot_values[name] = entry["value"]
            shares[name] = float(entry.get("share", 0.0))
        path = self._assemble(mechanism, slot_values)
        confidence = round(min(shares.values()) if shares else 0.0, 6)
        return BindOutcome(
            BINDER_BOUND, self._action_for(mechanism, path), confidence,
            "most frequent training value per slot, request ignored",
            slot_values, {"modal_share": shares},
        )
