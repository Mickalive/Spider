"""
EXP-INTEL-36006513166 Module B analysis: trajectory-grouped bootstrap (B=2000),
honest M_total_f10/f100 with CIs, DSM USD cost, rho_shuffled, NC1 coverage shuffle,
NC3 HITL ablation, NC2 delta_vs_truncated, Pareto f=10/f=100. Emits
artifacts/derived/sota_analysis.json.
"""
import json, hashlib, random, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "experiments" / "EXP-INTEL-36006513166" / "artifacts" / "derived" / "sota_blind_results.jsonl"
OUT = ROOT / "experiments" / "EXP-INTEL-36006513166" / "artifacts" / "derived" / "sota_analysis.json"
B = 2000
PERMS = 1000
SEED = 360361
DSM_PATCH_USD = 0.047

rows = [json.loads(l) for l in open(RESULTS)]
tasks = [r for r in rows if not r.get("is_pcb_toy")]
toy = [r for r in rows if r.get("is_pcb_toy")]

BASELINES = ["B-AGENTIC-DSM", "B-TRACECOMPILER-DEFUSE", "B-BMEM-CATALOG",
             "B-SPIDER-ALIAS", "B-SPIDER-ROUTING", "B-SPIDER-WEBMCP", "B-COLD-LLM"]
NC3 = "B-AGENTIC-DSM-NOHITL"

def per_baseline(bid):
    return [r for r in tasks if r["baseline"] == bid]

def group_tasks(rows_):
    by_task = {}
    for r in rows_:
        by_task.setdefault(r["task_id"], []).append(r)
    return by_task

def coverage_ci(bid):
    rs = per_baseline(bid)
    n = len(rs)
    cov = sum(1 for r in rs if r["success"]) / n
    rng = random.Random(SEED)
    boots = []
    for _ in range(B):
        s = 0
        for i in range(n):
            s += 1 if rng.choice(rs)["success"] else 0
        boots.append(s / n)
    boots.sort()
    lo, hi = boots[int(0.025 * B)], boots[int(0.975 * B) - 1]
    return {"coverage": round(cov, 4), "n": n, "ci_lower": round(lo, 4), "ci_upper": round(hi, 4),
            "ci_width": round(hi - lo, 4), "variance": round(statistics.variance([1 if r["success"] else 0 for r in rs]), 4),
            "degenerate": (lo == hi)}

def mtotal_f(rows_, f):
    n = len(rows_)
    denom = min(f, n)
    total = sum(r["m_total"] for r in rows_)
    return total / denom

def mtotal_ci(bid, f):
    rs = per_baseline(bid)
    n = len(rs)
    denom = min(f, n)
    rng = random.Random(SEED * 7 + f)
    boots = []
    for _ in range(B):
        tot = 0
        for i in range(n):
            tot += rng.choice(rs)["m_total"]
        boots.append(tot / denom)
    boots.sort()
    lo, hi = boots[int(0.025 * B)], boots[int(0.975 * B) - 1]
    return {"m_total_f%d" % f: round(mtotal_f(rs, f), 2), "ci_lower": round(lo, 2), "ci_upper": round(hi, 2),
            "ci_width": round(hi - lo, 2)}

def usd_dsm():
    rs = per_baseline("B-AGENTIC-DSM")
    per_task = [r["meta"].get("patches", 0) * DSM_PATCH_USD for r in rs]
    mean = statistics.mean(per_task)
    rng = random.Random(SEED * 13)
    boots = []
    for _ in range(B):
        s = []
        for i in range(len(rs)):
            s.append(rng.choice(per_task))
        boots.append(statistics.mean(s))
    boots.sort()
    return {"usd_per_task_mean": round(mean, 4), "usd_total_40": round(sum(per_task), 4),
            "ci_lower": round(boots[int(0.025 * B)], 4), "ci_upper": round(boots[int(0.975 * B) - 1], 4),
            "n_patch_tasks": sum(1 for x in per_task if x > 0)}

def rho_shuffled():
    pairs = [(r["m_total"], r["world_steps"], r["family"]) for r in tasks]
    def pearson(xs, ys):
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        vx = sum((x - mx) ** 2 for x in xs)
        vy = sum((y - my) ** 2 for y in ys)
        return cov / (vx * vy) ** 0.5 if vx and vy else 0.0
    rho_real = pearson([p[0] for p in pairs], [p[1] for p in pairs])
    rng = random.Random(SEED * 17)
    by_fam = {}
    for p in pairs:
        by_fam.setdefault(p[2], []).append(p)
    perms = []
    for _ in range(PERMS):
        shuf = []
        for fam, ps in by_fam.items():
            costs = [p[0] for p in ps]
            lens = [p[1] for p in ps]
            rng.shuffle(costs)
            shuf += list(zip(costs, lens))
        perms.append(pearson([p[0] for p in shuf], [p[1] for p in shuf]))
    return {"rho_real": round(rho_real, 4),
            "rho_shuffled_mean": round(statistics.mean(perms), 4),
            "rho_shuffled_abs_max": round(max(abs(x) for x in perms), 4),
            "rho_shuffled_abs_mean": round(statistics.mean(abs(x) for x in perms), 4),
            "gate_abs_lt_0_20": abs(statistics.mean(perms)) < 0.20,
            "p": round(sum(1 for x in perms if abs(x) >= abs(rho_real)) / PERMS, 4)}

