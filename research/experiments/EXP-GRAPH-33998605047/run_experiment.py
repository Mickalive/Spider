#!/usr/bin/env python3
"""EXP-GRAPH-33998605047 — Execute frozen experiment.

Tests whether the parameter-slot-count fix eliminates the original 5/5 false
accepts from the literal-vs-param equal-confidence hazard without regressing
any baseline conditions, and generalizes to multi-slot and template-only scenarios.

Applies the one-line fix temporarily during execution (production HEAD remains unfixed).
"""

import json
import sys
import tempfile
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from src.spider.kernel import SpiderKernel, _matches, _template_slots
from src.spider.registry import MechanismRegistry
from src.spider.models import Mechanism, ResolutionStatus

# =============================================================================
# MECHANISM DEFINITIONS
# =============================================================================

MECHANISMS = {
    "literal-fetch-posts-1": Mechanism(
        mechanism_id="literal-fetch-posts-1",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/1", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=[],
        confidence=0.95,
    ),
    "param-fetch-posts": Mechanism(
        mechanism_id="param-fetch-posts",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/${id}", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=["id"],
        confidence=0.95,
    ),
    "param-fetch-posts-high": Mechanism(
        mechanism_id="param-fetch-posts-high",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/${id}", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=["id"],
        confidence=0.98,
    ),
    "literal-fetch-posts-1-high": Mechanism(
        mechanism_id="literal-fetch-posts-1-high",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/1", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=[],
        confidence=0.98,
    ),
    "param-2slot": Mechanism(
        mechanism_id="param-2slot",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/${id}/${category}", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=["id", "category"],
        confidence=0.95,
    ),
    "template-only-fetch": Mechanism(
        mechanism_id="template-only-fetch",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/${id}", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=[],
        confidence=0.95,
    ),
    "param-fetch-alt": Mechanism(
        mechanism_id="param-fetch-alt",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/${id}", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=["id"],
        confidence=0.95,
    ),
}

# =============================================================================
# REGISTRY CONFIGURATIONS
# =============================================================================
# Registry insertion order: literal registered BEFORE param in competition conditions
# (to test that fix overcomes insertion-order bias)

REGISTRIES = {
    "empty": [],
    "literal-only": ["literal-fetch-posts-1"],
    "param-only": ["param-fetch-posts"],
    "shared-param-higher": ["param-fetch-posts-high", "literal-fetch-posts-1"],
    "shared-literal-higher": ["literal-fetch-posts-1-high", "param-fetch-posts"],
    "shared-equal": ["literal-fetch-posts-1", "param-fetch-posts"],
    "2slot-vs-1slot-equal-conf": ["param-2slot", "param-fetch-posts"],
    "template-only-vs-param": ["template-only-fetch", "param-fetch-posts"],
    "template-only-vs-literal": ["template-only-fetch", "literal-fetch-posts-1"],
    "equal-slot-param-vs-param": ["param-fetch-posts", "param-fetch-alt"],
}

# =============================================================================
# CONDITION DEFINITIONS (from frozen spec.json)
# =============================================================================

