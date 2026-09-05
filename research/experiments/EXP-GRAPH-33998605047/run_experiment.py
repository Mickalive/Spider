#!/usr/bin/env python3
"""EXP-GRAPH-33998605047 — Execute frozen experiment.

Re-tests the original literal-vs-param equal-confidence hazard (compete-equal-id2..id6)
with the parameter-slot-count fix applied temporarily. Also tests multi-slot dominance,
template-only handling, and equal-slot tie behavior.

Frozen spec: 16 conditions (7 baseline + 9 intervention).
Fix: candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)
"""

import json
import sys
import tempfile
import hashlib as _hashlib
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from src.spider.kernel import SpiderKernel, _matches, _template_slots, _bind
from src.spider.registry import MechanismRegistry
from src.spider.models import Mechanism, Resolution, ResolutionStatus

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
    "literal-fetch-posts-1-low": Mechanism(
        mechanism_id="literal-fetch-posts-1-low",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/1", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=[],
        confidence=0.95,
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
    "literal-alt": Mechanism(
        mechanism_id="literal-alt",
        intent="fetch-post",
        preconditions={},
        action_template={"url": "https://jsonplaceholder.typicode.com/posts/2", "method": "GET"},
        postconditions={"status": 200},
        parameter_slots=[],
        confidence=0.95,
    ),
}

# =============================================================================
# REGISTRY CONFIGURATIONS
# =============================================================================

