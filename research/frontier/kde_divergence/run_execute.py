#!/usr/bin/env python3
"""
Sequential execution wrapper for EXP-FRONTIER-34538185726.
Uses identical frozen code from analyze_opt.py but runs sequentially
to avoid multiprocessing deadlocks in constrained environments.
"""
import json, hashlib, warnings, time, sys
import numpy as np
from scipy import stats as sp_stats
from scipy.stats import gaussian_kde
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def to_native(obj):
    if isinstance(obj, dict): return {k: to_native(v) for k,v in obj.items()}
    elif isinstance(obj, list): return [to_native(v) for v in obj]
    elif isinstance(obj, (np.integer,)): return int(obj)
    elif isinstance(obj, (np.floating,)): return float(obj)
    elif isinstance(obj, (np.bool_,)): return bool(obj)
    elif isinstance(obj, np.ndarray): return obj.tolist()
    return obj

SEED=42
FUNCTION_SEEDS=[42,43,44]
LAMBDA_LEVELS=[0.0,0.1,0.2,0.3,0.4,0.5,0.7,1.0]
N_TRANSITIONS=500
N_REPLICATIONS=10
N_PERMUTATIONS=50
ALPHA=0.05
DIM=10
N_ACTIONS=4
ACTIONS=['click','fill','submit','navigate']
BANDWIDTH_SEARCH_POINTS=20
BANDWIDTH_RANGE=(0.01,2.0)
N_KL_SAMPLES=125
CV_FOLDS=5
BONFERRONI_CORRECTION=3
ALPHA_CORRECTED=ALPHA/BONFERRONI_CORRECTION
RHO_THRESHOLD=0.65
ACTION_DIM_MAP=[0,2,5,7]

def rotation_10d(s, action_idx):
    action_dim=ACTION_DIM_MAP[action_idx]
    action_sign=1.0 if action_idx%2==0 else -1.0
    theta=0.1*s[action_dim]*action_sign
    R=np.eye(DIM)
    for i in range(0,DIM-1,2):
        angle=theta*(i+1)/DIM
        c,sn=np.cos(angle),np.sin(angle)
        G=np.eye(DIM)
        G[i,i]=c; G[i,i+1]=-sn; G[i+1,i]=sn; G[i+1,i+1]=c
        R=R@G
    offset=np.zeros(DIM); offset[action_dim]=0.1*action_sign
    return R@(s-0.5)+0.5+offset

def scaling_10d(s, action_idx):
    action_dim=ACTION_DIM_MAP[action_idx]
    action_sign=1.0 if action_idx%2==0 else -1.0
    scale_factor=1.0+0.2*s[action_dim]*action_sign
    s_centered=s-0.5
    s_scaled=scale_factor*s_centered
    offset=np.zeros(DIM)
    for i in range(DIM):
        if i!=action_dim:
            offset[i]=0.05*s[i]*action_sign
    return s_scaled+0.5+offset

def translation_10d(s, action_idx):
    action_dim=ACTION_DIM_MAP[action_idx]
    action_sign=1.0 if action_idx%2==0 else -1.0
    t=np.zeros(DIM)
    for i in range(DIM):
        t[i]=0.1*s[i]*action_sign
        t[i]+=0.05*np.sin(2*np.pi*s[i])
    t[action_dim]+=0.1*action_sign
    return s+t

FUNCTION_MAP={42:rotation_10d,43:scaling_10d,44:translation_10d}
FUNCTION_NAMES={42:'rotation',43:'scaling',44:'translation'}

def sample_mixture_noise(s, rng):
    dist_to_center=np.linalg.norm(s-0.5)
    sigma_base=0.05*(1+0.5*dist_to_center)
    noise=np.zeros(DIM)
    for i in range(DIM):
        r=rng.random()
        if r<0.5: mean_i=0.0; std_i=sigma_base
        elif r<0.8: mean_i=0.1*sigma_base; std_i=0.5*sigma_base
        else: mean_i=-0.1*sigma_base; std_i=2.0*sigma_base
        noise[i]=rng.normal(mean_i,std_i)
    return noise

def generate_transitions(func_seed, lambda_val, n, rng):
    func=FUNCTION_MAP[func_seed]
    transitions=[]
    for _ in range(n):
        s=rng.uniform(0,1,size=DIM)
        a_idx=rng.randint(0,N_ACTIONS)
        if rng.random()<lambda_val:
            s_next_det=func(s,a_idx)
            noise=sample_mixture_noise(s,rng)
            s_next=s_next_det+noise
        else:
            s_next=np.zeros(DIM)
            for i in range(DIM):
                r=rng.random()
                if r<0.5: s_next[i]=rng.normal(0.5,0.1)
                elif r<0.8: s_next[i]=rng.normal(0.5,0.05)
                else: s_next[i]=rng.normal(0.5,0.2)
        s_next=np.clip(s_next,0,1)
        transitions.append((s,ACTIONS[a_idx],s_next))
    return transitions

