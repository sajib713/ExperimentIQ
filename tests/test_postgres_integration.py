"""Runs only against an explicitly dedicated disposable TEST_DATABASE_URL.
Never targets DATABASE_URL or any existing production database.
"""
import os
import pandas as pd
import pytest
from experimentiq.data import clean
from experimentiq.database import load_postgres,verify_postgres

@pytest.mark.skipif(not os.getenv('TEST_DATABASE_URL'),reason='PostgreSQL integration unavailable: TEST_DATABASE_URL not configured')
def test_transactional_postgres_load_and_parity(toy_raw,tmp_path):
    path=tmp_path/'test_fixture_only.csv'
    clean(toy_raw,expected_rows=None).to_csv(path,index=False)
    dsn=os.getenv('TEST_DATABASE_URL')
    assert 'test' in dsn.lower(), 'Dedicated disposable TEST database only'
    assert load_postgres(csv_path=path,dsn=dsn)['loaded_rows']==90
    assert len(verify_postgres(csv_path=path,dsn=dsn))==3
