"""Auditable results exports and conditional recommendation, never fake metrics."""
import json
from pathlib import Path
import pandas as pd
from .business import group_kpis,subgroup_rows
from .stats import analyze
from .config import REPORTS,DASHBOARD_DATA,RAW
from .data import sha256

def recommendation(result:dict)->str:
    if result['srm']['flag']:
        return 'HOLD: SRM diagnostic flagged unexpectedly imbalanced assignment counts; investigate logging/randomization before deployment.'
    winners=[(arm,item['conversion']['difference']) for arm,item in result['control_comparisons'].items()
             if item['conversion']['holm_reject_5pct'] and item['conversion']['difference']>0]
    if not winners:
        return ('Do not claim a proven conversion gain for either email variant at the pre-specified Holm-adjusted 5% level. '
                'Consider a larger prospective test and collect cost/margin information before choosing a rollout.')
    arm,max_lift=max(winners,key=lambda kv:kv[1])
    return (f'{arm} shows evidence of improved assignment-level conversion over control under the pre-specified '
            'Holm-adjusted comparison. Recommend a gated follow-up rollout/test, not an unconditional profit claim: '
            'confirm sending cost, contribution margin, deliverability and long-run effects first.')

def build_memo(res:dict, raw_sha:str, provenance:str)->str:
    arm=res['groups']; control=arm['No E-Mail']; lines=[
      '# ExperimentIQ — Business Decision Memo (actual-data generated)',
      '',f'**Raw SHA-256:** `{raw_sha}`  ',f'**Provenance record:** {provenance}  ',
      f'**Analyzed sample:** {res["n"]:,} randomized assignments; three mutually exclusive arms.',
      '', '## Business question',
      'Does assignment to a men’s or women’s merchandising email improve 2-week conversion relative to no email?',
      '', '## Measured evidence',
      '| Group | Assigned | Purchases | Conversion | Visits | Visit rate | Observed spend ($) | Spend/assigned ($) |',
      '|---|---:|---:|---:|---:|---:|---:|---:|']
    for name,item in arm.items():
        lines.append(f'| {name} | {item["assigned"]:,} | {item["conversions"]:,} | {item["conversion_rate"]:.3%} | {item["visits"]:,} | {item["visit_rate"]:.3%} | {item["spend_total"]:,.2f} | {item["spend_per_assigned"]:.4f} |')
    lines.extend(['','## Confirmatory primary outcome: conversion, ITT',
       'Pre-specified contrasts: each email arm vs no-email. Two-sided pooled-null proportion z-tests; '
       'Holm correction controls family-wise error at 5%. Independent-proportion Newcombe/Wilson 95% '
       'intervals show unadjusted contrast uncertainty and are NOT multiplicity-adjusted simultaneous intervals.', ''])
    for name,comp in res['control_comparisons'].items():
        d=comp['conversion']; lo,hi=d['ci95_diff'];s=comp['spend']
        lines.extend([f'### {name} compared with No E-Mail',
          f'- Absolute conversion difference: **{d["absolute_lift_pp"]:+.3f} percentage points** '
          f'(95% unadjusted CI **[{lo*100:+.3f}, {hi*100:+.3f}] pp**).',
          f'- Relative conversion lift: **{d["relative_lift"]*100:+.2f}%** versus control.' if d['relative_lift'] is not None else '- Relative lift undefined because control rate is zero.',
          f'- Estimated incremental conversions in the current treatment arm: **{comp["conversion_impact_estimate"]["estimated_incremental_conversions_in_assigned_treatment_arm"]:+,.1f}** (model-based ITT count; not individually observed).',
          f'- Two-sided unadjusted p = {d["raw_p_value"]:.6g}; Holm adjusted p = {d["holm_adjusted_p_value"]:.6g}; '
          f'passes primary 5% decision threshold: **{d["holm_reject_5pct"]}**.',
          f'- Two-week observed spend difference per assigned: **${s["revenue_per_assigned_difference"]:+.4f}**; '
          f'bootstrap 95% interval **[${s["bootstrap_ci95_per_assigned_customer"][0]:+.4f}, ${s["bootstrap_ci95_per_assigned_customer"][1]:+.4f}]**.',
          f'- Estimated incremental 2-week gross spend across **this arm’s assigned sample**: '
          f'**${s["incremental_spend_estimate_for_observed_treatment_arm"]:+,.2f}** (randomized group difference scaled to treated sample size; not recorded incremental receipts or profit).',''])
    lines.extend(['## Randomization check',
       f'Sample Ratio Mismatch (equal thirds) χ²={res["srm"]["chi_square"]:.3f}, '
       f'p={res["srm"]["p_value"]:.6g}, threshold={res["srm"]["threshold"]}. '
       f'Flag: **{res["srm"]["flag"]}**. SRM is a diagnostic, not proof of exchangeability.',
       '', '## Baseline covariate balance (diagnostic only)',
       'Pairwise standardized mean differences for prior recency, spend, mens/womens purchase and new-customer indicator: '
       + json.dumps(res['baseline_balance']['standardized_mean_differences_vs_control'],sort_keys=True) + '.',
       'Categorical independence diagnostics for historical customer attributes: '
       + json.dumps(res['baseline_balance']['categorical_independence_tests'],sort_keys=True) + '.',
       'Covariate balance neither proves valid randomization nor validates exposure logging.',
       '', '## Decision recommendation',recommendation(res),'',
       '## Limitations & next required data',
       '- Email assignment is randomized; actual delivery, opens, clicks and compliance were not supplied. Effects refer to assignment.',
       '- Historical email test (2008), one retailer, two-week window; current-market transportability is untested.',
       '- No cost of sending, margin, unsubscribes, lifetime value, campaign spend or exact customer identifiers: **ROI/profit cannot be calculated**.',
       '- No measured customer lifetime values; gross spend is not incremental profit.',
       '- Segment cuts are exploratory, even if visually large; validate interaction tests and corrections prospectively.',
       '- Revenue differences are highly skewed; bootstrap intervals are sensitivity estimates with a fixed seed.',
       '- A non-significant difference is not proof of equivalence; a positive significant result is not sufficient for a profit decision.',
       '', '## Reproducibility',
       '`python -m experimentiq.cli all` generates this memo from the checked raw dataset; '
       'see `reports/analysis_actual.json` and dashboard sources. No hard-coded outcome numbers are used.', ''])
    return '\n'.join(lines)

