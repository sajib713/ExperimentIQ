"""Canonical KPI aggregates. Denominator ALWAYS number randomized/assigned."""
import pandas as pd
from .config import ARMS

def group_kpis(frame:pd.DataFrame,keys:list[str]|None=None)->pd.DataFrame:
    keys=keys or ['segment']
    if 'segment' not in keys: raise ValueError('segment must be included')
    if frame.empty: raise ValueError('Empty experiment')
    if frame[['conversion','visit','spend']].isna().any().any(): raise ValueError('Missing outcomes')
    grouped=frame.groupby(keys,dropna=False,observed=True).agg(
        assigned=('conversion','size'), conversions=('conversion','sum'),
        visits=('visit','sum'), spend_total=('spend','sum')).reset_index()
    grouped['conversion_rate']=grouped['conversions']/grouped['assigned']
    grouped['visit_rate']=grouped['visits']/grouped['assigned']
    grouped['spend_per_assigned']=grouped['spend_total']/grouped['assigned']
    return grouped

SEGMENTS=['zip_code','channel','newbie','mens','womens','history_segment','recency']

def subgroup_rows(df:pd.DataFrame)->list[dict]:
    rows=[]
    for dimension in SEGMENTS:
        for record in group_kpis(df,['segment',dimension]).to_dict(orient='records'):
            rows.append({'dimension':dimension,'value':str(record[dimension]),
               **{k:(int(v) if k in ['assigned','conversions','visits'] else float(v))
                  for k,v in record.items() if k not in ('segment',dimension)},
               'segment':record['segment']})
    return rows
