"""
EXP-INTEL-36020904615 Module B analysis: trajectory-grouped bootstrap (B=2000),
honest M_total_f10/f100 with CIs, DSM USD cost, rho_shuffled, NC1 coverage shuffle,
NC3 HITL ablation, NC4 Stagehand stripping lift, Pareto f=10/f=100, per-channel.
Emits artifacts/derived/sota_analysis.json + stagehand_strip_delta.json.
"""
import hashlib
import json
import random
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "experiments" / "EXP-INTEL-36020904615"
RESULTS = EXP / "artifacts" / "derived" / "sota_blind_results.jsonl"
OUT = EXP / "artifacts" / "derived" / "sota_analysis.json"
STRIP_OUT = EXP / "artifacts" / "derived" / "stagehand_strip_delta.json"
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
STAGE = "B-STAGEHAND-SELECTOR"
STAGE_PRE = "B-STAGEHAND-SELECTOR-NOSTRIP"


def per_baseline(bid):
    return [r for r in tasks if r["baseline"] == bid]


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
    succ = [1 if r["success"] else 0 for r in rs]
    var = statistics.variance(succ) if n > 1 else 0.0
    return {"coverage": round(cov, 4), "n": n, "ci_lower": round(lo, 4), "ci_upper": round(hi, 4),
            "ci_width": round(hi - lo, 4), "variance": round(var, 4),
            "degenerate": (lo == hi)}


def hit_ci(bid):
    rs = per_baseline(bid)
    n = len(rs)
    hits = [1 if r["meta"].get("hit") else 0 for r in rs]
    rate = sum(hits) / n
    seed_off = int(hashlib.sha256(bid.encode()).hexdigest()[:4], 16)
    rng = random.Random(SEED * 3 + seed_off)
    boots = []
    for _ in range(B):
        s = 0
        for i in range(n):
            s += rng.choice(hits)
        boots.append(s / n)
    boots.sort()
    lo, hi = boots[int(0.025 * B)], boots[int(0.975 * B) - 1]
    return {"hit_rate": round(rate, 4), "n": n, "ci_lower": round(lo, 4), "ci_upper": round(hi, 4),
            "variance": round(statistics.variance(hits), 4) if n > 1 else 0.0,
            "hits": sum(hits)}


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
    return {"m_total_f%d" % f: round(mtotal_f(rs, f), 2), "ci_lower": round(lo, 2),
            "ci_upper": round(hi, 2), "ci_width": round(hi - lo, 2)}


