# ExperimentIQ — Business Decision Memo (actual-data generated)

**Raw SHA-256:** `27bab8c5d3669f26ec08ebb50a0a78317542f29501156f2e2af6781fab4cd7e2`
**Provenance record:** {
  "source_url": "https://raw.githubusercontent.com/W-Tran/uplift-modelling/master/data/hillstrom/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv",
  "source_type": "mirror_or_local",
  "sha256": "27bab8c5d3669f26ec08ebb50a0a78317542f29501156f2e2af6781fab4cd7e2",
  "rows": 64000,
  "original_columns": [
    "recency",
    "history_segment",
    "history",
    "mens",
    "womens",
    "zip_code",
    "newbie",
    "channel",
    "segment",
    "visit",
    "conversion",
    "spend"
  ],
  "size_bytes": 3900976
}
**Analyzed sample:** 64,000 randomized assignments; three mutually exclusive arms.

## Business question
Does assignment to a men’s or women’s merchandising email improve 2-week conversion relative to no email?

## Measured evidence
| Group | Assigned | Purchases | Conversion | Visits | Visit rate | Observed spend ($) | Spend/assigned ($) |
|---|---:|---:|---:|---:|---:|---:|---:|
| No E-Mail | 21,306 | 122 | 0.573% | 2,262 | 10.617% | 13,908.33 | 0.6528 |
| Mens E-Mail | 21,307 | 267 | 1.253% | 3,894 | 18.276% | 30,311.69 | 1.4226 |
| Womens E-Mail | 21,387 | 189 | 0.884% | 3,238 | 15.140% | 23,038.11 | 1.0772 |

## Confirmatory primary outcome: conversion, ITT
Pre-specified contrasts: each email arm vs no-email. Two-sided pooled-null proportion z-tests; Holm correction controls family-wise error at 5%. Independent-proportion Newcombe/Wilson 95% intervals show unadjusted contrast uncertainty and are NOT multiplicity-adjusted simultaneous intervals.

### Mens E-Mail compared with No E-Mail
- Absolute conversion difference: **+0.681 percentage points** (95% unadjusted CI **[+0.501, +0.864] pp**).
- Relative conversion lift: **+118.84%** versus control.
- Estimated incremental conversions in the current treatment arm: **+145.0** (model-based ITT count; not individually observed).
- Two-sided unadjusted p = 1.52322e-13; Holm adjusted p = 3.04645e-13; passes primary 5% decision threshold: **True**.
- Two-week observed spend difference per assigned: **$+0.7698**; bootstrap 95% interval **[$+0.4813, $+1.0533]**.
- Estimated incremental 2-week gross spend across **this arm’s assigned sample**: **$+16,402.71** (randomized group difference scaled to treated sample size; not recorded incremental receipts or profit).

### Womens E-Mail compared with No E-Mail
- Absolute conversion difference: **+0.311 percentage points** (95% unadjusted CI **[+0.150, +0.475] pp**).
- Relative conversion lift: **+54.33%** versus control.
- Estimated incremental conversions in the current treatment arm: **+66.5** (model-based ITT count; not individually observed).
- Two-sided unadjusted p = 0.000157105; Holm adjusted p = 0.000157105; passes primary 5% decision threshold: **True**.
- Two-week observed spend difference per assigned: **$+0.4244**; bootstrap 95% interval **[$+0.1710, $+0.6930]**.
- Estimated incremental 2-week gross spend across **this arm’s assigned sample**: **$+9,076.90** (randomized group difference scaled to treated sample size; not recorded incremental receipts or profit).

## Randomization check
Sample Ratio Mismatch (equal thirds) χ²=0.203, p=0.903693, threshold=0.001. Flag: **False**. SRM is a diagnostic, not proof of exchangeability.

## Baseline covariate balance (diagnostic only)
Pairwise standardized mean differences for prior recency, spend, mens/womens purchase and new-customer indicator: {"Mens E-Mail": {"history": 0.00761286832154239, "mens": -0.0045823256374879625, "newbie": -0.0008918953696535328, "recency": 0.006831532454259954, "womens": 0.007588929691887142}, "Womens E-Mail": {"history": 0.006510722458553667, "mens": -0.008630731202832915, "newbie": 0.0025567009140795606, "recency": 0.005180013205688683, "womens": 0.004946313992582152}}.
Categorical independence diagnostics for historical customer attributes: {"channel": {"chi_square": 3.6324016175409097, "dof": 4, "p_value": 0.45803390781197906}, "history_segment": {"chi_square": 13.153291572293611, "dof": 12, "p_value": 0.3579979967183696}, "zip_code": {"chi_square": 2.8719422089251405, "dof": 4, "p_value": 0.5794791381657298}}.
Covariate balance neither proves valid randomization nor validates exposure logging.

## Decision recommendation
Mens E-Mail shows evidence of improved assignment-level conversion over control under the pre-specified Holm-adjusted comparison. Recommend a gated follow-up rollout/test, not an unconditional profit claim: confirm sending cost, contribution margin, deliverability and long-run effects first.

## Limitations & next required data
- Email assignment is randomized; actual delivery, opens, clicks and compliance were not supplied. Effects refer to assignment.
- Historical email test (2008), one retailer, two-week window; current-market transportability is untested.
- No cost of sending, margin, unsubscribes, lifetime value, campaign spend or exact customer identifiers: **ROI/profit cannot be calculated**.
- No measured customer lifetime values; gross spend is not incremental profit.
- Segment cuts are exploratory, even if visually large; validate interaction tests and corrections prospectively.
- Revenue differences are highly skewed; bootstrap intervals are sensitivity estimates with a fixed seed.
- A non-significant difference is not proof of equivalence; a positive significant result is not sufficient for a profit decision.

## Reproducibility
`python -m experimentiq.cli all` generates this memo from the checked raw dataset; see `reports/analysis_actual.json` and dashboard sources. No hard-coded outcome numbers are used.
