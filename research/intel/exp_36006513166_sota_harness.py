"""
EXP-INTEL-36006513166 Module B: blind external-SOTA + SPIDER baseline harness on
synthetic 40-task alias-OOD (deterministic simulation; no LLM calls, per spec).

Blindness (MV8): external policies implemented ONLY from frozen recipe lines in
prereg.md (DSM: template->deterministic JSON IR->HITL patch hook; TraceCompiler:
trace->def-use chain->IR compilation; BMEM: exact catalog replay without alias
slots). Policies never read the synthetic task JSON (channels/aliases); they act
only on runtime world responses (resource descriptor, resolver replies, verify
outcome).

World model:
- Resource descriptor (state): names of required params; the page renders the
  CURRENT value only for the body channel (header/auth never rendered -> must be
  resolved).
- Resolver: returns current value for a param name.
- verify: server validates EVERY required channel's bound value against the
  CURRENT alias at verify time -> false accepts structurally impossible (FA=0,
  disclosed).
- Session rotation: at rotation_step_lt the current aliases rotate to deterministic
  B2.
- Bounded trajectories (MAX_STEPS=10 for every policy, fair comparator).

Honest counters (MV7): resolve/bind/verify/freshness_check/browser_steps counted
per executed action, reset at trajectory (task) start. No n*3200, no f*6.0, no
jitter.
"""
import json, hashlib, random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYNTH = Path(__file__).resolve().parent / "synthetic_alias_ood_40.json"
OUT = ROOT / "experiments" / "EXP-INTEL-36006513166" / "artifacts" / "derived" / "sota_blind_results.jsonl"

NAME_CH = {"X-Session-Key": "header", "session_token": "body", "auth_sig": "auth"}
MAX_STEPS = 10

class BudgetExceeded(Exception):
    pass

class World:
    def __init__(self, task):
        self.task = task
        self.channels = task["channels"]
        self.names = [task["param_names"][ch] for ch in self.channels]
        self.clock = 0
        self.current = {ch: task["alias_test"][ch] for ch in self.channels}
        self.rotp = task.get("rotp", 0.0)
        self.rng = random.Random(f"{task['task_id']}|rot|360360")
        self.rotations = 0

    def _advance(self):
        self.clock += 1
        if self.clock > MAX_STEPS:
            raise BudgetExceeded()
        if self.rotp and self.rng.random() < self.rotp:
            for ch in self.channels:
                self.current[ch] = self._newval(ch, self.rotations)
            self.rotations += 1

    def _newval(self, ch, idx):
        if ch == "header":
            return "".join(self.rng.choice("0123456789abcdef") for _ in range(32))
        if ch == "body":
            return str(self.rng.randint(10_000_000, 99_999_999))
        return "t-" + "".join(self.rng.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(24))

    def state(self):
        rendered = {}
        for ch in self.channels:
            if self.task["page_renders"][ch]:
                rendered[self.task["param_names"][ch]] = self.current[ch]
        out = {"names": list(self.names), "rendered": dict(rendered)}
        self._advance()
        return out

    def resolve(self, name):
        val = self.current[NAME_CH[name]]
        self._advance()
        return val

    def freshness(self):
        out = {n: self.current[NAME_CH[n]] for n in self.names}
        self._advance()
        return out

    def verify(self, bindings):
        ok = all(bindings.get(n) == self.current[NAME_CH[n]] for n in self.names)
        self._advance()
        return ok


def counters_struct():
    return {"resolve": 0, "bind": 0, "verify": 0, "freshness": 0, "browser": 0}

def ir_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:16]

# ---------------- external baselines (blind recipes) ----------------

def cold_llm(world, cnt):
    bindings = {}
    success = False
    for attempt in range(6):
        st = world.state(); cnt["browser"] += 1
        for n, v in st["rendered"].items():
            bindings[n] = v; cnt["bind"] += 1
        if world.verify(bindings):
            success = True; cnt["verify"] += 1; break
        cnt["verify"] += 1
    return success, bindings, {"recipe": "cold-llm-floor", "attempts": attempt + 1}

def bmem_catalog(world, cnt, catalog):
    bindings = {}
    for n in world.names:
        bindings[n] = catalog[NAME_CH[n]]; cnt["bind"] += 1
    ok = world.verify(bindings); cnt["verify"] += 1
    return ok, bindings, {"recipe": "bmem-catalog-replay", "catalog_slot": True}

