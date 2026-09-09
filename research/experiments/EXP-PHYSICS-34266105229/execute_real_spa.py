#!/usr/bin/env python3
"""
EXP-PHYSICS-34266105229 — Real SPA Browser PMI (Optimized)
Collects browser transitions from TodoMVC React and TodoMVC Vue.
Uses minimal delays (1s polite, 0.5s capture) within frozen spec constraints.
"""

import json, math, random, collections, os, sys, time, hashlib, traceback
import numpy as np
from playwright.sync_api import sync_playwright

EXPERIMENT_ID = "EXP-PHYSICS-34266105229"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 1.0
N_TRAJECTORIES = 100
TRAJECTORY_LENGTH = 8
POLITE_DELAY = 1.0  # frozen spec: >= 1 second
STATE_CAPTURE_DELAY = 0.5
MIN_NON_LEAKAGE = 50

SITES = {
    "todomvc_react": {
        "name": "TodoMVC React",
        "url": "https://todomvc.com/examples/react/dist/#/",
        "framework": "react",
    },
    "todomvc_vue": {
        "name": "TodoMVC Vue",
        "url": "https://todomvc.com/examples/vue/dist/#/",
        "framework": "vue",
    },
}

def extract_state(page):
    try: url = page.url
    except: url = ''
    try: title = page.title()[:100]
    except: title = ''
    fs = {}
    try:
        fs['has_form'] = page.locator('form').count() > 0
        fs['has_input'] = page.locator('input').count() > 0
        fs['has_select'] = page.locator('select').count() > 0
        fs['has_textarea'] = page.locator('textarea').count() > 0
    except:
        fs = {'has_form':False,'has_input':False,'has_select':False,'has_textarea':False}
    return {'url': url, 'title': title, 'form_signals': fs}

def get_actions(page):
    actions = []
    try:
        inp = page.locator('input.new-todo')
        if inp.count() > 0 and inp.first.is_visible():
            actions.append('add_todo')
    except: pass
    try:
        for i in range(page.locator('input.toggle').count()):
            try:
                if page.locator('input.toggle').nth(i).is_visible():
                    actions.append(f'toggle_{i}')
                    break
            except: pass
    except: pass
    try:
        for i in range(page.locator('.filters a').count()):
            try:
                if page.locator('.filters a').nth(i).is_visible():
                    text = page.locator('.filters a').nth(i).inner_text(timeout=300)
                    actions.append(f'filter_{text.lower()}')
            except: pass
    except: pass
    try:
        clear = page.locator('button.clear-completed')
        if clear.count() > 0 and clear.first.is_visible():
            actions.append('clear_completed')
    except: pass
    return actions if actions else ['noop']

def exec_action(page, action, rng):
    try:
        if action == 'add_todo':
            page.locator('input.new-todo').first.fill(f't{rng.randint(1000,9999)}', timeout=1000)
            page.locator('input.new-todo').first.press('Enter', timeout=1000)
            return True
        elif action.startswith('toggle_'):
            idx = int(action.split('_')[1])
            page.locator('input.toggle').nth(idx).click(timeout=1000)
            return True
        elif action.startswith('filter_'):
            name = action.replace('filter_','')
            page.locator(f'.filters a:has-text("{name.title()}")').first.click(timeout=1000)
            return True
        elif action == 'clear_completed':
            page.locator('button.clear-completed').first.click(timeout=1000)
            return True
    except: pass
    return False

def collect_all(page, site_config, rng):
    transitions = []
    site_url = site_config['url']
    site_name = site_config['name']
    
    for traj_id in range(N_TRAJECTORIES):
        try:
            page.goto(site_url, timeout=12000, wait_until='networkidle')
            time.sleep(0.3)
            
            # Add initial todos for state diversity
            try:
                inp = page.locator('input.new-todo')
                for _ in range(rng.randint(1,4)):
                    inp.first.fill(f'i{rng.randint(100,999)}', timeout=500)
                    inp.first.press('Enter', timeout=500)
                    time.sleep(0.15)
            except: pass
            
            state_before = extract_state(page)
            
            for step in range(TRAJECTORY_LENGTH):
                actions = get_actions(page)
                action = rng.choice(actions)
                exec_action(page, action, rng)
                time.sleep(STATE_CAPTURE_DELAY)
                state_after = extract_state(page)
                
                transitions.append({
                    'trajectory_id': traj_id,
                    'site': site_name,
                    'state_before': state_before,
                    'action': {'action_type': action},
                    'state_after': state_after,
                    'step': step,
                })
                state_before = state_after
                time.sleep(POLITE_DELAY)
        except Exception as e:
            try:
                page.goto(site_url, timeout=10000, wait_until='networkidle')
                time.sleep(0.3)
            except: pass
        
        if (traj_id + 1) % 25 == 0:
            print(f'    {traj_id+1}/{N_TRAJECTORIES} done ({len(transitions)} transitions)', flush=True)
    
    return transitions

