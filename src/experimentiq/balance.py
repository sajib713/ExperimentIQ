"""Pre-treatment covariate balance is a diagnostic only, not proof of valid randomization."""
from math import sqrt
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from .config import ARMS

NUMERIC_COVARIATES=('recency','history','mens','womens','newbie')
CATEGORICAL_COVARIATES=('zip_code','channel','history_segment')

def standardized_mean_difference(x, y):
    x=np.asarray(x,dtype=float);y=np.asarray(y,dtype=float)
    if len(x)<2 or len(y)<2 or not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError('At least two finite observations per arm')
    pooled=sqrt((float(x.var(ddof=1))+float(y.var(ddof=1)))/2)
    diff=float(x.mean()-y.mean())
    return float(diff/pooled) if pooled>0 else (0.0 if diff==0 else None)

def balance_diagnostics(df:pd.DataFrame)->dict:
    for name in ARMS:
        if (df.segment==name).sum()<2: raise ValueError('Missing or undersized treatment arm')
    num={};control=df.loc[df.segment=='No E-Mail']
    for arm in ARMS[1:]:
        t=df.loc[df.segment==arm]
        num[arm]={k:standardized_mean_difference(t[k],control[k]) for k in NUMERIC_COVARIATES}
    categorical={}
    for col in CATEGORICAL_COVARIATES:
        table=pd.crosstab(df.segment,df[col])
        chi,p,dof,_=chi2_contingency(table)
        categorical[col]={'chi_square':float(chi),'p_value':float(p),'dof':int(dof)}
    return {'standardized_mean_differences_vs_control':num,
            'categorical_independence_tests':categorical,
            'interpretation':'Exploratory pre-treatment balance diagnostics; no p-value is proof of successful randomization or proper exposure logging. No covariate selection/adjustment used to maximize a favorable result.'}
