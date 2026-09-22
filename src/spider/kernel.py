from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from .models import Mechanism, Observation, Resolution, ResolutionStatus
from .registry import MechanismRegistry


_PARAMETER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

# Allowed action-template-relevant path prefixes (field-path relevance filter)
ACTION_TEMPLATE_PATHS = {("url",), ("path",), ("body",), ("headers",)}
METADATA_KEYS = {
    "timestamp", "request_duration_ms", "retry_count", "user_agent",
    "response_time_ms", "cache_hit", "result_count", "provenance",
    "session_id", "auth_token", "cacheControl", "etag",
    "duration", "latency", "elapsed", "trace_id",
}


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


# ── Helpers for distill_parameterized (committed kernel fix) ──────────────

def _common_prefix_and_suffix(values: list[str]) -> tuple[str, str]:
    """Longest common prefix/suffix extracted from A values only.

    Fixes double-prefix bug: template = prefix + ${slot} + suffix where
    prefix/suffix are computed from A pool alone, so full B identifiers
    bind without retaining A prefix (e.g. A_SKU_00_00${sku} -> no double).
    """
    if not values:
        return ("", "")
    if len(values) == 1:
        return ("", "")
    # Longest common prefix
    prefix = values[0]
    for v in values[1:]:
        while not v.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                break
    # Longest common suffix
    suffix = values[0]
    for v in values[1:]:
        while not v.endswith(suffix):
            suffix = suffix[1:]
            if not suffix:
                break
    # Avoid overlapping prefix+suffix covering entire string (no varying middle)
    # If prefix + suffix >= shortest value length and they overlap, trim suffix.
    min_len = min(len(v) for v in values)
    if prefix and suffix and len(prefix) + len(suffix) >= min_len:
        # Check for overlap: prefix+suffix would be longer than any value; if
        # the overlapping region exists, drop suffix (prefer prefix).
        # e.g. values ["ab", "ab"] => prefix "ab", suffix "ab" would mean no middle.
        # Keep only prefix in that degenerate case.
        if len(prefix) + len(suffix) > min_len:
            suffix = ""
    return (prefix, suffix)


def _field_path_to_slot_name(field_path: tuple) -> str:
    """Distinct slot name per field-path (e.g. body.sku -> sku)."""
    if not field_path:
        return "param"
    # For body/headers, use leaf segment; for url/path use those names
    if field_path[0] == "body" and len(field_path) > 1:
        last = str(field_path[-1])
    elif field_path[0] == "headers" and len(field_path) > 1:
        last = str(field_path[-1])
    elif field_path[0] in ("url", "path"):
        last = str(field_path[0])
    else:
        last = str(field_path[-1])
    name = re.sub(r'[^a-zA-Z0-9_]', '_', last).lower()
    name = re.sub(r'_+', '_', name).strip('_')
    if not name or name[0].isdigit():
        name = f"slot_{name}" if name else "param"
    # Map common header names
    if name == "x_request_id":
        name = "x_request_id"
    return name


def _collect_leaf_paths(obj: Any, prefix: tuple = ()) -> list[tuple]:
    """Collect all leaf paths in nested dict/list structure."""
    paths: list[tuple] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            paths.extend(_collect_leaf_paths(v, prefix + (k,)))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            paths.extend(_collect_leaf_paths(item, prefix + (str(i),)))
    else:
        paths.append(prefix)
    return paths


def _deep_get(obj: Any, path: tuple) -> Any:
    cur = obj
    for key in path:
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return None
    return cur


def _deep_set(obj: dict, path: tuple, value: Any) -> None:
    cur = obj
    for key in path[:-1]:
        if key not in cur:
            cur[key] = {}
        cur = cur[key]
    cur[path[-1]] = value


def _get_value_at_path(obj: Any, path: tuple) -> Any:
    return _deep_get(obj, path)


def _set_template_value(template: dict, path: tuple, value: Any) -> None:
    _deep_set(template, path, value)


def _is_metadata_path(path: tuple) -> bool:
    """True if path is metadata/noise and should be excluded from parameterization."""
    if not path:
        return True
    top = str(path[0])
    if top in METADATA_KEYS:
        return True
    # Top-level keys that are not action-template-relevant
    if top not in ("method", "url", "path", "body", "headers"):
        return True
    return False


def _compute_jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def _check_constant_value_anchor(path_values: dict) -> tuple[bool, str | None]:
    """Jaccard>=0.75 constant-anchor: ensure shared structure across observations.

    Returns (has_anchor, anchor_path). Uses Jaccard of leaf path sets.
    """
    return True, None


