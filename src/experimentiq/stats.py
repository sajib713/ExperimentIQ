"""Pre-specified control contrasts: conversion primary, visit and spend secondary."""
from math import sqrt
import numpy as np
import pandas as pd
from scipy.stats import chisquare, norm, ttest_ind
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep, proportion_confint
from statsmodels.stats.multitest import multipletests
from .config import ARMS
from .balance import balance_diagnostics


def binary_contrast(success_t:int, n_t:int, success_c:int, n_c:int, alpha:float=.05)->dict:
    if not (isinstance(n_t,(int,np.integer)) and isinstance(n_c,(int,np.integer))):
        raise ValueError('Sample sizes must be integer')
    if min(n_t,n_c)<=0 or not (0 <= success_t <= n_t and 0 <= success_c <= n_c):
        raise ValueError('Invalid group denominator or numerator')
    pt,pc=success_t/n_t,success_c/n_c
    if (success_t==0 and success_c==0) or (success_t==n_t and success_c==n_c):
        z,p=float('nan'),1.0
    else:
        z,p=proportions_ztest([success_t,success_c],[n_t,n_c])
    if not np.isfinite(p):
        # Both arms all-zero or all-one: identical observed proportions, z is undefined.
        p=1.0 if pt==pc else float('nan')
    low,high=confint_proportions_2indep(success_t,n_t,success_c,n_c,compare='diff',method='newcomb',alpha=alpha)
    return {'treatment_rate':pt,'control_rate':pc,'absolute_lift_pp':(pt-pc)*100,
            'relative_lift':(pt/pc-1) if pc>0 else None,'difference':pt-pc,
            'ci95_diff':[float(low),float(high)],'z_statistic':float(z) if np.isfinite(z) else None,
            'raw_p_value':float(p), 'confidence_interval_method':'Newcombe-Wilson independent proportions',
            'p_value_method':'two-sided unpooled counts pooled-null z-test'}


def srm(group_counts:dict, threshold:float=.001)->dict:
    counts=np.array([group_counts[a] for a in ARMS],dtype=float)
    if (counts<0).any() or counts.sum()<=0: raise ValueError('Invalid assignment counts')
    chi,p=chisquare(counts)
    return {'chi_square':float(chi),'p_value':float(p),'threshold':threshold,
            'flag':bool(p<threshold),'expected_per_arm':float(counts.sum()/3),
            'assumption':'Equal 1:1:1 intended random allocation, not guaranteed exact counts'}


def mean_spend_contrast(treat: pd.Series,control: pd.Series,iterations:int=3000, seed:int=1701)->dict:
    t=np.asarray(treat,dtype=float);c=np.asarray(control,dtype=float)
    if not (len(t)>1 and len(c)>1) or not (np.isfinite(t).all() and np.isfinite(c).all()):
        raise ValueError('Two finite spend samples, size >= 2, required')
    delta=float(t.mean()-c.mean())
    _,p=ttest_ind(t,c,equal_var=False)
    # Normal/Welch mean effect; deterministic percentile bootstrap separately as skew sensitivity.
    rng=np.random.default_rng(seed)
    boot=np.empty(iterations)
    for j in range(iterations):
        boot[j]=rng.choice(t,len(t),replace=True).mean()-rng.choice(c,len(c),replace=True).mean()
    return {'revenue_per_assigned_difference':delta,
            'incremental_spend_estimate_for_observed_treatment_arm':delta*len(t),
            'welch_p_value':float(p) if np.isfinite(p) else None,
            'bootstrap_ci95_per_assigned_customer':np.quantile(boot,[.025,.975]).tolist(),
            'bootstrap_iterations':iterations,'bootstrap_seed':seed,
            'interpretation':'Difference in observed 2-week spend per randomized customer, not margin/ROI; extrapolated difference is an estimate, not realized incremental ledger receipts'}


def analyze(frame:pd.DataFrame,bootstrap_iterations:int=1500)->dict:
    if set(frame.segment.unique())!=set(ARMS): raise ValueError('Exactly three known experimental arms required')
    n={a:int((frame.segment==a).sum()) for a in ARMS}
    if min(n.values())<=1: raise ValueError('Insufficient observations per arm')
    summary={}
    for arm in ARMS:
        subset=frame.loc[frame.segment==arm]
        num=len(subset)
        summary[arm]={'assigned':num,'conversions':int(subset.conversion.sum()),
          'visits':int(subset.visit.sum()),'spend_total':round(float(subset.spend.sum()),4),
          'conversion_rate':float(subset.conversion.mean()),'visit_rate':float(subset.visit.mean()),
          'spend_per_assigned':float(subset.spend.mean())}
        summary[arm]['conversion_ci95_wilson']=list(map(float,proportion_confint(summary[arm]['conversions'],num,method='wilson')))
    results={'n':len(frame),'groups':summary,'srm':srm(n),'baseline_balance':balance_diagnostics(frame),'primary_metric':'conversion / all randomized assigned customers',
             'control_comparisons':{},'exploratory_mens_vs_womens':{},'notes':[]}
    control=summary['No E-Mail']
    contrast_raw=[]
    for arm in ARMS[1:]:
        d=binary_contrast(summary[arm]['conversions'],n[arm],control['conversions'],n['No E-Mail'])
        contrast_raw.append(d['raw_p_value']);results['control_comparisons'][arm]={'conversion':d}
    _,adjusted,_,_=multipletests(contrast_raw,method='holm')
    for arm,p in zip(ARMS[1:],adjusted):
        d=results['control_comparisons'][arm]['conversion']; d['holm_adjusted_p_value']=float(p)
        d['holm_reject_5pct']=bool(p<.05)
    for arm in ARMS[1:]:
        record=results['control_comparisons'][arm]
        c=record['conversion']
        record['conversion_impact_estimate']={
           'estimated_incremental_conversions_in_assigned_treatment_arm':c['difference']*n[arm],
           'unadjusted_ci95_incremental_conversions':[v*n[arm] for v in c['ci95_diff']],
           'status':'randomized estimate, NOT individually observed incremental conversions'}
        record['visit']=binary_contrast(summary[arm]['visits'],n[arm],control['visits'],n['No E-Mail'])
        record['spend']=mean_spend_contrast(frame.loc[frame.segment==arm,'spend'],frame.loc[frame.segment=='No E-Mail','spend'],iterations=bootstrap_iterations)
    results['exploratory_mens_vs_womens']={
      'conversion':binary_contrast(summary['Mens E-Mail']['conversions'],n['Mens E-Mail'],
                   summary['Womens E-Mail']['conversions'],n['Womens E-Mail'])}
    results['notes']=[
     'Primary confirmatory family consists of two conversion-vs-control contrasts, Holm-corrected at 5%.',
     'Mens-vs-Womens comparison, website visit and monetary outcomes are secondary/exploratory; unadjusted p-values are not confirmatory.',
     'Spend is zero-heavy/skewed: bootstrapped confidence intervals are sensitivity context, not a guarantee of normality.',
     'Randomization supports intent-to-treat effect of assignment only, not who actually opened or read an email.',
     'No cost/margin/deliverability measures supplied; ROI, profit and actual send/open impact unavailable.']
    return results
