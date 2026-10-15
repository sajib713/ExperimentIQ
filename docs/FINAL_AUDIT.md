# ExperimentIQ — Updated release audit (15 October 2026)

## Evidence-based release status
**Real-data analytics: VERIFIED against the documented public mirror and PostgreSQL in GitHub Actions. Full application production deployment and native Power BI binary: NOT VERIFIED.** No synthetic records are used in the actual memo.

### Actual source and transformations
- Publisher: Kevin Hillstrom, MineThatData 2008 E-Mail Analytics Challenge; documented public analysis invitation, no explicit dataset redistribution license.
- Acquired from publicly accessible GitHub mirror after publisher HTTPS certificate validation failed in the GitHub runner.
- SHA-256: `27bab8c5d3669f26ec08ebb50a0a78317542f29501156f2e2af6781fab4cd7e2`.
- 64,000 rows, 12 source columns, all 3 arms; no missing values; 6,562 exact duplicate *records* retained (no customer ID to prove duplicate people). Raw "Surburban" standardized to "Suburban" only in derived data. No deletion/imputation.
- Published mirror authenticity against an original publisher checksum: **UNVERIFIED**, since publisher does not supply a checksum.
- Raw customer rows and processed CSV: **not committed**.

### Actual observed arm metrics
| Assigned group | N | Conversions | Rate | Visits | Total 2-week spend |
|---|---:|---:|---:|---:|---:|
| No E-Mail | 21,306 | 122 | 0.5726% | 2,262 | $13,908.33 |
| Mens E-Mail | 21,307 | 267 | 1.2531% | 3,894 | $30,311.69 |
| Womens E-Mail | 21,387 | 189 | 0.8837% | 3,238 | $23,038.11 |

### Inferential checks
- Conversion Mens-control: +0.6805 pp, unadjusted 95% Newcombe CI [+0.5014,+0.8641] pp, two-comparison Holm p = 3.0464e-13.
- Conversion Womens-control: +0.3111 pp, unadjusted 95% Newcombe CI [+0.1502,+0.4745] pp, Holm p = 0.0001571.
- SRM: chi-square 0.20253, p = 0.90369 (threshold 0.001; no flag).
- Spend: estimated difference per assigned $+0.7698 (Mens) or $+0.4244 (Womens). These are gross-spend differences, not ROI or realized incremental ledger sales.
- Men-vs-women direct contrast is exploratory; population transportability and individual campaign exposure are unverified.

### Acceptance audit
| Requirement | State | Evidence |
|---|---|---|
| Obtain usable real Hillstrom data | VERIFIED FROM MIRROR | provenance URL/SHA in docs/REAL_DATA_VERIFICATION.md |
| Original-publisher checksum equivalence | UNVERIFIED | source publisher does not provide checksum; HTTPS connection validation failed |
| Source profiling, schema, null and anomaly checks | VERIFIED | reports/profile_actual.json |
| Cleaning, deterministic pipeline and lineage | VERIFIED ON SOURCE | SHA-256 + processed manifest + real-data batch |
| PostgreSQL transactional load and real SQL/Python parity | VERIFIED IN EPHEMERAL CI | 3/3 arm match, PostgreSQL 16 |
| Correct ITT KPIs and denominators | VERIFIED | reports/arm_kpis_actual.csv, SQL views |
| 2 pre-specified control tests, Newcombe CI and Holm | VERIFIED | reports/analysis_actual.json |
| SRM and pre-treatment balance diagnostics | VERIFIED | reports/analysis_actual.json |
| Gross-spend uncertainty / guarded business impacts | VERIFIED | bootstrap CI in analysis and memo |
| No unsupported ROI claim | VERIFIED | business memo explicitly disclaims margins and costs |
| Segments and interactive HTML dashboard data | GENERATED; BROWSER VISUAL QA NOT VERIFIED | dashboard/data/report.json; HTML/JS source, JS syntax test |
| Native Power BI .pbix | NOT GENERATED | Power BI Desktop unavailable; DAX/M/theme/build guide |
| Real business decision memo | GENERATED FROM VERIFIED MIRROR | reports/business_decision_memo_actual.md |
| Pytest & PostgreSQL integration | 39 PASSED ON GITHUB ACTIONS | .github/workflows/real-data.yml |
| Local sandbox tests | 38 PASSED, 1 SKIPPED | No PostgreSQL installed in local container |
| Documentation / code / SQL / CI | PUBLISHED | master branch |
| Live production uptime/monitoring/security audit | NOT VERIFIED | This is a reproducible analytics portfolio, not deployed SaaS |

**Important:** Every `*_actual` report is from the real-data workflow. Every `data/synthetic/` file and `dashboard/data/demo.json` is a separately marked fabricated demonstration.