def usd_dsm():
    rs = per_baseline("B-AGENTIC-DSM")
    per_task = [r["meta"].get("patches", 0) * DSM_PATCH_USD for r in rs]
    mean = statistics.mean(per_task)
    rng = random.Random(SEED * 13)
    boots = []
    for _ in range(B):
        s = [rng.choice(per_task) for _ in range(len(rs))]
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
    for bid in BASELINES + [NC3, STAGE]:
        rs = per_baseline(bid)
        fams = sorted({r["family"] for r in rs})
        if not rs:
            continue
        succ = [1 if r["success"] else 0 for r in rs]
        labels = [r["family"] for r in rs]
        real = {}
        for f, s in zip(labels, succ):
            real[f] = real.get(f, 0) + s
        real = {f: real.get(f, 0) / max(1, labels.count(f)) for f in fams}

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
            covmap = {f: perm[f] / cnt[f] for f in fams if cnt[f]}
            perm_stds.append(std_of(covmap))
        perm_stds.sort()
        p = sum(1 for x in perm_stds if x >= real_std - 1e-12) / PERMS
        out[bid] = {"real_family_coverage": {f: round(real[f], 3) for f in fams},
                    "real_family_std": round(real_std, 3),
                    "shuffled_family_std_mean": round(statistics.mean(perm_stds), 3),
                    "shuffled_family_std_ci": [round(perm_stds[int(0.025 * PERMS)], 3),
                                               round(perm_stds[int(0.975 * PERMS) - 1], 3)],
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


def stagehand_nc4():
    post = hit_ci(STAGE)
    pre = hit_ci(STAGE_PRE)
    lift = round(post["hit_rate"] - pre["hit_rate"], 4)
    # per-channel HIT breakdown
    per_ch = {}
    for fam in ("header_param", "body_param", "auth_param", "mixed_multi_channel"):
        for bid, arm in ((STAGE, "post"), (STAGE_PRE, "pre")):
            rs = [r for r in per_baseline(bid) if r["family"] == fam]
            h = sum(1 for r in rs if r["meta"].get("hit")) / len(rs) if rs else None
            per_ch.setdefault(fam, {})[arm] = {"hit": round(h, 4) if h is not None else None,
                                               "n": len(rs),
                                               "coverage": round(sum(1 for r in rs if r["success"]) / len(rs), 4) if rs else None}
    # per-channel label breakdown (header/body/auth/mixed from channels list)
    per_label = {}
    for label in ("header", "body", "auth", "header-body-auth"):
        rs = [r for r in per_baseline(STAGE) if r["channel_label"] == label]
        if rs:
            per_label[label] = {
                "hit": round(sum(1 for r in rs if r["meta"].get("hit")) / len(rs), 4),
                "coverage": round(sum(1 for r in rs if r["success"]) / len(rs), 4),
                "n": len(rs),
            }
    return {
        "M_STAGEHAND_HIT_POST_STRIP": post,
        "M_STAGEHAND_HIT_PRE_STRIP": pre,
        "M_STAGEHAND_LIFT": lift,
        "lift_ge_0_40": lift >= 0.40,
        "hit_post_ge_0_80": post["hit_rate"] >= 0.80,
        "hit_pre_lt_0_40": pre["hit_rate"] < 0.40,
        "nc4_delta_ge_0_40": lift >= 0.40,
        "nc4_pre_hit_lt_0_50": pre["hit_rate"] < 0.50,
        "per_channel_family": per_ch,
        "per_channel_label": per_label,
        "coverage_post": coverage_ci(STAGE),
        "coverage_pre": coverage_ci(STAGE_PRE),
        "false_accept": 0.0,
        "false_accept_reason": "verify checks every channel against current alias at verify time; stale HIT bindings fail verify (structural FA=0).",
    }


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
            "tool_bypass_n_of_%d" % n: sum(praised),
            "amortized_f10": round(amort(10), 4),
            "amortized_f100": round(amort(100), 4),
            "ci_lower": round(boots[int(0.025 * B)], 4),
            "ci_upper": round(boots[int(0.975 * B) - 1], 4)}


def pareto():
    out = {}
    all_b = BASELINES + [NC3, STAGE]
    for f in (10, 100):
        table = []
        for bid in all_b:
            rs = per_baseline(bid)
            cov = round(sum(1 for r in rs if r["success"]) / len(rs), 3)
            cost = round(mtotal_f(rs, f), 1)
            table.append({"baseline": bid, "coverage": cov, "m_total_f%d" % f: cost})
        out["pareto_f%d" % f] = sorted(table, key=lambda x: -x["coverage"])
    return out


def dsm_per_channel():
    out = {}
    for fam in ("header_param", "body_param", "auth_param", "mixed_multi_channel"):
        rs = [r for r in per_baseline("B-AGENTIC-DSM") if r["family"] == fam]
        cov = sum(1 for r in rs if r["success"]) / len(rs)
        out[fam] = {"coverage": round(cov, 4), "n": len(rs)}
    single = []
    for fam in ("header_param", "body_param", "auth_param"):
        single += [r for r in per_baseline("B-AGENTIC-DSM") if r["family"] == fam]
    single_cov = sum(1 for r in single if r["success"]) / len(single)
    mixed_cov = out["mixed_multi_channel"]["coverage"]
    return {"per_family": out,
            "single_channel_mean": round(single_cov, 4),
            "mixed": round(mixed_cov, 4),
            "structured_collapse": mixed_cov < 0.5 and single_cov >= 0.7}


