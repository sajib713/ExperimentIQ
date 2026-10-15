"""Run the relational SELECT logic on SQLite fixture; actual PostgreSQL remains a separate integration check."""
import re
import sqlite3
import pandas as pd
import pytest
from pathlib import Path
from experimentiq.data import clean
from experimentiq.business import group_kpis

SQL=(Path(__file__).resolve().parents[1]/'sql/002_views.sql').read_text()

def postgres_views_to_sqlite(script):
    return re.sub(r'CREATE OR REPLACE VIEW', 'CREATE VIEW', script, flags=re.IGNORECASE)

def test_all_sql_analytic_views_execute_on_fixture(toy_raw):
    df=clean(toy_raw,expected_rows=None)
    with sqlite3.connect(':memory:') as conn:
        df.to_sql('experiment_customers',conn,index=False)
        conn.executescript(postgres_views_to_sqlite(SQL))
        sql=pd.read_sql_query('SELECT * FROM vw_arm_kpis',conn).set_index('segment')
        py=group_kpis(df).set_index('segment')
        assert len(sql)==3
        for col in ['assigned','conversions','visits','spend_total','conversion_rate','visit_rate','spend_per_assigned']:
            for arm in sql.index:
                assert sql.loc[arm,col]==pytest.approx(py.loc[arm,col],abs=1e-7)
        assert pd.read_sql_query('SELECT COUNT(*) n FROM vw_segment_kpis',conn).loc[0,'n']>20
        lifts=pd.read_sql_query('SELECT * FROM vw_control_lifts',conn)
        assert len(lifts)==2
        assert lifts.set_index('treatment').loc['Mens E-Mail','conversion_lift_pp']==pytest.approx(10)
