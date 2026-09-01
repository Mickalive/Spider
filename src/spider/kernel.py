from __future__ import annotations

import hashlib
import json
import re
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


def _extract_varying_values(values: list[str]) -> dict[str, str] | None:
    """Given a list of string values, identify the longest common prefix and suffix.
    Return the varying middle portion mapped to a parameter name pattern, or None if
    all values are identical (no variation).
    
    This is the simplest possible parameter induction heuristic:
    - Find common prefix
    - Find common suffix (after prefix)
    - The middle is the parameter
    """
    if not values or all(v == values[0] for v in values):
        return None
    
    # Find common prefix
    prefix_len = 0
    min_len = min(len(v) for v in values)
    for i in range(min_len):
        chars = set(v[i] for v in values)
        if len(chars) == 1:
            prefix_len = i + 1
        else:
            break
    
    # Find common suffix (after prefix)
    suffix_len = 0
    for i in range(1, min_len - prefix_len + 1):
        chars = set(v[-i] for v in values)
        if len(chars) == 1:
            suffix_len = i
        else:
            break
    
    # The varying part is the middle
    varying = []
    for v in values:
        middle = v[prefix_len:len(v)-suffix_len if suffix_len > 0 else len(v)]
        varying.append(middle)
    
    # Check if varying parts look like identifiers (alphanumeric + common separators)
    import re
    is_id_like = all(re.match(r'^[A-Za-z0-9_\-]+$', v) for v in varying)
    
    if not is_id_like:
        return None
    
    return {
        "prefix": values[0][:prefix_len],
        "suffix": values[0][-suffix_len:] if suffix_len > 0 else "",
        "values": varying,
        "param_name": "id"
    }


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
        mechanism_id: str = "parameterized",
        min_observations: int = 2,
    ) -> Mechanism | None:
        """Distill a parameterized mechanism from multiple successful observations.
        
        Parameter induction heuristic:
        1. All observations must have the same intent, preconditions, and postconditions
        2. Compare action templates across observations
        3. Identify values that vary across observations as parameter candidates
        4. Replace varying values with ${param_name} slots
        
        This is a simple POC heuristic. Research 2.0 will evaluate whether this
        approach is viable via C-PARAM-INHERIT.
        
        Returns None if:
        - Fewer than min_observations successful observations
        - Observations have inconsistent intent/preconditions/postconditions
        - No parameterizable variation detected
        """
        successful = [o for o in observations if o.success]
        if len(successful) < min_observations:
            return None
        
        # Check consistency: all must have same intent, preconditions, postconditions
        ref = successful[0]
        for o in successful[1:]:
            if o.intent != ref.intent:
                return None
            if o.state != ref.state:
                return None
            if o.next_state != ref.next_state:
                return None
        
        # Collect all action values across observations for comparison
        # We need to compare leaf values in the action dictionaries
        def collect_paths(d: dict, prefix: str = "") -> list[tuple[str, str]]:
            """Collect all (path, value) pairs from a nested dict."""
            paths = []
            for k, v in d.items():
                full_path = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict):
                    paths.extend(collect_paths(v, full_path))
                elif isinstance(v, list):
                    # For lists, compare element by element
                    for i, item in enumerate(v):
                        item_path = f"{full_path}[{i}]"
                        if isinstance(item, dict):
                            paths.extend(collect_paths(item, item_path))
                        else:
                            paths.append((item_path, str(item)))
                else:
                    paths.append((full_path, str(v)))
            return paths
        
        # Collect paths from all observations
        all_paths = {}
        for i, o in enumerate(successful):
            paths = collect_paths(o.action)
            for path, value in paths:
                if path not in all_paths:
                    all_paths[path] = []
                all_paths[path].append((i, value))
        
        # Find paths that vary across observations
        varying_paths = {}
        for path, vals in all_paths.items():
            values = [v for _, v in vals]
            if len(set(values)) > 1:  # Values differ
                # Try to extract parameter info
                param_info = _extract_varying_values(values)
                if param_info:
                    varying_paths[path] = param_info
        
        if not varying_paths:
            return None  # No parameterizable variation found
        
        # Build parameterized action template
        def substitute_params(d: dict, paths: dict, current_prefix: str = "") -> dict:
            """Replace varying values with ${param} slots, preserving prefix/suffix."""
            result = {}
            for k, v in d.items():
                full_path = f"{current_prefix}.{k}" if current_prefix else k
                if isinstance(v, dict):
                    result[k] = substitute_params(v, paths, full_path)
                elif isinstance(v, list):
                    new_list = []
                    for i, item in enumerate(v):
                        item_path = f"{full_path}[{i}]"
                        if isinstance(item, dict):
                            new_list.append(substitute_params(item, paths, item_path))
                        elif item_path in paths:
                            # Preserve prefix and suffix, insert param in middle
                            info = paths[item_path]
                            param_name = info["param_name"]
                            prefix = info.get("prefix", "")
                            suffix = info.get("suffix", "")
                            new_list.append(f"{prefix}${{{param_name}}}{suffix}")
                        else:
                            new_list.append(item)
                    result[k] = new_list
                elif full_path in paths:
                    # Preserve prefix and suffix, insert param in middle
                    info = paths[full_path]
                    param_name = info["param_name"]
                    prefix = info.get("prefix", "")
                    suffix = info.get("suffix", "")
                    result[k] = f"{prefix}${{{param_name}}}{suffix}"
                else:
                    result[k] = v
            return result
        
        parameterized_action = substitute_params(ref.action, varying_paths)
        
        # Extract parameter names from the slots we inserted
        import re
        param_pattern = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
        
        def find_slots(d: Any) -> set[str]:
            if isinstance(d, str):
                return set(param_pattern.findall(d))
            elif isinstance(d, dict):
                slots = set()
                for v in d.values():
                    slots.update(find_slots(v))
                return slots
            elif isinstance(d, list):
                slots = set()
                for item in d:
                    slots.update(find_slots(item))
                return slots
            return set()
        
        parameter_slots = sorted(find_slots(parameterized_action))
        
        # Create the mechanism
        evidence_ids = [self.observe(o)[:16] for o in successful]
        
        return Mechanism(
            mechanism_id=mechanism_id,
            intent=ref.intent,
            preconditions=dict(ref.state),
            action_template=parameterized_action,
            postconditions=dict(ref.next_state),
            parameter_slots=parameter_slots,
            evidence=evidence_ids,
            confidence=0.9,  # Higher confidence from multiple observations
        )

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
