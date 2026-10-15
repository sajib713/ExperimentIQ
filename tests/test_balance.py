import pytest
from experimentiq.balance import standardized_mean_difference,balance_diagnostics
from experimentiq.data import clean

def test_zero_smd_for_equal_distributions():
    assert standardized_mean_difference([1,2,3],[1,2,3])==pytest.approx(0)

def test_nonzero_smd():
    assert standardized_mean_difference([3,4,5],[1,2,3])>0

def test_balance_has_all_expected_pre_treatment_features(toy_raw):
    data=balance_diagnostics(clean(toy_raw,expected_rows=None))
    assert set(data['standardized_mean_differences_vs_control']['Mens E-Mail'])=={'recency','history','mens','womens','newbie'}
    assert set(data['categorical_independence_tests'])=={'zip_code','channel','history_segment'}

def test_balance_rejects_insufficient_samples(toy_raw):
    df=clean(toy_raw,expected_rows=None)
    with pytest.raises(ValueError): balance_diagnostics(df.iloc[:2])
