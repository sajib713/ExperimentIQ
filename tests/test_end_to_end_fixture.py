"""End-to-end smoke using fixture ONLY; never presented as actual Hillstrom results."""
import json
import pandas as pd
from experimentiq.data import run_pipeline,clean,sha256
from experimentiq.report import export_results

def test_fixture_pipeline_to_interactive_json_and_memo(toy_raw,tmp_path):
    raw=tmp_path/'synthetic_test_only.csv'
    processed=tmp_path/'processed.csv'
    toy_raw.to_csv(raw,index=False)
    pipeline=run_pipeline(raw,processed,expected_rows=None)
    assert pipeline['profile']['rows']==90
    actual=clean(pd.read_csv(raw),expected_rows=None)
    stats=export_results(actual,raw_path=raw,reports_dir=tmp_path/'reports',
                         dashboard_path=tmp_path/'dashboard/data/report.json',iterations=30)
    data=json.loads((tmp_path/'dashboard/data/report.json').read_text())
    assert data['metadata']['observed_sample']==90
    assert data['metadata']['source_sha256']==sha256(raw)
    assert 'holm_adjusted_p_value' in json.dumps(data)
    assert stats['n']==90
    for file in ['arm_kpis_actual.csv','segment_kpis_actual.csv','control_comparisons_actual.csv',
                 'analysis_actual.json','business_decision_memo_actual.md']:
        assert (tmp_path/'reports'/file).is_file()
    assert 'ROI/profit cannot be calculated' in (tmp_path/'reports/business_decision_memo_actual.md').read_text()