def dsm(world, cnt, hitl=True):
    st = world.state(); cnt["browser"] += 1
    ir = {"recipe": "dsm-template-v1", "slots": {}}
    bindings = {}
    for n in st["names"]:
        if n in st["rendered"]:
            ir["slots"][n] = {"source": "page_render", "value": st["rendered"][n]}
            bindings[n] = st["rendered"][n]; cnt["bind"] += 1
        else:
            ipr = ir["slots"][n] = {"source": "template", "value": None}
            del ipr
    ok = world.verify(bindings); cnt["verify"] += 1
    patches = 0
    if not ok and hitl:
        patches = 1
        for n in st["names"]:
            v = world.resolve(n); cnt["resolve"] += 1
            if bindings.get(n) != v:
                bindings[n] = v; cnt["bind"] += 1
        ok = world.verify(bindings); cnt["verify"] += 1
    return ok, bindings, {"recipe": "dsm-template-ir-hitl" if hitl else "dsm-template-ir-nohitl",
                          "ir": ir, "patches": patches}

def trace_compiler(world, cnt):
    st = world.state(); cnt["browser"] += 1
    ir = {"recipe": "trace-defuse", "defs": {}}
    bindings = {}
    for n in st["names"]:
        if n in st["rendered"]:
            ir["defs"][n] = "page"
            bindings[n] = st["rendered"][n]; cnt["bind"] += 1
        else:
            ir["defs"][n] = None
    ok = world.verify(bindings); cnt["verify"] += 1
    return ok, bindings, {"recipe": "trace-defuse-ir", "ir": ir}

# ---------------- SPIDER baselines (identically measured) ----------------

def spider_alias(world, cnt):
    st = world.state(); cnt["browser"] += 1
    bindings = {}
    for n in st["names"]:
        if n in st["rendered"]:
            bindings[n] = st["rendered"][n]; cnt["bind"] += 1
    success = False
    for attempt in range(4):
        cur = world.freshness(); cnt["freshness"] += 1
        for n in st["names"]:
            if bindings.get(n) != cur[n]:
                bindings[n] = world.resolve(n); cnt["resolve"] += 1; cnt["bind"] += 1
        if world.verify(bindings):
            success = True; cnt["verify"] += 1; break
        cnt["verify"] += 1
    return success, bindings, {"recipe": "spider-alias-catalog-freshness-gated"}

def spider_routing(world, cnt):
    st = world.state(); cnt["browser"] += 1
    n_hidden = sum(1 for n in st["names"] if n not in st["rendered"])
    n_render = len(st["names"]) - n_hidden
    browse_conf = 0.95 * n_render + 0.85 * n_hidden
    tool_conf = 0.85 * n_hidden + 0.95 * n_render
    if abs(tool_conf - browse_conf) < 1e-9:
        route = "tool" if n_hidden >= n_render else "browse"
    else:
        route = "tool" if tool_conf > browse_conf else "browse"
    conf = tool_conf if route == "tool" else browse_conf
    abstained = conf < 0.80
    bindings = {}
    if route == "tool":
        for n in st["names"]:
            bindings[n] = world.resolve(n); cnt["resolve"] += 1; cnt["bind"] += 1
    else:
        for n in st["names"]:
            if n in st["rendered"]:
                bindings[n] = st["rendered"][n]; cnt["bind"] += 1
    success = False
    for attempt in range(4):
        cur = world.freshness(); cnt["freshness"] += 1
        for n in st["names"]:
            if bindings.get(n) != cur[n]:
                bindings[n] = cur[n]; cnt["resolve"] += 1; cnt["bind"] += 1
        if world.verify(bindings):
            success = True; cnt["verify"] += 1; break
        cnt["verify"] += 1
    meta = {"recipe": "spider-routing-recalib-conf", "route": route, "confidence": round(conf, 3),
            "abstained": abstained, "slots": len(st["names"])}
    return success, bindings, meta

def spider_webmcp(world, cnt):
    st = world.state(); cnt["browser"] += 1
    bindings = {}
    for n in st["names"]:
        bindings[n] = world.resolve(n); cnt["resolve"] += 1; cnt["bind"] += 1
    tool_ok = world.verify(bindings); cnt["verify"] += 1
    meta = {"recipe": "spider-webmcp-toolbypass", "tool_bypass_attempted": True,
            "tool_bypass_success_1st": tool_ok}
    if tool_ok:
        return True, bindings, meta
    success = False
    for attempt in range(4):
        cur = world.freshness(); cnt["freshness"] += 1
        for n in st["names"]:
            if bindings.get(n) != cur[n]:
                bindings[n] = cur[n]; cnt["resolve"] += 1; cnt["bind"] += 1
        if world.verify(bindings):
            success = True; cnt["verify"] += 1; break
        cnt["verify"] += 1
    return success, bindings, meta


