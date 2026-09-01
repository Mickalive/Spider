#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ["request.json","spec.json","prereg.md","freeze.json","result.json","report.md","provenance.json","audit.json","verdict.json","handoff.json"]

def git(*args, check=True):
    return subprocess.run(["git",*args],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=check).stdout

def show(ref,path):
    p=subprocess.run(["git","show",f"{ref}:{path}"],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return None if p.returncode else p.stdout

def main():
    refs=[x.strip() for x in git("for-each-ref","--format=%(refname:short)","refs/remotes/origin/lab2").splitlines() if x.strip()]
    dest_root=ROOT/"codex/experiments"; dest_root.mkdir(parents=True,exist_ok=True)
    gaps=[]; entries={}
    for ref in refs:
        lane=ref.split("origin/lab2/",1)[-1]
        paths=git("ls-tree","-r","--name-only",ref,"research/experiments",check=False).splitlines()
        exp_ids=sorted({p.split("/")[2] for p in paths if p.startswith("research/experiments/") and len(p.split("/"))>=4})
        for exp_id in exp_ids:
            if show(ref,f"research/experiments/{exp_id}/verdict.json") is None: continue
            missing=[name for name in PACKET if show(ref,f"research/experiments/{exp_id}/{name}") is None]
            if missing:
                gaps.append({"lane":lane,"experiment_id":exp_id,"ref":ref,"missing":missing}); continue
            packet={}; out=dest_root/exp_id; out.mkdir(parents=True,exist_ok=True)
            for name in PACKET:
                raw=show(ref,f"research/experiments/{exp_id}/{name}")
                (out/name).write_bytes(raw); packet[name]=hashlib.sha256(raw).hexdigest()
            req=json.loads((out/"request.json").read_text()); spec=json.loads((out/"spec.json").read_text()); aud=json.loads((out/"audit.json").read_text()); ver=json.loads((out/"verdict.json").read_text())
            entries[exp_id]={"lane":lane,"request_id":req["request_id"],"claim_ids":spec["claim_ids"],"question":spec["question"],"audit_status":aud["status"],"decision":ver["decision"],"promote_to_product":ver["promote_to_product"],"source_ref":ref,"hashes":packet}
    (ROOT/"codex/coverage_gaps.json").write_text(json.dumps(gaps,indent=2)+"\n")
    (ROOT/"codex/index.json").write_text(json.dumps({"schema_version":1,"experiments":entries},indent=2)+"\n")
    lines=["# SPIDER CODEX — Research 2.0","","Pre-2.0 canonical memory remains frozen at `archive/spider-codex-ultimate:SPIDER_CODEX_ULTIME.md`.","","This file is generated only from complete finalized Research 2.0 experiment packets.",f"Ingested experiments: **{len(entries)}**. Coverage gaps: **{len(gaps)}**.","","## Index","","| Experiment | Lane | Audit | Verdict | Claims |","|---|---|---|---|---|"]
    for exp_id,e in sorted(entries.items()): lines.append(f"| {exp_id} | {e['lane']} | {e['audit_status']} | {e['decision']} | {', '.join(e['claim_ids'])} |")
    lines += ["","## Complete experiment records",""]
    for exp_id in sorted(entries):
        out=dest_root/exp_id; lines += [f"# {exp_id}",""]
        for name in PACKET:
            text=(out/name).read_text(encoding="utf-8",errors="replace")
            lines += [f"## {name}","","```text",text.rstrip(),"```",""]
    if gaps: lines += ["## Coverage gaps","","The following finalized experiments are not silently omitted from coverage accounting:","","```json",json.dumps(gaps,indent=2),"```",""]
    (ROOT/"SPIDER_CODEX.md").write_text("\n".join(lines),encoding="utf-8")
    print(f"SPIDER_CODEX_SYNC_OK experiments={len(entries)} gaps={len(gaps)} refs={len(refs)}")

if __name__ == "__main__":
    main()
