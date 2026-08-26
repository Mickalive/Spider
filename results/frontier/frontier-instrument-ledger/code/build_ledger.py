#!/usr/bin/env python3
"""frontier-instrument-ledger — mechanical backfill extractor (charter v1, PREREG_FREEZE d33228a).

Derives instrument-use ledger entries ONLY from accepted mount sources S1-S4
(frozen in PREREG_FREEZE.md sect.2). UNKNOWN-safe semantics per sect.3.
Anti-gaming A1/A2: reads no expectation list; reads only mounted evidence.
"""
import json, hashlib, os, re, sys

MOUNTS = {
    "graph": "/tmp/spider_graph",
    "physics": "/tmp/spider_physics",
    "intel": "/tmp/spider_intel",
    "product": "/tmp/spider_product",
    "runtime": "/tmp/spider_runtime",
}

# --- Instrument name gazetteer (defines WHAT COUNTS as an instrument name;
# --- all facts about each instance are derived from files, never typed here).
GAZETTEER = {
    # physics programs/datasets/harnesses
    r"\bWP-001\b": ("WP-001", "mechanism_lineage"),
    r"\bWP-002B\b": ("WP-002B", "mechanism_lineage"),
    r"\bWP-003B?-R2\b|\bWP-003\b": ("WP-003", "mechanism_lineage"),
    r"\bWP-004\b": ("WP-004", "mechanism_lineage"),
    r"\bWP-005\b": ("WP-005", "mechanism_lineage"),
    r"\bWP-006\b": ("WP-006", "mechanism_lineage"),
    r"\bwp006_v1\b": ("wp006_v1", "dataset"),
    r"collector_wp006\.py": ("collector_wp006", "harness"),
    # graph programs / addressing instruments
    r"\bG-H[1-6]\b": (None, "eval_fixture"),  # canonical id taken from match
    r"graph-addressing-robustness|graph-inheritance-scaling|graph-inheritance-generalization|graph-addressing-fused-retrieval": (None, "benchmark"),
    r"\bV31\b|\bfrag_v31\b": ("graph-arm-V31", "eval_fixture"),
    r"\bV00\b": ("graph-arm-V00", "eval_fixture"),
    r"\bfrag_legacy\b": ("graph-arm-frag_legacy", "eval_fixture"),
    r"\bgiter_v31\b": ("graph-arm-giter_v31", "eval_fixture"),
    r"\bgiter_legacy\b": ("graph-arm-giter_legacy", "eval_fixture"),
    r"paraphrases_confirm_cycle4\.json": ("paraphrases_confirm_cycle4", "prereg"),
    r"\bbooks\b": ("fixture-books-composite", "eval_fixture"),
    r"\bquotes\b": ("fixture-quotes-composite", "eval_fixture"),
    # intel mechanisms
    r"\bSGDR\b|sgdr-state-grounded-dynamic-retrieval": ("SGDR-fused-retrieval", "mechanism_lineage"),
    r"[Uu]nbrowse(?:[- ]route-capture-replay-ladder)?": ("unbrowse-route-capture-replay-ladder", "mechanism_lineage"),
    # product beta instruments
    r"\bPB-001\b": ("PB-001-beta-benchmark", "benchmark"),
    r"compute_verdict|verdict_script": ("pb001-verdict-script", "gate_or_metric_script"),
    r"dress[-_ ]rehearsal": ("pb001-dress-rehearsal-replay", "gate_or_metric_script"),
    # shared test fixture
    r"PhysicsLeakageGuardTests": ("shared-fixture-PhysicsLeakageGuardTests", "shared_test_fixture"),
    # runtime gate/witness derivation machinery (W-C2-3 class)
    r"gate[- ]code|witness refs?|gate.repair_status": ("runtime-gate-witness-code", "gate_or_metric_script"),
}

PRE_MARKERS = re.compile(
    r"pre-evaluation|pre-outcome|pre-freeze|before any (?:outcomes?|data)|zero outcomes observed|"
    r"G8 compliant|pre-fix|predates? (?:all rows|the freeze|any outcome)|rows postdate the freeze", re.I)
POST_MARKERS = re.compile(
    r"post-outcome|post-evaluation|from outcomes|post-pin|after outcomes|outcomes-era|"
    r"exists-only-from-outcomes|DISCLOSED|dress.rehearsal replay BYTE-IDENTICAL", re.I)