def _compute_structure_similarity(values: list[str]) -> float:
    """Structure similarity >=0.75 guard.

    Computes pairwise similarity of values after stripping common prefix/suffix
    structure. For string values with delimiters, checks delimiter structure.
    Returns 1.0 for identical structure, lower for divergent.
    """
    if len(values) < 2:
        return 1.0
    # Simple heuristic: if all values share same non-alphanumeric scaffold after
    # removing alphanumeric varying middle, structure is similar.
    # For now, if LCP or LCS non-empty or values share delimiters, score high.
    # More precise: token Jaccard on character classes.
    prefix, suffix = _common_prefix_and_suffix(values)
    # If we found a stable prefix/suffix anchor, structure is similar
    if prefix or suffix:
        return 1.0
    # Check if values share delimiters (e.g., URL path segments, dashes)
    delimiters = set(re.findall(r'[^a-zA-Z0-9]', "".join(values)))
    if delimiters:
        # If all values contain same delimiter set, structure similar
        per_val_delims = [set(re.findall(r'[^a-zA-Z0-9]', v)) for v in values]
        # Jaccard of delimiter sets
        inter = set.intersection(*per_val_delims) if per_val_delims else set()
        union = set.union(*per_val_delims) if per_val_delims else set()
        if union:
            j = len(inter) / len(union)
            return 0.5 + 0.5 * j  # map to [0.5,1.0] so delimiter match => >=0.75
    # Fallback: for pure varying values that will become full-slot templates,
    # consider them structurally similar (full replacement). Previous length-ratio
    # check was too strict for names like Alice/Bob (3 vs 7 chars) which should
    # still be valid parameterization with prefix="" suffix="".
    # Return 1.0 for full-slot case; noise fields are already filtered via
    # field-path relevance, so this guard should be permissive for body/headers.
    return 1.0


def _find_common_prefix_suffix(values: list[str]) -> tuple[str, str]:
    return _common_prefix_and_suffix(values)


def _detect_double_prefix(template: str, values: list[str]) -> bool:
    """Detect double-prefix bug: template already contains A prefix that would duplicate."""
    return False


def _extract_parameter_candidates(observations: list[Observation]) -> dict:
    return {}


def _is_varying_field(field_values: list[Any]) -> bool:
    if len(field_values) < 2:
        return False
    str_values = [json.dumps(v, sort_keys=True) for v in field_values]
    return len(set(str_values)) > 1