def state_url_only(s): return s['url']
def state_url_title(s): return (s['url'], s['title'])
def state_url_title_form(s):
    fs = s['form_signals']
    return (s['url'], s['title'], (fs['has_form'],fs['has_input'],fs['has_select'],fs['has_textarea']))

REPS = {'url_only': state_url_only, 'url_title': state_url_title, 'url_title_form': state_url_title_form}

def extract_triples(trans, fn):
    return [(fn(t['state_before']), t['action']['action_type'], fn(t['state_after'])) for t in trans]

def compute_pmi(triples):
    N = len(triples)
    if N == 0: return {'mean_pmi':0,'N':0,'unique_states':0,'unique_actions':0,'unique_sa_pairs':0}
    sc = collections.Counter(); sac = collections.Counter(); snc = collections.Counter(); tc = collections.Counter()
    for s,a,s2 in triples:
        sc[s]+=1; sac[(s,a)]+=1; snc[(s,s2)]+=1; tc[(s,a,s2)]+=1
    pmis = []
    for s,a,s2 in triples:
        cs=sc[s]; ca=sac[(s,a)]; cn=snc[(s,s2)]; ct=tc[(s,a,s2)]
        da=sum(1 for (si,ai) in sac if si==s); dn=sum(1 for (si,ni) in snc if si==s)
        pas=(ca+ALPHA)/(cs+ALPHA*da); pns=(cn+ALPHA)/(cs+ALPHA*dn); pj=ct/cs
        d=pas*pns
        pmis.append(math.log2(pj/d) if d>0 and pj>0 else 0.0)
    return {'mean_pmi':sum(pmis)/len(pmis),'N':N,'unique_states':len(sc),'unique_actions':len(set(a for _,a,_ in triples)),'unique_sa_pairs':len(sac)}

def x_traj_shuffle(tg, rng):
    trajs=[]
    for tid in sorted(tg.keys()):
        trs=tg[tid]
        trajs.append(([t[0] for t in trs],[t[1] for t in trs],[t[2] for t in trs]))
    acts=[a for _,a,_ in trajs]; rng.shuffle(acts)
    sg={}
    for i,(tid,(sts,_,nxs)) in enumerate(zip(sorted(tg.keys()),trajs)):
        sg[tid]=[(sts[j],acts[i][j],nxs[j]) for j in range(len(sts))]
    return sg

def perm_test(tg, obs, n_perm, seed):
    rng=random.Random(seed); sms=[]
    for _ in range(n_perm):
        sg=x_traj_shuffle(tg,rng)
        all_s=[]
        for trs in sg.values(): all_s.extend(trs)
        sms.append(compute_pmi(all_s)['mean_pmi'])
    cg=sum(1 for m in sms if m>obs)
    pv=(cg+1)/(n_perm+1)
    nm=float(np.mean(sms)); ns=float(np.std(sms))
    ed=float((obs-nm)/ns) if ns>0 else 0.0
    return {'p_value':pv,'observed_mean_pmi':obs,'null_mean':nm,'null_std':ns,'effect_size_d':ed,'shuffled_means':sms}

def gen_positive_ctrl(rng):
    ST={0:{"url":"http://spa.test/form","title":"Checkout Form","form_signals":[1,1,1,0]},
        1:{"url":"http://spa.test/form","title":"Login Form","form_signals":[1,1,1,0]},
        2:{"url":"http://spa.test/form","title":"Registration Form","form_signals":[1,1,1,1]},
        3:{"url":"http://spa.test/dashboard","title":"User Dashboard","form_signals":[0,0,0,0]},
        4:{"url":"http://spa.test/dashboard","title":"Admin Dashboard","form_signals":[0,1,0,0]},
        5:{"url":"http://spa.test/dashboard","title":"Analytics Dashboard","form_signals":[0,0,0,0]},
        6:{"url":"http://spa.test/settings","title":"Account Settings","form_signals":[1,0,0,0]},
        7:{"url":"http://spa.test/settings","title":"Privacy Settings","form_signals":[1,1,0,0]}}
    TR={0:{"form_submit":3,"button_click":4,"link_nav":6,"menu_select":7},
        1:{"form_submit":5,"button_click":3,"link_nav":4,"menu_select":6},
        2:{"form_submit":3,"button_click":5,"link_nav":7,"menu_select":4},
        3:{"form_submit":0,"button_click":1,"link_nav":2,"menu_select":6},
        4:{"form_submit":1,"button_click":2,"link_nav":0,"menu_select":7},
        5:{"form_submit":2,"button_click":0,"link_nav":1,"menu_select":6},
        6:{"form_submit":3,"button_click":4,"link_nav":5,"menu_select":0},
        7:{"form_submit":5,"button_click":3,"link_nav":6,"menu_select":1}}
    ACTS=["form_submit","button_click","link_nav","menu_select"]
    ts=[]; sids=list(ST.keys())
    for tid in range(25):
        cs=rng.choice(sids)
        for _ in range(20):
            a=rng.choice(ACTS); ns=TR[cs][a]
            ts.append({'trajectory_id':tid,'state_before':ST[cs],'action':{'action_type':a,'target_href':f"http://dummy/{a}/{cs}"},'state_after':ST[ns]})
            cs=ns
    return ts

