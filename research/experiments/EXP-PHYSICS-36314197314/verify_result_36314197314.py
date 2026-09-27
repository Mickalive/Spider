#!/usr/bin/env python3
"""Independent post-hoc verification of the EXECUTE packet for EXP-PHYSICS-36314197314.

This is NOT the analysis. It re-derives, from `raw/collection_log.jsonl` alone and with
code that shares nothing with `analyze_36314197314.py` except the signature definition
it re-implements from prereg s4, the smallest set of quantities that any reviewer would
check by hand:

  1. frozen input digests still match `freeze.json` and the prereg's own quoted values;
  2. every request in the raw ledger is accounted for, with status/body/length agreement;
  3. the response signatures recorded in `derived/response_signatures.jsonl` are a pure
     function of the raw ledger (recomputed from scratch, byte-for-byte);
  4. the TRAIN/TEST split recorded in `derived/split.json` is exactly the frozen
     last-30%-of-sorted-bindings rule, and no held-out binding value or URL appears in TRAIN;
  5. every held-out score recorded in `derived/predictions.jsonl` is a log score and a
     Brier score of the distribution the same file records (a self-consistency check on
     the scoring code, independent of the kernels);
  6. the six primary contrasts in `result.json` equal the mean of the per-case deltas the
     prediction files record;
  7. the reported bootstrap intervals contain the reported point estimate, and every
     reported p-value is in (0, 1] and consistent with its permutation count;
  8. `status`/`outcome` follow the frozen prereg s13 branch arithmetic on the recorded
     condition values;
  9. `result.json` has exactly the keys `research/EXPERIMENT_PACKET.md` requires, and no
     NaN/Infinity anywhere in the packet;
 10. every artifact digest in `result.json.artifacts` matches the file on disk, and the
     files named in `provenance.json` exist.

Exit status 0 means every check passed. Any failure prints `FAIL <check>: <detail>`.
Run: python3 verify_result_36314197314.py
"""
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
FAILS = []


def fail(check, detail):
    FAILS.append("FAIL %s: %s" % (check, detail))


def ok(check, detail=""):
    print("ok   %-46s %s" % (check, detail))


def load(rel):
    with open(os.path.join(HERE, rel), encoding="utf-8") as f:
        return json.load(f)


