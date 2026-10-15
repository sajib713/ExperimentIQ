import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import pytest
import pandas as pd

@pytest.fixture
def toy_raw():
    # SYNTHETIC test fixture ONLY, not Hillstrom actual findings.
    records=[]
    for i,arm in enumerate(['No E-Mail','Mens E-Mail','Womens E-Mail']):
        for j in range(30):
            conv = int(j<(3+3*i))
            records.append({'recency':1+j%12,'history_segment':'1) $0 - $100',
              'history':round(30+j/10,2),'mens':j%2,'womens':1-j%2,
              'zip_code':'Surburban' if j%2 else 'Urban','newbie':j%2,
              'channel':'Web' if j%2 else 'Phone','segment':arm,
              'visit':int(j<10+2*i),'conversion':conv,'spend':float(conv*35)})
    return pd.DataFrame(records)
