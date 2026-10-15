# SYNTHETIC DEMO DATA — NOT REAL EXPERIMENT FINDINGS

`demo_customers.csv` is generated from deterministic pseudo-random distributions by `python -m experimentiq.cli demo` (seed `20261015`). Every single customer and outcome is **invented** for software smoke-testing.

**Do not claim the sample is Hillstrom, or quote its conversion lift, spend, p-values, confidence intervals, or A/B recommendations as empirical evidence.** It is not derived from, and is not a substitute for, Hillstrom.

The demo command writes `dashboard/data/demo.json`. Open `http://localhost:8000/?demo=1` only for UI testing. Default `http://localhost:8000/` remains fail-closed until real data are acquired. The real pipeline still requires 64,000 source rows.
