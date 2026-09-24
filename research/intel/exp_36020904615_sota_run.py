"""
EXP-INTEL-36020904615 Module B: byte-identical blind harness re-run + Stagehand
B-STAGEHAND-SELECTOR with NC4 stripping ablation.

- Harness exp_35999366789_blind_harness.py is imported UNMODIFIED (sha b11ea970...);
  only module OUT is redirected to this experiment's artifacts path.
- Stagehand is implemented blind from the frozen recipe: selector +
  relevant-subtree SHA256, expanded stripping {form_key,uenc,store,session,nonce,
  fotorama\\d{6,}}; ablation logs BOTH strip=True and strip=False (NC4).
- Stagehand rows are appended to sota_blind_results.jsonl (same per-task log file
  required by MV8: toy + 40x7 baselines + Stagehand x2 arms).
"""
import hashlib
import importlib.util
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "experiments" / "EXP-INTEL-36020904615"
OUT = EXP / "artifacts" / "derived" / "sota_blind_results.jsonl"
HARNESS_PATH = ROOT / "intel" / "exp_35999366789_blind_harness.py"
EXPECTED_HARNESS_SHA = "b11ea9700c7190f1fb7ef6f169af1f5da4d04dd6d52ae631376cc3c51f59ff21"
STAGEHAND_ID = "B-STAGEHAND-SELECTOR"
STAGEHAND_NOSTRIP_ID = "B-STAGEHAND-SELECTOR-NOSTRIP"
EXPANDED_SET = ["form_key", "uenc", "store", "session", "nonce"]