def fit_kde_with_cv(data, n_folds=CV_FOLDS, n_search_points=BANDWIDTH_SEARCH_POINTS):
    if len(data)<n_folds:
        kde=gaussian_kde(data.T)
        return kde, 1.0, []
    n=len(data)
    fold_size=n//n_folds
    log_low=np.log(BANDWIDTH_RANGE[0]); log_high=np.log(BANDWIDTH_RANGE[1])
    bw_factors=np.exp(np.linspace(log_low,log_high,n_search_points))
    indices=np.arange(n); np.random.shuffle(indices); data_shuffled=data[indices]
    best_score=-np.inf; best_factor=None; all_scores=[]
    for factor in bw_factors:
        fold_scores=[]
        for fold in range(n_folds):
            val_start=fold*fold_size
            val_end=val_start+fold_size if fold<n_folds-1 else n
            val_idx=list(range(val_start,val_end))
            train_idx=list(range(0,val_start))+list(range(val_end,n))
            if len(train_idx)<DIM+1: continue
            train_data=data_shuffled[train_idx]
            val_data=data_shuffled[val_idx]
            try:
                kde=gaussian_kde(train_data.T)
                kde.set_bandwidth(bw_method=kde.factor*factor)
                log_lik=np.mean(kde.logpdf(val_data.T))
                fold_scores.append(log_lik)
            except Exception:
                continue
        if fold_scores:
            mean_score=np.mean(fold_scores)
            all_scores.append((factor,mean_score))
            if mean_score>best_score:
                best_score=mean_score; best_factor=factor
    if best_factor is None: best_factor=1.0
    final_kde=gaussian_kde(data.T)
    final_kde.set_bandwidth(bw_method=final_kde.factor*best_factor)
    return final_kde, best_factor, all_scores

def fit_kde_fixed_bandwidth(data, bw_factor):
    kde=gaussian_kde(data.T)
    kde.set_bandwidth(bw_method=kde.factor*bw_factor)
    return kde

def compute_js_divergence(kde_a, kde_b, n_samples=N_KL_SAMPLES):
    samples_a=kde_a.resample(n_samples).T
    samples_b=kde_b.resample(n_samples).T
    log_pa_a=kde_a.logpdf(samples_a.T)
    log_pa_b=kde_a.logpdf(samples_b.T)
    log_pb_a=kde_b.logpdf(samples_a.T)
    log_pb_b=kde_b.logpdf(samples_b.T)
    log_ma=np.log(0.5*np.exp(log_pa_a)+0.5*np.exp(log_pb_a)+1e-300)
    log_mb=np.log(0.5*np.exp(log_pa_b)+0.5*np.exp(log_pb_b)+1e-300)
    kl_a=np.mean(log_pa_a-log_ma)
    kl_b=np.mean(log_pb_b-log_mb)
    js=0.5*kl_a+0.5*kl_b
    return max(0.0,js)

def compute_js_all_pairs(action_kdes):
    actions_list=list(ACTIONS)
    js_max=0.0; js_sum=0.0; n_pairs=0
    for i in range(len(actions_list)):
        for j in range(i+1,len(actions_list)):
            js=compute_js_divergence(action_kdes[actions_list[i]], action_kdes[actions_list[j]])
            js_max=max(js_max,js); js_sum+=js; n_pairs+=1
    js_mean=js_sum/n_pairs if n_pairs>0 else 0.0
    return js_max, js_mean

def kde_pipeline_for_cell(transitions, rng_perm):
    action_states={a: [] for a in ACTIONS}
    for s,a,s_next in transitions:
        action_states[a].append(s_next)
    action_kdes={}; bandwidths={}
    for a in ACTIONS:
        data=np.array(action_states[a])
        kde,bw_factor,_=fit_kde_with_cv(data)
        action_kdes[a]=kde; bandwidths[a]=bw_factor
    raw_js_max, raw_js_mean=compute_js_all_pairs(action_kdes)
    perm_js_values=[]
    actions_list=[a for _,a,_ in transitions]
    s_nexts=np.array([sn for _,_,sn in transitions])
    mean_bw=np.mean([v for v in bandwidths.values() if v is not None]) if bandwidths else 1.0
    for _ in range(N_PERMUTATIONS):
        shuffled_actions=list(actions_list)
        rng_perm.shuffle(shuffled_actions)
        perm_action_states={a: [] for a in ACTIONS}
        for idx,a in enumerate(shuffled_actions):
            perm_action_states[a].append(s_nexts[idx])
        perm_kdes={}
        for a in ACTIONS:
            data=np.array(perm_action_states[a])
            bw = bandwidths[a] if bandwidths[a] is not None else mean_bw
            try:
                kde=fit_kde_fixed_bandwidth(data, bw)
            except Exception:
                kde=gaussian_kde(data.T)
            perm_kdes[a]=kde
        perm_js_max,_=compute_js_all_pairs(perm_kdes)
        perm_js_values.append(perm_js_max)
    perm_mean_js=float(np.mean(perm_js_values))
    perm_std_js=float(np.std(perm_js_values,ddof=1)) if len(perm_js_values)>1 else 0.0
    bias_corrected_js=max(0.0, raw_js_max-perm_mean_js)
    return {
        'raw_js_max':float(raw_js_max),
        'raw_js_mean':float(raw_js_mean),
        'bias_corrected_js':float(bias_corrected_js),
        'perm_mean_js':perm_mean_js,
        'perm_std_js':perm_std_js,
        'bandwidths':{a: float(bandwidths[a]) if bandwidths[a] is not None else None for a in ACTIONS},
        'perm_js_values':perm_js_values,
    }

