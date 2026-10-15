# ExperimentIQ — Power BI Desktop authoring guide

**Power BI Desktop is Windows-only and is not available in the execution environment that built this repository.** Consequently, no `.pbix`, `.pbit`, or `.pbip` report has been fabricated. The checked-in assets are **DAX measures, a Power Query M import, a visual theme and precise construction steps**. The separately built `dashboard/` is a functional browser-based dashboard that needs actual report data.

## Prerequisites

1. For a complete row-level report, download the documented Hillstrom data independently (as allowed) with `python -m experimentiq.cli acquire` or, if the original host is unavailable, `python -m experimentiq.cli acquire --mirror`, then run `python -m experimentiq.cli all`. Verify the source SHA against `docs/REAL_DATA_VERIFICATION.md`. Alternatively, for **aggregate-only reporting without customer rows**, use the already committed `reports/arm_kpis_actual.csv`, `reports/control_comparisons_actual.csv` and `reports/segment_kpis_actual.csv`; the row-level measures do not apply to this aggregate-only mode.
2. Launch Power BI Desktop. Import `theme.json` at **View > Themes > Browse for themes**.
3. Set a Power Query text parameter `ProjectDirectory` pointing to your local clone (Windows path with no trailing slash). **Get data > Blank query > Advanced Editor**, paste `transform.pq`, set its query name to `Customers`, apply. Or import `data/processed/experiment_customers.csv` directly with explicitly verified data types.
4. Import `reports/control_comparisons_actual.csv` as `Comparisons`, `reports/segment_kpis_actual.csv` as `Segments` for optional exploratory tables; do not create fact-to-fact many-to-many relationships. Prefer displaying these as disconnected reporting tables.
5. Add the measures in `measures.dax` to Customers, creating each measure separately in **Modeling > New measure**. They rely on the Customers table and its row-level assignment data, not a calculated visitors-only denominator.

## Exact report layout

### Page 1 — Executive Overview (16:9)

- Top row: 4 Card visuals: `[Assigned Customers]`, `[Conversions]`, `[Conversion Rate]`, `[Observed Spend]`.
- Main area: Clustered bar with `Customers[segment]` on axis; `[Conversion Rate]` as value. Secondary clustered bar for `[Spend per Assigned]`; include `[Visit Rate]` in tooltip.
- Below: Table with `segment`, `[Assigned Customers]`, `[Conversions]`, `[Conversion Rate]`, `[Visit Rate]`, `[Spend per Assigned]`.
- Slicers: `zip_code`, `channel`, `newbie`, `history_segment`. All are historical/pre-treatment variables. Add a strong visual warning: *"Segment filtered metrics are exploratory; do not use unfiltered p-values to claim segment significance."*
- Text banner: *"Historical 2008 random assignment, 2-week assignment-to-email effect; no cost/margin data, not an ROI dashboard."*

### Page 2 — Statistical Inference

- Table visualization bound to disconnected `Comparisons`: `treatment`, `conversion_lift_pp`, `conversion_ci_low_pp`, `conversion_ci_high_pp`, `raw_conversion_p`, `holm_adjusted_conversion_p`, `holm_reject_5pct`.
- Use a scatter/error-bar visual if supported for the CI columns (point = lift, interval endpoints = lower/upper); a custom visual must undergo independent trust/security review. Otherwise use a table, which is reliable.
- Static text: *"Two pre-specified primary comparisons: mens vs control; womens vs control. Two-sided z-test, Holm-adjusted p. Newcombe 95% intervals are unadjusted and NOT simultaneous intervals. Primary conversion inference is for the unfiltered full dataset."*
- Add a Card for SRM warning manually from `reports/analysis_actual.json` or create a dedicated input table; never silently declare SRM passed.

### Page 3 — Customer Segments (Exploratory)

- Slicers: prior channel, zip class, purchase history segment, newbie, mens prior buyer, womens prior buyer, recency.
- Clustered columns: `Customers[segment]` on legend, `[Conversion Rate]` value, `Customers[channel]` on axis.
- Heatmap matrix: `Customers[history_segment]` on row, `Customers[segment]` on column, `[Conversion Rate]` as value, conditional formatting by scale.
- Show sample sizes in tables and tooltips. No statistical claims from apparent subgroup differences without multiplicity-aware interaction tests.

