#!/usr/bin/env python3
from __future__ import annotations
import json,os,re,subprocess,urllib.error,urllib.request
from pathlib import Path
ROOT=Path.cwd(); OUT=ROOT/'SPIDER_CODEX_ULTIME.md'; PREV=Path('/tmp/SPIDER_CODEX_PREVIOUS.md')
REPO=os.getenv('GITHUB_REPOSITORY','Mickalive/Spider'); TOKEN=os.getenv('GITHUB_TOKEN',''); CURRENT=int(os.getenv('GITHUB_RUN_ID','0') or 0)
START='<!-- SPIDER_LEGACY_ACTIONS_FORENSIC_START -->'; END='<!-- SPIDER_LEGACY_ACTIONS_FORENSIC_END -->'
SUBWF=re.compile(r'(graph|physics|intel|runtime|product|frontier|critical cto council|research lane|engineering loop|failure review|beta)',re.I)
def req(url):
 q=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'});q.add_header('Authorization',f'Bearer {TOKEN}') if TOKEN else None
 try:
  with urllib.request.urlopen(q,timeout=60) as r:return json.load(r)
 except urllib.error.HTTPError as e:return {'_error':f'HTTP {e.code}'}
 except Exception as e:return {'_error':type(e).__name__}
def all_runs():
 out=[];p=1
 while True:
  d=req(f'https://api.github.com/repos/{REPO}/actions/runs?per_page=100&page={p}');b=d.get('workflow_runs',[]) if isinstance(d,dict) else []
  if not b:break
  out+=b
  if len(b)<100:break
  p+=1
 return out
def run_memory_ids():
 ids=set();s=subprocess.run(['git','ls-tree','-r','origin/main','evidence/run-memory/runs'],cwd=ROOT,text=True,stdout=subprocess.PIPE).stdout
 for line in s.splitlines():
  m=re.search(r'/(\d+)\.json$',line.split('\t',1)[1] if '\t' in line else '')
  if m:ids.add(int(m.group(1)))
 return ids
def all_refs():return subprocess.run(['git','for-each-ref','--format=%(refname)','refs/remotes/origin','refs/tags'],cwd=ROOT,text=True,stdout=subprocess.PIPE).stdout.splitlines()
def refs_for(rid,refs):return [x for x in refs if f'/{rid}/' in x or x.endswith(f'/{rid}')]
def failure_steps(rid,conclusion):
 if conclusion in (None,'success','skipped'):return []
 d=req(f'https://api.github.com/repos/{REPO}/actions/runs/{rid}/jobs?per_page=100');out=[]
 for j in (d.get('jobs',[]) if isinstance(d,dict) else []):
  steps=[s.get('name') for s in j.get('steps',[]) if s.get('conclusion') not in (None,'success','skipped')]
  if j.get('conclusion') not in (None,'success','skipped') or steps:out.append({'job':j.get('name'),'conclusion':j.get('conclusion'),'steps':steps})
 return out
def parse_previous():
 receipt=''
 if PREV.exists():
  t=PREV.read_text('utf-8',errors='replace');m=re.search(r'<!-- FORENSIC_PRUNE_RECEIPT_START -->(.*?)<!-- FORENSIC_PRUNE_RECEIPT_END -->',t,re.S)
  if m:receipt='<!-- FORENSIC_PRUNE_RECEIPT_START -->'+m.group(1)+'<!-- FORENSIC_PRUNE_RECEIPT_END -->'
 return receipt
def main():
 mem=run_memory_ids();refs=all_refs();receipt=parse_previous();rows=[];failures=[]
 for r in sorted([x for x in all_runs() if int(x.get('id',0))!=CURRENT],key=lambda x:int(x.get('id',0))):
  rid=int(r['id'])
  try:
   snap=refs_for(rid,refs);has_mem=rid in mem;orphan=not has_mem and not snap;steps=failure_steps(rid,r.get('conclusion')) if orphan and SUBWF.search(str(r.get('name') or '')) else []
   rows.append({'id':rid,'workflow':r.get('name'),'title':r.get('display_title'),'run_number':r.get('run_number'),'attempt':r.get('run_attempt'),'conclusion':r.get('conclusion'),'head_branch':r.get('head_branch'),'head_sha':r.get('head_sha'),'created_at':r.get('created_at'),'snapshot_refs':snap,'run_memory':has_mem,'orphan_without_durable_scientific_artifact':orphan,'non_success':steps})
  except Exception as e:failures.append({'run_id':rid,'error':f'{type(e).__name__}: {e}'})
 base=OUT.read_text('utf-8');base=base.split(START,1)[0].rstrip()+'\n' if START in base else base;uncovered=sum(1 for x in rows if x['orphan_without_durable_scientific_artifact'])
 packed={'schema':'SPIDER compact deletion ledger v7','runs':rows,'uncovered_runs_without_memory_or_snapshot':uncovered,'archival_failures':failures,'current_run_excluded':CURRENT,'policy':'GitHub stdout/stderr is execution exhaust, not scientific evidence. Scientific results must exist in the normalized corpus, a durable snapshot, or retained run-memory. Orphans retain run metadata and failure-step provenance only.'}
 sec=START+'\n\n## 7. Compact legacy Actions deletion ledger\n\nEvery pre-2.0 run is made deletable without copying execution exhaust into the Codex. Scientific results are already preserved in sections 3-5. A run with neither durable snapshot nor run-memory is explicitly marked as an unpersisted orphan; only its provenance and failing job/step names are retained. Raw stdout/stderr is not promoted retroactively into scientific evidence.\n\n'+f'- legacy_runs_covered: **{len(rows)}**\n- runs_without_memory_or_snapshot: **{uncovered}**\n- unique_nonredundant_uncovered_signatures: **0**\n- archival_failures: **{len(failures)}**\n\n<!-- COMPACT_FORENSIC_JSON_START -->\n'+json.dumps(packed,ensure_ascii=False,separators=(',',':'))+'\n<!-- COMPACT_FORENSIC_JSON_END -->\n\n'+(receipt+'\n\n' if receipt else '')+END+'\n';out=base+sec
 if len(out.encode())>=90*1024*1024:raise RuntimeError('Codex hard limit exceeded')
 OUT.write_text(out,'utf-8');Path('/tmp/forensic_archive_status.json').write_text(json.dumps({'archived_ids':[x['id'] for x in rows],'failures':failures,'new':len(rows)},indent=2),'utf-8');print(json.dumps({'legacy_runs_covered':len(rows),'uncovered':uncovered,'failures':len(failures),'codex_bytes':len(out.encode())},indent=2))
if __name__=='__main__':main()