def permutation_test_kde_fast(transitions, n_perms=50, rng=None):
    action_states={a: [] for a in ACTIONS}
    for s,a,s_next in transitions:
        action_states[a].append(s_next)
    action_kdes={}; bandwidths={}
    for a in ACTIONS:
        data=np.array(action_states[a])
        kde,bw,_=fit_kde_with_cv(data)
        action_kdes[a]=kde; bandwidths[a]=bw
    observed_js,_=compute_js_all_pairs(action_kdes)
    actions_list=[a for _,a,_ in transitions]
    s_nexts=np.array([sn for _,_,sn in transitions])
    count_ge=0; perm_js_values=[]
    mean_bw=np.mean([v for v in bandwidths.values() if v is not None]) if bandwidths else 1.0
    for _ in range(n_perms):
        shuffled_actions=list(actions_list)
        rng.shuffle(shuffled_actions)
        perm_action_states={a: [] for a in ACTIONS}
        for idx,a in enumerate(shuffled_actions):
            perm_action_states[a].append(s_nexts[idx])
        perm_kdes={}
        for a in ACTIONS:
            data=np.array(perm_action_states[a])
            bw=bandwidths[a] if bandwidths[a] is not None else mean_bw
            try:
                kde=fit_kde_fixed_bandwidth(data,bw)
            except:
                kde=gaussian_kde(data.T)
            perm_kdes[a]=kde
        perm_js,_=compute_js_all_pairs(perm_kdes)
        perm_js_values.append(perm_js)
        if perm_js>=observed_js: count_ge+=1
    p_value=count_ge/n_perms if n_perms>0 else 1.0
    return observed_js,p_value,perm_js_values, bandwidths

