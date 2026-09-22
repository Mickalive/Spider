#!/usr/bin/env python3
"""Independent audit-style recomputation for EXP-RUNTIME-35764329925.

Recomputes fingerprints from raw observation fields (NOT from stored fingerprint
fields) using the frozen parent algorithm, then recomputes every Jaccard
distance + degenerate CI and compares 1:1 with the producer's
experiment_result.json metrics. Spec requires 0 mismatches.
"""
import hashlib
import json
import random
from collections import defaultdict

RAW = "raw_observations.jsonl"
RESULT = "experiment_result.json"

EXCLUDED = {"date", "server", "x-request-id", "x-worker-pid"}


def compute_fingerprint(status, body_hex, headers_dict, source):
    body_bytes = bytes.fromhex(body_hex)
    if source == "full":
        parts = [str(status), repr(body_bytes),
                 json.dumps(headers_dict, sort_keys=True)]
    elif source == "status":
        parts = [str(status)]
    elif source == "body":
        parts = [repr(body_bytes)]
    elif source == "headers":
        parts = [json.dumps(headers_dict, sort_keys=True)]
    elif source == "headers_no_clen":
        filtered = {k: v for k, v in headers_dict.items()
                    if k.lower() != "content-length"}
        parts = [json.dumps(filtered, sort_keys=True)]
    else:
        raise ValueError(source)
    return hashlib.sha256("||".join(parts).encode()).hexdigest()


def jaccard(a, b):
    if not a and not b:
        return 0.0
    return 1.0 - (len(a & b) / len(a | b))


def boot_ci(seed, set_a, set_b, n=1000, alpha=0.05):
    rng = random.Random(seed)
    if not set_a and not set_b:
        return 0.0, 0.0, 0.0
    d0 = jaccard(set_a, set_b)
    ds = []
    for _ in range(n):
        ba = set(rng.choices(list(set_a), k=len(set_a))) if set_a else set()
        bb = set(rng.choices(list(set_b), k=len(set_b))) if set_b else set()
        ds.append(jaccard(ba, bb))
    ds.sort()
    return d0, ds[int(alpha / 2 * len(ds))], ds[int((1 - alpha / 2) * len(ds))]


records = [json.loads(l) for l in open(RAW)]
print(f"records: {len(records)}")

# Recompute fingerprints from raw fields only.
mism = 0
for r in records:
    hdrs = json.loads(r["headers_filtered_json"])
    for src in ("full", "status", "body", "headers", "headers_no_clen"):
        got = compute_fingerprint(r["status"], r["body_hex"], hdrs, src)
        if got != r[f"fingerprint_{src}"]:
            mism += 1
            if mism <= 3:
                print(f"FP MISMATCH state={r['state']} src={src}")
print(f"fingerprint recomputation mismatches: {mism}")

# Group recomputed sets by state.
sets = defaultdict(lambda: {s: set() for s in
                            ("full", "status", "body", "headers", "headers_no_clen")})
for r in records:
    st = sets[r["state"]]
    for src in ("full", "status", "body", "headers", "headers_no_clen"):
        st[src].add(compute_fingerprint(r["status"], r["body_hex"],
                                        json.loads(r["headers_filtered_json"]), src))

res = json.load(open(RESULT))
producer = res["metrics"]
PROD_COMPARISONS = [
    ("body_drift_AvsC", "prod_body_A", "prod_body_C"),
    ("body_drift_AvsB", "prod_body_A", "prod_body_B"),
    ("header_drift_AvsE", "prod_hdr_A", "prod_hdr_E"),
    ("header_iso_CC", "prod_hdr_A", "prod_iso_cc"),
    ("header_iso_ETag", "prod_hdr_A", "prod_iso_etag"),
    ("header_iso_SC", "prod_hdr_A", "prod_iso_sc"),
    ("null_body", "prod_null_body_A1", "prod_null_body_A2"),
    ("null_hdr", "prod_null_hdr_A1", "prod_null_hdr_A2"),
    ("classic_perm", "prod_perm_403", "prod_perm_200"),
    ("classic_sess", "prod_sess_401", "prod_sess_200"),
    ("perm_null", "prod_perm403_null_1", "prod_perm403_null_2"),
    ("sess_null", "prod_sess401_null_1", "prod_sess401_null_2"),
    ("fold_E2_keys", "prod_hdr_E", "prod_hdr_E_foldkeys"),
    ("fold_E2_pad", "prod_hdr_E", "prod_hdr_E_foldpad"),
]
SEQ_COMPARISONS = [
    ("seq_body_AvsC", "seq_body_A", "seq_body_C"),
    ("seq_body_AvsB", "seq_body_A", "seq_body_B"),
    ("seq_hdr_AvsE", "seq_hdr_A", "seq_hdr_E"),
]
SOURCES = ("full", "status", "body", "headers", "headers_no_clen")

metric_mism = 0
checked = 0
for name, a, b in PROD_COMPARISONS + SEQ_COMPARISONS:
    for src in SOURCES:
        key = f"{name}_{src}"
        if key not in producer:
            print(f"MISSING producer metric: {key}")
            continue
        pm = producer[key]
        d, lo, hi = boot_ci(44, sets[a][src], sets[b][src])
        checked += 1
        ok = (abs(d - pm["discrimination"]) < 1e-12
              and abs(lo - pm["ci_95"][0]) < 1e-12
              and abs(hi - pm["ci_95"][1]) < 1e-12)
        if not ok:
            metric_mism += 1
            print(f"METRIC MISMATCH {key}: producer={pm['discrimination']} "
                  f"recomputed={d} ci_prod={pm['ci_95']} ci_re={[lo, hi]}")
print(f"metric comparisons checked: {checked}, mismatches: {metric_mism}")

# Sanity L names (they are in raw, verify counts and full sets)
for lbl in ("l_body_A", "l_body_C", "l_hdr_E"):
    n = sum(1 for r in records if r["state"] == lbl)
    print(f"sanity {lbl}: n={n} full_set_size={len(sets[lbl]['full'])}")

# Distinct fingerprint report for effective N
for lbl in ("prod_body_A", "prod_body_C", "prod_hdr_A", "prod_hdr_E",
            "prod_perm_403", "prod_perm_200", "prod_sess_401", "prod_sess_200"):
    print(f"{lbl}: full_set_size={len(sets[lbl]['full'])}")

print("AUDIT_RECOMPUTATION_OK" if (mism == 0 and metric_mism == 0) else "AUDIT_RECOMPUTATION_FAIL")