analysis = {
    "experiment_id": "EXP-INTEL-36020904615",
    "module": "B",
    "coverage": {bid: coverage_ci(bid) for bid in BASELINES + [NC3, STAGE, STAGE_PRE]},
    "mtotal": {bid: {"f10": mtotal_ci(bid, 10), "f100": mtotal_ci(bid, 100)}
               for bid in BASELINES + [NC3, STAGE]},
    "usd_dsm": usd_dsm(),
    "per_channel_coverage": {},
    "dsm_per_channel": dsm_per_channel(),
    "rho": rho_shuffled(),
    "nc1_coverage_shuffle": nc1_coverage_shuffle(),
    "nc3_ablation": nc3_ablation(),
    "nc4_stagehand_strip": stagehand_nc4(),
    "webmcp_tool_bypass_prevalence": webmcp_prevalence(),
    "false_accept": {"all_baselines": 0.0,
                     "reason": "world verifies every required channel against current alias at verify time; false accepts structurally impossible (strict server); disclosed."},
    "pareto": pareto(),
    "pcb_toy": {r["baseline"]: r["success"] for r in toy},
    "pcb_toy_stagehand_hit": {r["baseline"]: r["meta"].get("hit")
                              for r in toy if r["baseline"] in (STAGE, STAGE_PRE)},
}
for fam in ("header_param", "body_param", "auth_param", "mixed_multi_channel"):
    analysis["per_channel_coverage"][fam] = {}
    for bid in BASELINES + [NC3, STAGE]:
        rs = [r for r in per_baseline(bid) if r["family"] == fam]
        if rs:
            analysis["per_channel_coverage"][fam][bid] = round(
                sum(1 for r in rs if r["success"]) / len(rs), 3)

s = json.dumps(analysis, sort_keys=True, indent=1)
OUT.write_text(s + "\n")
print("wrote", OUT, "sha256", hashlib.sha256(s.encode()).hexdigest())

# NC4 dedicated strip-delta table (MV9 provenance path)
strip = analysis["nc4_stagehand_strip"]
strip_tab = {
    "experiment_id": "EXP-INTEL-36020904615",
    "control_id": "NC4",
    "expanded_set": ["form_key", "uenc", "store", "session", "nonce", r"fotorama\d{6,}"],
    "M_STAGEHAND_HIT_POST_STRIP": strip["M_STAGEHAND_HIT_POST_STRIP"],
    "M_STAGEHAND_HIT_PRE_STRIP": strip["M_STAGEHAND_HIT_PRE_STRIP"],
    "M_STAGEHAND_LIFT": strip["M_STAGEHAND_LIFT"],
    "gates": {
        "hit_post_ge_0.80": strip["hit_post_ge_0_80"],
        "lift_ge_0.40": strip["lift_ge_0_40"],
        "pre_lt_0.40": strip["hit_pre_lt_0_40"],
        "nc4_delta_ge_0.40": strip["nc4_delta_ge_0_40"],
        "nc4_pre_lt_0.50": strip["nc4_pre_hit_lt_0_50"],
    },
    "per_channel_label": strip["per_channel_label"],
    "per_channel_family": strip["per_channel_family"],
    "coverage_post": strip["coverage_post"],
}
STRIP_OUT.write_text(json.dumps(strip_tab, sort_keys=True, indent=1) + "\n")
print("wrote", STRIP_OUT)

print()
print("coverage:", json.dumps({k: analysis["coverage"][k]["coverage"] for k in analysis["coverage"]}, indent=1))
print("nc3:", analysis["nc3_ablation"])
print("nc4:", {k: strip[k] for k in ("M_STAGEHAND_HIT_POST_STRIP", "M_STAGEHAND_HIT_PRE_STRIP",
                                     "M_STAGEHAND_LIFT", "lift_ge_0_40", "hit_post_ge_0_80")})
print("rho:", analysis["rho"])
print("dsm_per_channel:", analysis["dsm_per_channel"])
print("toy:", analysis["pcb_toy"], analysis["pcb_toy_stagehand_hit"])
print("mtotal_f10:", {b: analysis["mtotal"][b]["f10"]["m_total_f10"] for b in analysis["mtotal"]})