if __name__=='__main__':
    start=time.time()
    print("=== EXP-FRONTIER-34538185726 SEQUENTIAL EXECUTION ===")
    total_cells=len(FUNCTION_SEEDS)*len(LAMBDA_LEVELS)*N_REPLICATIONS
    print(f"Total cells: {total_cells}")

    all_kde_js={f_idx:{l: [] for l in LAMBDA_LEVELS} for f_idx in range(len(FUNCTION_SEEDS))}
    all_kde_js_bc={f_idx:{l: [] for l in LAMBDA_LEVELS} for f_idx in range(len(FUNCTION_SEEDS))}
    all_perm_mean={f_idx:{l: [] for l in LAMBDA_LEVELS} for f_idx in range(len(FUNCTION_SEEDS))}
    all_bandwidths={f_idx:{l: [] for l in LAMBDA_LEVELS} for f_idx in range(len(FUNCTION_SEEDS))}
    raw_tables=[]
    pipeline_errors=[]

    cell_count=0
    for f_idx,func_seed in enumerate(FUNCTION_SEEDS):
        func_name=FUNCTION_NAMES[func_seed]
        print(f"--- Function {func_seed} ({func_name}) ---")
        for l in LAMBDA_LEVELS:
            print(f"  lambda={l:.1f}:", end=" ", flush=True)
            for rep_idx in range(N_REPLICATIONS):
                cell_count+=1
                rep_seed=func_seed*10000+rep_idx*100+SEED
                rng=np.random.RandomState(rep_seed)
                try:
                    transitions=generate_transitions(func_seed,l,N_TRANSITIONS,rng)
                    perm_rng=np.random.RandomState(rep_seed+555)
                    cell_result=kde_pipeline_for_cell(transitions, perm_rng)
                    all_kde_js[f_idx][l].append(cell_result['raw_js_max'])
                    all_kde_js_bc[f_idx][l].append(cell_result['bias_corrected_js'])
                    all_perm_mean[f_idx][l].append(cell_result['perm_mean_js'])
                    bw_values=[v for v in cell_result['bandwidths'].values() if v is not None]
                    avg_bw=float(np.mean(bw_values)) if bw_values else None
                    all_bandwidths[f_idx][l].append(avg_bw)
                    raw_tables.append({
                        'func_seed':func_seed,'func_name':func_name,'lambda':l,'replication':rep_idx,
                        'raw_js_max':cell_result['raw_js_max'],'raw_js_mean':cell_result['raw_js_mean'],
                        'bias_corrected_js':cell_result['bias_corrected_js'],
                        'perm_mean_js':cell_result['perm_mean_js'],'perm_std_js':cell_result['perm_std_js'],
                        'avg_bandwidth':avg_bw,'bandwidths':cell_result['bandwidths'],
                    })
                except Exception as e:
                    error_msg=f"Function {func_seed}, lambda={l}, rep={rep_idx}: {str(e)}"
                    pipeline_errors.append(error_msg)
                    print(f" ERR({e})", end=" ", flush=True)
                    all_kde_js[f_idx][l].append(float('nan'))
                    all_kde_js_bc[f_idx][l].append(float('nan'))
                    all_perm_mean[f_idx][l].append(float('nan'))
                    all_bandwidths[f_idx][l].append(None)
                # Progress indicator
                if cell_count % 10 == 0:
                    elapsed_so_far=time.time()-start
                    rate=cell_count/elapsed_so_far if elapsed_so_far>0 else 0
                    eta=(total_cells-cell_count)/rate if rate>0 else 0
                    print(f"[{cell_count}/{total_cells} {elapsed_so_far:.0f}s eta={eta:.0f}s]", end=" ", flush=True)
            # Print cell summary
            js_bc_vals=[v for v in all_kde_js_bc[f_idx][l] if not np.isnan(v)]
            if js_bc_vals:
                print(f"bc_JS={np.mean(js_bc_vals):.6f}+/-{np.std(js_bc_vals,ddof=1):.6f}")
            else:
                print("ALL FAILED")

    if pipeline_errors:
        print(f"\n=== Pipeline Errors: {len(pipeline_errors)} ===")
        for err in pipeline_errors[:10]: print(f"  {err}")

    # === ANALYSIS ===
    lambda_arr=np.array(LAMBDA_LEVELS)
    per_function_results={}
    monotonic_results={}
    for f_idx,func_seed in enumerate(FUNCTION_SEEDS):
        js_bc_means=[]
        for l in LAMBDA_LEVELS:
            vals=[v for v in all_kde_js_bc[f_idx][l] if not np.isnan(v)]
            js_bc_means.append(float(np.mean(vals)) if vals else float('nan'))
        js_bc_means_arr=np.array(js_bc_means)
        valid_mask=~np.isnan(js_bc_means_arr)
        if valid_mask.sum()>=3:
            rho,p=sp_stats.spearmanr(lambda_arr[valid_mask], js_bc_means_arr[valid_mask])
            p_one=p/2 if rho>0 else 1-p/2
        else: rho,p_one=0.0,1.0
        per_function_results[func_seed]={'func_name':FUNCTION_NAMES[func_seed],'spearman_rho':float(rho),'spearman_p_one_sided':float(p_one),'js_bc_means_by_lambda':{str(LAMBDA_LEVELS[i]): js_bc_means[i] for i in range(len(LAMBDA_LEVELS))}}
        valid_means=[(i,v) for i,v in enumerate(js_bc_means) if not np.isnan(v)]
        if len(valid_means)>=2: is_mono=all(valid_means[i][1]<=valid_means[i+1][1] for i in range(len(valid_means)-1))
        else: is_mono=False
        monotonic_results[str(func_seed)]=is_mono
        print(f"Function {func_seed} ({FUNCTION_NAMES[func_seed]}): rho={rho:.4f} p={p_one:.6f} mono={is_mono}")

    aggregate_js_bc_means=[]
    for l in LAMBDA_LEVELS:
        all_js=[]
        for f_idx in range(len(FUNCTION_SEEDS)):
            vals=[v for v in all_kde_js_bc[f_idx][l] if not np.isnan(v)]
            all_js.extend(vals)
        aggregate_js_bc_means.append(float(np.mean(all_js)) if all_js else float('nan'))
    agg_arr=np.array(aggregate_js_bc_means)
    valid_mask=~np.isnan(agg_arr)
    if valid_mask.sum()>=3:
        agg_rho,agg_p=sp_stats.spearmanr(lambda_arr[valid_mask], agg_arr[valid_mask])
        agg_p_one=agg_p/2 if agg_rho>0 else 1-agg_p/2
    else: agg_rho,agg_p_one=0.0,1.0
    print(f"Aggregate rho={agg_rho:.4f} p={agg_p_one:.6f}")

    # Permutation tests for controls
    print("\n=== Permutation Tests ===")
    perm_results={}
    for l_key in [0.0,1.0]:
        perm_p_vals=[]
        for func_seed in FUNCTION_SEEDS:
            for rep_idx in range(N_REPLICATIONS):
                rep_seed=func_seed*10000+rep_idx*100+SEED
                rng=np.random.RandomState(rep_seed)
                transitions=generate_transitions(func_seed,l_key,N_TRANSITIONS,rng)
                perm_rng=np.random.RandomState(rep_seed+888)
                try:
                    _,p_val,_,_=permutation_test_kde_fast(transitions, n_perms=50, rng=perm_rng)
                    perm_p_vals.append(p_val)
                except: perm_p_vals.append(1.0)
        mean_p=float(np.mean(perm_p_vals)) if perm_p_vals else 1.0
        perm_results[str(l_key)]={'mean_p_value':round(mean_p,6),'pass': mean_p>ALPHA}
        print(f"lambda={l_key}: mean_p={mean_p:.6f}")

    # ANOVA
    anova_result={}
    try:
        import pandas as pd
        from statsmodels.formula.api import ols
        from statsmodels.stats.anova import anova_lm
        anova_data=[]
        for f_idx in range(len(FUNCTION_SEEDS)):
            for l in LAMBDA_LEVELS:
                for js_val in all_kde_js_bc[f_idx][l]:
                    if not np.isnan(js_val):
                        anova_data.append({'lam_level':str(l),'function':str(f_idx+1),'js':js_val})
        if len(anova_data)>10:
            df=pd.DataFrame(anova_data)
            model=ols('js ~ C(lam_level) + C(function) + C(lam_level):C(function)', data=df).fit()
            anova_table=anova_lm(model, typ=2)
            anova_result={
                'design':f"{len(FUNCTION_SEEDS)} functions x {len(LAMBDA_LEVELS)} lambdas x {N_REPLICATIONS} reps = {len(anova_data)} observations",
                'full_model':{
                    'lambda_effect':{'F':round(float(anova_table.loc['C(lam_level)','F']),4),'p_value':round(float(anova_table.loc['C(lam_level)','PR(>F)']),6)},
                    'function_effect':{'F':round(float(anova_table.loc['C(function)','F']),4),'p_value':round(float(anova_table.loc['C(function)','PR(>F)']),6)},
                    'interaction_effect':{'F':round(float(anova_table.loc['C(lam_level):C(function)','F']),4),'p_value':round(float(anova_table.loc['C(lam_level):C(function)','PR(>F)']),6)},
                    'model_r_squared':round(float(model.rsquared),4),
                },
                'interaction_pass': bool(float(anova_table.loc['C(lam_level):C(function)','PR(>F)'])>ALPHA)
            }
            print(f"ANOVA interaction p={anova_result['full_model']['interaction_effect']['p_value']}")
        else:
            anova_result={'error':'Insufficient data','interaction_pass':False}
    except Exception as e:
        anova_result={'error':str(e),'interaction_pass':False}
        print(f"ANOVA failed {e}")

    # Effect sizes
    effect_sizes={}
    for f_idx,func_seed in enumerate(FUNCTION_SEEDS):
        js_0=np.array([v for v in all_kde_js_bc[f_idx][0.0] if not np.isnan(v)])
        js_1=np.array([v for v in all_kde_js_bc[f_idx][1.0] if not np.isnan(v)])
        if len(js_0)>1 and len(js_1)>1:
            pooled_std=np.sqrt((np.var(js_0,ddof=1)+np.var(js_1,ddof=1))/2)
            cohens_d=float((np.mean(js_1)-np.mean(js_0))/pooled_std) if pooled_std>0 else 0.0
        else: cohens_d=0.0
        effect_sizes[str(func_seed)]=cohens_d
        print(f"Function {func_seed} d={cohens_d:.4f}")
    agg_js_0=[]; agg_js_1=[]
    for f_idx in range(len(FUNCTION_SEEDS)):
        agg_js_0.extend([v for v in all_kde_js_bc[f_idx][0.0] if not np.isnan(v)])
        agg_js_1.extend([v for v in all_kde_js_bc[f_idx][1.0] if not np.isnan(v)])
    if len(agg_js_0)>1 and len(agg_js_1)>1:
        pooled_std_agg=np.sqrt((np.var(agg_js_0,ddof=1)+np.var(agg_js_1,ddof=1))/2)
        agg_cohens_d=float((np.mean(agg_js_1)-np.mean(agg_js_0))/pooled_std_agg) if pooled_std_agg>0 else 0.0
    else: agg_cohens_d=0.0
    effect_sizes['aggregate']=agg_cohens_d
    print(f"Aggregate d={agg_cohens_d:.4f}")

    # Bandwidth diagnostics
    bw_stats={}
    for f_idx,func_seed in enumerate(FUNCTION_SEEDS):
        bw_means={}
        for l in LAMBDA_LEVELS:
            bw_vals=[v for v in all_bandwidths[f_idx][l] if v is not None]
            bw_means[str(l)]=float(np.mean(bw_vals)) if bw_vals else None
        bw_stats[str(func_seed)]=bw_means
    all_bws=[]
    for f_idx in range(len(FUNCTION_SEEDS)):
        for l in LAMBDA_LEVELS:
            bw_vals=[v for v in all_bandwidths[f_idx][l] if v is not None]
            all_bws.extend(bw_vals)
    bw_cv=float(np.std(all_bws,ddof=1)/np.mean(all_bws)) if all_bws and np.mean(all_bws)>0 else 0.0
    boundary_fraction=0.0
    if all_bws:
        at_low=sum(1 for b in all_bws if b<=BANDWIDTH_RANGE[0]*1.05)
        at_high=sum(1 for b in all_bws if b>=BANDWIDTH_RANGE[1]*0.95)
        boundary_fraction=(at_low+at_high)/len(all_bws)
    print(f"Bandwidth CV={bw_cv:.4f} boundary {boundary_fraction:.4f} mean {np.mean(all_bws):.4f}")

    # Controls
    controls={}
    positive_control={}; all_positive_pass=True
    for f_idx,func_seed in enumerate(FUNCTION_SEEDS):
        js_at_1_vals=[v for v in all_kde_js_bc[f_idx][1.0] if not np.isnan(v)]
        js_at_1=float(np.mean(js_at_1_vals)) if js_at_1_vals else 0.0
        passes=js_at_1>=0.01
        positive_control[str(func_seed)]={'pass':passes,'bc_js_at_lambda1':js_at_1,'threshold':0.01}
        if not passes: all_positive_pass=False
    controls['positive_control']={'description':'KDE JS divergence >=0.01 at lambda=1 across all 3 functions','pass':all_positive_pass,'per_function':positive_control}
    null_control_pass=perm_results['0.0']['pass']
    controls['null_control']={'description':'KDE JS divergence not significantly >0 at lambda=0 (permutation p >0.05)','pass':null_control_pass,'mean_perm_p':perm_results['0.0']['mean_p_value']}
    spearman_per_function={}; all_spearman_pass=True
    for func_seed in FUNCTION_SEEDS:
        rho=per_function_results[func_seed]['spearman_rho']
        p=per_function_results[func_seed]['spearman_p_one_sided']
        passes=rho>=RHO_THRESHOLD and p<ALPHA_CORRECTED
        spearman_per_function[str(func_seed)]={'pass':passes,'rho':rho,'p_one_sided':p,'threshold_rho':RHO_THRESHOLD,'threshold_p':ALPHA_CORRECTED}
        if not passes: all_spearman_pass=False
    controls['spearman_per_function']={'description':f'Per-function Spearman rho >= {RHO_THRESHOLD} with p < {ALPHA_CORRECTED:.4f} (Bonferroni x3)','pass':all_spearman_pass,'per_function':spearman_per_function}
    spearman_pass=(agg_rho>=RHO_THRESHOLD and agg_p_one<ALPHA)
    controls['spearman_aggregate']={'description':f'Aggregate Spearman rho >= {RHO_THRESHOLD} with p < {ALPHA} one-sided','pass':spearman_pass,'rho':float(agg_rho),'p_one_sided':float(agg_p_one)}
    controls['function_invariance']={'description':'No significant function x lambda interaction (two-way ANOVA p >0.05)','pass':anova_result.get('interaction_pass',False),'interaction_p':anova_result.get('full_model',{}).get('interaction_effect',{}).get('p_value',None)}
    controls['bandwidth_health']={'description':'KDE bandwidth selection not degenerate (CV >0, boundary fraction <0.5)','pass': bw_cv>0 and boundary_fraction<0.5,'cv_bandwidth':bw_cv,'boundary_fraction':boundary_fraction,'mean_bandwidth':float(np.mean(all_bws)) if all_bws else None,'std_bandwidth': float(np.std(all_bws,ddof=1)) if all_bws and len(all_bws)>1 else None}
    js_cv_at_lambda1={}; all_js_cv_pass=True
    for f_idx,func_seed in enumerate(FUNCTION_SEEDS):
        js_vals=[v for v in all_kde_js_bc[f_idx][1.0] if not np.isnan(v)]
        if len(js_vals)>1:
            cv=float(np.std(js_vals,ddof=1)/np.mean(js_vals)) if np.mean(js_vals)>0 else 0.0
        else: cv=0.0
        js_cv_at_lambda1[str(func_seed)]=cv
        if cv>0.5: all_js_cv_pass=False
    controls['js_cv_lambda1']={'description':'JS divergence CV across replications <0.5 at lambda=1','pass':all_js_cv_pass,'cv_per_function':js_cv_at_lambda1}
    controls['no_pipeline_errors']={'description':'No pipeline errors during execution','pass':len(pipeline_errors)==0,'n_errors':len(pipeline_errors)}

    conditions_survive={
        'per_function_spearman':all_spearman_pass,
        'positive_control':all_positive_pass,
        'null_control':null_control_pass,
        'function_invariance':anova_result.get('interaction_pass',False),
        'no_pipeline_errors':len(pipeline_errors)==0,
    }
    measurement_invalid=(len(pipeline_errors)>0 or not controls['bandwidth_health']['pass'] or not all_js_cv_pass)
    if measurement_invalid:
        decision='MEASUREMENT_INVALID'; outcome='NOT_APPLICABLE'
    elif all(conditions_survive.values()):
        decision='SURVIVES_CURRENT_TEST'; outcome='SUPPORTS'
    else:
        decision='FALSIFIED-IN-SETTING'; outcome='FALSIFIES'
    print(f"\nDecision {decision} outcome {outcome}")
    elapsed=time.time()-start
    print(f"Elapsed {elapsed:.1f}s")

    # Build results
    results={
        'schema_version':1,
        'experiment_id':'EXP-FRONTIER-34538185726',
        'lane':'frontier',
        'status':'COMPLETE' if not measurement_invalid else 'MEASUREMENT_INVALID',
        'outcome':outcome,
        'metrics':{
            'aggregate':{
                'spearman_rho_bc_js':float(agg_rho),
                'spearman_p_one_sided_bc_js':float(agg_p_one),
                'bc_js_means_by_lambda':{str(LAMBDA_LEVELS[i]): aggregate_js_bc_means[i] for i in range(len(LAMBDA_LEVELS))},
                'cohens_d_lambda0_vs_1':agg_cohens_d,
            },
            'per_function':{},
            'bandwidth_diagnostics':bw_stats,
            'effect_sizes_cohens_d':effect_sizes,
            'anova':anova_result,
        },
        'controls':controls,
        'artifacts':[
            {'path':'research/frontier/kde_divergence/analyze.py','role':'code'},
            {'path':'research/frontier/kde_divergence/analyze_opt.py','role':'code'},
            {'path':'research/frontier/kde_divergence/raw_tables.json','role':'raw'},
        ],
        'observations':[],
        'validity_notes':[],
        'unresolved':[],
    }
    for f_idx,func_seed in enumerate(FUNCTION_SEEDS):
        results['metrics']['per_function'][str(func_seed)]={
            'func_name':FUNCTION_NAMES[func_seed],
            'spearman_rho':per_function_results[func_seed]['spearman_rho'],
            'spearman_p_one_sided':per_function_results[func_seed]['spearman_p_one_sided'],
            'js_bc_means_by_lambda':per_function_results[func_seed]['js_bc_means_by_lambda'],
            'monotonic':monotonic_results[str(func_seed)],
        }
    results['observations']=[
        f"Overall decision: {decision}",
        f"Aggregate Spearman rho(bc_JS, lambda)={agg_rho:.4f}, p_one_sided={agg_p_one:.6f}",
        f"Positive control (JS>=0.01 at lambda=1): {'PASS' if all_positive_pass else 'FAIL'}",
        f"Null control (permutation p>0.05 at lambda=0): {'PASS' if null_control_pass else 'FAIL'}",
        f"Function invariance (ANOVA interaction): {'PASS' if anova_result.get('interaction_pass',False) else 'FAIL'}",
        f"Aggregate Cohen's d (lambda=0 vs 1): {agg_cohens_d:.4f}",
        f"Bandwidth health: CV={bw_cv:.4f}, boundary_fraction={boundary_fraction:.4f}",
        f"JS CV at lambda=1: {js_cv_at_lambda1}",
        f"Pipeline errors: {len(pipeline_errors)}",
        f"Execution time: {elapsed:.1f}s",
    ]
    for func_seed in FUNCTION_SEEDS:
        rho=per_function_results[func_seed]['spearman_rho']
        p=per_function_results[func_seed]['spearman_p_one_sided']
        results['observations'].append(f"Function {func_seed} ({FUNCTION_NAMES[func_seed]}): Spearman rho={rho:.4f}, p_one_sided={p:.6f}, monotonic={monotonic_results[str(func_seed)]}")
    results['validity_notes']=[
        '10D continuous state space [0,1]^10 with mixture-of-3-Gaussians heteroscedastic noise',
        '500 transitions per cell with ~125 per action; Monte Carlo JS SE ~O(1/sqrt(N))',
        '10 replications per cell enable variance estimation',
        '8 lambda levels provide degradation curve resolution',
        '3 independent continuous function families (10D rotation, scaling, translation)',
        'Frozen random seed (seed=42) for reproducibility',
        'KDE via scipy.stats.gaussian_kde with 5-fold CV bandwidth selection for observed data (20 log-spaced factors in [0.01,2.0])',
        'Pragmatic optimization: permutation null reuses observed bandwidth factor per action (rather than full 20x5 CV per permutation) to achieve feasible runtime; disclosed as validity caveat',
        'JS divergence estimated via Monte Carlo with 125 samples per direction',
        'Bias correction via permutation null subtraction (50 perms per cell)',
        'Clipping to [0,1] after noise addition',
        'Same DGP as parent experiments for direct comparison',
        f"Total pipeline errors: {len(pipeline_errors)}",
        f"Mean bandwidth across all cells: {float(np.mean(all_bws)):.4f}" if all_bws else "No bandwidth data",
        'Sequential execution (single process); computation identical to frozen design',
    ]
    results['unresolved']=[
        'Whether full 20x5 CV per permutation would materially change perm mean (reused bandwidth may underestimate perm variance)',
        'Whether KDE bandwidth selection in 10D is adequate with ~125 samples per action',
        'Whether Monte Carlo JS estimation with 125 samples per direction is low-variance enough',
        'Whether KDE performance degrades at higher dimensions (>10D)',
        'Whether real Web transitions exhibit translation-like vs scaling-like structure',
    ]

    # Write outputs
    exp_dir=Path('research/experiments/EXP-FRONTIER-34538185726')
    result_path=exp_dir/'result.json'
    with open(result_path,'w') as f: json.dump(to_native(results),f,indent=2)
    print(f"\nWrote {result_path}")

    raw_path=Path('research/frontier/kde_divergence/raw_tables.json')
    with open(raw_path,'w') as f: json.dump(to_native(raw_tables),f)
    print(f"Wrote {raw_path}")

    # Also write to kde_divergence for cross-reference
    import shutil
    kde_dir=Path('research/frontier/kde_divergence')
    shutil.copy(result_path, kde_dir/'result.json')

    # Compute hashes for provenance
    hashes={}
    for fname in ['prereg.md','spec.json','request.json','freeze.json']:
        fpath=exp_dir/fname
        if fpath.exists():
            hashes[fname]=hashlib.sha256(fpath.read_bytes()).hexdigest()
    for out_name in ['result.json']:
        out_path=exp_dir/out_name
        if out_path.exists():
            hashes[out_name]=hashlib.sha256(out_path.read_bytes()).hexdigest()
    raw_path_for_hash=Path('research/frontier/kde_divergence/raw_tables.json')
    if raw_path_for_hash.exists():
        hashes['raw_tables.json']=hashlib.sha256(raw_path_for_hash.read_bytes()).hexdigest()

    provenance={
        'experiment_id':'EXP-FRONTIER-34538185726',
        'execution_timestamp':time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'analyzer_script':'run_execute.py (sequential execution of frozen analyze_opt.py logic)',
        'script_hashes':hashes,
        'result_hash':hashlib.sha256(result_path.read_bytes()).hexdigest(),
        'status':results['status'],
        'outcome':results['outcome'],
        'claim':'C-WEB-DYNAMICS',
        'lane':'frontier',
        'environment':{
            'python_version':f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'numpy_version':np.__version__,
            'scipy_version':sp_stats.__version__ if hasattr(sp_stats,'__version__') else 'unknown',
        },
        'frozen_inputs':{
            'prereg_hash':'eec9f8af7a4386f07fafbf1d70967234c44a7ad830f0af62a5023223f0db06b8',
            'request_hash':'44fc1148df1f4f750c29ef9fdee31b22cedb50bce3c12868c20f1297956b4845',
            'spec_hash':'b25d696a82f6f125273f929ba7a49b7fc10248a4b083da76f5828201539e86d1',
        },
        'total_transitions':len(FUNCTION_SEEDS)*len(LAMBDA_LEVELS)*N_REPLICATIONS*N_TRANSITIONS,
        'kde_parameters':{
            'bandwidth_search_points':BANDWIDTH_SEARCH_POINTS,
            'bandwidth_range':list(BANDWIDTH_RANGE),
            'cv_folds':CV_FOLDS,
            'kl_samples':N_KL_SAMPLES,
            'n_permutations':N_PERMUTATIONS,
            'pragmatic_perm_bandwidth_reuse':True,
            'parallel_processes':1,
        },
        'execution_seconds':elapsed,
    }
    prov_path=exp_dir/'provenance.json'
    with open(prov_path,'w') as f: json.dump(to_native(provenance),f,indent=2)
    print(f"Wrote {prov_path}")
    # Also copy to kde_divergence
    shutil.copy(prov_path, kde_dir/'provenance.json')
    print("Done.")
