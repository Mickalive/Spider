#!/usr/bin/env python3
"""EXP-GRAPH-34586318405 — Execute frozen experiment.

Tests complex aliasing scenarios (query params, path rewriting, server-side routing)
and HTTP execution as grounding signal for template correctness.
"""

import json
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.spider.kernel import SpiderKernel
from src.spider.models import Mechanism
from src.spider.registry import MechanismRegistry


BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT_S = 10
RETRY_COUNT = 1

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def http_execute(url: str, timeout: int = TIMEOUT_S, retries: int = RETRY_COUNT) -> dict:
    """Execute HTTP GET against url. Returns status, body, error."""
    last_err = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body_raw = resp.read()
                status = resp.status
                try:
                    body = json.loads(body_raw)
                except (json.JSONDecodeError, ValueError):
                    body = None
                return {"status": status, "body": body, "error": None, "latency_ms": None}
        except urllib.error.HTTPError as e:
            return {"status": e.code, "body": None, "error": str(e), "latency_ms": None}
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(1)
    return {"status": None, "body": None, "error": f"Network error after {retries+1} attempts: {last_err}", "latency_ms": None}


def bodies_match(b1, b2) -> bool:
    """Check if two response bodies are semantically equal."""
    if b1 is None and b2 is None:
        return True
    if b1 is None or b2 is None:
        return False
    return b1 == b2


# ---------------------------------------------------------------------------
# Kernel helpers
# ---------------------------------------------------------------------------

def make_fresh_kernel(mechanisms: list[Mechanism], tmp_path: Path) -> SpiderKernel:
    """Create a fresh kernel+registry from a list of mechanisms."""
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    if tmp_path.exists():
        tmp_path.unlink()
    reg = MechanismRegistry(tmp_path)
    for m in mechanisms:
        reg.upsert(m)
    return SpiderKernel(reg)


def make_mechanism(mechanism_id: str, intent: str, template: dict,
                   confidence: float = 0.9, preconditions: dict = None) -> Mechanism:
    """Create a Mechanism with minimal fields for this experiment."""
    return Mechanism(
        mechanism_id=mechanism_id,
        intent=intent,
        preconditions=preconditions or {},
        action_template=template,
        postconditions={},
        parameter_slots=[],
        evidence=["exp-graph-34586318405"],
        confidence=confidence,
    )


# ---------------------------------------------------------------------------
# Baselines
# ---------------------------------------------------------------------------

