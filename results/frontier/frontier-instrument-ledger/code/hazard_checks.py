#!/usr/bin/env python3
"""frontier-instrument-ledger — mechanical hazard checks + safety verification.

Implements PREREG_FREEZE.md sect.4 checks C-REUSE, C-POSTADAPT, C-COMPARABILITY,
C-SPENTNESS, C-GATELINEAGE, C-SHAREDFIXTURE and sect.5 verbatim-safety invariant,
plus D3 UNKNOWN-safety accounting (sect.8). Reads ONLY the built ledger and the
mounted evidence files it cites.
"""
import json, os, re, sys

MOUNT_ROOTS = ("/tmp/spider_graph", "/tmp/spider_physics", "/tmp/spider_intel",
               "/tmp/spider_product", "/tmp/spider_runtime")

CAVEAT_MARKERS = re.compile(r"caveat|binding|adaptation|amendment|erratum|repair|repin|supersession|pre-evaluation|pre-outcome|pre-freeze", re.I)
INVALID_MARKERS = re.compile(
    r"MEASUREMENT_INVALID|zero power|undecidable|by construction|min achievable|Holm-adjusted|"
    r"invalidated|process-randomized|non-deterministic seed|prev_action_label|instrument defects", re.I)
SPENT_MARKERS = re.compile(
    r"instrument spent|spent-instrument|selection-on-instrument|capped|final round|closed permanently|"
    r"CAP is not extended|once-extended CAP|no repair round", re.I)
QUANT_CLAIM_MARKERS = re.compile(r"speedup|accuracy|@1|wins|ratio|x faster|median|success rate|retrieved-correct|reconstruction", re.I)
SHARED_FIXTURE_KIND = "shared_test_fixture"


def joined_evidence(rec):
    parts = []
    for u in rec["uses"]:
        parts.append(u.get("status_at_source_verbatim") or "")
        psf = u.get("parsed_status_field")
        if psf and psf.get("value"):
            parts.append(str(psf["value"]))
    parts.extend(ae.get("evidence_quote", "") for ae in rec["adaptation_events"])
    return " ".join(parts)


def run_checks(records):
    flags = []
    for rec in records:
        cid = rec["instrument_id"]
        lanes = rec["lanes_seen"]
        uses = rec["uses"]
        ev = joined_evidence(rec)

        # C-GATELINEAGE: invalid/power-deficient lineage markers in use evidence,
        # adaptation quotes, or full-section provenance evidence
        emitted = False
        for u in uses:
            txt_parts = [u.get("status_at_source_verbatim") or ""]
            psf = u.get("parsed_status_field")
            if psf and psf.get("value"):
                txt_parts.append(str(psf["value"]))
            txt = " ".join(txt_parts)
            if INVALID_MARKERS.search(txt):
                flags.append(flag(rec, "C-GATELINEAGE", "HAZARD_INVALID_OR_POWERLESS_INSTRUMENT_LINEAGE",
                                  u["source_ref"], INVALID_MARKERS.search(txt).group(0)))
                emitted = True
        for ae in rec["adaptation_events"]:
            if INVALID_MARKERS.search(ae.get("evidence_quote", "")):
                flags.append(flag(rec, "C-GATELINEAGE", "HAZARD_INVALID_OR_POWERLESS_INSTRUMENT_LINEAGE",
                                  ae.get("_path"), INVALID_MARKERS.search(ae["evidence_quote"]).group(0)))
                emitted = True
        for se in rec.get("section_evidence", []):
            if se.get("invalid_marker_hit"):
                flags.append(flag(rec, "C-GATELINEAGE", "HAZARD_INVALID_OR_POWERLESS_INSTRUMENT_LINEAGE",
                                  se["path"], se["invalid_marker_hit"]))
                emitted = True

        # C-REUSE: multi-lane or repeat claim-bearing use without disclosure marker on some pair
        if len(lanes) >= 2 or len(uses) >= 2:
            missing = [u["source_ref"] for u in uses if not CAVEAT_MARKERS.search(u.get("status_at_source_verbatim") or "") and
                       not any(CAVEAT_MARKERS.search(ae.get("evidence_quote", "")) for ae in rec["adaptation_events"])]
            kind = "HAZARD_REUSE_WITHOUT_DISCLOSURE" if missing else "OK"
            flags.append(flag(rec, "C-REUSE", kind,
                              missing[0] if missing else uses[0]["source_ref"],
                              f"lanes={lanes}; undisclosed_uses={len(missing)}"))

        # C-POSTADAPT: adaptation events with non-PRE timing
        for ae in rec["adaptation_events"]:
            t = ae["timing"]
            if t == "POST_EVALUATION_DISCLOSED":
                flags.append(flag(rec, "C-POSTADAPT", "HAZARD_POST_ADAPTATION_DISCLOSED", ae["_path"], ae["evidence_quote"]))
            elif t == "POST_EVALUATION_UNDISCLOSED_SUSPECTED":
                flags.append(flag(rec, "C-POSTADAPT", "HAZARD_POST_ADAPTATION_UNDISCLOSED", ae["_path"], ae["evidence_quote"]))
            elif t == "UNKNOWN":
                flags.append(flag(rec, "C-POSTADAPT", "REVIEW_UNKNOWN", ae["_path"], "timing undatable"))

        # C-COMPARABILITY: cross-lane / multi-use with quantitative-claim context but UNKNOWN scope
        if (len(lanes) >= 2) and QUANT_CLAIM_MARKERS.search(ev):
            flags.append(flag(rec, "C-COMPARABILITY", "HAZARD_COMPARABILITY_RISK",
                              uses[0]["source_ref"], "quantitative claims across lanes/uses; scope fields UNKNOWN"))

        # C-SPENTNESS
        sp = rec["spentness"]
        later = bool(rec.get("later_use_reference_after_spentness"))
        if sp == "SPENT_CONFIRMATORY" and later:
            flags.append(flag(rec, "C-SPENTNESS", "HAZARD_SPENT_REUSE", uses[0]["source_ref"], rec["spentness_basis"]))
        elif sp == "SPENT_CONFIRMATORY":
            flags.append(flag(rec, "C-SPENTNESS", "OK", uses[0]["source_ref"], rec["spentness_basis"]))
        elif sp == "UNKNOWN":
            flags.append(flag(rec, "C-SPENTNESS", "REVIEW_UNKNOWN", uses[0]["source_ref"], "spentness not derivable"))
        else:
            flags.append(flag(rec, "C-SPENTNESS", "OK", uses[0]["source_ref"], f"spentness={sp}"))

        # C-SHAREDFIXTURE
        if rec["instrument_kind"] == SHARED_FIXTURE_KIND and len(lanes) >= 2:
            flags.append(flag(rec, "C-SHAREDFIXTURE", "HAZARD_SHARED_FIXTURE_STATUS_DIVERGENCE_OR_OWNERSHIP_AMBIGUITY",
                              uses[0]["source_ref"], f"referenced by lanes={lanes}"))

        # D3 UNKNOWN-safety: any UNKNOWN in load-bearing fields must produce REVIEW_UNKNOWN at minimum
        load_unknown = (sp == "UNKNOWN" or
                        any(ae["timing"] == "UNKNOWN" for ae in rec["adaptation_events"]) or
                        any(u["status_at_source_verbatim"] == "UNKNOWN" for u in uses))
        has_review = any(f["record_id"] == rec["record_id"] and f["level"] == "REVIEW_UNKNOWN" for f in flags)
        if load_unknown and not has_review:
            flags.append(flag(rec, "D3-UNKNOWN-SAFETY", "REVIEW_UNKNOWN", "-", "UNKNOWN present; forced review flag"))
        rec["d3_load_bearing_unknown"] = load_unknown

    return flags


