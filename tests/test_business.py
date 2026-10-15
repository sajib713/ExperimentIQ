import pytest
from experimentiq.business import group_kpis,subgroup_rows
from experimentiq.data import clean

def test_denominator_all_assigned(toy_raw):
    df=clean(toy_raw,expected_rows=None)
    vals=group_kpis(df).set_index('segment')
    assert vals.loc['No E-Mail','assigned']==30
    assert vals.loc['Mens E-Mail','conversions']==6
    assert vals.loc['Mens E-Mail','conversion_rate']==.2
    assert vals.loc['Womens E-Mail','spend_per_assigned']==10.5

def test_segments_reconcile(toy_raw):
    df=clean(toy_raw,expected_rows=None)
    seg=subgroup_rows(df)
    assert sum(r['assigned'] for r in seg if r['dimension']=='zip_code')==len(df)

def test_invalid_keys(toy_raw):
    with pytest.raises(ValueError,match='segment'):group_kpis(toy_raw,['zip_code'])