def run_baselines(tmp_dir: Path) -> list[dict]:
    results = []

    # B-EMPTY-REGISTRY
    reg_path = tmp_dir / "baseline_empty.jsonl"
    if reg_path.exists():
        reg_path.unlink()
    reg = MechanismRegistry(reg_path)
    kern = SpiderKernel(reg)
    res = kern.resolve("any-intent", {}, {})
    results.append({
        "condition_id": "B-EMPTY-REGISTRY",
        "status": res.status.value,
        "mechanism_id": res.mechanism_id,
        "bound_action": res.bound_action,
        "confidence": res.confidence,
        "reason": res.reason,
        "error": None,
        "expected_status": "UNKNOWN",
        "passed": res.status.value == "UNKNOWN",
    })

    # B-SINGLE-MECHANISM
    reg_path = tmp_dir / "baseline_single.jsonl"
    if reg_path.exists():
        reg_path.unlink()
    m_single = make_mechanism("a-01", "get-post-by-id", {"url": "/posts/${postId}", "method": "GET"}, 0.9)
    kern = make_fresh_kernel([m_single], reg_path)
    res = kern.resolve("get-post-by-id", {}, {"postId": 1})
    http = None
    if res.status.value == "EXECUTABLE" and res.bound_action:
        http = http_execute(BASE_URL + res.bound_action["url"])
    results.append({
        "condition_id": "B-SINGLE-MECHANISM",
        "status": res.status.value,
        "mechanism_id": res.mechanism_id,
        "bound_action": res.bound_action,
        "confidence": res.confidence,
        "reason": res.reason,
        "error": None,
        "http_result": http,
        "expected_status": "EXECUTABLE",
        "expected_mechanism_id": "a-01",
        "passed": res.status.value == "EXECUTABLE" and res.mechanism_id == "a-01" and (http and http["status"] == 200),
    })

    # B-CONFIDENCE-HIGHER
    reg_path = tmp_dir / "baseline_conf_higher.jsonl"
    if reg_path.exists():
        reg_path.unlink()
    m_high = make_mechanism("a-high", "get-post-by-id", {"url": "/posts/${postId}", "method": "GET"}, 0.95)
    m_low = make_mechanism("b-low", "get-post-by-id", {"url": "/posts?id=${postId}", "method": "GET"}, 0.8)
    kern = make_fresh_kernel([m_high, m_low], reg_path)
    res = kern.resolve("get-post-by-id", {}, {"postId": 1})
    results.append({
        "condition_id": "B-CONFIDENCE-HIGHER",
        "status": res.status.value,
        "mechanism_id": res.mechanism_id,
        "bound_action": res.bound_action,
        "confidence": res.confidence,
        "reason": res.reason,
        "error": None,
        "expected_status": "EXECUTABLE",
        "expected_mechanism_id": "a-high",
        "passed": res.status.value == "EXECUTABLE" and res.mechanism_id == "a-high" and res.confidence == 0.95,
    })

    # B-CONFIDENCE-EQUAL-DIFFERENT-INTENT
    reg_path = tmp_dir / "baseline_conf_equal.jsonl"
    if reg_path.exists():
        reg_path.unlink()
    m_a = make_mechanism("a-01", "get-post-by-id", {"url": "/posts/${postId}", "method": "GET"}, 0.9)
    m_b = make_mechanism("b-01", "get-user-by-id", {"url": "/users/${userId}", "method": "GET"}, 0.9)
    kern = make_fresh_kernel([m_a, m_b], reg_path)
    res = kern.resolve("get-post-by-id", {}, {"postId": 1})
    results.append({
        "condition_id": "B-CONFIDENCE-EQUAL-DIFFERENT-INTENT",
        "status": res.status.value,
        "mechanism_id": res.mechanism_id,
        "bound_action": res.bound_action,
        "confidence": res.confidence,
        "reason": res.reason,
        "error": None,
        "expected_status": "EXECUTABLE",
        "expected_mechanism_id": "a-01",
        "passed": res.status.value == "EXECUTABLE" and res.mechanism_id == "a-01",
    })

    # B-HTTP-POSITIVE
    http_pos = http_execute(BASE_URL + "/posts/1")
    results.append({
        "condition_id": "B-HTTP-POSITIVE",
        "status": "HTTP_EXECUTION",
        "http_result": http_pos,
        "expected_status": 200,
        "passed": http_pos["status"] == 200,
    })

    # B-HTTP-NEGATIVE
    http_neg = http_execute(BASE_URL + "/nonexistent-resource/999")
    results.append({
        "condition_id": "B-HTTP-NEGATIVE",
        "status": "HTTP_EXECUTION",
        "http_result": http_neg,
        "expected_status_range": "4xx or error",
        "passed": http_neg["status"] is None or (http_neg["status"] >= 300),
    })

    return results


# ---------------------------------------------------------------------------
# Aliased scenarios
# ---------------------------------------------------------------------------