### Page 4 — Decision & Caveats

- Copy the **actual** recommendation from `reports/business_decision_memo_actual.md` only after pipeline execution.
- Note missing delivery/open metrics, costs, margins, customer lifetime value, unsubscribes, and 2008 generalizability limitations.
- Document gross spend estimates as experimental differences, not realized ROI.

## Report verification steps (manual, not executed in this Linux environment)

- Compare three arm rows in Page 1 with `reports/arm_kpis_actual.csv` (strict tolerance 0.000001).
- Verify control denominator uses *all assigned*, not only site visitors.
- Check each treatment's conversion lift with `reports/control_comparisons_actual.csv`.
- Confirm filters never modify displayed overall statistical p-values without a visible warning.
- Verify `Power BI > Refresh` works after data changes and that raw CSV is not embedded/published without usage permission.

Report binary status: **NOT GENERATED / NOT VERIFIED**. Save your verified local file as `powerbi/ExperimentIQ.pbix` only after completing the steps above.

## Aggregate-only reproducible option (no raw-data redistribution)

1. Check out the private repository's `master` branch. In Windows Power BI Desktop, **Get Data > Text/CSV** and import `reports/arm_kpis_actual.csv` as `ArmKPIs`, `reports/control_comparisons_actual.csv` as `Comparisons`, and `reports/segment_kpis_actual.csv` as `Segments`.
2. Set `ArmKPIs[segment]` to Text, `assigned`/`conversions`/`visits` to Whole Number, and conversion/visit/spend fields to Decimal Number. Validate exactly 3 arm rows, counts 21,306 / 21,307 / 21,387, and 64,000 total.
3. Build three cards for `SUM(ArmKPIs[assigned])`, `SUM(ArmKPIs[conversions])` and `SUM(ArmKPIs[spend_total])`. **Do not average arm conversion rates**: use `DIVIDE(SUM(ArmKPIs[conversions]), SUM(ArmKPIs[assigned]))` for a weighted overall conversion KPI.
4. Plot arm conversion rates using `ArmKPIs[segment]` with `ArmKPIs[conversion_rate]`. Put comparisons, confidence bounds, Holm p-values in a **static unfiltered table** (these tests are defined on the full sample).
5. Use a disconnected `Segments` table for subgroup exploration. Slicers on one table do NOT re-estimate the full-population p-values in `Comparisons`; label this visibly.
6. Import `theme.json`. Reconcile the table with `reports/analysis_actual.json` and `reports/business_decision_memo_actual.md`. Save `ExperimentIQ.pbix` locally only after visually verifying the model/filters and data source.

**Limitation:** These files constitute a reproducible Power BI authoring package, not a prebuilt or independently validated native `.pbix`. The aggregate-only report cannot implement all row-level drilldowns available from the uncommitted customer-level CSV.

## Verified release alternative — no raw-data download needed

The complete [Power BI rebuild ZIP](ExperimentIQ-PowerBI-Rebuild.zip) (not a PBIX) contains typed `powerbi/desktop/*.pq` queries for ArmKPIs, Comparisons, Segments and SourceMetadata, `measures_aggregate.dax`, theme, all verified actual aggregate CSV, `analysis_actual.json`, the full memo and source-provenance files. Extract to Windows and follow `powerbi/desktop/VISUAL_BLUEPRINT.md`. This is the preferred **aggregate-only** path: no need to download, embed, or redistribute customer rows. Source file SHA and 64,000-cohort checks run in the Python pipeline; M performs additional basic shape/KPI consistency checks (Power BI Desktop M evaluation has NOT been executed in this Linux environment).

The dashboard screenshot at `docs/images/dashboard-real.png` proves **Chromium validation of the browser-based dashboard**, not a Power BI Desktop report. A valid native PBIX requires saving, refreshing, and verifying in Windows Power BI Desktop.