CONDITIONS = [
    # --- Baselines (7) ---
    {
        "id": "cold",
        "registry": "empty",
        "params": {"id": 2},
        "expected_resolution": "UNKNOWN",
        "expected_url": None,
        "expected_winning_mechanism": None,
        "role": "baseline",
    },
    {
        "id": "literal-only-original",
        "registry": "literal-only",
        "params": {"id": 1},
        "expected_resolution": "EXECUTABLE",
        "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
        "expected_winning_mechanism": "literal-fetch-posts-1",
        "role": "baseline",
    },
    {
        "id": "literal-only-unseen",
        "registry": "literal-only",
        "params": {"id": 2},
        "expected_resolution": "EXECUTABLE",
        "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
        "expected_winning_mechanism": "literal-fetch-posts-1",
        "role": "baseline",
    },
    {
        "id": "param-only-original",
        "registry": "param-only",
        "params": {"id": 1},
        "expected_resolution": "EXECUTABLE",
        "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
        "expected_winning_mechanism": "param-fetch-posts",
        "role": "baseline",
    },
    {
        "id": "param-only-unseen",
        "registry": "param-only",
        "params": {"id": 2},
        "expected_resolution": "EXECUTABLE",
        "expected_url": "https://jsonplaceholder.typicode.com/posts/2",
        "expected_winning_mechanism": "param-fetch-posts",
        "role": "baseline",
    },
    {
        "id": "compete-param-higher",
        "registry": "shared-param-higher",
        "params": {"id": 3},
        "expected_resolution": "EXECUTABLE",
        "expected_url": "https://jsonplaceholder.typicode.com/posts/3",
        "expected_winning_mechanism": "param-fetch-posts-high",
        "role": "baseline",
    },
    {
        "id": "compete-literal-higher",
        "registry": "shared-literal-higher",
        "params": {"id": 3},
        "expected_resolution": "EXECUTABLE",
        "expected_url": "https://jsonplaceholder.typicode.com/posts/1",
        "expected_winning_mechanism": "literal-fetch-posts-1-high",
        "role": "baseline",
    },
    # --- Interventions: false-accept hazard (5) ---
    {
        "id": "compete-equal-id2",
        "registry": "shared-equal",
        "params": {"id": 2},
        "expected_resolution": "EXECUTABLE",
        "expected_url": "https://jsonplaceholder.typicode.com/posts/2",
        "expected_winning_mechanism": "param-fetch-posts",
        "role": "intervention",
        "note": "Original hazard: before fix, literal won (false accept). After fix, param must win.",
    },
    {
        "id": "compete-equal-id3",
        "registry": "shared-equal",
        "params": {"id": 3},
        "expected_resolution": "EXECUTABLE",
        "expected_url": "https://jsonplaceholder.typicode.com/posts/3",
        "expected_winning_mechanism": "param-fetch-posts",
        "role": "intervention",
        "note": "Original hazard: before fix, literal won (false accept). After fix, param must win.",
    },
    {
        "id": "compete-equal-id4",
        "registry": "shared-equal",
        "params": {"id": 4},
        "expected_resolution": "EXECUTABLE",
        "expected_url": "https://jsonplaceholder.typicode.com/posts/4",
        "expected_winning_mechanism": "param-fetch-posts",
        "role": "intervention",
        "note": "Original hazard: before fix, literal won (false accept). After fix, param must win.",
    },
    {
        "id": "compete-equal-id5",
        "registry": "shared-equal",
        "params": {"id": 5},
        "expected_resolution": "EXECUTABLE",
        "expected_url": "https://jsonplaceholder.typicode.com/posts/5",
        "expected_winning_mechanism": "param-fetch-posts",
        "role": "intervention",
        "note": "Original hazard: before fix, literal won (false accept). After fix, param must win.",
    },
    {
        "id": "compete-equal-id6",
        "registry": "shared-equal",
        "params": {"id": 6},
        "expected_resolution": "EXECUTABLE",
        "expected_url": "https://jsonplaceholder.typicode.com/posts/6",
        "expected_winning_mechanism": "param-fetch-posts",
        "role": "intervention",
        "note": "Original hazard: before fix, literal won (false accept). After fix, param must win.",
    },
    # --- Interventions: generalization (4) ---
    {
        "id": "multi-slot-beats-1-slot",
        "registry": "2slot-vs-1slot-equal-conf",
        "params": {"id": "3", "category": "tech"},
        "expected_resolution": "EXECUTABLE",
        "expected_url": "https://jsonplaceholder.typicode.com/posts/3/tech",
        "expected_winning_mechanism": "param-2slot",
        "role": "intervention",
        "note": "2-slot param (len=2) beats 1-slot param (len=1) at equal confidence via tuple sort.",
    },
    {
        "id": "template-only-vs-param",
        "registry": "template-only-vs-param",
        "params": {"id": 3},
        "expected_resolution": "EXECUTABLE",
        "expected_url": "https://jsonplaceholder.typicode.com/posts/3",
        "expected_winning_mechanism": "param-fetch-posts",
        "role": "intervention",
        "note": "Template-only (parameter_slots=[], len=0) vs declared param (parameter_slots=['id'], len=1). Declared param wins.",
    },
    {
        "id": "template-only-vs-literal",
        "registry": "template-only-vs-literal",
        "params": {"id": 3},
        "expected_resolution": "EXECUTABLE",
        "expected_url": None,
        "expected_winning_mechanism": None,
        "role": "intervention",
        "note": "Template-only vs literal at equal confidence. Both len=0 -> tie -> lexicographic. Record actual winner.",
    },
    {
        "id": "equal-slot-tie-param-vs-param",
        "registry": "equal-slot-param-vs-param",
        "params": {"id": 3},
        "expected_resolution": "EXECUTABLE",
        "expected_url": None,
        "expected_winning_mechanism": None,
        "role": "intervention",
        "note": "Two params with same slot count at equal confidence. Tie -> lexicographic. Record actual winner.",
    },
]