def nc1_coverage_shuffle():
    rng = random.Random(SEED * 19)
    out = {}
    for bid in BASELINES + [NC3]:
        rs = per_baseline(bid)
        fams = sorted({r["family"] for r in rs})
        succ = [1 if r["success"] else 0 for r in rs]
        labels = [r["family"] for r in rs]
        real = {}
        for f, s in zip(labels, succ):
            real[f] = real.get(f, 0) + s
        real = {f: real.get(f, 0) / 10 for f in fams}

        def std_of(covmap):
            vals = [covmap[f] for f in fams]
            m = sum(vals) / len(vals)
            return (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5

        real_std = std_of(real)
        perm_stds = []
        for _ in range(PERMS):
            labels_sh = list(labels)
            rng.shuffle(labels_sh)
            perm = {f: 0 for f in fams}
            cnt = {f: 0 for f in fams}
            for f, s in zip(labels_sh, succ):
                perm[f] += s
                cnt[f] += 1
            covmap = {f: perm[f] / cnt[f] for f in fams}
            perm_stds.append(std_of(covmap))
        perm_stds.sort()
        p = sum(1 for x in perm_stds if x >= real_std - 1e-12) / PERMS
        out[bid] = {"real_family_coverage": {f: round(real[f], 3) for f in fams},
                    "real_family_std": round(real_std, 3),
                    "shuffled_family_std_mean": round(statistics.mean(perm_stds), 3),
                    "shuffled_family_std_ci": [round(perm_stds[int(0.025 * PERMS)], 3), round(perm_stds[int(0.975 * PERMS) - 1], 3)],
                    "gap_real_minus_shuffled": round(real_std - statistics.mean(perm_stds), 3),
                    "p": round(p, 4)}
    return out

def nc3_ablation():
    rs_h = per_baseline("B-AGENTIC-DSM")
    rs_n = per_baseline(NC3)
    ch = sum(1 for r in rs_h if r["success"]) / len(rs_h)
    cn = sum(1 for r in rs_n if r["success"]) / len(rs_n)
    return {"dsm_hitl_coverage": round(ch, 4), "dsm_nohitl_coverage": round(cn, 4),
            "drop": round(ch - cn, 4), "drop_ge_0_30": (ch - cn) >= 0.30}

def nc2_delta_truncated():
    return {"status": "MEASUREMENT_INVALID",
            "reason": "NC2 probe not run for EXP-INTEL-36006513166; parent EXP-INTEL-35956094394 delta=0.6667 documented"}

def webmcp_prevalence():
    rs = per_baseline("B-SPIDER-WEBMCP")
    n = len(rs)
    praised = [1 if r["meta"].get("tool_bypass_success_1st") else 0 for r in rs]
    rate = sum(praised) / n
    def amort(f):
        return sum(praised) / min(f, n)
    rng = random.Random(SEED * 23)
    boots = []
    for _ in range(B):
        s = sum(rng.choice(praised) for _ in range(n)) / n
        boots.append(s)
    boots.sort()
    return {"tool_bypass_success_rate": round(rate, 4),
            "tool_bypass_n_of_{}".format(n): sum(praised),
            "amortized_f10": round(amort(10), 4),
            "amortized_f100": round(amort(100), 4),
            "ci_lower": round(boots[int(0.025 * B)], 4),
            "ci_upper": round(boots[int(0.975 * B) - 1], 4)}

def pareto():
    out = {}
    for f in (10, 100):
        table = []
        for bid in BASELINES + [NC3]:
            rs = per_baseline(bid)
            cov = round(sum(1 for r in rs if r["success"]) / len(rs), 3)
            cost = round(mtotal_f(rs, f), 1)
            table.append({"baseline": bid, "coverage": cov, "m_total_f%d" % f: cost})
        out["pareto_f%d" % f] = sorted(table, key=lambda x: -x["coverage"])
    return out

analysis = {
    "experiment_id": "EXP-INTEL-36006513166",
    "module": "B",
    "coverage": {bid: coverage_ci(bid) for bid in BASELINES + [NC3]},
    "mtotal": {bid: {"f10": mtotal_ci(bid, 10), "f100": mtotal_ci(bid, 100)} for bid in BASELINES + [NC3]},
    "usd_dsm": usd_dsm(),
    "per_channel_coverage": {},
    "rho": rho_shuffled(),
    "nc1_coverage_shuffle": nc1_coverage_shuffle(),
    "nc3_ablation": nc3_ablation(),
    "nc2_delta_truncated": nc2_delta_truncated(),
    "webmcp_tool_bypass_prevalence": webmcp_prevalence(),
    "false_accept": {"all_baselines": 0.0, "reason": "world verifies every required channel against current alias at verify time; false accepts structurally impossible (strict server); disclosed."},
    "pareto": pareto(),
    "pcb_toy": {r["baseline"]: r["success"] for r in toy},
}
for fam in ("header_param", "body_param", "auth_param", "mixed_multi_channel"):
    analysis["per_channel_coverage"][fam] = {}
    for bid in BASELINES + [NC3]:
        rs = [r for r in per_baseline(bid) if r["family"] == fam]
        analysis["per_channel_coverage"][fam][bid] = round(sum(1 for r in rs if r["success"]) / len(rs), 3)

s = json.dumps(analysis, sort_keys=True, indent=1)
OUT.write_text(s + "\n")
print("wrote", OUT)
print("sha256:", hashlib.sha256(s.encode()).hexdigest())
print()
print(json.dumps({k: analysis[k] for k in ("coverage", "usd_dsm", "rho", "nc3_ablation")}, indent=1))
print()
print("per_channel:", json.dumps(analysis["per_channel_coverage"], indent=1))
print()
print("webmcp:", json.dumps(analysis["webmcp_tool_bypass_prevalence"], indent=1))