BASELINES = {
    "B-AGENTIC-DSM": lambda w, c: dsm(w, c, hitl=True),
    "B-TRACECOMPILER-DEFUSE": lambda w, c: trace_compiler(w, c),
    "B-BMEM-CATALOG": None,
    "B-SPIDER-ALIAS": spider_alias,
    "B-SPIDER-ROUTING": spider_routing,
    "B-SPIDER-WEBMCP": spider_webmcp,
    "B-COLD-LLM": cold_llm,
}
NC3_NAME = "B-AGENTIC-DSM-NOHITL"

def run_task(task, baseline_id, catalog=None):
    world = World(task)
    cnt = counters_struct()
    try:
        if baseline_id == "B-BMEM-CATALOG":
            assert catalog is not None
            ok, bindings, meta = bmem_catalog(world, cnt, catalog)
        else:
            ok, bindings, meta = BASELINES[baseline_id](world, cnt)
    except BudgetExceeded:
        ok, meta = False, {"recipe": "budget-exceeded", "truncated": True}
    return {
        "task_id": task["task_id"],
        "family": task["family"],
        "channels": task["channels"],
        "channel_label": "-".join(task["channels"]),
        "baseline": baseline_id,
        "success": ok,
        "resolution_success": ok,
        "counters": cnt,
        "m_total": sum(cnt.values()),
        "world_steps": world.clock,
        "ir_hash": ir_hash(meta),
        "meta": meta,
        "false_accept": 0,
    }

def main():
    data = json.load(open(SYNTH))
    tasks = data["tasks"]
    toy = data["pcb_toy"]
    cat_per_task = {t["task_id"]: dict(t["alias_train"]) for t in tasks}
    cat_toy = dict(toy["alias_train"])

    rows = []
    for t in tasks:
        for bid in ("B-AGENTIC-DSM", "B-TRACECOMPILER-DEFUSE", "B-BMEM-CATALOG",
                    "B-SPIDER-ALIAS", "B-SPIDER-ROUTING", "B-SPIDER-WEBMCP", "B-COLD-LLM"):
            rows.append(run_task(t, bid, catalog=cat_per_task[t["task_id"]]))
        world = World(t); cnt = counters_struct()
        try:
            ok, bindings, meta = dsm(world, cnt, hitl=False)
        except BudgetExceeded:
            ok, meta = False, {"recipe": "budget-exceeded", "truncated": True}
        rows.append({"task_id": t["task_id"], "family": t["family"], "channels": t["channels"],
                     "channel_label": "-".join(t["channels"]), "baseline": NC3_NAME, "success": ok,
                     "resolution_success": ok, "counters": cnt, "m_total": sum(cnt.values()),
                     "world_steps": world.clock, "ir_hash": ir_hash(meta), "meta": meta, "false_accept": 0})
    out_rows = rows[:]
    for bid in ("B-AGENTIC-DSM", "B-TRACECOMPILER-DEFUSE", "B-BMEM-CATALOG",
                "B-SPIDER-ALIAS", "B-SPIDER-ROUTING", "B-SPIDER-WEBMCP", "B-COLD-LLM"):
        r = run_task(toy, bid, catalog=cat_toy)
        r["is_pcb_toy"] = True
        out_rows.append(r)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        for r in out_rows:
            f.write(json.dumps(r) + "\n")
    print("wrote", OUT, "rows:", len(out_rows))
    from collections import Counter
    cov = Counter()
    for r in out_rows:
        if r.get("is_pcb_toy"):
            continue
        cov[r["baseline"]] += 1 if r["success"] else 0
    print("coverage/40:", {k: f"{v}/40" for k, v in sorted(cov.items())})
    m = Counter()
    for r in out_rows:
        if r.get("is_pcb_toy"):
            continue
        m[r["baseline"]] += r["m_total"]
    print("sum M_total:", {k: v for k, v in sorted(m.items())})
    toy_cov = {r["baseline"]: r["success"] for r in out_rows if r.get("is_pcb_toy")}
    print("PC-B toy (DSM must be True):", toy_cov)

if __name__ == "__main__":
    main()
