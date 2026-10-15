# Verified Hillstrom real-data provenance — ExperimentIQ

**Dataset:** Hillstrom / MineThatData 2008 E-Mail Analytics Challenge (64,000 randomized assignments).
**Source URL:** https://raw.githubusercontent.com/W-Tran/uplift-modelling/master/data/hillstrom/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv
**Source class:** mirror_or_local
**SHA-256:** `27bab8c5d3669f26ec08ebb50a0a78317542f29501156f2e2af6781fab4cd7e2`
**Rows and variables:** 64000 rows, 12 original columns.
**Raw dataset storage:** local/ephemeral CI only; deliberately NOT committed or uploaded.
**Transformations:** 1-based positional source_row_number and Surburban -> Suburban spelling correction in processed copy. All 64,000 rows retained.
**PostgreSQL:** live PostgreSQL 16 load and 3/3 arm-level SQL/Python KPI parity verified in ephemeral CI.
**Statistics:** see reports/analysis_actual.json and reports/business_decision_memo_actual.md; confidence intervals are unadjusted and Holm applies to the 2 primary conversion p-values.
**Business restriction:** no advertising costs, margins, delivery/open tracking or ROI in source.
**License:** publisher invited public analysis but provided no explicit standard redistribution license. The source CSV and row-level processed CSV are excluded.
**Provenance caveat:** a mirror is not a cryptographic publisher-verified original; this file records the exact downloaded SHA and URL, not independent authenticity certification.
**Synthetic demo:** data/synthetic/* and dashboard/data/demo.json are demonstrative and never merged with actual analysis.
**Native .pbix:** not produced; Windows Power BI Desktop required. DAX/M/theme and reproducible guide are provided.