ADAPT_MARKERS = re.compile(r"amendment|erratum|repair|repin|supersession|reversion", re.I)
SPENT_MARKERS = re.compile(
    r"instrument spent|spent-instrument|selection-on-instrument|capped|final round|closed permanently|"
    r"CAP is not extended|once-extended CAP|TERMINATE|no repair round", re.I)
LATER_USE_MARKERS = re.compile(r"confirmatory|confirmation round|round 4|successor|adopt|integration|R-2", re.I)
CAVEAT_MARKERS = re.compile(r"caveat|binding|travel|must not be relabeled|wording ceilings?", re.I)
INVALID_MARKERS = re.compile(
    r"MEASUREMENT_INVALID|zero power|undecidable|by construction|min achievable|Holm-adjusted|"
    r"invalidated|process-randomized|non-deterministic seed|prev_action_label|instrument defects", re.I)
INVALID_MARKERS = re.compile(
    r"MEASUREMENT_INVALID|zero power|undecidable|by construction|min achievable|Holm-adjusted|"
    r"invalidated|process-randomized|non-deterministic seed|prev_action_label|powerless|FALSIFIED.*instrument defect|instrument defects", re.I)
COMMIT_RE = re.compile(r"\b[0-9a-f]{7,40}\b")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def find_names(text):
    """Return list of (canonical_id, kind, start, end, matched_text)."""
    out = []
    for pat, (canon, kind) in GAZETTEER.items():
        for m in re.finditer(pat, text):
            cid = canon if canon else m.group(0)
            out.append((cid, kind, m.start(), m.end(), m.group(0)))
    return out


def adapt_events_by_proximity(text, name_hits):
    """Associate each adaptation-marker match to the nearest instrument-name
    occurrence within ASSOC_RADIUS chars (mechanical association rule)."""
    events = []
    for am in ADAPT_MARKERS.finditer(text):
        best = None
        for cid, kind, s, e, _m in name_hits:
            d = min(abs(am.start() - e), abs(s - am.start()))
            if best is None or d < best[0]:
                best = (d, cid, kind, s)
        if best and best[0] <= 1500:
            events.append((best[1], best[2], text[max(0, am.start() - 400):am.start() + 400]))
    return events