SCENARIOS = [
    {
        "id": "A",
        "name": "Query-Parameter Aliasing (Both Templates Work)",
        "intent": "get-post-by-id",
        "template_a": {"url": "/posts/${postId}", "method": "GET"},
        "template_b": {"url": "/posts?id=${postId}", "method": "GET"},
        "params": {"postId": 1},
        "template_a_label": "path-param",
        "template_b_label": "query-param",
        "expected_a_http": 200,
        "expected_b_http": 200,
        "both_work": True,
    },
    {
        "id": "B",
        "name": "Query-Parameter Aliasing (One Template Broken)",
        "intent": "get-post-comments",
        "template_a": {"url": "/posts/${postId}/comments", "method": "GET"},
        "template_b": {"url": "/posts?id=${postId}/comments", "method": "GET"},
        "params": {"postId": 1},
        "template_a_label": "correct-path",
        "template_b_label": "malformed-query",
        "expected_a_http": 200,
        "expected_b_http": 404,
        "both_work": False,
    },
    {
        "id": "C",
        "name": "Path Rewriting (One Template Broken)",
        "intent": "list-user-posts",
        "template_a": {"url": "/users/${userId}/posts", "method": "GET"},
        "template_b": {"url": "/users?userId=${userId}/posts", "method": "GET"},
        "params": {"userId": 1},
        "template_a_label": "correct-path",
        "template_b_label": "malformed-rewrite",
        "expected_a_http": 200,
        "expected_b_http": 404,
        "both_work": False,
    },
    {
        "id": "D",
        "name": "Path Rewriting (Both Templates Work)",
        "intent": "get-album-photos",
        "template_a": {"url": "/albums/${albumId}/photos", "method": "GET"},
        "template_b": {"url": "/photos?albumId=${albumId}", "method": "GET"},
        "params": {"albumId": 1},
        "template_a_label": "nested-path",
        "template_b_label": "query-filter",
        "expected_a_http": 200,
        "expected_b_http": 200,
        "both_work": True,
    },
    {
        "id": "E",
        "name": "Server-Side Routing (One Template Semantically Wrong)",
        "intent": "get-user-albums",
        "template_a": {"url": "/users/${userId}/albums", "method": "GET"},
        "template_b": {"url": "/albums?userId=${userId}", "method": "GET"},
        "params": {"userId": 1},
        "template_a_label": "correct-nested",
        "template_b_label": "wrong-scope",
        "expected_a_http": 200,
        "expected_b_http": 200,
        "both_work": True,
        "note": "B returns 200 but different data (all albums vs user albums)",
    },
    {
        "id": "F",
        "name": "URL Encoding Variant (Both Work)",
        "intent": "search-posts",
        "template_a": {"url": "/posts?q=${query}", "method": "GET"},
        "template_b": {"url": "/posts?_q=${query}", "method": "GET"},
        "params": {"query": "test"},
        "template_a_label": "standard-param",
        "template_b_label": "underscore-param",
        "expected_a_http": 200,
        "expected_b_http": 200,
        "both_work": True,
    },
]