def load_harness():
    actual = hashlib.sha256(HARNESS_PATH.read_bytes()).hexdigest()
    if actual != EXPECTED_HARNESS_SHA:
        raise RuntimeError(f"harness sha mismatch: {actual} != {EXPECTED_HARNESS_SHA}")
    spec = importlib.util.spec_from_file_location("exp_35999366789_blind_harness", HARNESS_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    mod.OUT = OUT  # redirect only; source bytes untouched
    return mod, actual


# ---------- Stagehand blind recipe ----------

_STRIP_RE = re.compile(
    r"\b(?:form_key|uenc|store|session|nonce)\s*=\s*(\"[^\"]*\"|'[^']*')"
)


def strip_expanded(s: str) -> str:
    """Frozen Stagehand expanded set: {form_key,uenc,store,session,nonce,fotorama\\d{6,}}."""
    s = _STRIP_RE.sub(lambda m: m.group(0).split("=", 1)[0] + '=""', s)
    s = re.sub(r"fotorama\d{6,}", "fotorama", s)
    return s


def dyn_tokens(task_id: str, epoch: int) -> dict:
    rng = random.Random(f"{task_id}|dyn|{epoch}|360360")
    return {
        "form_key": "".join(rng.choice("0123456789abcdef") for _ in range(32)),
        "uenc": "".join(rng.choice("0123456789abcdef") for _ in range(24)),
        "store": str(rng.randint(1, 9)),
        "session": "".join(rng.choice("0123456789abcdef") for _ in range(16)),
        "nonce": "".join(rng.choice("0123456789abcdef") for _ in range(12)),
        "fotorama": f"fotorama{rng.randint(100000, 999999)}",
    }


def build_subtree(task_id: str, names, rendered: dict, epoch: int) -> str:
    d = dyn_tokens(task_id, epoch)
    parts = ['<div class="page"']
    # dynamic Magento-style attributes covered by expanded stripping
    attrs = " ".join(f'{k}="{d[k]}"' for k in EXPANDED_SET)
    parts.append(attrs + ">")
    parts.append(f'<div class="{d["fotorama"]} product-gallery"></div>')
    for n in names:
        v = rendered.get(n, "")
        parts.append(f'<input type="hidden" name="{n}" value="{v}">')
    parts.append("</div>")
    return "".join(parts)


def selector_from(names) -> str:
    # structural selector only (blind to channel labels / alias values)
    return ",".join(f'input[name="{n}"]' for n in sorted(names))


def subtree_sha(task_id, names, rendered, epoch, strip: bool) -> str:
    sub = build_subtree(task_id, names, rendered, epoch)
    if strip:
        sub = strip_expanded(sub)
    return hashlib.sha256(sub.encode()).hexdigest()


def stagehand_extract(world, st, cnt):
    """Cold path: bind page-rendered slots; resolve hidden slots (agent must obtain them)."""
    bindings = {}
    for n in st["names"]:
        if n in st["rendered"]:
            bindings[n] = st["rendered"][n]
            cnt["bind"] += 1
    for n in st["names"]:
        if n not in bindings:
            bindings[n] = world.resolve(n)
            cnt["resolve"] += 1
            cnt["bind"] += 1
    return bindings


def stagehand(h, task, strip: bool):
    world = h.World(task)
    cnt = h.counters_struct()
    try:
        st1 = world.state()
        cnt["browser"] += 1
        names = st1["names"]
        sel = selector_from(names)
        k1 = subtree_sha(task["task_id"], names, st1["rendered"], 0, strip)
        bindings = stagehand_extract(world, st1, cnt)
        ok1 = world.verify(bindings)
        cnt["verify"] += 1
        cache = {(sel, k1): dict(bindings)}

        st2 = world.state()
        cnt["browser"] += 1
        k2 = subtree_sha(task["task_id"], st2["names"], st2["rendered"], 1, strip)
        hit = (sel, k2) in cache
        if hit:
            bindings2 = dict(cache[(sel, k2)])
            ok = world.verify(bindings2)
            cnt["verify"] += 1
        else:
            bindings2 = stagehand_extract(world, st2, cnt)
            ok = world.verify(bindings2)
            cnt["verify"] += 1
        meta = {
            "recipe": "stagehand-selector-subtree-sha256",
            "strip": strip,
            "expanded_set": EXPANDED_SET if strip else [],
            "hit": hit,
            "verify1": ok1,
            "selector": sel,
            "k1": k1[:16],
            "k2": k2[:16],
        }
    except h.BudgetExceeded:
        ok, meta = False, {"recipe": "budget-exceeded", "strip": strip, "truncated": True, "hit": False}
    return {
        "task_id": task["task_id"],
        "family": task["family"],
        "channels": task["channels"],
        "channel_label": "-".join(task["channels"]),
        "baseline": STAGEHAND_ID if strip else STAGEHAND_NOSTRIP_ID,
        "success": ok,
        "resolution_success": ok,
        "counters": cnt,
        "m_total": sum(cnt.values()),
        "world_steps": world.clock,
        "ir_hash": h.ir_hash(meta),
        "meta": meta,
        "false_accept": 0,
    }


def main():
    mod, harness_sha = load_harness()
    # byte-identical harness run (writes 327 rows: 40x8 including NC3 + 7 toy)
    mod.main()
    if not OUT.exists():
        raise RuntimeError("harness did not write OUT")

    data = json.load(open(mod.SYNTH))
    tasks = data["tasks"]
    toy = data["pcb_toy"]

    stagehand_rows = []
    for t in tasks:
        stagehand_rows.append(stagehand(mod, t, strip=True))
        stagehand_rows.append(stagehand(mod, t, strip=False))
    for strip in (True, False):
        r = stagehand(mod, toy, strip)
        r["is_pcb_toy"] = True
        stagehand_rows.append(r)

    with OUT.open("a") as f:
        for r in stagehand_rows:
            f.write(json.dumps(r) + "\n")

    lines = OUT.read_text().splitlines()
    print("harness_sha", harness_sha)
    print("total_rows", len(lines))
    post = [json.loads(l) for l in lines if f'"baseline": "{STAGEHAND_ID}"' in l]
    pre = [json.loads(l) for l in lines if f'"baseline": "{STAGEHAND_NOSTRIP_ID}"' in l]
    post40 = [r for r in post if not r.get("is_pcb_toy")]
    pre40 = [r for r in pre if not r.get("is_pcb_toy")]
    hit_p = sum(1 for r in post40 if r["meta"].get("hit")) / len(post40)
    hit_n = sum(1 for r in pre40 if r["meta"].get("hit")) / len(pre40)
    print("HIT_post", round(hit_p, 4), "HIT_pre", round(hit_n, 4), "lift", round(hit_p - hit_n, 4))
    toy_hit = {r["baseline"]: r["meta"].get("hit") for r in post + pre if r.get("is_pcb_toy")}
    print("toy_hit", toy_hit)

    # provenance sidecar for this runner
    sidecar = {
        "harness_path": str(HARNESS_PATH.relative_to(ROOT.parent)),
        "harness_sha256": harness_sha,
        "harness_expected_sha256": EXPECTED_HARNESS_SHA,
        "harness_byte_identity": harness_sha == EXPECTED_HARNESS_SHA,
        "harness_out_redirected_only": True,
        "stagehand_id": STAGEHAND_ID,
        "stagehand_nostrip_id": STAGEHAND_NOSTRIP_ID,
        "expanded_set": EXPANDED_SET,
        "rows_total": len(lines),
        "rows_stagehand_post": len(post),
        "rows_stagehand_pre": len(pre),
        "hit_post_strip_40": round(hit_p, 6),
        "hit_pre_strip_40": round(hit_n, 6),
        "lift": round(hit_p - hit_n, 6),
        "synthetic_fixture_sha256": hashlib.sha256(mod.SYNTH.read_bytes()).hexdigest(),
    }
    side_path = EXP / "artifacts" / "derived" / "sota_run_manifest.json"
    side_path.write_text(json.dumps(sidecar, indent=1) + "\n")
    print("wrote", side_path)


if __name__ == "__main__":
    main()
