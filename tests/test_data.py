import pandas as pd
import pytest
from experimentiq.data import validate_raw,clean,DataQualityError,run_pipeline,sha256

def test_valid_and_clean_preserves_rows(toy_raw):
    orig=toy_raw.copy(deep=True)
    profile=validate_raw(toy_raw,expected_rows=None)
    assert profile['rows']==90
    out=clean(toy_raw,expected_rows=None)
    assert len(out)==90 and out.source_row_number.iloc[-1]==90
    assert 'Surburban' not in out.zip_code.unique()
    pd.testing.assert_frame_equal(toy_raw,orig)

def test_missing_rejected(toy_raw):
    toy_raw.loc[0,'history']=None
    with pytest.raises(DataQualityError,match='Missing'): validate_raw(toy_raw,expected_rows=None)

def test_wrong_arm_rejected(toy_raw):
    toy_raw.loc[0,'segment']='Experimental'
    with pytest.raises(DataQualityError,match='arm'): clean(toy_raw,expected_rows=None)

def test_bad_binary_rejected(toy_raw):
    toy_raw.loc[2,'conversion']=2
    with pytest.raises(DataQualityError,match='binary'): clean(toy_raw,expected_rows=None)

def test_bad_schema_rejected(toy_raw):
    with pytest.raises(DataQualityError,match='schema'): validate_raw(toy_raw.drop(columns=['spend']),expected_rows=None)

def test_no_dedup_even_if_identical(toy_raw):
    x=toy_raw.iloc[[0,0,30,60]].reset_index(drop=True)
    assert len(clean(x,expected_rows=None))==4

def test_wrong_count_rejected(toy_raw):
    with pytest.raises(DataQualityError,match='Expected 64000'):validate_raw(toy_raw)

def test_pipeline_checks_missing_dataset(tmp_path):
    with pytest.raises(FileNotFoundError):run_pipeline(tmp_path/'absent.csv',tmp_path/'clean.csv')

def test_deterministic_csv_and_sha(toy_raw,tmp_path):
    path=tmp_path/'fixture.csv';toy_raw.to_csv(path,index=False)
    p1=run_pipeline(path,tmp_path/'out.csv',expected_rows=None);p2=run_pipeline(path,tmp_path/'out.csv',expected_rows=None)
    assert p1['processed_sha256']==p2['processed_sha256']
    assert sha256(path)==p1['raw_sha256']


def test_missing_experimental_arm_rejected(toy_raw):
    missing=toy_raw.loc[toy_raw.segment!='Womens E-Mail'].copy()
    with pytest.raises(DataQualityError,match='Missing experimental arms'):
        validate_raw(missing,expected_rows=None)
