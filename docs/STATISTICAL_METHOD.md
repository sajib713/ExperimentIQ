# Statistical analysis plan, scope, and interpretation

## Experiment design

MineThatData presents a randomized three-arm email experiment with a two-week observation window. The estimand is the **intent-to-treat (assignment-to-variant)** effect relative to no email; delivery/open are unobserved. The source lacks full randomization code, exact timestamps, IDs, and device-level exposure records. We cannot prove implementation integrity from an end-state CSV.

## Confirmation hierarchy

- **Primary:** Conversion rate. Two pre-declared control contrasts: `Mens E-Mail` vs `No E-Mail` and `Womens E-Mail` vs `No E-Mail`. Each two-sided proportion z-test uses the null pooled standard error. The two p-values are adjusted using **Holm step-down family-wise error control** at 5%. Reject only if adjusted p <0.05.
- **95% effect uncertainty:** Newcombe independent-proportion difference intervals based on Wilson scores (`statsmodels.stats.proportion.confint_proportions_2indep(method='newcomb')`). These are **unadjusted pointwise** intervals, not 95% simultaneous family-wise coverage. Interpret adjusted p-values for the confirmatory decision.
- **Secondary / exploratory:** Website visits via z-test, gross spend per assigned via Welch test plus deterministic percentile bootstrap, direct mens-vs-womens conversion contrast, subgroup slice summaries. These are not multiplicity-protected confirmatory results. Avoid subgroup performance claims until powered interaction tests and corrections.
- **Baseline balance diagnostics:** standardized mean differences for prior recency, spend, mens/womens purchase, newbie vs control and chi-square independence checks for historical channel, area class and spend band. These are descriptive diagnostics, **not** post-hoc adjustment, not confirmatory inference, and not proof of assignment integrity.
- **Sample Ratio Mismatch:** Pearson chi-square goodness-of-fit against equal 1:1:1 allocations; flag at p < 0.001. SRM is only an alert for potential allocation/logging issues, not a proof of independence or validation of the treatment effect. A clear SRM flags rollout recommendation as HOLD.
- **Spend CI:** Nonparametric independently resampled bootstrap percentile (default 1,500 repetitions, seed 1701). Monetary outcome is often skewed and zero-inflated; uncertainty may be sensitive to tails. No customer-level cluster ID is available.

## Inferential guardrails

Absolute lift = difference of proportions; relative lift = proportional change vs the control proportion. Subgroup splits are after exposure only on **pre-treatment** characteristics. No selection by outcomes for estimators. Results from historical 2008 retailers may fail to transport to 2026. No campaign costs, margins, email delivery/open rates, LTV or long-term retention were provided; **ROI, profit, payback and effective email-open treatment effects cannot be inferred**.

If primary differences are non-significant, this is **not** evidence of equivalence. If a positive primary result passes Holm, next step should be a controlled/gated rollout with prospective monitoring and collection of incremental contribution costs and margins, rather than a blanket profit guarantee.

Validation cases use synthetic, explicitly marked fixture data in `tests/conftest.py`, and never appear in executive reports.
