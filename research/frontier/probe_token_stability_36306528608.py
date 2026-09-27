"""Cross-session identifier stability probe for EXP-FRONTIER-36306528608.

Mandated by the frozen prereg:

  * prereg 11 classification protocol step 3 -- determine whether `required_action` can be
    constructed solely from ONE unconditional GET of the root observation. A named token
    field is not a token; only a VALUE present in the root body is. This probe measures
    that value directly and measures whether it is stable across INDEPENDENT fresh
    sessions, which is the operational definition of "not re-derivable".
  * prereg measurement_validity.durable_evidence.identifier_classification_log -- "every
    detected identifier with type, subtype, value, source, episode, stability
    classification".

SAFETY. This probe issues READ-ONLY GET requests only. It never submits a form, never
mints an account, never sends a non-GET request to a third party, and never causes a
state transition on a production system. No write leg is exercised, by design.
"""

from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from harness_36306528608 import (  # noqa: E402
    EXPERIMENT_ID, RAW_DIR, HttpSubstrate, JsonlWriter, ResponseCache, sha256_hex,
    parse_forms,
)

# Sites whose screen record already exhibited a server-minted token-gated POST form.
PROBE_TARGETS = [
    ("gitlab_trial_registration", "https://gitlab.com/-/trial_registrations/new/"),
    ("wikipedia_create_account", "https://auth.wikimedia.org/enwiki/w/index.php?title=Special:CreateAccount"),
]
INDEPENDENT_SESSIONS = 3

TOKEN_VALUE_RE = {
    "gitlab": re.compile(
        r"<input[^>]*name=[\"']authenticity_token[\"'][^>]*value=[\"']([^\"']+)[\"']", re.IGNORECASE),
    "wikimedia": re.compile(
        r"<input[^>]*name=[\"'](?:wpCreateaccountToken|wpEditToken)[\"'][^>]*value=[\"']([^\"']+)[\"']",
        re.IGNORECASE),
}


def _field_name_of(matched_input_tag: str) -> str:
    """Recover the input's name attribute from the matched <input ...> tag."""
    m = re.search(r"""name=["']([^"']+)["']""", matched_input_tag, re.IGNORECASE)
    return m.group(1) if m else ""


def main() -> int:
    os.makedirs(RAW_DIR, exist_ok=True)
    http_w = JsonlWriter(os.path.join(RAW_DIR, "http.jsonl"))
    ident_w = JsonlWriter(os.path.join(RAW_DIR, "identifiers.jsonl"))
    probe_w = JsonlWriter(os.path.join(RAW_DIR, "token_stability.jsonl"))
    cache = ResponseCache()

    report = {
        "experiment_id": EXPERIMENT_ID,
        "design": "read-only GET only; no non-GET request; no state transition on any host",
        "independent_sessions_per_target": INDEPENDENT_SESSIONS,
        "targets": [],
    }

    for label, url in PROBE_TARGETS:
        key = "gitlab" if "gitlab" in label else "wikimedia"
        per_session = []
        for s in range(INDEPENDENT_SESSIONS):
            # A genuinely independent fresh session: new opener, new cookie jar, no reuse.
            sess = HttpSubstrate(cookies=True, label=f"{label}-s{s}",
                                 cache=cache, cache_key_prefix=f"probe|{label}|s{s}")
            r = sess.fetch(url)
            ev = r.evidence()
            ev["kind"] = "token_stability_probe"
            ev["probe_label"] = label
            ev["session"] = s
            http_w.write(ev)
            cache.put(r, f"probe:{label}:s{s}")

            forms = parse_forms(r.text, r.final_url)
            values: dict[str, str] = {}
            for m in TOKEN_VALUE_RE[key].finditer(r.text):
                nm = _field_name_of(m.group(0))
                if nm:
                    values[nm] = m.group(1)
            per_session.append({
                "session": s,
                "url": r.final_url or url,
                "status_code": r.status_code,
                "body_sha256": r.body_sha256,
                "cookie_names": sess.cookie_names(),
                "cookie_fingerprint": sess.cookie_fingerprint(),
                "n_forms": len(forms),
                "nonget_forms_with_token_input": [
                    {"action": f["action"], "method": f["method"], "token_fields": f["token_fields"]}
                    for f in forms if f["method"] != "GET" and f["has_token_field"]
                ],
                "token_values_found": {k: sha256_hex(v) for k, v in values.items()},
                "token_value_lengths": {k: len(v) for k, v in values.items()},
                "token_value_prefixes": {k: v[:12] for k, v in values.items()},
            })
            for k, v in values.items():
                ident_w.write({
                    "experiment_id": EXPERIMENT_ID,
                    "site": label, "episode": f"probe_session_{s}",
                    "page_url": r.final_url or url, "page_depth": None,
                    "identifier_type": "server_minted_csrf_token",
                    "subtype": k, "value_sha256": sha256_hex(v),
                    "value_prefix": v[:12], "value_len": len(v),
                    "source": "token_gated_form_page",
                    "in_root_observation": True,
                    "stability": "PENDING_CROSS_SESSION_COMPARISON",
                })

        # Cross-session stability: the operational test for re-derivability.
        distinct_by_field = {}
        for fname in sorted({k for s in per_session for k in s["token_values_found"]}):
            seen = [s["token_values_found"].get(fname) for s in per_session]
            distinct = {v for v in seen if v}
            distinct_by_field[fname] = {
                "n_sessions_with_value": len(distinct),
                "n_distinct_values": len(distinct),
                "distinct_value_sha256": sorted(distinct),
                "STABLE_ACROSS_INDEPENDENT_SESSIONS": len(distinct) == 1 and len(seen) > 1,
            }
        distinct_cookies = {s["cookie_fingerprint"] for s in per_session}
        distinct_bodies = {s["body_sha256"] for s in per_session}

        rec = {
            "experiment_id": EXPERIMENT_ID,
            "probe_label": label,
            "url": url,
            "sessions": per_session,
            "token_stability_by_field": distinct_by_field,
            "n_distinct_cookie_fingerprints": len(distinct_cookies),
            "n_distinct_body_hashes": len(distinct_bodies),
            "finding": (
                "token value is minted per session and differs across independent fresh "
                "sessions, so it cannot be obtained from one unconditional GET of the root "
                "observation: the action-gating object is NOT re-derivable"
                if any(not v["STABLE_ACROSS_INDEPENDENT_SESSIONS"] for v in distinct_by_field.values())
                else "token value is stable across independent fresh sessions"
            ) if distinct_by_field else "no token value present in the page",
        }
        probe_w.write(rec)
        report["targets"].append(rec)
        print(f"[probe] {label}: {json.dumps(rec['token_stability_by_field'])[:400]}", flush=True)
        print(f"        distinct_cookie_fingerprints={rec['n_distinct_cookie_fingerprints']} "
              f"distinct_body_hashes={rec['n_distinct_body_hashes']}", flush=True)

    cache.flush_keys()
    cache.flush_index()
    for w in (http_w, ident_w, probe_w):
        w.close()
    out = os.path.join("research", "experiments", EXPERIMENT_ID, "derived", "token_stability.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1, sort_keys=True)
    print("[probe] done ->", out, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
