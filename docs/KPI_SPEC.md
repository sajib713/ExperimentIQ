# KPI definitions, exact denominators and interpretation

All metrics are calculated separately for three mutually exclusive randomized arms. `n_g` always includes **every assigned** customer in group `g`, including people who never visited.

| KPI | Definition | Interpretation |
|---|---|---|
| Assigned | `COUNT(*)` where `segment=g` | Sample size denominator |
| Conversions | `SUM(conversion)` | Customers who purchased within 2 weeks |
| Conversion rate | `SUM(conversion) / COUNT(*)` | Two-week assignment-level purchase probability |
| Visits | `SUM(visit)` | Visited within 2 weeks |
| Visit rate | `SUM(visit) / COUNT(*)` | Visited proportion among assigned |
| Observed spend | `SUM(spend)` | Gross attributed observations; **not profit** |
| Spend per assigned | `SUM(spend) / COUNT(*)` | Revenue proxy per randomized customer; includes zeros |
| Absolute conversion lift | `(p_t - p_c)*100` | Percentage points, not percent change |
| Relative conversion lift | `(p_t/p_c)-1` if `p_c>0` | Proportional change vs control; not defined at control rate zero |
| Spend lift per assigned | `(sum(spend_t)/n_t)-(sum(spend_c)/n_c)` | Difference in **observed mean** spend per assigned |
| Incremental conversions (estimated) | `(p_t - p_c) * n_t` | Randomized estimated incremental outcomes among treated assignments; not observed ledger entries |
| Estimated incremental gross spend | `(mean_spend_t - mean_spend_c)*n_t` | Randomized estimated sample-arm effect, not net profit, not ROI |

## SQL-Python parity

`sql/002_views.sql` implements KPIs using SQL `SUM`/`COUNT`. `src/experimentiq/business.py` implements the same formulas. `tests/test_sql.py` executes adapted SELECT/view SQL on an in-memory relational SQLite fixture and checks equality. When PostgreSQL is available run `python -m experimentiq.cli verify-db` for an actual server-side parity check. The SQLite test is **not** a PostgreSQL integration test.

## Segment caution

`zip_code`, `channel`, `newbie`, `mens`, `womens`, `history_segment`, `recency` are prior attributes and can be used for exploratory subgroup descriptions. Segment filters alter denominators; primary global Holm-adjusted p-values are **not** valid as subgroup p-values. Never filter on visit, conversion or spend and call the result an unbiased A/B estimate.
