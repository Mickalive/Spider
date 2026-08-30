#!/usr/bin/env python3
from __future__ import annotations
import json, os, re, time, urllib.error, urllib.request
from pathlib import Path

OUT=Path('SPIDER_CODEX_ULTIME.md'); STATUS=Path('/tmp/forensic_archive_status.json')
REPO=os.getenv('GITHUB_REPOSITORY','Mickalive/Spider'); TOKEN=os.getenv('GITHUB_TOKEN',''); CURRENT=int(os.getenv('GITHUB_RUN_ID','0') or 0)
RSTART='<!-- FORENSIC_PRUNE_RECEIPT_START -->'; REND='<!-- FORENSIC_PRUNE_RECEIPT_END -->'

def delete_run(rid):
    q=urllib.request.Request(f'https://api.github.com/repos/{REPO}/actions/runs/{rid}',method='DELETE',headers={'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
    if TOKEN:q.add_header('Authorization',f'Bearer {TOKEN}')
    try:
        with urllib.request.urlopen(q,timeout=60) as r:return r.status in (202,204)
    except urllib.error.HTTPError as e:
        if e.code==404:return True
        return f'HTTP {e.code}'
    except Exception as e:return type(e).__name__

def main():
    st=json.loads(STATUS.read_text('utf-8')); failures={int(x['run_id']) for x in st.get('failures',[])}
    ids=[int(x) for x in st.get('archived_ids',[]) if int(x)!=CURRENT and int(x) not in failures]
    deleted=[]; failed=[]
    for i,rid in enumerate(ids,1):
        res=delete_run(rid)
        if res is True:deleted.append(rid)
        else:failed.append({'run_id':rid,'error':res})
        if i%50==0:time.sleep(1)
    receipt={'schema':'SPIDER legacy Actions prune receipt v1','current_run_retained':CURRENT,'archived_before_delete':len(ids),'deleted_or_already_absent':len(deleted),'delete_failures':failed,'failed_archives_not_deleted':sorted(failures)}
    t=OUT.read_text('utf-8')
    block=RSTART+'\n\n### 7.cleanup — legacy Actions deletion receipt\n\n```json\n'+json.dumps(receipt,ensure_ascii=False,indent=2)+'\n```\n'+REND
    if RSTART in t:
        t=re.sub(re.escape(RSTART)+r'.*?'+re.escape(REND),block,t,flags=re.S)
    else:
        pos=t.rfind('<!-- SPIDER_LEGACY_ACTIONS_FORENSIC_END -->')
        if pos<0:raise RuntimeError('forensic archive marker missing; refusing cleanup receipt')
        t=t[:pos]+block+'\n\n'+t[pos:]
    OUT.write_text(t,'utf-8')
    print(json.dumps(receipt,indent=2))
    if failed:raise SystemExit('some archived runs could not be deleted; receipt persisted in working tree')
if __name__=='__main__':main()
