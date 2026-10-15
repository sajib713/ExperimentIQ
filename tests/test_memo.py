from experimentiq.data import clean
from experimentiq.stats import analyze
from experimentiq.report import recommendation,build_memo

def test_memo_never_claims_roi(toy_raw):
    x=analyze(clean(toy_raw,expected_rows=None),bootstrap_iterations=20)
    memo=build_memo(x,'testing_sha','SYNTHETIC TEST ONLY')
    assert 'ROI/profit cannot be calculated' in memo
    assert 'SYNTHETIC TEST ONLY' in memo
    assert 'Holm' in memo
    assert 'Business question' in memo

def test_srm_gates_rollout(toy_raw):
    x=analyze(clean(toy_raw,expected_rows=None),bootstrap_iterations=20)
    x['srm']['flag']=True
    assert recommendation(x).startswith('HOLD:')