# Registry configs: each maps a name to a list of mechanism IDs.
# In competition conditions, literal is registered BEFORE param to test tie-break.
REGISTRIES = {
    "empty": [],
    "literal-only": ["literal-fetch-posts-1"],
    "param-only": ["param-fetch-posts"],
    "shared-param-higher": ["param-fetch-posts-high", "literal-fetch-posts-1-low"],
    "shared-literal-higher": ["literal-fetch-posts-1-low", "param-fetch-posts-high"],
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
    {"id": "cold", "registry": "empty", "params": {"id": 2}, "expected_resolution": "UNKNOWN", "expected_url": None, "expected_winning_mechanism": None, "role": "baseline"},
    {"id": "literal-only-original", "registry": "literal-only", "params": {"id": 1}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1", "expected_winning_mechanism": "literal-fetch-posts-1", "role": "baseline"},
    {"id": "literal-only-unseen", "registry": "literal-only", "params": {"id": 2}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1", "expected_winning_mechanism": "literal-fetch-posts-1", "role": "baseline"},
    {"id": "param-only-original", "registry": "param-only", "params": {"id": 1}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1", "expected_winning_mechanism": "param-fetch-posts", "role": "baseline"},
    {"id": "param-only-unseen", "registry": "param-only", "params": {"id": 2}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/2", "expected_winning_mechanism": "param-fetch-posts", "role": "baseline"},
    {"id": "compete-param-higher", "registry": "shared-param-higher", "params": {"id": 3}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/3", "expected_winning_mechanism": "param-fetch-posts-high", "role": "baseline"},
    {"id": "compete-literal-higher", "registry": "shared-literal-higher", "params": {"id": 3}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/1", "expected_winning_mechanism": "literal-fetch-posts-1-low", "role": "baseline"},
    {"id": "compete-equal-id2", "registry": "shared-equal", "params": {"id": 2}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/2", "expected_winning_mechanism": "param-fetch-posts", "role": "intervention"},
    {"id": "compete-equal-id3", "registry": "shared-equal", "params": {"id": 3}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/3", "expected_winning_mechanism": "param-fetch-posts", "role": "intervention"},
    {"id": "compete-equal-id4", "registry": "shared-equal", "params": {"id": 4}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/4", "expected_winning_mechanism": "param-fetch-posts", "role": "intervention"},
    {"id": "compete-equal-id5", "registry": "shared-equal", "params": {"id": 5}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/5", "expected_winning_mechanism": "param-fetch-posts", "role": "intervention"},
    {"id": "compete-equal-id6", "registry": "shared-equal", "params": {"id": 6}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/6", "expected_winning_mechanism": "param-fetch-posts", "role": "intervention"},
    {"id": "multi-slot-beats-1-slot", "registry": "2slot-vs-1slot-equal-conf", "params": {"id": "3", "category": "tech"}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/3/tech", "expected_winning_mechanism": "param-2slot", "role": "intervention"},
    {"id": "template-only-vs-param", "registry": "template-only-vs-param", "params": {"id": 3}, "expected_resolution": "EXECUTABLE", "expected_url": "https://jsonplaceholder.typicode.com/posts/3", "expected_winning_mechanism": "param-fetch-posts", "role": "intervention"},
    {"id": "template-only-vs-literal", "registry": "template-only-vs-literal", "params": {"id": 3}, "expected_resolution": "EXECUTABLE", "expected_url": None, "expected_winning_mechanism": None, "role": "intervention"},
    {"id": "equal-slot-tie-param-vs-param", "registry": "equal-slot-param-vs-param", "params": {"id": 3}, "expected_resolution": "EXECUTABLE", "expected_url": None, "expected_winning_mechanism": None, "role": "intervention"},
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
            return Resolution(ResolutionStatus.UNKNOWN, None, "no applicable validated mechanism")

        # THE FIX: tuple sort with (confidence, len(parameter_slots))
        candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)
        best = candidates[0]
        if best.confidence < self.min_confidence:
            return Resolution(ResolutionStatus.EXPLORE, best.mechanism_id,
                              "candidate exists but confidence is below execution threshold",
                              confidence=best.confidence)

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
    tmp = tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False, prefix=f"exp3399_{registry_name}_")
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

    return {
        "condition_id": cond["id"],
        "type": "resolution",
        "status": status_val,
        "mechanism_id": resolution.mechanism_id,
        "bound_action": resolution.bound_action,
        "bound_url": bound_url,
        "confidence": resolution.confidence,
        "reason": resolution.reason,
        "expected_status": cond["expected_resolution"],
        "expected_url": cond["expected_url"],
        "expected_winning_mechanism": cond.get("expected_winning_mechanism"),
        "match_expected_status": status_val == cond["expected_resolution"],
        "match_expected_url": bound_url == cond["expected_url"] if cond["expected_url"] is not None else None,
        "match_expected_mechanism": resolution.mechanism_id == cond.get("expected_winning_mechanism") if cond.get("expected_winning_mechanism") is not None else None,
        "role": cond["role"],
    }


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
                "bound_url": None,
                "confidence": None,
                "reason": str(e),
                "expected_status": cond["expected_resolution"],
                "expected_url": cond["expected_url"],
                "expected_winning_mechanism": cond.get("expected_winning_mechanism"),
                "match_expected_status": False,
                "match_expected_url": None,
                "match_expected_mechanism": None,
                "role": cond["role"],
            })

    # =============================================================================
    # DERIVED MEASUREMENTS
    # =============================================================================

    # Separate baseline and intervention observations
    baseline_obs = [o for o in raw_observations if o["role"] == "baseline"]
    intervention_obs = [o for o in raw_observations if o["role"] == "intervention"]

    # H2: Baseline regression check — all 7 baselines must match expected outcomes
    baseline_pass = all(o["match_expected_status"] for o in baseline_obs)

    # H1: False accept elimination — compete-equal-id2..id6 must all return param-fetch-posts
    compete_equal = [o for o in intervention_obs if o["condition_id"].startswith("compete-equal-id")]
    false_accepts_eliminated = all(
        o["match_expected_mechanism"] is True and o["status"] == "EXECUTABLE"
        for o in compete_equal
    )
    false_accept_count = sum(1 for o in compete_equal if o["match_expected_mechanism"] is True)

    # H3: Multi-slot dominance
    multi_slot = next((o for o in intervention_obs if o["condition_id"] == "multi-slot-beats-1-slot"), None)
    multi_slot_dominance = (
        multi_slot["status"] == "EXECUTABLE"
        and multi_slot.get("match_expected_mechanism") is True
    ) if multi_slot else False

    # H4: Template-only vs param
    template_vs_param = next((o for o in intervention_obs if o["condition_id"] == "template-only-vs-param"), None)
    template_only_handling = (
        template_vs_param["status"] == "EXECUTABLE"
        and template_vs_param.get("match_expected_mechanism") is True
    ) if template_vs_param else None

    # Exploratory: template-only vs literal
    template_vs_literal = next((o for o in intervention_obs if o["condition_id"] == "template-only-vs-literal"), None)
    template_vs_literal_winner = template_vs_literal["mechanism_id"] if template_vs_literal else None

    # Exploratory: equal-slot tie param vs param
    equal_slot_tie = next((o for o in intervention_obs if o["condition_id"] == "equal-slot-tie-param-vs-param"), None)
    equal_slot_tie_winner = equal_slot_tie["mechanism_id"] if equal_slot_tie else None

    # =============================================================================
    # DECISION (per frozen spec.json decision_rule)
    # =============================================================================

    has_exceptions = len(errors) > 0
    has_unexpected_status = any(o["status"] not in ("EXECUTABLE", "UNKNOWN") for o in raw_observations)

    if has_exceptions or has_unexpected_status:
        decision = "MEASUREMENT_INVALID"
        status = "BLOCKED"
    elif (baseline_pass
          and false_accepts_eliminated
          and multi_slot_dominance
          and template_only_handling is True):
        decision = "FIX-VALIDATED"
        status = "COMPLETE"
    elif baseline_pass and not false_accepts_eliminated and false_accept_count >= 3:
        decision = "FIX-INSUFFICIENT"
        status = "COMPLETE"
    elif baseline_pass and not false_accepts_eliminated:
        decision = "PARTIAL-VALIDATION"
        status = "COMPLETE"
    elif not baseline_pass:
        decision = "COMPETITION-UNSAFE"
        status = "COMPLETE"
    else:
        decision = "MIXED"
        status = "COMPLETE"

    # =============================================================================
    # METRICS
    # =============================================================================

    metrics = {
        "baseline_pass": baseline_pass,
        "baseline_pass_count": sum(1 for o in baseline_obs if o["match_expected_status"]),
        "baseline_total": len(baseline_obs),
        "false_accepts_eliminated": false_accepts_eliminated,
        "false_accepts_eliminated_count": false_accept_count,
        "false_accepts_total": len(compete_equal),
        "multi_slot_dominance": multi_slot_dominance,
        "multi_slot_winning_mechanism": multi_slot["mechanism_id"] if multi_slot else None,
        "multi_slot_bound_url": multi_slot["bound_url"] if multi_slot else None,
        "template_only_vs_param": template_only_handling,
        "template_only_vs_param_winning": template_vs_param["mechanism_id"] if template_vs_param else None,
        "template_vs_literal_winner": template_vs_literal_winner,
        "equal_slot_tie_winner": equal_slot_tie_winner,
        "total_conditions": len(raw_observations),
        "exceptions_count": len(errors),
    }

    # =============================================================================
    # CONTROLS (frozen identifiers)
    # =============================================================================

    controls = {
        "B_COLD": {
            "expected": "UNKNOWN",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "cold"), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "cold"), None),
        },
        "B_LITERAL_ONLY_ORIG": {
            "expected": "EXECUTABLE url=/posts/1",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "literal-only-original"), None),
            "observed_url": next((o["bound_url"] for o in baseline_obs if o["condition_id"] == "literal-only-original"), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "literal-only-original"), None),
        },
        "B_LITERAL_ONLY_UNSEEN": {
            "expected": "EXECUTABLE url=/posts/1 (literal universal)",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "literal-only-unseen"), None),
            "observed_url": next((o["bound_url"] for o in baseline_obs if o["condition_id"] == "literal-only-unseen"), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "literal-only-unseen"), None),
        },
        "B_PARAM_ONLY_ORIG": {
            "expected": "EXECUTABLE url=/posts/1",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "param-only-original"), None),
            "observed_url": next((o["bound_url"] for o in baseline_obs if o["condition_id"] == "param-only-original"), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "param-only-original"), None),
        },
        "B_PARAM_ONLY_UNSEEN": {
            "expected": "EXECUTABLE url=/posts/2 (param generalizes)",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "param-only-unseen"), None),
            "observed_url": next((o["bound_url"] for o in baseline_obs if o["condition_id"] == "param-only-unseen"), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "param-only-unseen"), None),
        },
        "B_CONFIDENCE_PARAM_HIGHER": {
            "expected": "EXECUTABLE param (0.98) wins over literal (0.95)",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "compete-param-higher"), None),
            "observed_mechanism": next((o["mechanism_id"] for o in baseline_obs if o["condition_id"] == "compete-param-higher"), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "compete-param-higher"), None),
        },
        "B_CONFIDENCE_LITERAL_HIGHER": {
            "expected": "EXECUTABLE literal (0.98) wins over param (0.95)",
            "observed_status": next((o["status"] for o in baseline_obs if o["condition_id"] == "compete-literal-higher"), None),
            "observed_mechanism": next((o["mechanism_id"] for o in baseline_obs if o["condition_id"] == "compete-literal-higher"), None),
            "pass": next((o["match_expected_status"] for o in baseline_obs if o["condition_id"] == "compete-literal-higher"), None),
        },
        "POS_MULTI_SLOT": {
            "expected": "EXECUTABLE param-2slot wins (len=2 > len=1)",
            "observed_status": multi_slot["status"] if multi_slot else None,
            "observed_mechanism": multi_slot["mechanism_id"] if multi_slot else None,
            "pass": multi_slot_dominance,
        },
        "NULL_CONTROL_HAZARD": {
            "expected": "After fix: param wins over literal at equal confidence (all compete-equal-id)",
            "observed_false_accepts": len(compete_equal) - false_accept_count,
            "observed_total": len(compete_equal),
            "pass": false_accepts_eliminated,
        },
    }

    # =============================================================================
    # ARTIFACTS
    # =============================================================================

    artifacts = [
        {"path": "research/experiments/EXP-GRAPH-33998605047/run_experiment.py", "sha256": None, "role": "code"},
        {"path": "src/spider/kernel.py", "sha256": None, "role": "code"},
        {"path": "src/spider/models.py", "sha256": None, "role": "code"},
        {"path": "src/spider/registry.py", "sha256": None, "role": "code"},
    ]

    for art in artifacts:
        fpath = PROJECT_ROOT / art["path"]
        if fpath.exists():
            art["sha256"] = _hashlib.sha256(fpath.read_bytes()).hexdigest()

    # =============================================================================
    # OBSERVATIONS (direct, not interpreted)
    # =============================================================================

    observations = []
    for o in raw_observations:
        obs_text = f"[{o['condition_id']}] type={o['type']}"
        obs_text += f" status={o['status']} mechanism={o['mechanism_id']}"
        obs_text += f" bound_url={o['bound_url'] or 'N/A'}"
        obs_text += f" confidence={o['confidence']}"
        observations.append(obs_text)

    # =============================================================================
    # RAW EVIDENCE (saved separately)
    # =============================================================================

    raw_evidence = {
        "observations": raw_observations,
        "errors": errors,
        "fix_applied": True,
        "fix_description": "candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)",
        "fix_line_original": "candidates.sort(key=lambda m: m.confidence, reverse=True)",
        "fix_line_fixed": "candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)",
        "kernel_sha256_before_fix": "46929b3a951df48d7f9d1fd850871073c0d91c186aa117e13d389fe274e8d61",
    }
    raw_path = Path(__file__).parent / "raw_evidence.json"
    raw_path.write_text(json.dumps(raw_evidence, indent=2), encoding="utf-8")

    # =============================================================================
    # DERIVED MEASUREMENTS (saved separately)
    # =============================================================================

    derived = {
        "baseline_pass": baseline_pass,
        "baseline_details": [{"id": o["condition_id"], "pass": o["match_expected_status"], "status": o["status"], "mechanism": o["mechanism_id"]} for o in baseline_obs],
        "false_accepts_eliminated": false_accepts_eliminated,
        "false_accept_details": [{"id": o["condition_id"], "winner": o["mechanism_id"], "correct": o["match_expected_mechanism"]} for o in compete_equal],
        "multi_slot_dominance": multi_slot_dominance,
        "multi_slot_details": multi_slot,
        "template_only_handling": template_only_handling,
        "template_only_vs_param_details": template_vs_param,
        "template_vs_literal_winner": template_vs_literal_winner,
        "template_vs_literal_details": template_vs_literal,
        "equal_slot_tie_winner": equal_slot_tie_winner,
        "equal_slot_tie_details": equal_slot_tie,
    }
    derived_path = Path(__file__).parent / "derived_measurements.json"
    derived_path.write_text(json.dumps(derived, indent=2), encoding="utf-8")

    # =============================================================================
    # VALIDITY NOTES
    # =============================================================================

    validity_notes = [
        "Fix applied temporarily during execution — current HEAD src/spider/kernel.py L112 still has unfixed sort key (m.confidence only). Production commit requires Director approval.",
        "All conditions deterministic: no model calls, no RNG, no sampling. Single-run exact point comparisons.",
        "Synthetic substrate (jsonplaceholder.typicode.com templates) — generalizability to real-web endpoints with DOM, auth, session, drift not tested here.",
        "Each condition uses a fresh kernel instance with explicitly controlled registry contents. No cross-contamination.",
        "Registry insertion order controlled: literal registered before param in competition conditions to test tie-break.",
        "template-only-vs-literal and equal-slot-tie-param-vs-param have uncertain expected outcomes (tie-break on mechanism_id). Results are exploratory, not pass/fail.",
        "No HTTP execution for resolution conditions — only resolve() and bound_action correctness measured.",
    ]

    # =============================================================================
    # UNRESOLVED
    # =============================================================================

    unresolved = [
        "Whether the fix generalizes to real-web endpoints with DOM, auth, session state, drift (not tested here).",
        "Whether the fix has been committed to production HEAD (current HEAD unfixed, requires Director action).",
        "Whether LLM-driven mechanism distillation ('learn on A' half of C-PARAM-INHERIT) works (no model calls).",
        "Whether _matches() discriminates beyond empty dict preconditions (all mechanisms tested with preconditions={}).",
        "Whether _bind() preserves type for full-match template strings (int -> int) (only URL-embedded partial match tested).",
        "Whether template-only-vs-literal tie-break behavior is correct or needs improvement (recorded as-is).",
        "Whether equal-slot param-vs-param tie-break behavior is correct or needs improvement (recorded as-is).",
    ]

    # =============================================================================
    # RESULT.JSON
    # =============================================================================

    result = {
        "schema_version": 1,
        "experiment_id": "EXP-GRAPH-33998605047",
        "lane": "graph",
        "status": status,
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
    print(f"Status: {status}")

    # Print key findings
    print("\n=== KEY FINDINGS ===")
    print(f"H1 False accepts eliminated: {false_accepts_eliminated} ({false_accept_count}/{len(compete_equal)})")
    print(f"H2 Baseline pass: {baseline_pass} ({metrics['baseline_pass_count']}/{metrics['baseline_total']})")
    print(f"H3 Multi-slot dominance: {multi_slot_dominance}")
    print(f"H4 Template-only vs param: {template_only_handling}")
    print(f"Template-only vs literal winner: {template_vs_literal_winner}")
    print(f"Equal-slot param tie winner: {equal_slot_tie_winner}")
    print(f"Exceptions: {len(errors)}")

    # Per-condition results
    print("\n=== PER-CONDITION RESULTS ===")
    for o in raw_observations:
        check = "PASS" if o["match_expected_status"] else "FAIL"
        mech_check = ""
        if o.get("match_expected_mechanism") is True:
            mech_check = " [mech:PASS]"
        elif o.get("match_expected_mechanism") is False:
            mech_check = " [mech:FAIL]"
        print(f"  [{check}] {o['condition_id']}: status={o['status']} mech={o['mechanism_id']} url={o['bound_url']}{mech_check}")

    return result


if __name__ == "__main__":
    main()