def flag(rec, check, level, ref, quote):
    return {"check": check, "level": level, "instrument_id": rec["instrument_id"],
            "record_id": rec["record_id"], "evidence_ref": ref,
            "verbatim_quote": (quote or "")[:300]}


def safety_verify(records):
    out = {"violations": [], "checked": 0}
    for rec in records:
        for u in rec["uses"]:
            st = u.get("status_at_source_verbatim")
            if st in (None, "UNKNOWN"):
                continue
            out["checked"] += 1
            path = u["source_ref"]
            ok = False
            if os.path.exists(path) and path.startswith(MOUNT_ROOTS):
                content = open(path, encoding="utf-8", errors="replace").read()
                probe = st[:200]
                ok = probe in content
            if not ok:
                out["violations"].append({"record_id": rec["record_id"], "source_ref": path,
                                          "status_probe": st[:120]})
    out["false_reclassification_count"] = len(out["violations"])
    return out


if __name__ == "__main__":
    team_dir, = sys.argv[1:]
    ledger = json.load(open(f"{team_dir}/ledger/instrument_ledger.json"))
    records = ledger["records"]
    flags = run_checks(records)
    json.dump({"flags": flags}, open(f"{team_dir}/ledger/hazard_flags.json", "w"), indent=1)
    sv = safety_verify(records)
    d3_total = sum(1 for r in records if r["d3_load_bearing_unknown"])
    d3_flagged = len({f["record_id"] for f in flags if f["level"] == "REVIEW_UNKNOWN"})
    d3_ok = all(any(f["record_id"] == r["record_id"] and f["level"] == "REVIEW_UNKNOWN" for f in flags)
                for r in records if r["d3_load_bearing_unknown"])
    json.dump({"safety": sv,
               "unknown_safety": {"records_with_load_bearing_unknown": d3_total,
                                   "records_with_review_flag": d3_flagged,
                                   "all_unknown_flagged": d3_ok}},
              open(f"{team_dir}/ledger/safety_verification.json", "w"), indent=1)
    n_hazard = sum(1 for f in flags if f["level"].startswith("HAZARD"))
    print(f"records={len(records)} flags={len(flags)} hazards={n_hazard} "
          f"reclass_violations={sv['false_reclassification_count']} unknown_all_flagged={d3_ok}")