# =============================================================================
# APPLY THE ONE-LINE FIX (temporary patch for execution)
# =============================================================================

def apply_fix():
    """Apply the one-line fix: tuple sort with (confidence, len(parameter_slots))."""
    import src.spider.kernel as kernel_mod
    original_resolve = kernel_mod.SpiderKernel.resolve

    def patched_resolve(self, intent, context, params=None):
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
            from src.spider.models import Resolution
            return Resolution(ResolutionStatus.UNKNOWN, None, "no applicable validated mechanism")

        # THE FIX: tuple sort with (confidence, len(parameter_slots))
        candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)
        best = candidates[0]
        if best.confidence < self.min_confidence:
            from src.spider.models import Resolution
            return Resolution(ResolutionStatus.EXPLORE, best.mechanism_id,
                              "candidate exists but confidence is below execution threshold",
                              confidence=best.confidence)

        from src.spider.models import Resolution
        from src.spider.kernel import _bind
        return Resolution(
            ResolutionStatus.EXECUTABLE,
            best.mechanism_id,
            "applicability guards and confidence threshold passed",
            bound_action=_bind(best.action_template, params),
            confidence=best.confidence,
        )

    kernel_mod.SpiderKernel.resolve = patched_resolve

# =============================================================================
# EXECUTION
# =============================================================================

def create_kernel(registry_name: str) -> SpiderKernel:
    """Create a fresh kernel with specified registry mechanisms."""
    tmp = tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False, prefix=f"exp340_{registry_name}_")
    tmp.close()
    registry = MechanismRegistry(tmp.name)
    mech_ids = REGISTRIES[registry_name]
    mechanisms = [MECHANISMS[mid] for mid in mech_ids]
    registry.replace(mechanisms)
    return SpiderKernel(registry, min_confidence=0.8)


def run_condition(cond: dict) -> dict:
    """Run a resolution condition and return raw observation."""
    kernel = create_kernel(cond["registry"])
    resolution = kernel.resolve("fetch-post", {}, cond["params"])

    status_val = resolution.status.value if hasattr(resolution.status, 'value') else str(resolution.status)
    bound_url = resolution.bound_action.get("url") if resolution.bound_action else None

    observation = {
        "condition_id": cond["id"],
        "type": "resolution",
        "status": status_val,
        "mechanism_id": resolution.mechanism_id,
        "bound_action": resolution.bound_action,
        "confidence": resolution.confidence,
        "reason": resolution.reason,
        "expected_status": cond["expected_resolution"],
        "expected_url": cond["expected_url"],
        "expected_winning_mechanism": cond.get("expected_winning_mechanism"),
        "match_expected_status": status_val == cond["expected_resolution"],
        "match_expected_url": bound_url == cond["expected_url"] if cond["expected_url"] is not None else None,
        "match_expected_mechanism": (
            resolution.mechanism_id == cond["expected_winning_mechanism"]
            if cond.get("expected_winning_mechanism") is not None
            else None
        ),
        "role": cond["role"],
        "note": cond.get("note"),
    }
    return observation


