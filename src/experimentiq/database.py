"""PostgreSQL loading is opt-in; no default credentials embedded in source code."""
import os
from pathlib import Path
import pandas as pd
from .config import PROJECT_ROOT, PROCESSED, RAW
from .business import group_kpis
from .data import verify_processed_input

COLUMNS=['source_row_number','recency','history_segment','history','mens','womens','zip_code','newbie','channel','segment','visit','conversion','spend']

def load_postgres(csv_path:Path=PROCESSED,dsn:str|None=None,raw_path:Path=RAW,
                  expected_rows:int|None=64000)->dict:
    try: import psycopg
    except ImportError as exc: raise RuntimeError('Install optional dependency: pip install ".[postgres]"') from exc
    dsn=dsn or os.getenv('DATABASE_URL')
    if not dsn: raise ValueError('DATABASE_URL must be set')
    df=verify_processed_input(raw=raw_path,processed=csv_path,expected_rows=expected_rows)
    if list(df.columns)!=COLUMNS: raise ValueError('Processed CSV schema mismatch')
    # Single transaction: no partial success. Temporary staging then replace within txn.
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute((PROJECT_ROOT/'sql/001_schema.sql').read_text())
            cur.execute('LOCK TABLE experiment_customers IN ACCESS EXCLUSIVE MODE')
            cur.execute('CREATE TEMP TABLE iq_import (LIKE experiment_customers INCLUDING ALL) ON COMMIT DROP')
            with cur.copy('COPY iq_import ('+', '.join(COLUMNS)+') FROM STDIN WITH (FORMAT CSV, HEADER TRUE)') as copy:
                with open(csv_path,'rb') as handle:
                    for chunk in iter(lambda:handle.read(1 << 16),b''): copy.write(chunk)
            cur.execute('SELECT COUNT(*) FROM iq_import')
            loaded=cur.fetchone()[0]
            if loaded != len(df): raise RuntimeError('Staging count mismatch')
            cur.execute('TRUNCATE TABLE experiment_customers')
            cur.execute('INSERT INTO experiment_customers SELECT * FROM iq_import')
            cur.execute((PROJECT_ROOT/'sql/002_views.sql').read_text())
    return {'loaded_rows':loaded, 'status':'committed'}


def verify_postgres(csv_path:Path=PROCESSED,dsn:str|None=None,raw_path:Path=RAW,
                    expected_rows:int|None=64000)->list[dict]:
    try: import psycopg
    except ImportError as exc: raise RuntimeError('Install psycopg') from exc
    dsn=dsn or os.getenv('DATABASE_URL')
    if not dsn: raise ValueError('DATABASE_URL required')
    df=verify_processed_input(raw=raw_path,processed=csv_path,expected_rows=expected_rows)
    expected=group_kpis(df).set_index('segment')
    with psycopg.connect(dsn) as conn,conn.cursor() as cur:
        cur.execute('SELECT segment,assigned,conversions,visits,spend_total,conversion_rate,visit_rate,spend_per_assigned FROM vw_arm_kpis')
        rows=cur.fetchall()
    errors=[]
    for row in rows:
        arm=row[0]
        if arm not in expected.index: errors.append(f'unexpected arm {arm}'); continue
        for k,actual in zip(['assigned','conversions','visits','spend_total','conversion_rate','visit_rate','spend_per_assigned'],row[1:]):
            if abs(float(actual)-float(expected.loc[arm,k]))>1e-6:
                errors.append(f'{arm} {k}: SQL {actual} != Python {expected.loc[arm,k]}')
    if len(rows)!=len(expected): errors.append('Arm count mismatch')
    if errors: raise AssertionError('\n'.join(errors))
    return [{'segment':x[0], 'assigned':x[1], 'status':'matched'} for x in rows]
