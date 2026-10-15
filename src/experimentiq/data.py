"""Never silently mutate the source: every row retained; strict type checks."""
import hashlib
import json
import os
import tempfile
import urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
from .config import RAW, PROCESSED, ORIGINAL_URL, PUBLIC_MIRROR, ARMS, INPUT_COLUMNS, ZIP_CLASSES, CHANNELS

class DataQualityError(ValueError):
    """Invalid or unsupported experimental data."""


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def acquire(destination: Path = RAW, source: str | None = None, use_mirror: bool = False) -> dict:
    """Try the original source; mirror is opt-in. Never replace existing data."""
    destination = Path(destination)
    if destination.exists():
        raise FileExistsError(f'Existing raw file preserved: {destination}')
    url = source or (PUBLIC_MIRROR if use_mirror else ORIGINAL_URL)
    if not url.startswith('https://'):
        raise ValueError('Only HTTPS source URLs are accepted; manually verify other sources.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    pending = destination.with_suffix('.download')
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'ExperimentIQ/1.0'}), timeout=35) as r:
            with pending.open('wb') as file:
                while True:
                    chunk = r.read(65536)
                    if not chunk: break
                    file.write(chunk)
        df = pd.read_csv(pending)
        validate_raw(df, expected_rows=64000)
        digest = sha256(pending)
        pending.replace(destination)
        manifest = {'source_url':url, 'source_type':'original' if url == ORIGINAL_URL else 'mirror_or_local',
                    'sha256':digest, 'rows':len(df), 'original_columns':list(df.columns), 'size_bytes':destination.stat().st_size}
        destination.with_suffix('.source.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
        return manifest
    finally:
        pending.unlink(missing_ok=True)


def load_raw(path: Path = RAW) -> pd.DataFrame:
    if not Path(path).is_file():
        raise FileNotFoundError(f'Dataset is absent: {path}. See docs/DATA_SOURCES.md; do NOT substitute simulated real data.')
    return pd.read_csv(path)


def validate_raw(frame: pd.DataFrame, expected_rows: int | None = 64000) -> dict:
    df = frame.copy(deep=True)
    errors = []
    if list(df.columns) != list(INPUT_COLUMNS):
        raise DataQualityError(f'Unexpected raw schema: {list(df.columns)}. Expected {list(INPUT_COLUMNS)}')
    if expected_rows is not None and len(df) != expected_rows:
        errors.append(f'Expected {expected_rows} rows, found {len(df)}')
    if df.isna().any().any():
        errors.append(f'Missing values: {df.isna().sum()[df.isna().sum()>0].to_dict()}')
    if len(df) == 0: errors.append('Dataset empty')
    for col in ['recency','history','spend','mens','womens','newbie','visit','conversion']:
        v = pd.to_numeric(df[col], errors='coerce')
        if v.isna().any() or not np.isfinite(v.to_numpy(dtype=float)).all():
            errors.append(f'{col}: nonnumeric/nonfinite value'); continue
        if col in ('mens','womens','newbie','visit','conversion') and not v.isin([0,1]).all():
            errors.append(f'{col}: expected binary 0 or 1')
        if col == 'recency' and (not v.between(1,12).all() or not (v == v.round()).all()):
            errors.append('recency: expected integer 1..12')
        if col in ('history','spend') and (v<0).any():
            errors.append(f'{col}: negative currency')
    if not df['segment'].isin(ARMS).all(): errors.append('Unknown experimental arm')
    missing_arms=[arm for arm in ARMS if arm not in set(df['segment'].dropna())]
    if missing_arms: errors.append(f'Missing experimental arms: {missing_arms}')
    if not df['zip_code'].isin(ZIP_CLASSES).all(): errors.append('Unknown zip_code category')
    if not df['channel'].isin(CHANNELS).all(): errors.append('Unknown channel category')
    if not df['history_segment'].astype(str).str.match(r'^[1-7]\) ').all():
        errors.append('Unexpected history_segment category')
    if errors: raise DataQualityError('\n'.join(errors))
    return {'rows':len(df),'columns':len(df.columns),
            'missing_per_column':{c:int(v) for c,v in df.isna().sum().items()},
            'exact_duplicate_feature_rows':int(df.duplicated().sum()),
            'duplicate_policy':'Retain exact duplicate rows: original dataset has no unique customer ID.',
            'arm_counts':{arm:int((df.segment == arm).sum()) for arm in ARMS},
            'zip_code_values':{str(k):int(v) for k,v in df.zip_code.value_counts().items()},
            'outcome_anomalies':{
                'conversion_without_visit':int(((df.conversion==1)&(df.visit==0)).sum()),
                'positive_spend_without_conversion':int(((df.spend>0)&(df.conversion==0)).sum()),
                'conversion_without_positive_spend':int(((df.conversion==1)&(df.spend==0)).sum())}}


def clean(frame: pd.DataFrame, expected_rows: int | None = 64000) -> pd.DataFrame:
    validate_raw(frame, expected_rows=expected_rows)
    out = frame.copy(deep=True)
    out.insert(0, 'source_row_number', np.arange(1, len(out)+1, dtype=np.int64))
    # Published CSV spells suburban as 'Surburban'; canonicalize only processed data.
    out['zip_code'] = out['zip_code'].replace({'Surburban':'Suburban'})
    for col in ['recency','mens','womens','newbie','visit','conversion']:
        out[col] = pd.to_numeric(out[col], errors='raise').astype('int64')
    for col in ['history','spend']:
        out[col] = pd.to_numeric(out[col], errors='raise').astype('float64')
    return out


def run_pipeline(raw: Path = RAW, processed: Path = PROCESSED, expected_rows: int | None = 64000) -> dict:
    df = load_raw(raw)
    profile = validate_raw(df, expected_rows=expected_rows)
    out = clean(df, expected_rows=expected_rows)
    processed.parent.mkdir(parents=True,exist_ok=True)
    # Write to a temp file then atomically replace. If interrupted, the prior artifact survives.
    fd, tmp = tempfile.mkstemp(prefix='.experimentiq-',suffix='.csv',dir=processed.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8',newline='') as handle:
            out.to_csv(handle,index=False,float_format='%.12g')
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp,processed)
    finally:
        Path(tmp).unlink(missing_ok=True)
    info = {'raw_sha256':sha256(raw), 'processed_sha256':sha256(processed),
            'profile':profile, 'transformations':['Added source_row_number as 1-based positional technical key',
             "Canonicalized 'Surburban' to 'Suburban' only in processed data", 'Preserved ALL input rows (no deduplication or imputation)']}
    # The manifest prevents a stale or manually changed processed file from reaching PostgreSQL.
    manifest = processed.with_suffix('.manifest.json')
    fd, tmp_meta = tempfile.mkstemp(prefix='.experimentiq-',suffix='.json',dir=processed.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as handle:
            json.dump({'pipeline_version':1,'raw_sha256':info['raw_sha256'],
                       'processed_sha256':info['processed_sha256'],
                       'rows':len(out)},handle,indent=2)
            handle.write('\n')
            handle.flush();os.fsync(handle.fileno())
        os.replace(tmp_meta,manifest)
    finally:
        Path(tmp_meta).unlink(missing_ok=True)
    return info


def verify_processed_input(raw:Path=RAW, processed:Path=PROCESSED,
                           expected_rows:int|None=64000)->pd.DataFrame:
    """Fail closed when DB input is stale, mutated, or not derived from the raw CSV."""
    raw,processed=Path(raw),Path(processed)
    if not processed.is_file():
        raise FileNotFoundError(f'Validated processed CSV missing: {processed}. Run pipeline first.')
    manifest=processed.with_suffix('.manifest.json')
    if not manifest.is_file():
        raise DataQualityError('Processed lineage manifest missing: rerun pipeline')
    try:
        meta=json.loads(manifest.read_text(encoding='utf-8'))
    except (ValueError, OSError) as err:
        raise DataQualityError('Invalid processed lineage manifest') from err
    if meta.get('pipeline_version') != 1:
        raise DataQualityError('Unsupported processing manifest version')
    checked=clean(load_raw(raw), expected_rows=expected_rows)
    saved=pd.read_csv(processed)
    if meta.get('raw_sha256') != sha256(raw) or meta.get('processed_sha256') != sha256(processed):
        raise DataQualityError('Raw or processed SHA-256 does not match lineage manifest')
    if meta.get('rows') != len(saved):
        raise DataQualityError('Processed manifest row count mismatch')
    try:
        pd.testing.assert_frame_equal(saved,checked,check_dtype=False,
                                      check_exact=False,atol=1e-9,rtol=1e-11)
    except AssertionError as err:
        raise DataQualityError('Processed rows differ from validated raw-derived output') from err
    return saved
