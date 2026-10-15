# ExperimentIQ — real-data business memo status

**GENERATED AND VERIFIED FROM THE DOCUMENTED HILLSTROM PUBLIC MIRROR** (15 October 2026, 64,000 original-schema customer records). The actual-data report is `reports/business_decision_memo_actual.md`. Read `docs/REAL_DATA_VERIFICATION.md` for source SHA-256, provenance limitation, and 3/3 PostgreSQL SQL–Python reconciliation.

The publisher's HTTPS endpoint failed certificate validation, so the pipeline used a documented mirror; the mirror matches the public schema and expected sample size, but no publisher-provided checksum establishes exact identity with the original.

**Summary:** Mens E-Mail (1.253%) and Womens E-Mail (0.884%) exceed control (0.573%) conversion. Both Holm-adjusted comparisons pass p<0.05, while Mens has the larger positive difference. Gross spend is NOT net profit or ROI. Recommended follow-up requires margin/cost/exposure data.

**Tests:** 39 passed on GitHub Actions Python 3.12 + ephemeral PostgreSQL 16; local test environment 38 passed and 1 PostgreSQL-specific skip.

**Synthetic:** `data/synthetic/` and `dashboard/data/demo.json` are fabricated and explicitly not source data.

**Power BI:** DAX/M/theme/build guide exist, but a native `.pbix` was not created on the Linux runner. Rebuild using `powerbi/BUILD_GUIDE.md`.