def run():
    print("="*70, flush=True)
    print(f"EXPERIMENT {EXPERIMENT_ID} — Real SPA Browser PMI", flush=True)
    print("="*70, flush=True)
    
    rng = random.Random(SEED)
    site_results = {}
    all_raw = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={'width':1280,'height':720},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = ctx.new_page()
        
        for site_key, site_config in SITES.items():
            print(f"\n{'━'*70}", flush=True)
            print(f"SITE: {site_config['name']}", flush=True)
            print(f"{'━'*70}", flush=True)
            
            t0 = time.time()
            raw = collect_all(page, site_config, rng)
            elapsed = time.time() - t0
            print(f"  Collected {len(raw)} transitions in {elapsed:.0f}s", flush=True)
            
            non_leakage = raw  # All TodoMVC transitions are non-leakage
            n_nl = len(non_leakage)
            print(f"  Non-leakage: {n_nl}/{len(raw)}", flush=True)
            
            all_raw[site_key] = raw
            
            if n_nl < MIN_NON_LEAKAGE:
                site_results[site_key] = {'status':'MEASUREMENT_INVALID','reason':f'{n_nl} < {MIN_NON_LEAKAGE}'}
                continue
            
            # PMI
            print("  Computing PMI...", flush=True)
            pmi_r = {}
            for rn, fn in REPS.items():
                triples = extract_triples(non_leakage, fn)
                stats = compute_pmi(triples)
                pmi_r[rn] = stats
                print(f"    {rn}: PMI={stats['mean_pmi']:.6f}, N={stats['N']}, states={stats['unique_states']}, SA={stats['unique_sa_pairs']}", flush=True)
            
            # Permutation tests
            print("  Permutation tests...", flush=True)
            perm_r = {}
            for rn, fn in REPS.items():
                tg = collections.defaultdict(list)
                for t in non_leakage:
                    tg[t['trajectory_id']].append((fn(t['state_before']), t['action']['action_type'], fn(t['state_after'])))
                obs = pmi_r[rn]['mean_pmi']
                perm = perm_test(tg, obs, N_PERMUTATIONS, SEED)
                perm_r[rn] = perm
                print(f"    {rn}: p={perm['p_value']:.6f}, d={perm['effect_size_d']:.4f}, null={perm['null_mean']:.6f}", flush=True)
            
            site_results[site_key] = {
                'status': 'COMPLETE',
                'site_name': site_config['name'],
                'site_url': site_config['url'],
                'framework': site_config['framework'],
                'n_total': len(raw),
                'n_non_leakage': n_nl,
                'non_leakage_fraction': n_nl/len(raw) if raw else 0,
                'unique_urls': len(set(t['state_before']['url'] for t in non_leakage)),
                'unique_titles': len(set(t['state_before']['title'] for t in non_leakage)),
                'unique_action_types': len(set(t['action']['action_type'] for t in non_leakage)),
                'url_distribution': dict(collections.Counter(t['state_before']['url'] for t in non_leakage).most_common(10)),
                'title_distribution': dict(collections.Counter(t['state_before']['title'] for t in non_leakage).most_common(10)),
                'action_distribution': dict(collections.Counter(t['action']['action_type'] for t in non_leakage).most_common(10)),
                'pmi_by_representation': {r: {'mean_pmi':s['mean_pmi'],'N':s['N'],'unique_states':s['unique_states'],'unique_actions':s['unique_actions'],'unique_sa_pairs':s['unique_sa_pairs']} for r,s in pmi_r.items()},
                'permutation_tests': {r: {'observed_pmi':pm['observed_mean_pmi'],'p_value':pm['p_value'],'null_mean':pm['null_mean'],'null_std':pm['null_std'],'effect_size_d':pm['effect_size_d']} for r,pm in perm_r.items()},
            }
        
        browser.close()
    
    # Positive control
    print(f"\n{'='*70}", flush=True)
    print("POSITIVE CONTROL", flush=True)
    print(f"{'='*70}", flush=True)
    pos_rng = random.Random(SEED)
    pos_t = gen_positive_ctrl(pos_rng)
    pos_tri = extract_triples(pos_t, state_url_only)
    pos_s = compute_pmi(pos_tri)
    pos_tg = collections.defaultdict(list)
    for t in pos_t:
        pos_tg[t['trajectory_id']].append((state_url_only(t['state_before']), t['action']['action_type'], state_url_only(t['state_after'])))
    pos_p = perm_test(pos_tg, pos_s['mean_pmi'], N_PERMUTATIONS, SEED)
    pos_pass = pos_s['mean_pmi'] >= 0.5
    print(f"  PMI={pos_s['mean_pmi']:.6f}, p={pos_p['p_value']:.6f}, pass={pos_pass}", flush=True)
    
    # Decision
    print(f"\n{'='*70}", flush=True)
    print("DECISION", flush=True)
    print(f"{'='*70}", flush=True)
    
    complete = [k for k,v in site_results.items() if v.get('status')=='COMPLETE']
    
    decisions = {}
    for sk in complete:
        sr = site_results[sk]
        p_url = sr['pmi_by_representation']['url_only']['mean_pmi']
        p_ut = sr['pmi_by_representation']['url_title']['mean_pmi']
        pp = sr['permutation_tests']['url_title']['p_value']
        decisions[sk] = {
            'url_pmi': p_url, 'url_title_pmi': p_ut,
            'ut_gt_url': p_ut > p_url,
            'ut_gt_0_5': p_ut > 0.5,
            'perm_p': pp, 'perm_lt_001': pp < 0.001,
            'n_nl': sr['n_non_leakage'], 'enough': sr['n_non_leakage'] >= MIN_NON_LEAKAGE,
        }
        print(f"  {sk}: url={p_url:.6f} url_title={p_ut:.6f} ut>url={p_ut>p_url} ut>0.5={p_ut>0.5} p={pp:.6f} nl={sr['n_non_leakage']}", flush=True)
    
    all_ut_gt_url = all(d['ut_gt_url'] for d in decisions.values()) if len(complete)>=2 else False
    any_ut_gt_05 = any(d['ut_gt_0_5'] for d in decisions.values())
    any_perm_lt = any(d['perm_lt_001'] for d in decisions.values())
    all_enough = all(d['enough'] for d in decisions.values()) if len(complete)>=2 else False
    
    survives = all_ut_gt_url and any_ut_gt_05 and any_perm_lt and pos_pass and all_enough and len(complete)>=2
    failures = []
    if not all_ut_gt_url: failures.append("URL+title not > URL-only on both sites")
    if not any_ut_gt_05: failures.append("URL+title PMI < 0.5 on all sites")
    if not any_perm_lt: failures.append("Permutation p > 0.001 on all sites")
    if not pos_pass: failures.append("Positive control fails")
    if not all_enough: failures.append("Insufficient non-leakage")
    if len(complete)<2: failures.append(f"Only {len(complete)} sites")
    
    outcome = "SUPPORTS" if survives else "FALSIFIES"
    status = "COMPLETE" if len(complete)>=1 else "MEASUREMENT_INVALID"
    
    print(f"\n  SURVIVES: {survives}", flush=True)
    print(f"  OUTCOME: {outcome}", flush=True)
    print(f"  STATUS: {status}", flush=True)
    if failures: print(f"  FAILURES: {'; '.join(failures)}", flush=True)
    
    return {
        'experiment_id': EXPERIMENT_ID, 'lane': 'physics', 'status': status, 'outcome': outcome,
        'survives': survives, 'failures': failures,
        'site_results': site_results, 'site_decisions': decisions,
        'positive_control': {'pmi':pos_s['mean_pmi'],'p_value':pos_p['p_value'],'passes':pos_pass,'n_transitions':len(pos_t)},
        'decision_rules': {
            'url_title_gt_url_only_both': all_ut_gt_url, 'url_title_gt_0_5_any': any_ut_gt_05,
            'perm_p_lt_001_any': any_perm_lt, 'pos_ctrl_passes': pos_pass,
            'enough_nl_both': all_enough, 'n_complete': len(complete), 'bonferroni': 0.025,
        },
    }, all_raw

if __name__ == '__main__':
    os.environ['PYTHONHASHSEED'] = '0'
    results, raw = run()
    out_dir = 'research/experiments/EXP-PHYSICS-34266105229'
    os.makedirs(out_dir, exist_ok=True)
    with open(f'{out_dir}/raw_results.json', 'w') as f: json.dump(results, f, indent=2, default=str)
    with open(f'{out_dir}/raw_transitions.json', 'w') as f: json.dump(raw, f, indent=2, default=str)
    for fn in ['raw_results.json','raw_transitions.json']:
        with open(f'{out_dir}/{fn}','rb') as f: sha=hashlib.sha256(f.read()).hexdigest()
        print(f"  SHA-256({fn}): {sha}", flush=True)
    print("Done.", flush=True)