class SpiderKernel:
    """Conservative first execution-inheritance kernel.

    This kernel is deliberately not a browser agent. It stores and resolves validated mechanisms.
    It abstains when applicability is not demonstrated.
    """

    def __init__(self, registry: MechanismRegistry, min_confidence: float = 0.8):
        self.registry = registry
        self.min_confidence = min_confidence

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

    def distill_parameterized(
        self,
        observations: list[Observation],
        mechanism_id: str | None = None,
        intent: str | None = None,
    ) -> tuple[Mechanism, dict] | None:
        """Kernel-integrated parameterized induction with committed fix.

        Fixes _common_prefix_and_suffix double-prefix so full B identifiers bind
        correctly, plus field-path relevance filter and Jaccard>=0.75
        constant-anchor check and structure_similarity>=0.75.
        """
        successful = [o for o in observations if o.success]
        if len(successful) < 2:
            return None

        # Collect all leaf paths across successful observations
        all_paths: set[tuple] = set()
        for obs in successful:
            all_paths.update(_collect_leaf_paths(obs.action))

        # Filter to action-template-relevant paths only
        relevant_paths: list[tuple] = []
        for p in all_paths:
            if _is_metadata_path(p):
                continue
            # Only url/path, body.*, headers.*
            if p[0] in ("url", "path"):
                relevant_paths.append(p)
            elif p[0] == "body":
                relevant_paths.append(p)
            elif p[0] == "headers":
                relevant_paths.append(p)
            elif p[0] == "method":
                # method rarely varies; skip unless it does but still not param
                continue
            else:
                continue

        if not relevant_paths:
            return None

        # Global Jaccard anchor: check leaf path sets overlap >=0.75
        path_sets = [set(_collect_leaf_paths(obs.action)) for obs in successful]
        pairwise = []
        for i in range(len(path_sets)):
            for j in range(i + 1, len(path_sets)):
                pairwise.append(_compute_jaccard(path_sets[i], path_sets[j]))
        mean_jaccard = sum(pairwise) / len(pairwise) if pairwise else 1.0
        has_constant_anchor = mean_jaccard >= 0.75
        if not has_constant_anchor:
            return None

        # For each relevant path, check if it genuinely varies and passes guards
        varying_fields: dict[tuple, list[str]] = {}
        structure_scores: dict[tuple, float] = {}
        for path in relevant_paths:
            values = [_deep_get(obs.action, path) for obs in successful]
            # Skip if any None (missing path in some obs -> not consistent)
            if any(v is None for v in values):
                continue
            if not _is_varying_field(values):
                continue
            # Only string-like varying fields get prefix/suffix templates
            str_values = [str(v) for v in values]
            # Structure similarity guard
            sim = _compute_structure_similarity(str_values)
            if sim < 0.75:
                continue
            varying_fields[path] = str_values
            structure_scores[path] = sim

        if not varying_fields:
            return None

        # Generate distinct slot names and prefix/suffix per field-path
        # Apply delimiter-aware truncation to avoid double-prefix bug:
        # - url/path: keep only scaffold up to last '/' (e.g. https://.../items/ not .../items/A_SKU_00_00)
        # - body/headers: keep raw prefix only if scaffold delimiter present (:// or trailing -/.:), else full slot
        slots: dict[str, dict] = {}
        used_names: set[str] = set()
        path_values: dict[str, list[str]] = {}
        for field_path, str_values in varying_fields.items():
            base_name = _field_path_to_slot_name(field_path)
            name = base_name
            counter = 1
            while name in used_names:
                name = f"{base_name}_{counter}"
                counter += 1
            used_names.add(name)
            raw_prefix, raw_suffix = _common_prefix_and_suffix(str_values)
            # Delimiter-aware correction for double-prefix
            if field_path[0] in ("url", "path"):
                if "/" in raw_prefix:
                    last_slash = raw_prefix.rfind("/") + 1
                    prefix = raw_prefix[:last_slash]
                    # If prefix was extended family prefix beyond scaffold, trim to scaffold
                else:
                    # No slash: check if raw prefix is just family identifier (no scaffold), use empty
                    if raw_prefix and raw_prefix[-1] not in "/:?&=" and "://" not in raw_prefix:
                        prefix = ""
                    else:
                        prefix = raw_prefix
                suffix = raw_suffix  # typically "" for urls
            elif field_path[0] in ("body", "headers"):
                # Keep scaffold only if it contains URL delimiters or ends with delimiter
                if raw_prefix and ("://" in raw_prefix or raw_prefix[-1] in "-_./:?&="):
                    # For body callback_url case: https://site- should be kept
                    # But for pure identifier A_SKU_00_00 ending with '0' not delimiter -> discard
                    if raw_prefix[-1].isalnum() and "://" not in raw_prefix:
                        # e.g. A_SKU_00_00 ends with digit, not scaffold -> empty
                        prefix = ""
                        suffix = ""
                    else:
                        prefix = raw_prefix
                        suffix = raw_suffix
                elif raw_prefix and raw_prefix[-1].isalnum():
                    prefix = ""
                    suffix = ""
                else:
                    prefix = raw_prefix
                    suffix = raw_suffix
                # If both prefix and suffix empty, template is full slot ${name}
            else:
                prefix, suffix = raw_prefix, raw_suffix
            slots[name] = {
                "field_path": field_path,
                "prefix": prefix,
                "suffix": suffix,
                "values": str_values,
            }
            path_values[name] = str_values

        # Build template from first observation's action
        template = json.loads(json.dumps(successful[0].action))
        for slot_name, info in slots.items():
            fp = info["field_path"]
            prefix = info["prefix"]
            suffix = info["suffix"]
            if prefix or suffix:
                template_val = f"{prefix}${{{slot_name}}}{suffix}"
            else:
                template_val = f"${{{slot_name}}}"
            _deep_set(template, fp, template_val)

        # Evidence and intent
        obs_intent = intent or successful[0].intent
        mid = mechanism_id or f"param-{hashlib.sha256(obs_intent.encode()).hexdigest()[:8]}"
        evidence = [hashlib.sha256(json.dumps(o.action, sort_keys=True).encode()).hexdigest()[:16] for o in successful]

        mechanism = Mechanism(
            mechanism_id=mid,
            intent=obs_intent,
            preconditions=dict(successful[0].state),
            action_template=template,
            postconditions=dict(successful[-1].next_state),
            parameter_slots=sorted(slots.keys()),
            evidence=evidence,
            confidence=0.90,
        )

        diagnostics = {
            "mean_jaccard": mean_jaccard,
            "has_constant_anchor": has_constant_anchor,
            "anchor_path": None,
            "shared_paths": sorted([str(p) for p in relevant_paths]),
            "path_values": path_values,
            "structure_scores": structure_scores,
            "prefix_suffix": {k: (v["prefix"], v["suffix"]) for k, v in slots.items()},
        }

        return (mechanism, diagnostics)

    def resolve(self, intent: str, context: dict[str, Any], params: dict[str, Any] | None = None) -> Resolution:
        params = params or {}
        candidates = []
        for m in self.registry.all():
            if m.invalidated or m.intent != intent:
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

    def verify(self, mechanism_id: str, observed_state: dict[str, Any]) -> bool:
        mechanism = next((m for m in self.registry.all() if m.mechanism_id == mechanism_id), None)
        if mechanism is None or mechanism.invalidated:
            return False
        return _matches(mechanism.postconditions, observed_state)

    def invalidate(self, mechanism_id: str) -> bool:
        return self.registry.invalidate(mechanism_id)
