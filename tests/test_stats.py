import numpy as np
import pytest
from experimentiq.stats import binary_contrast,srm,mean_spend_contrast,analyze
from experimentiq.data import clean

def test_known_binary_difference():
    d=binary_contrast(60,100,40,100)
    assert d['absolute_lift_pp']==pytest.approx(20)
    assert d['difference']==pytest.approx(.2)
    assert d['relative_lift']==pytest.approx(.5)
    assert d['ci95_diff'][0]<.2<d['ci95_diff'][1]
    assert d['raw_p_value']<.01

def test_equivalent_proportions():
    d=binary_contrast(50,100,50,100)
    assert d['raw_p_value']==pytest.approx(1)
    assert d['ci95_diff'][0]<0<d['ci95_diff'][1]

def test_edge_all_zero_valid():
    d=binary_contrast(0,10,0,10)
    assert d['raw_p_value']==1

def test_invalid_numerator_denominator():
    with pytest.raises(ValueError):binary_contrast(3,2,1,9)
    with pytest.raises(ValueError):binary_contrast(0,0,1,10)

def test_srm_balanced_and_unbalanced():
    assert not srm({'No E-Mail':100,'Mens E-Mail':100,'Womens E-Mail':100})['flag']
    assert srm({'No E-Mail':900,'Mens E-Mail':50,'Womens E-Mail':50})['flag']

def test_spend_bootstrap_seed_reproducible():
    a=mean_spend_contrast([1,2,3,4],[2,3,4,5],iterations=100,seed=22)
    b=mean_spend_contrast([1,2,3,4],[2,3,4,5],iterations=100,seed=22)
    assert a==b and a['revenue_per_assigned_difference']==pytest.approx(-1)

def test_full_analysis_toy(toy_raw):
    x=analyze(clean(toy_raw,expected_rows=None),bootstrap_iterations=50)
    assert x['n']==90
    assert set(x['control_comparisons'])=={'Mens E-Mail','Womens E-Mail'}
    assert all(0<=i['conversion']['holm_adjusted_p_value']<=1 for i in x['control_comparisons'].values())
