"""Release guards prevent stale / edited analysis inputs entering the database."""
import json
from pathlib import Path
import pandas as pd
import pytest
from experimentiq.data import DataQualityError, run_pipeline, verify_processed_input, sha256


def paths(toy_raw, tmp_path):
    raw = tmp_path/'raw.csv'
    processed = tmp_path/'processed.csv'
    toy_raw.to_csv(raw,index=False)
    run_pipeline(raw,processed,expected_rows=None)
    return raw,processed


def test_valid_raw_and_processed_lineage(toy_raw,tmp_path):
    raw,processed = paths(toy_raw,tmp_path)
    verified = verify_processed_input(raw,processed,expected_rows=None)
    assert len(verified)==len(toy_raw)
    manifest = json.loads(processed.with_suffix('.manifest.json').read_text())
    assert manifest['raw_sha256']==sha256(raw)
    assert manifest['processed_sha256']==sha256(processed)
    assert manifest['rows']==len(toy_raw)


def test_mutated_processed_csv_rejected(toy_raw,tmp_path):
    raw,processed = paths(toy_raw,tmp_path)
    df=pd.read_csv(processed)
    df.loc[0,'conversion'] = 1-df.loc[0,'conversion']
    df.to_csv(processed,index=False)
    with pytest.raises(DataQualityError,match='SHA-256'):
        verify_processed_input(raw,processed,expected_rows=None)


def test_changed_raw_csv_rejected(toy_raw,tmp_path):
    raw,processed = paths(toy_raw,tmp_path)
    df=pd.read_csv(raw)
    df.loc[0,'history'] += 1
    df.to_csv(raw,index=False)
    with pytest.raises(DataQualityError,match='SHA-256'):
        verify_processed_input(raw,processed,expected_rows=None)


def test_missing_manifest_rejected(toy_raw,tmp_path):
    raw,processed = paths(toy_raw,tmp_path)
    processed.with_suffix('.manifest.json').unlink()
    with pytest.raises(DataQualityError,match='manifest missing'):
        verify_processed_input(raw,processed,expected_rows=None)


def test_wrong_processed_row_order_rejected_even_if_manifest_updated(toy_raw,tmp_path):
    raw,processed = paths(toy_raw,tmp_path)
    df=pd.read_csv(processed).iloc[::-1].reset_index(drop=True)
    df.to_csv(processed,index=False)
    manifest=processed.with_suffix('.manifest.json')
    meta=json.loads(manifest.read_text())
    meta['processed_sha256']=sha256(processed)
    manifest.write_text(json.dumps(meta))
    with pytest.raises(DataQualityError,match='differ from validated'):
        verify_processed_input(raw,processed,expected_rows=None)


def test_schema_migration_does_not_commit_inside_loader_transaction():
    script=(Path(__file__).resolve().parents[1]/'sql/001_schema.sql').read_text()
    statements=[line.strip().upper() for line in script.splitlines()
                if line.strip() and not line.strip().startswith('--')]
    assert 'COMMIT;' not in statements
    assert 'BEGIN;' not in statements