def main():
    apply_fix()

    raw_observations = []
    errors = []

    # Run all 16 conditions
    for cond in CONDITIONS:
        try:
            obs = run_condition(cond)
            raw_observations.append(obs)
        except Exception as e:
            errors.append({"condition_id": cond["id"], "error": str(e), "type": "exception"})
            raw_observations.append({
                "condition_id": cond["id"],
                "type": "resolution",
                "status": "EXCEPTION",
                "mechanism_id": None,
                "bound_action": None,
                "confidence": None,
                "reason": str(e),
                "expected_status": cond["expected_resolution"],
                "expected_url": cond["expected_url"],
                "expected_winning_mechanism": cond.get("expected_winning_mechanism"),
                "match_expected_status": False,
                "match_expected_url": None,
                "match_expected_mechanism": None,
                "role": cond["role"],
                "note": cond.get("note"),
            })

    # =============================================================================
    # DERIVED MEASUREMENTS
    # =============================================================================

    # Baseline regression check (7 conditions)
    baseline_ids = ["cold", "literal-only-original", "literal-only-unseen",
                    "param-only-original", "param-only-unseen",
                    "compete-param-higher", "compete-literal-higher"]
    baseline_obs = [o for o in raw_observations if o["condition_id"] in baseline_ids]
    baseline_pass = all(o["match_expected_status"] for o in baseline_obs)

    # Cold null control
    cold = next((o for o in raw_observations if o["condition_id"] == "cold"), None)
    cold_null_pass = cold is not None and cold["status"] == "UNKNOWN"

    # False accept elimination (5 conditions: compete-equal-id2 through id6)
    hazard_ids = ["compete-equal-id2", "compete-equal-id3", "compete-equal-id4",
                  "compete-equal-id5", "compete-equal-id6"]
    hazard_obs = [o for o in raw_observations if o["condition_id"] in hazard_ids]
    false_accepts_eliminated = all(
        o["status"] == "EXECUTABLE" and o.get("match_expected_mechanism") is True
        for o in hazard_obs
    )
    false_accept_count = sum(
        1 for o in hazard_obs
        if o["status"] == "EXECUTABLE" and o.get("match_expected_mechanism") is True
    )

    # Multi-slot dominance
    multi_slot = next((o for o in raw_observations if o["condition_id"] == "multi-slot-beats-1-slot"), None)
    multi_slot_dominance = (
        multi_slot["status"] == "EXECUTABLE"
        and multi_slot.get("match_expected_mechanism") is True
    ) if multi_slot else False

    # Template-only vs param
    template_vs_param = next((o for o in raw_observations if o["condition_id"] == "template-only-vs-param"), None)
    template_only_handling = (
        template_vs_param["status"] == "EXECUTABLE"
        and template_vs_param.get("match_expected_mechanism") is True
    ) if template_vs_param else None

    # Template-only vs literal (record winner, no pass/fail)
    template_vs_literal = next((o for o in raw_observations if o["condition_id"] == "template-only-vs-literal"), None)
    template_vs_literal_winner = template_vs_literal["mechanism_id"] if template_vs_literal else None

    # Equal-slot tie param vs param (record winner)
    tie_param = next((o for o in raw_observations if o["condition_id"] == "equal-slot-tie-param-vs-param"), None)
    tie_param_winner = tie_param["mechanism_id"] if tie_param else None

    # Confidence disambiguation (param-higher vs literal-higher)
    compete_param_higher = next((o for o in raw_observations if o["condition_id"] == "compete-param-higher"), None)
    compete_literal_higher = next((o for o in raw_observations if o["condition_id"] == "compete-literal-higher"), None)
    confidence_disambiguation_pass = (
        compete_param_higher is not None
        and compete_param_higher.get("match_expected_mechanism") is True
        and compete_literal_higher is not None
        and compete_literal_higher.get("match_expected_mechanism") is True
    )

    # =============================================================================
    # DECISION (per frozen spec.json decision_rule)
    # =============================================================================

    has_exceptions = len(errors) > 0
    has_unexpected_status = any(
        o["status"] not in ("EXECUTABLE", "UNKNOWN")
        for o in raw_observations
    )

    # Count conditions for decision
    all_baselines_pass = baseline_pass
    all_false_accepts_eliminated = false_accepts_eliminated and false_accept_count == 5
    multi_slot_pass = multi_slot_dominance
    template_pass = template_only_handling is True

    if has_exceptions or has_unexpected_status:
        decision = "MEASUREMENT_INVALID"
    elif (all_baselines_pass and all_false_accepts_eliminated
          and multi_slot_pass and template_pass):
        decision = "FIX-VALIDATED"
    elif all_baselines_pass and not all_false_accepts_eliminated and false_accept_count >= 3:
        decision = "FIX-INSUFFICIENT"
    elif all_baselines_pass and not all_false_accepts_eliminated and false_accept_count < 5:
        decision = "PARTIAL-VALIDATION"
    elif not all_baselines_pass:
        decision = "COMPETITION-UNSAFE"
    else:
        decision = "MEASUREMENT_INVALID"

    # =============================================================================
    # METRICS
    # =============================================================================

    metrics = {
        "baseline_regression": "PASS" if baseline_pass else "FAIL",
        "baseline_pass_count": sum(1 for o in baseline_obs if o["match_expected_status"]),
        "baseline_total": len(baseline_obs),
        "cold_null_control": "PASS" if cold_null_pass else "FAIL",
        "false_accepts_eliminated": "PASS" if false_accepts_eliminated else "FAIL",
        "false_accepts_correct_count": false_accept_count,
        "false_accepts_total": 5,
        "multi_slot_dominance": "PASS" if multi_slot_dominance else "FAIL",
        "multi_slot_winning_mechanism": multi_slot["mechanism_id"] if multi_slot else None,
        "multi_slot_bound_url": (
            multi_slot["bound_action"].get("url")
            if multi_slot and multi_slot.get("bound_action")
            else None
        ),
        "template_only_vs_param": (
            "PASS" if template_only_handling
            else ("FAIL" if template_only_handling is False else "INCONCLUSIVE")
        ),
        "template_only_vs_param_winning": template_vs_param["mechanism_id"] if template_vs_param else None,
        "template_vs_literal_winner": template_vs_literal_winner,
        "equal_slot_tie_param_winner": tie_param_winner,
        "confidence_disambiguation": "PASS" if confidence_disambiguation_pass else "FAIL",
        "compete_param_higher_winning": compete_param_higher["mechanism_id"] if compete_param_higher else None,
        "compete_literal_higher_winning": compete_literal_higher["mechanism_id"] if compete_literal_higher else None,
        "total_conditions": 16,
        "exceptions_count": len(errors),
    }

    # =============================================================================
    # CONTROLS
    # =============================================================================

    controls = {
        "B_COLD": {
            "expected": "UNKNOWN (empty registry)",
            "observed_status": cold["status"] if cold else None,
            "pass": cold_null_pass,
        },
        "B_LITERAL_ONLY_ORIG": {
            "expected": "EXECUTABLE url=/posts/1",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "literal-only-original"), None),
            "observed_url": next((o["bound_action"].get("url") for o in baseline_obs if o["condition_id"] == "literal-only-original" and o.get("bound_action")), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "literal-only-original"), None),
        },
        "B_LITERAL_ONLY_UNSEEN": {
            "expected": "EXECUTABLE url=/posts/1 (literal universal)",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "literal-only-unseen"), None),
            "observed_url": next((o["bound_action"].get("url") for o in baseline_obs if o["condition_id"] == "literal-only-unseen" and o.get("bound_action")), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "literal-only-unseen"), None),
        },
        "B_PARAM_ONLY_ORIG": {
            "expected": "EXECUTABLE url=/posts/1",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "param-only-original"), None),
            "observed_url": next((o["bound_action"].get("url") for o in baseline_obs if o["condition_id"] == "param-only-original" and o.get("bound_action")), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "param-only-original"), None),
        },
        "B_PARAM_ONLY_UNSEEN": {
            "expected": "EXECUTABLE url=/posts/2 (param generalizes)",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "param-only-unseen"), None),
            "observed_url": next((o["bound_action"].get("url") for o in baseline_obs if o["condition_id"] == "param-only-unseen" and o.get("bound_action")), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "param-only-unseen"), None),
        },
        "B_CONFIDENCE_PARAM_HIGHER": {
            "expected": "EXECUTABLE param (0.98) wins over literal (0.95)",
            "observed_status": compete_param_higher["status"] if compete_param_higher else None,
            "observed_mechanism": compete_param_higher["mechanism_id"] if compete_param_higher else None,
            "pass": compete_param_higher.get("match_expected_mechanism") if compete_param_higher else None,
        },
        "B_CONFIDENCE_LITERAL_HIGHER": {
            "expected": "EXECUTABLE literal (0.98) wins over param (0.95)",
            "observed_status": compete_literal_higher["status"] if compete_literal_higher else None,
            "observed_mechanism": compete_literal_higher["mechanism_id"] if compete_literal_higher else None,
            "pass": compete_literal_higher.get("match_expected_mechanism") if compete_literal_higher else None,
        },
        "NULL_HAZARD_ELIMINATION": {
            "expected": "param wins over literal at equal confidence in all 5 compete-equal-id conditions",
            "observed_false_accept_count": 5 - false_accept_count,
            "pass": false_accepts_eliminated,
        },
        "POS_MULTI_SLOT": {
            "expected": "EXECUTABLE param-2slot wins (len=2 > len=1)",
            "observed_status": multi_slot["status"] if multi_slot else None,
            "observed_mechanism": multi_slot["mechanism_id"] if multi_slot else None,
            "pass": multi_slot_dominance,
        },
        "POS_TEMPLATE_VS_PARAM": {
            "expected": "EXECUTABLE param-fetch-posts wins (len=1 > len=0)",
            "observed_status": template_vs_param["status"] if template_vs_param else None,
            "observed_mechanism": template_vs_param["mechanism_id"] if template_vs_param else None,
            "pass": template_only_handling,
        },
    }

    # =============================================================================
    # ARTIFACTS
    # =============================================================================

    import hashlib
    artifacts = []
    artifact_paths = [
        ("src/spider/kernel.py", "code"),
        ("src/spider/models.py", "code"),
        ("src/spider/registry.py", "code"),
        ("research/experiments/EXP-GRAPH-33998605047/run_experiment.py", "code"),
    ]
    for path, role in artifact_paths:
        fpath = PROJECT_ROOT / path
        sha = None
        if fpath.exists():
            sha = hashlib.sha256(fpath.read_bytes()).hexdigest()
        artifacts.append({"path": path, "sha256": sha, "role": role})

    # =============================================================================
    # OBSERVATIONS (direct, not interpreted)
    # =============================================================================

    observations = []
    for o in raw_observations:
        obs_text = f"[{o['condition_id']}] type={o['type']}"
        if o["type"] == "resolution":
            bound_url = o.get('bound_action', {}).get('url') if o.get('bound_action') else 'N/A'
            obs_text += f" status={o['status']} mechanism={o['mechanism_id']} bound_url={bound_url}"
        observations.append(obs_text)

    # =============================================================================
    # VALIDITY NOTES
    # =============================================================================

    validity_notes = [
        "Fix applied temporarily during execution — current HEAD src/spider/kernel.py L112 still has unfixed sort key (m.confidence only). Production commit requires Director approval.",
        "All conditions deterministic: no model calls, no RNG, no sampling. Single-run exact point comparisons.",
        "Synthetic substrate (jsonplaceholder.typicode.com) — generalizability to real-web endpoints with DOM, auth, session, drift not tested here.",
        "Each condition uses a fresh kernel instance with explicitly controlled registry contents. No cross-contamination.",
        "Registry insertion order controlled: literal registered before param in competition conditions to test tie-break.",
        "template-only-vs-literal and equal-slot-tie conditions have uncertain expected outcomes (lexicographic tie-break on mechanism_id when len=0 ties). Results are informative but not pass/fail for the primary claim.",
        "Fix is NOT committed to HEAD — this experiment validates the fix on the original hazard before production commit.",
    ]

    # =============================================================================
    # UNRESOLVED
    # =============================================================================

    unresolved = [
        "Whether the fix generalizes to real-web endpoints with DOM, auth, session state, and drift (synthetic substrate only).",
        "Whether the fix generalizes to other slot counts (3 vs 2, 5 vs 1), other template shapes, or other intents beyond fetch-post.",
        "Whether LLM-driven mechanism distillation ('learn on A' half of C-PARAM-INHERIT) works (no model calls).",
        "Whether _matches() discriminates beyond empty dict preconditions (all mechanisms tested with preconditions={}).",
        "Whether _bind() preserves type for full-match template strings (int -> int) (only URL-embedded partial match tested).",
        "Whether the fix has been committed to production HEAD (current HEAD unfixed, requires Director action).",
        "Whether registry upsert sorting (registry.py L35-38) affects production tie-break behavior (this experiment uses replace() without sorting).",
        "Whether template-only params need explicit required_slots-based handling or should be deprecated alongside literals at equal confidence.",
    ]

    # =============================================================================
    # RESULT.JSON
    # =============================================================================

    result = {
        "schema_version": 1,
        "experiment_id": "EXP-GRAPH-33998605047",
        "lane": "graph",
        "status": "COMPLETE",
        "outcome": decision,
        "metrics": metrics,
        "controls": controls,
        "artifacts": artifacts,
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    result_path = Path(__file__).parent / "result.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"result.json written: {result_path}")
    print(f"Outcome: {decision}")

    # =============================================================================
    # RAW EVIDENCE (separate artifact for downstream audit)
    # =============================================================================

    raw_evidence = {
        "observations": raw_observations,
        "errors": errors,
        "fix_applied": True,
        "fix_description": "candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)",
        "kernel_source_sha256": artifacts[0]["sha256"],
    }
    raw_path = Path(__file__).parent / "raw_evidence.json"
    raw_path.write_text(json.dumps(raw_evidence, indent=2), encoding="utf-8")

    # =============================================================================
    # DERIVED MEASUREMENTS (separate artifact)
    # =============================================================================

    derived = {
        "baseline_pass": baseline_pass,
        "baseline_details": [
            {"id": o["condition_id"], "pass": o["match_expected_status"]}
            for o in baseline_obs
        ],
        "cold_null_pass": cold_null_pass,
        "false_accepts_eliminated": false_accepts_eliminated,
        "false_accept_count": false_accept_count,
        "hazard_details": [
            {
                "id": o["condition_id"],
                "winning_mechanism": o["mechanism_id"],
                "expected": "param-fetch-posts",
                "pass": o.get("match_expected_mechanism") is True,
            }
            for o in hazard_obs
        ],
        "multi_slot_dominance": multi_slot_dominance,
        "multi_slot_details": multi_slot,
        "template_only_handling": template_only_handling,
        "template_only_vs_param_details": template_vs_param,
        "template_vs_literal_winner": template_vs_literal_winner,
        "template_vs_literal_details": template_vs_literal,
        "tie_param_winner": tie_param_winner,
        "confidence_disambiguation_pass": confidence_disambiguation_pass,
        "compete_param_higher_details": compete_param_higher,
        "compete_literal_higher_details": compete_literal_higher,
        "conditions_met": sum(1 for o in raw_observations if o.get("match_expected_status") is True),
        "conditions_total": len(raw_observations),
        "exceptions_count": len(errors),
    }
    derived_path = Path(__file__).parent / "derived_measurements.json"
    derived_path.write_text(json.dumps(derived, indent=2), encoding="utf-8")

    # Print key findings
    print("\n=== KEY FINDINGS ===")
    print(f"Baseline regression: {'PASS' if baseline_pass else 'FAIL'}")
    print(f"Cold null control: {'PASS' if cold_null_pass else 'FAIL'}")
    print(f"False accepts eliminated: {'PASS' if false_accepts_eliminated else 'FAIL'} ({false_accept_count}/5)")
    for o in hazard_obs:
        print(f"  [{o['condition_id']}] winning={o['mechanism_id']} expected=param-fetch-posts pass={o.get('match_expected_mechanism')}")
    print(f"Multi-slot dominance: {'PASS' if multi_slot_dominance else 'FAIL'}")
    print(f"Template-only vs param: {'PASS' if template_only_handling else 'FAIL'}")
    print(f"Template-only vs literal winner: {template_vs_literal_winner}")
    print(f"Equal-slot tie param winner: {tie_param_winner}")
    print(f"Confidence disambiguation: {'PASS' if confidence_disambiguation_pass else 'FAIL'}")
    print(f"Decision: {decision}")

    return result


if __name__ == "__main__":
    main()