def verbatim_snippet(text, pos, width=300):
    """Raw slice WITHOUT any transformation, so probes remain byte-exact substrings."""
    s = max(0, pos - width // 2)
    return text[s:s + width]


def raw_contains(raw_text, probe):
    return bool(probe) and probe in raw_text


def classify_timing(region):
    pre = bool(PRE_MARKERS.search(region))
    post = bool(POST_MARKERS.search(region))
    if pre and not post:
        return "PRE_EVALUATION"
    if post and not pre:
        return "POST_EVALUATION_DISCLOSED"
    if pre and post:
        return "UNKNOWN"  # mixed markers, do not guess
    return "UNKNOWN"


def parse_markdown_sections(path):
    """Yield (section_title, section_text) for '## ' headings."""
    txt = open(path, encoding="utf-8", errors="replace").read()
    parts = re.split(r"(?m)^## ", txt)
    for p in parts[1:]:
        title = p.split("\n", 1)[0]
        yield title, p


def status_line_in(section):
    m = re.search(r"(?im)^\s*[-*>]?\s*\**status\*?\*?\s*[:：]\s*(.+)$", section)
    return m.group(1).strip() if m else None


class LedgerBuilder:
    def __init__(self):
        self.records = {}
        self.manifest = []

    def rec(self, cid, kind):
        if cid not in self.records:
            self.records[cid] = {
                "record_id": None,
                "instrument_id": cid,
                "instrument_kind": kind,
                "lanes_seen": [],
                "uses": [],
                "adaptation_events": [],
                "spentness": "UNKNOWN",
                "spentness_basis": "UNKNOWN",
                "cross_lane_links": [],
                "unknown_fields": ["spentness"],
            }
        return self.records[cid]

    def add_use(self, cid, kind, lane, path, run_id, role, status_verbatim, method):
        r = self.rec(cid, kind)
        if lane not in r["lanes_seen"]:
            r["lanes_seen"].append(lane)
        r["uses"].append({
            "source_ref": path, "run_id": run_id, "role": role,
            "status_at_source_verbatim": status_verbatim if status_verbatim else "UNKNOWN",
            "extraction_method": method,
        })

    def add_adapt(self, cid, kind, lane, path, region):
        am = ADAPT_MARKERS.search(region)
        if not am:
            return
        cm = COMMIT_RE.search(region)
        timing = classify_timing(region)
        self.rec(cid, kind)["adaptation_events"].append({
            "kind": am.group(0).lower(),
            "commit": cm.group(0) if cm else None,
            "timing": timing,
            "lane_source": lane_of(path),
            "evidence_quote": verbatim_snippet(region, am.start(), 260),
            "_path": path,
        })

    # ---- S1: loop-state JSONs ----
    def scan_state_json(self, lane, path):
        raw = open(path, encoding="utf-8", errors="replace").read()
        self.manifest.append({"source_class": "S1", "path": path, "sha256": sha256(path)})
        for cid, kind, s, e, _m in find_names(raw):
            status, parsed = None, None
            try:
                data = json.loads(raw)
                # parsed-field attempt: program/mechanism/gate style fields
                for key in ("program_status", "gate", "mechanism_status", "state", "status"):
                    def walk(o):
                        if isinstance(o, dict):
                            for k, v in o.items():
                                if k == key and isinstance(v, str):
                                    yield v
                                else:
                                    yield from walk(v)
                        elif isinstance(o, list):
                            for x in o:
                                yield from walk(x)
                    for v in walk(data):
                        if len(v) < 120 and raw_contains(raw, v):
                            status, parsed = v, {"field": key, "value": v}
                            break
                    if status:
                        break
            except Exception:
                pass
            method = "parsed_field" if status else "regex_extracted"
            self.add_use(cid, kind, lane, path, None, "producer",
                         status if status else verbatim_snippet(raw, s), method)
            self.records[cid]["uses"][-1]["parsed_status_field"] = parsed
            self.add_adapt(cid, kind, lane, path, raw[max(0, s - 1200):s + 1200])
        # proximity-association pass: adaptation markers linked to nearest name occurrence
        for cid, kind, quote in adapt_events_by_proximity(raw, find_names(raw)):
            am = ADAPT_MARKERS.search(quote)
            cm = COMMIT_RE.search(quote)
            self.rec(cid, kind)["adaptation_events"].append({
                "kind": am.group(0).lower(),
                "commit": cm.group(0) if cm else None,
                "timing": classify_timing(quote),
                "lane_source": lane_of(path),
                "evidence_quote": quote[:300],
                "_path": path,
                "association": "adaptation-marker-proximity<=1500",
            })

    # ---- S2: lane ledger markdown sections ----
    def scan_ledger_md(self, lane, path):
        self.manifest.append({"source_class": "S2", "path": path, "sha256": sha256(path)})
        raw = open(path, encoding="utf-8", errors="replace").read()
        for title, sec in parse_markdown_sections(path):
            rm = re.search(r"\b((?:CYCLE_)?\d{9})\b|\brun (\d{9})\b", title)
            run_id = (rm.group(1) or rm.group(2)) if rm else None
            st = status_line_in(sec)
            seen_here = set()
            for cid, kind, s, e, _m in find_names(sec):
                if cid in seen_here:
                    continue
                seen_here.add(cid)
                self.add_use(cid, kind, lane, path, run_id, "producer", st, "section_parse")
                region = sec[max(0, s - 1200):s + 1200]
                self.add_adapt(cid, kind, lane, path, region)
                r = self.rec(cid, kind)
                # section-level evidence (mechanical markers over the full provenance section)
                se = r.setdefault("section_evidence", [])
                im, spm, lum, cvm = (INVALID_MARKERS.search(sec), SPENT_MARKERS.search(sec),
                                     LATER_USE_MARKERS.search(sec), CAVEAT_MARKERS.search(sec))
                se.append({
                    "path": path, "section_title": title,
                    "invalid_marker_hit": im.group(0) if im else None,
                    "spent_marker_hit": spm.group(0) if spm else None,
                    "later_use_marker_hit": lum.group(0) if lum else None,
                    "caveat_marker_hit": cvm.group(0) if cvm else None,
                })
                if spm and r["spentness"] == "UNKNOWN":
                    r["spentness"] = "SPENT_CONFIRMATORY"
                    r["spentness_basis"] = verbatim_snippet(sec, spm.start(), 220)
                    r["unknown_fields"] = [f for f in r.get("unknown_fields", []) if f != "spentness"]
                if lum and r["spentness"] == "SPENT_CONFIRMATORY":
                    r["later_use_reference_after_spentness"] = True

    # ---- S3: audit gate JSONs ----
    def scan_gate_json(self, lane, path):
        self.manifest.append({"source_class": "S3", "path": path, "sha256": sha256(path)})
        raw = open(path, encoding="utf-8", errors="replace").read()
        gate_val = None
        run_id = None
        try:
            data = json.loads(raw)
            gate_val = data.get("gate")
            run_id = str(data.get("run_id") or "")
        except Exception:
            pass
        for cid, kind, s, e, _m in find_names(raw):
            gv = None
            if gate_val and raw_contains(raw, str(gate_val)):
                gv = str(gate_val)
            method = "parsed_field" if gv else "regex_extracted"
            self.add_use(cid, kind, lane, path, run_id or None, "audit",
                         gv if gv else verbatim_snippet(raw, s), method)
            self.records[cid]["uses"][-1]["parsed_status_field"] = (
                {"field": "gate", "value": gv} if gv else None)
            self.add_adapt(cid, kind, lane, path, raw[max(0, s - 500):s + 700])

    # ---- S4: intel result JSONs ----
    def scan_intel_json(self, lane, path):
        self.manifest.append({"source_class": "S4", "path": path, "sha256": sha256(path)})
        raw = open(path, encoding="utf-8", errors="replace").read()
        for cid, kind, s, e, _m in find_names(raw):
            self.add_use(cid, kind, lane, path, None, "producer", verbatim_snippet(raw, s), "regex_extracted")

    def build(self):
        for lane, root in MOUNTS.items():
            s1 = [
                f"{root}/state/graph_loop.json", f"{root}/state/physics_loop.json",
                f"{root}/state/intel_loop.json", f"{root}/state/runtime_loop.json",
                f"{root}/state/product_current.json",
            ]
            for p in s1:
                if os.path.exists(p):
                    self.scan_state_json(lane, p)
            for name in ("GRAPH_LEDGER.md", "PHYSICS_LEDGER.md", "INTEL_LEDGER.md", "PRODUCT_LEDGER.md"):
                p = f"{root}/docs/{name}"
                if os.path.exists(p):
                    self.scan_ledger_md(lane, p)
            gdir = f"{root}/results/audit"
            if os.path.isdir(gdir):
                for fn in sorted(os.listdir(gdir)):
                    if fn.endswith(".json"):
                        self.scan_gate_json(lane, f"{gdir}/{fn}")
            for fn in ("VALIDATED_MECHANISMS.json", "COMPETITOR_INDEX.json", "MECHANISM_CANDIDATES.json"):
                p = f"{root}/results/intel/{fn}"
                if os.path.exists(p):
                    self.scan_intel_json(lane, p)

        # finalize ids + cross-lane links (same instrument id seen in >1 lane)
        n = 0
        for cid, r in sorted(self.records.items()):
            n += 1
            r["record_id"] = f"IUL-{r['lanes_seen'][0] if r['lanes_seen'] else 'none'}-{n:03d}"
        for cid, r in self.records.items():
            if len(r["lanes_seen"]) > 1:
                for a, b in zip(r["lanes_seen"], r["lanes_seen"][1:]):
                    r["cross_lane_links"].append({
                        "from_lane": a, "to_lane": b,
                        "via_ref": "; ".join(sorted({u["source_ref"] for u in r["uses"]})),
                        "caveat_travel_documented": any(
                            CAVEAT_MARKERS.search(u["status_at_source_verbatim"] or "") for u in r["uses"]
                        ) if r["uses"] else None,
                    })
        # unknown-field bookkeeping
        for r in self.records.values():
            ufs = set(r.get("unknown_fields", []))
            for ae in r["adaptation_events"]:
                if ae["timing"] == "UNKNOWN":
                    ufs.add("adaptation_timing")
            for u in r["uses"]:
                if u["run_id"] is None:
                    ufs.add("use_run_id")
            if not r["adaptation_events"]:
                ufs.add("adaptation_history")
            r["unknown_fields"] = sorted(ufs)
        return self.records


def lane_of(path):
    for lane, root in MOUNTS.items():
        if path.startswith(root):
            return lane
    return "unknown"


if __name__ == "__main__":
    out_dir = sys.argv[1]
    b = LedgerBuilder()
    recs = b.build()
    os.makedirs(out_dir, exist_ok=True)
    with open(f"{out_dir}/ledger/instrument_ledger.json", "w") as f:
        json.dump({"schema_version": "v0", "records": list(recs.values())}, f, indent=1)
    with open(f"{out_dir}/raw/extraction_manifest.json", "w") as f:
        json.dump(b.manifest, f, indent=1)
    print(f"records={len(recs)} sources={len(b.manifest)}")