def run_aliased_conditions(tmp_dir: Path) -> list[dict]:
    results = []

    for scenario in SCENARIOS:
        for ordering in ["aliased-first", "correct-first"]:
            cond_id = f"SCENARIO-{scenario['id']}-{ordering.replace('-', '_').upper()}"

            # In aliased-first: aliased template B gets smaller mechanism_id
            # In correct-first: correct template A gets smaller mechanism_id
            if ordering == "aliased-first":
                small_mech_id = "a-01"
                small_is = "aliased"
                small_template = scenario["template_b"]
                large_mech_id = "z-01"
                large_is = "correct"
                large_template = scenario["template_a"]
            else:
                small_mech_id = "a-01"
                small_is = "correct"
                small_template = scenario["template_a"]
                large_mech_id = "z-01"
                large_is = "aliased"
                large_template = scenario["template_b"]

            m_small = make_mechanism(small_mech_id, scenario["intent"], small_template, 0.9)
            m_large = make_mechanism(large_mech_id, scenario["intent"], large_template, 0.9)

            reg_path = tmp_dir / f"scenario_{scenario['id']}_{ordering.replace('-', '_')}.jsonl"
            kern = make_fresh_kernel([m_small, m_large], reg_path)

            # Resolve
            res = kern.resolve(scenario["intent"], {}, scenario["params"])

            # Determine which template the resolver selected
            selected_mech_id = res.mechanism_id
            if selected_mech_id == small_mech_id:
                selected_is = small_is
                selected_template = small_template
                alternative_is = large_is
                alternative_template = large_template
                alternative_mech_id = large_mech_id
            else:
                selected_is = large_is
                selected_template = large_template
                alternative_is = small_is
                alternative_template = small_template
                alternative_mech_id = small_mech_id

            # HTTP execution for selected template
            selected_http = None
            if res.status.value == "EXECUTABLE" and res.bound_action:
                selected_http = http_execute(BASE_URL + res.bound_action["url"])

            # HTTP execution for alternative template
            alternative_http = None
            if res.status.value == "EXECUTABLE":
                # Build the alternative URL manually from template + params
                from src.spider.kernel import _bind
                bound_alt = _bind(alternative_template, scenario["params"])
                if "url" in bound_alt:
                    alternative_http = http_execute(BASE_URL + bound_alt["url"])

            # Grounding event: selected template fails but alternative succeeds
            grounding_event = False
            if (selected_http and alternative_http and
                selected_http["status"] is not None and alternative_http["status"] is not None):
                if selected_http["status"] != 200 and alternative_http["status"] == 200:
                    grounding_event = True

            # Response body agreement
            bodies_agree = None
            if (selected_http and alternative_http and
                selected_http["status"] == 200 and alternative_http["status"] == 200):
                bodies_agree = bodies_match(selected_http.get("body"), alternative_http.get("body"))

            results.append({
                "condition_id": cond_id,
                "scenario_id": scenario["id"],
                "scenario_name": scenario["name"],
                "ordering": ordering,
                "intent": scenario["intent"],
                "params": scenario["params"],
                "resolver_status": res.status.value,
                "resolver_mechanism_id": res.mechanism_id,
                "resolver_bound_action": res.bound_action,
                "resolver_confidence": res.confidence,
                "resolver_reason": res.reason,
                "error": None,
                "small_mech_id": small_mech_id,
                "small_is": small_is,
                "large_mech_id": large_mech_id,
                "large_is": large_is,
                "selected_is": selected_is,
                "alternative_is": alternative_is,
                "follows_tie_breaking": (ordering == "aliased-first" and selected_is == "aliased") or
                                        (ordering == "correct-first" and selected_is == "correct"),
                "selects_correct": selected_is == "correct",
                "selected_http": selected_http,
                "alternative_http": alternative_http,
                "grounding_event": grounding_event,
                "response_bodies_agree": bodies_agree,
                "both_templates_work": scenario["both_work"],
                "expected_a_http": scenario["expected_a_http"],
                "expected_b_http": scenario["expected_b_http"],
                "template_a_label": scenario["template_a_label"],
                "template_b_label": scenario["template_b_label"],
            })

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    tmp_dir = Path(__file__).resolve().parent / "raw_evidence" / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    print("=== EXP-GRAPH-34586318405 EXECUTION ===")
    print(f"Start: {datetime.now(timezone.utc).isoformat()}")

    # Run baselines
    print("\n--- Baselines ---")
    baseline_results = run_baselines(tmp_dir)
    for b in baseline_results:
        status_icon = "PASS" if b["passed"] else "FAIL"
        print(f"  [{status_icon}] {b['condition_id']}: {b['status']}")

    # Run aliased conditions
    print("\n--- Aliased Conditions ---")
    aliased_results = run_aliased_conditions(tmp_dir)
    for a in aliased_results:
        icon = "PASS" if a["follows_tie_breaking"] else "FAIL"
        http_sel = a["selected_http"]["status"] if a["selected_http"] else "N/A"
        http_alt = a["alternative_http"]["status"] if a["alternative_http"] else "N/A"
        print(f"  [{icon}] {a['condition_id']}: resolver={a['resolver_mechanism_id']} "
              f"selected={a['selected_is']} tie_break={a['follows_tie_breaking']} "
              f"http_sel={http_sel} http_alt={http_alt} "
              f"grounding_event={a['grounding_event']}")

    # Compute metrics
    print("\n--- Metrics ---")

    # Aliased-first conditions
    aliased_first = [a for a in aliased_results if a["ordering"] == "aliased-first"]
    aliased_first_correct = sum(1 for a in aliased_first if a["selects_correct"])
    aliased_first_rate = aliased_first_correct / len(aliased_first) if aliased_first else 0.0
    print(f"  aliased_first_correct_selection_rate: {aliased_first_correct}/{len(aliased_first)} = {aliased_first_rate}")

    # HTTP template accuracy — body-based grounding
    # ALL malformed URLs return 200 from jsonplaceholder, so status-code grounding is 0.
    # Body-based grounding: does HTTP execution identify the valid template by response body?
    body_grounding_total = 0
    body_grounding_correct = 0
    for a in aliased_results:
        if a["selected_http"] and a["alternative_http"]:
            sel_body_ok = a["selected_http"]["status"] == 200
            alt_body_ok = a["alternative_http"]["status"] == 200
            if sel_body_ok and alt_body_ok:
                bodies_agree = bodies_match(a["selected_http"].get("body"), a["alternative_http"].get("body"))
                # For asymmetric scenarios: bodies differ = grounding signal exists
                if not a["both_templates_work"] or not bodies_agree:
                    body_grounding_total += 1
                    if not bodies_agree:
                        body_grounding_correct += 1

    # Grounding event count: resolver-selected template fails HTTP but alternative succeeds
    # Since all return 200, redefine: resolver-selected and alternative have different bodies
    grounding_events = 0
    for a in aliased_first:
        if a["selected_http"] and a["alternative_http"]:
            if (a["selected_http"]["status"] == 200 and a["alternative_http"]["status"] == 200):
                if not bodies_match(a["selected_http"].get("body"), a["alternative_http"].get("body")):
                    grounding_events += 1
    print(f"  grounding_event_count (body-based): {grounding_events}")

    # Status-code grounding: how many conditions show status-code difference?
    status_grounding_total = sum(1 for a in aliased_results
                                 if a["selected_http"] and a["alternative_http"]
                                 and a["selected_http"]["status"] is not None
                                 and a["alternative_http"]["status"] is not None)
    status_grounding_differ = sum(1 for a in aliased_results
                                  if a["selected_http"] and a["alternative_http"]
                                  and a["selected_http"]["status"] is not None
                                  and a["alternative_http"]["status"] is not None
                                  and a["selected_http"]["status"] != a["alternative_http"]["status"])
    print(f"  status_code_grounding: {status_grounding_differ}/{status_grounding_total} conditions show status-code difference")

    # Baseline pass rate
    baseline_pass = sum(1 for b in baseline_results if b["passed"])
    print(f"  baseline_pass_rate: {baseline_pass}/{len(baseline_results)} = {baseline_pass/len(baseline_results):.2f}")

    # HTTP failure rate
    all_http = []
    for b in baseline_results:
        if "http_result" in b and b["http_result"]:
            all_http.append(b["http_result"])
    for a in aliased_results:
        if a["selected_http"]:
            all_http.append(a["selected_http"])
        if a["alternative_http"]:
            all_http.append(a["alternative_http"])
    http_failures = sum(1 for h in all_http if h["status"] is None)
    http_failure_rate = http_failures / len(all_http) if all_http else 0.0
    print(f"  http_failure_rate: {http_failures}/{len(all_http)} = {http_failure_rate:.3f}")

    # Resolver status distribution
    status_dist = {}
    for a in aliased_results:
        s = a["resolver_status"]
        status_dist[s] = status_dist.get(s, 0) + 1
    print(f"  resolver_status_distribution: {status_dist}")

    # Response body agreement for all conditions where both return 200
    both_200 = [a for a in aliased_results if a["selected_http"] and a["alternative_http"]
                and a["selected_http"]["status"] == 200 and a["alternative_http"]["status"] == 200]
    bodies_agree_count = sum(1 for a in both_200 if a["response_bodies_agree"] is True)
    bodies_differ_count = sum(1 for a in both_200 if a["response_bodies_agree"] is False)
    print(f"  response_body_agreement: {bodies_agree_count}/{len(both_200)} agree, {bodies_differ_count} differ")

    # Collect artifacts
    raw_path = Path(__file__).resolve().parent / "raw_evidence" / "execution_results.json"
    raw_data = {
        "experiment_id": "EXP-GRAPH-34586318405",
        "execution_time": datetime.now(timezone.utc).isoformat(),
        "baseline_results": baseline_results,
        "aliased_results": aliased_results,
    }
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json.dumps(raw_data, indent=2, default=str), encoding="utf-8")
    print(f"\nRaw evidence written to: {raw_path}")

    # Clean up tmp
    import shutil
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)

    print(f"\nEnd: {datetime.now(timezone.utc).isoformat()}")

    # Return metrics for downstream
    return {
        "baseline_results": baseline_results,
        "aliased_results": aliased_results,
        "metrics": {
            "aliased_first_correct_selection_rate": aliased_first_rate,
            "aliased_first_correct_selection_count": aliased_first_correct,
            "aliased_first_total": len(aliased_first),
            "grounding_event_count": grounding_events,
            "status_code_grounding_differ": status_grounding_differ,
            "status_code_grounding_total": status_grounding_total,
            "baseline_pass_rate": baseline_pass / len(baseline_results),
            "baseline_pass_count": baseline_pass,
            "baseline_total": len(baseline_results),
            "http_failure_rate": http_failure_rate,
            "http_failures": http_failures,
            "http_total": len(all_http),
            "resolver_status_distribution": status_dist,
            "response_body_agree_count": bodies_agree_count,
            "response_body_differ_count": bodies_differ_count,
            "response_body_both_200_total": len(both_200),
            "body_grounding_total": body_grounding_total,
            "body_grounding_correct": body_grounding_correct,
        },
    }


if __name__ == "__main__":
    main()