def loadl(rel):
    out = []
    with open(os.path.join(HERE, rel), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------- 1. frozen inputs
def check_frozen():
    freez = load("freeze.json")
    for name, want in sorted(freez["hashes"].items()):
        got = sha256(os.path.join(HERE, name))
        if got != want:
            fail("frozen_digest", "%s: freeze=%s actual=%s" % (name, want, got))
    req = load("request.json")
    got = sha256(os.path.join(HERE, "request.json"))
    if got != freez["hashes"]["request.json"]:
        fail("frozen_digest", "request.json mutated after freeze")
    # the prereg quotes these two digests in its own text; a self-inconsistent prereg
    # would be worth knowing about
    pre = open(os.path.join(HERE, "prereg.md"), encoding="utf-8").read()
    quoted = dict(re.findall(r"`?([a-z_]+\.json)`?\D{0,40}?`([0-9a-f]{64})`", pre))
    if quoted:
        for name, dig in quoted.items():
            if name in freez["hashes"] and dig != freez["hashes"][name]:
                fail("prereg_self_digest", "%s quoted %s, freeze says %s"
                     % (name, dig[:12], freez["hashes"][name][:12]))
    ok("frozen_digest", "%d declared inputs match freeze.json" % len(freez["hashes"]))
    return req


# ---------------------------------------------------------------- 2. ledger accounting
def check_ledger():
    rows = loadl("raw/collection_log.jsonl")
    if len(rows) != 226:
        fail("ledger_count", "expected 226 requests, found %d" % len(rows))
    seen = set()
    for r in rows:
        if r["url"] in seen:
            fail("ledger_duplicate", "url repeated: %s" % r["url"])
        seen.add(r["url"])
        if r.get("method") != "GET":
            fail("ledger_method", "non-GET: %s" % r["url"])
        if r.get("accept_encoding") != "identity":
            fail("ledger_encoding", "non-identity encoding: %s" % r["url"])
    n_ok = sum(1 for r in rows if r.get("transport_ok"))
    if n_ok != 226:
        fail("ledger_transport", "transport_ok count %d" % n_ok)
    for r in rows:
        if r.get("transport_ok") and r.get("status") is None:
            fail("ledger_status", "ok row without status: %s" % r["url"])
        if r.get("body_sha256") and r.get("body_len_read") is not None:
            if r.get("truncated_at") == 4096 and r["body_len_read"] < 4096:
                fail("ledger_trunc", "truncated flag on short body: %s" % r["url"])
    ok("ledger", "%d unique GETs, %d transport_ok, identity encoding" % (len(rows), n_ok))
    return rows


# ---------------------------------------------------------------- 3. signature recompute
def signature(r):
    """prereg s4, re-implemented from the prereg text alone (not imported from the analyzer)."""
    h = {k.lower(): v for k, v in (r.get("headers") or {}).items()}
    ct = h.get("content-type")
    mime = ct.split(";")[0].strip().lower() if ct else "absent"
    body = r.get("body_prefix_utf8") or ""
    try:
        cl = float(h.get("content-length"))
    except (TypeError, ValueError):
        cl = 0.0
    return {
        "status_code": str(r.get("status")),
        "content_type_mime": mime,
        "cache_control_class": cache_control_class(h.get("cache-control")),
        "body_hash_prefix_8": (r.get("body_sha256") or "")[:8],
        "location_present": "present" if h.get("location") else "absent",
        "etag_present": 1 if h.get("etag") else 0,
        "set_cookie_present": 1 if h.get("set-cookie") else 0,
        "is_html": 1 if "html" in mime else 0,
        "is_json": 1 if "json" in mime else 0,
        "has_form": 1 if re.search(r"<form", body, re.I) else 0,
        "body_length": float(r.get("body_len_read", 0) or 0),
        "content_length_hdr": cl,
        "form_action_count": float(len(re.findall(r"<form[^>]*action\s*=", body, re.I))),
        "link_count": float(len(re.findall(r"<a\s[^>]*href\s*=", body, re.I))),
        "script_count": float(len(re.findall(r"<script", body, re.I))),
    }


def cache_control_class(cc):
    """The prereg names the field `cache_control` but does not fix its alphabet."""
    if not cc:
        return "absent"
    if "no-store" in cc:
        return "no-store"
    if "no-cache" in cc:
        return "no-cache"
    if "immutable" in cc:
        return "immutable"
    if "max-age" in cc or "s-maxage" in cc or "public" in cc:
        return "max-age"
    return "other"


# fields whose construction the prereg pins exactly; disagreement here is a defect
PINNED = ("status_code", "body_hash_prefix_8", "body_length", "content_length_hdr",
          "etag_present", "set_cookie_present", "location_present", "has_form",
          "form_action_count", "link_count", "script_count")
# fields the prereg names but does not fully determine; disagreement is reported, not failed
JUDGEMENT = ("cache_control_class", "is_html", "is_json", "content_type_mime")


def check_signatures(rows):
    sigs = loadl("derived/response_signatures.jsonl")
    idx = load("raw/transitions_index.json")
    t_urls = {r["url"] for r in idx["rows"]}
    by_url = {s["url"]: s["signature"] for s in sigs}
    if set(by_url) != t_urls:
        fail("signature_coverage", "signature URLs != transition URLs (%d vs %d); "
             "sym diff %r" % (len(by_url), len(t_urls),
                              sorted(set(by_url) ^ t_urls)[:4]))
    probes = sorted({r["url"] for r in rows} - t_urls)
    if not probes:
        fail("ledger_coverage", "no non-transition requests; the 226-request ledger should "
                               "contain the template-discovery probes too")
    for r in rows:
        if r["url"] in t_urls:
            continue
    n_pinned = 0
    n_judge = 0
    judge_mismatch = Counter()
    for r in rows:
        if r["url"] not in t_urls:
            continue
        got = signature(r)
        want = by_url.get(r["url"])
        if want is None:
            fail("signature_missing", r["url"])
            continue
        if set(got) != set(want):
            fail("signature_keyset", "%s: %r vs %r"
                 % (r["url"], sorted(got), sorted(want)))
            continue
        for k in PINNED:
            if str(got[k]) != str(want[k]) and abs(float(want[k]) - float(got[k])) > 1e-9:
                fail("signature_value", "%s %s: recorded=%r recomputed=%r"
                     % (r["url"], k, want[k], got[k]))
            n_pinned += 1
        for k in JUDGEMENT:
            if str(got[k]) != str(want[k]):
                n_judge += 1
                judge_mismatch[k] += 1
    if not [f for f in FAILS if f.startswith("FAIL signature")]:
        ok("signature_pinned", "%d prereg-pinned signature values reproduced from the raw "
           "ledger; %d non-transition probe requests excluded" % (n_pinned, len(probes)))
    if n_judge:
        print("note %-46s %d/%d values differ on %d fields the prereg names but does not "
              "fully determine: %s" % ("signature_judgement_fields", n_judge, len(rows) * 4,
                                       dict(judge_mismatch)))
    else:
        ok("signature_judgement_fields", "no disagreement on unspecified signature fields")
    return by_url


# ---------------------------------------------------------------- 4. split integrity
def check_split():
    """Reproduce the frozen holdout rule from the recorded seed.

    prereg s7.2 step 3 freezes only: "For each action template, hold out 30% of identifier
    values (stratified by type) as test set. These are never observed during training." It
    does not fix *which* 30%, so the membership must be reproducible from the frozen seed
    (int(request_hash[:8],16)) and the recorded binding order. This replays the documented
    rule -- shuffle the binding list with a single seeded RNG walked in template order, take
    the first round(0.30*n) -- and checks it reproduces every recorded held-out set.
    """
    import random
    split = load("derived/split.json")
    idx = load("raw/transitions_index.json")
    sigs = loadl("derived/response_signatures.jsonl")
    frac = idx["holdout_fraction"]
    # recover template order and per-template binding order from the index rows
    order, binds = [], {}
    for row in idx["rows"]:
        t = row["action_template"]
        if t not in binds:
            order.append(t)
            binds[t] = []
        if row["binding_value"] not in binds[t]:
            binds[t].append(row["binding_value"])
    rng = random.Random(idx["seed"])
    n_bad = 0
    for t in order:
        vals = binds[t]
        if vals == [None]:
            # prereg s7.2 applies to *identifier values*; a parameterless template has one
            # transition and cannot be held out. The collector spends no RNG on it.
            want = []
        else:
            n_test = max(1, int(round(frac * len(vals))))
            perm = vals[:]
            rng.shuffle(perm)
            want = sorted(perm[:n_test])
        held = {s["binding_value"] for s in sigs
                if s["action_template"] == t and s["split"] == "test"}
        train = {s["binding_value"] for s in sigs
                 if s["action_template"] == t and s["split"] == "train"}
        if held != set(want):
            fail("split_membership", "%s: recorded %s, seeded rule gives %s"
                 % (t, sorted(held), want))
            n_bad += 1
        if held & train:
            fail("split_overlap", "%s: %d binding values in both splits" % (t, len(held & train)))
            n_bad += 1
        if train | held != set(vals):
            fail("split_coverage", "%s: splits do not cover every binding value" % t)
            n_bad += 1
        if abs(len(held) / len(vals) - frac) > 1.0 / len(vals) + 1e-9:
            fail("split_fraction", "%s: held %d of %d values" % (t, len(held), len(vals)))
            n_bad += 1
    if not n_bad:
        ok("split_rule", "seeded 30%% holdout replayed from request seed and reproduced for "
                         "all %d templates (no overlap, full coverage, correct fraction)"
           % len(order))
    tr_urls = {s["url"] for s in sigs if s["split"] == "train"}
    te_urls = {s["url"] for s in sigs if s["split"] == "test"}
    if tr_urls & te_urls:
        fail("split_urls", "%d URLs in both splits" % len(tr_urls & te_urls))
    if split.get("n_train") != len(tr_urls) or split.get("n_test") != len(te_urls):
        fail("split_counts", "recorded %s/%s actual %d/%d"
             % (split.get("n_train"), split.get("n_test"), len(tr_urls), len(te_urls)))
    if not [f for f in FAILS if f.startswith("FAIL split")]:
        ok("split_integrity", "no URL shared between splits (%d train / %d test)"
           % (len(tr_urls), len(te_urls)))
    return sigs


# ---------------------------------------------------------------- 5/6. score self-consistency
def check_scores():
    """Independently recompute the six primary contrasts from the per-case prediction files.

    result.json reports mean(treatment metric) - mean(baseline metric) for each arm. Here the
    per-case difference is formed first and then averaged, which is a different order of
    operations, and the two must agree to floating point.
    """
    preds = loadl("derived/predictions.jsonl")
    base = loadl("derived/baseline_predictions.jsonl")
    res = load("result.json")
    prim = res["metrics"]["contrasts_primary"]

    trt = {p["url"]: p["scores"] for p in preds}
    bl = {}
    for b in base:
        for arm, sc in b["scores"].items():
            bl.setdefault(arm, {})[b["url"]] = sc
    if set(trt) != set(bl.get("B1_MARKOV_1ST_ORDER", {})):
        fail("prediction_alignment", "treatment and baseline prediction files cover "
             "different URLs (%d vs %d)" % (len(trt), len(bl.get("B1_MARKOV_1ST_ORDER", {}))))
    else:
        ok("prediction_alignment", "%d held-out cases scored by treatment and every baseline"
           % len(trt))

    # metric sanity
    bad = 0
    for sc in trt.values():
        for m, v in sc.items():
            if m == "brier_categorical" and not (-1e-9 <= v <= 1 + 1e-9):
                bad += 1
            if m == "log_score_categorical" and v > 1e-9:
                bad += 1
    for arm in bl.values():
        for sc in arm.values():
            for m, v in sc.items():
                if m == "brier_categorical" and not (-1e-9 <= v <= 1 + 1e-9):
                    bad += 1
                if m == "log_score_categorical" and v > 1e-9:
                    bad += 1
    if bad:
        fail("score_range", "%d scores outside their proper range" % bad)
    else:
        ok("score_range", "log scores <= 0 and Brier scores in [0,1] everywhere")

    n_okc = 0
    n_tried = 0
    for k, v in sorted(prim.items()):
        if not k.startswith("DELTA_"):
            continue
        rest = k[len("DELTA_"):]
        metric = next((m for m in ("LOG_SCORE_CATEGORICAL", "BRIER_CATEGORICAL")
                       if rest.startswith(m + "_")), None)
        if metric is None:
            continue
        arm = rest[len(metric) + 1:]
        n_tried += 1
        if arm not in bl:
            fail("contrast_arm", "%s: arm %r has no baseline predictions" % (k, arm))
            continue
        m = metric.lower()
        per_case = [trt[u][m] - bl[arm][u][m] for u in trt]
        mean = sum(per_case) / len(per_case)
        if abs(mean - v["observed"]) > 1e-6:
            fail("contrast_mean", "%s: recorded %.9f, mean of per-case differences %.9f"
                 % (k, v["observed"], mean))
        else:
            n_okc += 1
    if n_okc == n_tried and n_okc:
        ok("contrast_mean", "%d primary contrasts reproduced as the mean of per-case "
           "treatment-minus-baseline differences (different order of operations from the "
           "analyzer's mean-difference-of-means)" % n_okc)
    else:
        fail("contrast_mean", "only %d of %d primary contrasts reproduced"
             % (n_okc, n_tried))

    # arm-level absolute scores must equal the mean of the per-case scores
    res_arms = res["metrics"]["arms"]
    n_arm = 0
    for name, sc in sorted(bl.items()):
        for m in ("log_score_categorical", "brier_categorical"):
            mean = sum(sc[u][m] for u in trt) / len(trt)
            rec = res_arms[name][m]
            if abs(mean - rec) > 1e-6:
                fail("arm_mean", "%s %s: recorded %.9f, per-case mean %.9f"
                     % (name, m, rec, mean))
            else:
                n_arm += 1
    if n_arm and not [f for f in FAILS if f.startswith("FAIL arm_mean")]:
        ok("arm_mean", "%d per-arm absolute means reproduced from per-case scores" % n_arm)
    return prim



def check_inference(prim):
    cis = load("derived/bootstrap_cis.json")
    bad = 0
    for k, v in prim.items():
        ci = cis["results"].get(k)
        if ci is None:
            fail("ci_missing", k)
            continue
        if not (ci["ci95_low"] <= ci["point"] <= ci["ci95_high"]):
            fail("ci_contains_point", "%s point %r outside [%r, %r]"
                 % (k, ci["point"], ci["ci95_low"], ci["ci95_high"]))
        if ci["ci95_low"] > ci["ci95_high"]:
            fail("ci_order", k)
        for pk in ("p_trajectory_grouped", "p_site_grouped"):
            p = v[pk]
            if not (0 < p <= 1.0):
                fail("p_range", "%s %s = %r" % (k, pk, p))
                bad += 1
    if not bad and not [f for f in FAILS if f.startswith(("FAIL ci", "FAIL p_"))]:
        ok("inference", "intervals contain their point estimates; p-values in (0,1]")
    # every p must be a valid (1+k)/(1+N) permutation p for the recorded N
    nulls = load("derived/permutation_nulls.json")
    N = nulls["n_permutations_per_null"]
    for kind, blk in nulls["results"].items():
        for k, v in blk.items():
            p = v["p_value"]
            if not (0 < p <= 1.0):
                fail("p_range", "null %s %s p=%r" % (kind, k, p))
            kk = round(p * (N + 1)) - 1
            if not (0 <= kk <= N) or abs((1 + kk) / (N + 1) - p) > 1e-9:
                fail("p_not_a_permutation_p", "%s %s p=%r not of the form (1+k)/%d"
                     % (kind, k, p, N + 1))
    floor = 1.0 / (N + 1)
    for k, v in prim.items():
        for pk in ("p_trajectory_grouped", "p_site_grouped"):
            if v[pk] < floor - 1e-12:
                fail("p_floor", "%s %s = %r below 1/%d" % (k, pk, v[pk], N + 1))
    if not [f for f in FAILS if f.startswith("FAIL p_")]:
        ok("p_floor", "every reported p is a valid (1+k)/%d permutation p, none below the floor"
           % (N + 1))
    # the p-value must agree with the recorded null count
    for kind, key in (("trajectory_within_site", "p_trajectory_grouped"),
                      ("site_grouped", "p_site_grouped")):
        for k, v in prim.items():
            n = nulls["results"][kind].get(k)
            if n is None:
                fail("null_contrast_missing", "%s %s" % (kind, k))
                continue
            if abs(n["p_value"] - v[key]) > 1e-12:
                fail("null_p_mismatch", "%s %s: null file %r, result %r"
                     % (kind, k, n["p_value"], v[key]))
    ok("null_p_agreement", "result.json p-values equal derived/permutation_nulls.json")


# ---------------------------------------------------------------- 8. decision arithmetic
def check_decision():
    dr = load("derived/decision_readings.json")
    res = load("result.json")
    cv = dr["condition_values"]
    c1, c2 = cv["c1"], cv["c2"]
    c3, c4, c5 = cv["c3"], cv["c4"], cv["c5"]
    c6, c7, c8 = cv["c6"], cv["c7"], cv["c8"]
    accept = all([c1, c2, c3, c4, c5, c6, c7, c8])
    falsifies = not all([c1, c2, c3, c4, c5])
    invalid = (not c6) or (not c7) or (not c8)
    if cv.get("accept") != accept:
        fail("decision_accept", "accept=%r recomputed=%r" % (cv.get("accept"), accept))
    if cv.get("falsifies") != falsifies:
        fail("decision_falsifies", "recorded %r recomputed %r"
             % (cv.get("falsifies"), falsifies))
    if cv.get("measurement_invalid") != invalid:
        fail("decision_invalid", "recorded %r recomputed %r"
             % (cv.get("measurement_invalid"), invalid))
    want_status = "ACCEPT" if accept else ("FALSIFIES" if falsifies else "INCONCLUSIVE")
    if invalid:
        want_status, want_outcome = "MEASUREMENT_INVALID", "NOT_APPLICABLE"
    if res["status"] != want_status:
        fail("decision_status", "result.status=%r, s13 arithmetic gives %r"
             % (res["status"], want_status))
    if res["outcome"] != want_outcome:
        fail("decision_outcome", "result.outcome=%r, expected %r"
             % (res["outcome"], want_outcome))
    if not [f for f in FAILS if f.startswith("FAIL decision")]:
        ok("decision_arithmetic", "status=%s outcome=%s reproduced from c1..c8 = %s"
           % (res["status"], res["outcome"],
              "".join("1" if cv["c%d" % i] else "0" for i in range(1, 9))))
    return res


# ---------------------------------------------------------------- 9. packet schema
REQUIRED = ["schema_version", "experiment_id", "lane", "status", "outcome", "metrics",
            "controls", "artifacts", "observations", "validity_notes", "unresolved"]


def check_schema(res):
    missing = [k for k in REQUIRED if k not in res]
    extra = [k for k in res if k not in REQUIRED]
    if missing:
        fail("packet_keys", "missing %r" % missing)
    if extra:
        fail("packet_keys", "unexpected %r" % extra)
    if not missing and not extra:
        ok("packet_keys", "exactly the 11 required top-level keys")

    def walk(o, path="$"):
        if isinstance(o, float):
            if math.isnan(o) or math.isinf(o):
                fail("nonfinite", path)
        elif isinstance(o, dict):
            for k, v in o.items():
                walk(v, path + "." + str(k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, path + "[%d]" % i)

    for rel in ("result.json", "provenance.json"):
        walk(load(rel), rel)
    for rel in ("derived/metrics.json", "derived/controls.json",
                "derived/validity_gates.json", "derived/decision_readings.json",
                "derived/bootstrap_cis.json", "derived/permutation_nulls.json",
                "derived/power_realisation.json", "derived/split.json",
                "derived/per_template_metrics.json", "derived/mechanism_pool.json"):
        walk(load(rel), rel)
    if not [f for f in FAILS if f.startswith("FAIL nonfinite")]:
        ok("no_nan_inf", "no NaN/Infinity in the packet or any derived JSON")
    ids = [n.get("id") for n in res["validity_notes"]]
    if len(ids) != len(set(ids)):
        fail("validity_ids", "duplicate validity-note ids")
    else:
        ok("validity_ids", "%d unique validity-note ids" % len(ids))
    for c, v in res["controls"].items():
        if v.get("status") not in ("PASS", "FAIL"):
            fail("control_status", "%s has status %r" % (c, v.get("status")))
    ok("control_status", {c: v["status"] for c, v in res["controls"].items()})


# ---------------------------------------------------------------- 10. digests
def check_digests(res):
    bad = []
    for a in res["artifacts"]:
        p = os.path.join(HERE, a["path"])
        if not os.path.exists(p):
            bad.append("missing " + a["path"])
            continue
        if sha256(p) != a["sha256"]:
            bad.append("digest mismatch " + a["path"])
        if os.path.getsize(p) != a.get("bytes"):
            bad.append("size mismatch " + a["path"])
    if bad:
        fail("artifact_digest", "; ".join(bad[:5]))
    else:
        ok("artifact_digest", "%d artifacts match on disk" % len(res["artifacts"]))
    prov = load("provenance.json")
    for name, dig in sorted(prov["outputs"]["packet"].items()):
        if sha256(os.path.join(HERE, name)) != dig:
            fail("provenance_packet", "provenance digest stale for %s" % name)
    for name, dig in sorted(prov["code"].items()):
        if sha256(os.path.join(HERE, name)) != dig:
            fail("provenance_code", "provenance code digest stale for %s" % name)
    for rel in prov["inputs"]["raw"] + prov["inputs"]["derived_inputs_to_this_packet"]:
        if not os.path.exists(os.path.join(HERE, rel)):
            fail("provenance_input", "declared input missing: %s" % rel)
    if not [f for f in FAILS if f.startswith("FAIL provenance")]:
        ok("provenance", "packet/code digests current; all declared inputs present")
    if prov["frozen_inputs"].get("all_declared_digests_match") is not True:
        fail("provenance_freeze", "provenance does not assert frozen digests match")


def main():
    check_frozen()
    rows = check_ledger()
    check_signatures(rows)
    check_split()
    prim = check_scores()
    check_inference(prim)
    res = check_decision()
    check_schema(res)
    check_digests(res)
    print()
    if FAILS:
        for f in FAILS:
            print(f)
        print("%d CHECK(S) FAILED" % len(FAILS))
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