def export_results(clean_df:pd.DataFrame, raw_path:Path=RAW, reports_dir:Path=REPORTS, dashboard_path:Path=DASHBOARD_DATA, iterations:int=1500)->dict:
    results=analyze(clean_df,bootstrap_iterations=iterations)
    segments=subgroup_rows(clean_df)
    arm_df=group_kpis(clean_df)
    reports_dir.mkdir(parents=True,exist_ok=True);dashboard_path.parent.mkdir(parents=True,exist_ok=True)
    arm_df.to_csv(reports_dir/'arm_kpis_actual.csv',index=False)
    comparison_rows=[]
    for arm,contrasts in results['control_comparisons'].items():
        d=contrasts['conversion']; v=contrasts['visit']; m=contrasts['spend']
        comparison_rows.append({'treatment':arm,'control':'No E-Mail',
          'conversion_lift_pp':d['absolute_lift_pp'],
          'conversion_ci_low_pp':d['ci95_diff'][0]*100,
          'conversion_ci_high_pp':d['ci95_diff'][1]*100,
          'relative_conversion_lift':d['relative_lift'],
          'raw_conversion_p':d['raw_p_value'],
          'holm_adjusted_conversion_p':d['holm_adjusted_p_value'],
          'holm_reject_5pct':d['holm_reject_5pct'],
          'visit_lift_pp':v['absolute_lift_pp'],
          'revenue_per_assigned_lift':m['revenue_per_assigned_difference'],
          'bootstrap_spend_ci_low':m['bootstrap_ci95_per_assigned_customer'][0],
          'bootstrap_spend_ci_high':m['bootstrap_ci95_per_assigned_customer'][1],
          'incremental_spend_estimate_on_arm':m['incremental_spend_estimate_for_observed_treatment_arm']})
    pd.DataFrame(comparison_rows).to_csv(reports_dir/'control_comparisons_actual.csv',index=False)
    pd.DataFrame(segments).to_csv(reports_dir/'segment_kpis_actual.csv',index=False)
    raw_sha=sha256(raw_path)
    (reports_dir/'analysis_actual.json').write_text(json.dumps(results,indent=2,allow_nan=False)+'\n',encoding='utf8')
    payload={'metadata':{'source_sha256':raw_sha,'observed_sample':len(clean_df),
             'warning':'Exploratory subgroups; ITT assignment effect, not delivered-email impact or ROI.'},
             'analysis':results, 'segments':segments,'recommendation':recommendation(results)}
    dashboard_path.write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n',encoding='utf8')
    manifest_path=raw_path.with_suffix('.source.json')
    provenance=manifest_path.read_text(encoding='utf8').strip() if manifest_path.exists() else 'UNKNOWN: locally provided raw CSV without acquisition manifest; independent provenance NOT verified.'
    (reports_dir/'business_decision_memo_actual.md').write_text(build_memo(results,raw_sha,provenance),encoding='utf8')
    return results
