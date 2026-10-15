"""Synthetic demonstrations must be reproducible and impossible to confuse with actual source."""
import json
import pytest
import pandas as pd
from experimentiq.demo import make_synthetic, make_demo
from experimentiq.config import RAW, DASHBOARD_DATA


def test_synthetic_reproducibility_and_validity():
    a=make_synthetic()
    b=make_synthetic()
    pd.testing.assert_frame_equal(a,b)
    assert len(a)==900
    assert set(a.segment)=={'No E-Mail','Mens E-Mail','Womens E-Mail'}


def test_synthetic_invalid_size():
    for v in [0,-1,3,False,1.5]:
        with pytest.raises(ValueError):make_synthetic(rows_per_arm=v)


def test_demo_is_labeled(tmp_path):
    csv=tmp_path/'demo.csv';out=tmp_path/'demo.json'
    result=make_demo(csv,out)
    payload=json.loads(out.read_text())
    assert result['kind']==payload['metadata']['kind']=='SYNTHETIC_DEMO_ONLY'
    assert payload['analysis']['n']==900
    assert 'SYNTHETIC DEMO ONLY' in payload['recommendation']


def test_demo_cannot_overwrite_real(tmp_path):
    with pytest.raises(ValueError):make_demo(RAW,tmp_path/'demo.json')
    with pytest.raises(ValueError):make_demo(tmp_path/'demo.csv',DASHBOARD_DATA)
    with pytest.raises(ValueError):make_demo(tmp_path/'same',tmp_path/'same')
