"""Independent contract tests for published REAL Hillstrom analytics assets (never synthetic)."""
from pathlib import Path
import json
import pandas as pd
import pytest
from scipy.stats import chisquare
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportions_ztest

ROOT=Path(__file__).resolve().parents[1]
EXPECTED_SHA='27bab8c5d3669f26ec08ebb50a0a78317542f29501156f2e2af6781fab4cd7e2'
def data():
    paths=[ROOT/'reports/arm_kpis_actual.csv',ROOT/'reports/control_comparisons_actual.csv',
           ROOT/'reports/analysis_actual.json',ROOT/'reports/segment_kpis_actual.csv',
           ROOT/'dashboard/data/report.json']
    if not all(p.is_file() for p in paths):
        pytest.skip('published real-data aggregates absent locally; run on master CI')
    return pd.read_csv(paths[0]),pd.read_csv(paths[1]),json.loads(paths[2].read_text()),pd.read_csv(paths[3]),json.loads(paths[4].read_text())

def test_published_real_arms_and_denominators():
    arm,comparison,stats,segments,dashboard=data()
    expected={'No E-Mail':(21306,122,2262,13908.33),'Mens E-Mail':(21307,267,3894,30311.69),
              'Womens E-Mail':(21387,189,3238,23038.11)}
    assert stats['n']==dashboard['analysis']['n']==dashboard['metadata']['observed_sample']==64000
    assert dashboard['metadata']['source_sha256']==EXPECTED_SHA
    assert dashboard['metadata'].get('kind')!='SYNTHETIC_DEMO_ONLY'
    assert len(arm)==3 and set(arm.segment)==set(expected) and len(comparison)==2 and len(segments)>=90
    assert arm.assigned.sum()==64000 and arm.conversions.sum()==578
    assert arm.spend_total.sum()==pytest.approx(67258.13,abs=1e-7)
    for name,(n,c,v,s) in expected.items():
        row=arm.set_index('segment').loc[name]
        assert (row.assigned,row.conversions,row.visits)==(n,c,v)
        assert row.spend_total==pytest.approx(s,abs=1e-7)
        assert row.conversion_rate==pytest.approx(c/n,abs=1e-12)
        assert row.visit_rate==pytest.approx(v/n,abs=1e-12)
        assert stats['groups'][name]['conversion_rate']==pytest.approx(c/n)
        assert dashboard['analysis']['groups'][name]['assigned']==n

def test_published_holm_and_sample_ratio_mismatch():
    arms,comparisons,stats,_,_=data()
    arms=arms.set_index('segment')
    ctrl=arms.loc['No E-Mail']
    pvalues=[]
    for name in ['Mens E-Mail','Womens E-Mail']:
        a=arms.loc[name]
        z,p=proportions_ztest([a.conversions,ctrl.conversions],[a.assigned,ctrl.assigned])
        r=comparisons.set_index('treatment').loc[name]
        reported=stats['control_comparisons'][name]['conversion']
        assert r.conversion_lift_pp==pytest.approx(100*(a.conversions/a.assigned-ctrl.conversions/ctrl.assigned),abs=1e-10)
        assert r.raw_conversion_p==pytest.approx(p,rel=1e-7,abs=1e-15)
        assert reported['z_statistic']==pytest.approx(z,rel=1e-8)
        assert r.conversion_ci_low_pp < r.conversion_lift_pp < r.conversion_ci_high_pp
        assert r.revenue_per_assigned_lift==pytest.approx(a.spend_total/a.assigned-ctrl.spend_total/ctrl.assigned,abs=1e-10)
        pvalues.append(p)
    holm=multipletests(pvalues,alpha=0.05,method='holm')[1]
    for i,name in enumerate(['Mens E-Mail','Womens E-Mail']):
        assert comparisons.set_index('treatment').loc[name].holm_adjusted_conversion_p==pytest.approx(holm[i],rel=1e-7,abs=1e-15)
    assert stats['srm']['p_value']==pytest.approx(chisquare(arms.assigned).pvalue,rel=1e-8)
    assert not stats['srm']['flag']

def test_exploratory_dimensions_are_not_additive():
    arms,_,_,segments,_=data()
    for dimension,group in segments.groupby('dimension'):
        for row in arms.itertuples():
            assert group.loc[group.segment==row.segment,'assigned'].sum()==row.assigned,dimension

def test_reproducible_powerbi_files_and_safe_aggregate_logic():
    base=ROOT/'powerbi/desktop'
    for f in ['ArmKPIs.pq','Comparisons.pq','Segments.pq','SourceMetadata.pq','measures_aggregate.dax','VISUAL_BLUEPRINT.md']:
        assert (base/f).exists()
    dax=(base/'measures_aggregate.dax').read_text()
    assert 'DIVIDE([Conversions], [Assigned Customers])' in dax
    assert 'LOOKUPVALUE(Comparisons[holm_adjusted_conversion_p]' in dax
    assert 'Comparisons[treatment] = [Selected Treatment]' not in dax
    for file in ('ArmKPIs.pq','Comparisons.pq','Segments.pq'):
        q=(base/file).read_text()
        assert 'ProjectDirectory' in q and 'Error.Record' in q
        assert 'synthetic' not in q.lower()
