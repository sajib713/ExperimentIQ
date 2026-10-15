# ExperimentIQ — Reproducible Native Power BI Desktop Report Blueprint

**Status:** Complete authoring assets, not a fabricated .pbix. The Linux environment has no native Windows Power BI Desktop engine or verified PBIX serializer. Power Query M/DAX have not been executed inside Desktop. The visual report must be saved and visually tested on Windows before claiming a native PBIX exists.

## Prepare the strictly real-data model

1. Authenticated checkout: `git clone --branch master https://github.com/sajib713/ExperimentIQ.git` (the repository is private). Alternatively extract `powerbi/ExperimentIQ-PowerBI-Rebuild.zip` after the screenshot/package CI publishes it. That ZIP is **not a PBIX**.
2. Open Windows Power BI Desktop > Blank Report. Home > Transform data > Manage Parameters > New Parameter: `ProjectDirectory`, type Text, value = repository/extraction full Windows root, no trailing backslash (e.g. `C:\ExperimentIQ-PowerBI`).
3. Home > Transform data > Blank query > Advanced Editor: paste and name, respectively, `ArmKPIs.pq` as **ArmKPIs**, `Comparisons.pq` as **Comparisons**, `Segments.pq` as **Segments**, `SourceMetadata.pq` as **SourceMetadata**. Check generated row validation errors before Close & Apply. Inputs: `reports/*actual*` only, NEVER `data/synthetic/` or `dashboard/data/demo.json`. No row-level customer CSV is redistributed.
4. Model view: leave all FOUR tables **disconnected**. This is intentional: ArmKPIs has 3 all-population rows, Comparisons 2 precomputed full-sample contrasts, Segments duplicated customer aggregates over 7 different dimensions. Joining/summing across dimensions double-counts customers. New measure > create each definition from `measures_aggregate.dax` separately (line breaks belong to the measure until the next named measure).
5. Apply `powerbi/theme.json` at View > Themes > Browse for Themes; enable **single-select** on the Comparisons[treatment] slicer and default to **Mens E-Mail**.
6. Configure four landscape 16:9 pages as below. Format rate measures % with two decimals, relative lift as %, pp measures as decimal numbers with 3 decimals, spend measures as USD. All text/CI/p-value values are full-population estimates only.

## Page 1 — Executive Overview

Cards: `[Assigned Customers]` = **64,000**, `[Conversions]`=**578**, `[Conversion Rate]`=**0.903125%**, `[Observed Gross Spend]`=**$67,258.13**. Clustered columns: Axis `ArmKPIs[segment]`; Values `[Conversion Rate]`; tooltips assigned, conversions, `[Visit Rate]`, `[Gross Spend / Assigned]`. Second bar: `[Visit Rate]` and third `[Gross Spend / Assigned]`; use separate value scales. Arm details table: assigned, conversions, visits, spend and rates. Banner: **2008 historical ITT (assignment), two-week window; gross spend is NOT ROI.**

## Page 2 — Treatment vs Control / Statistical Evidence

**Slicer:** Comparisons[treatment] single-select; choices Mens E-Mail and Womens E-Mail. Cards: `[Selected Absolute Lift (pp)]`, `[Selected Relative Lift]`, `[Selected Holm p]`, `[Selected Visit Lift (pp)]`, `[Selected Spend Lift per Assigned]`, `[Selected Incremental Gross Spend Estimate]`. Native table with Comparisons fields treatment, conversion_lift_pp, conversion_ci_low_pp, conversion_ci_high_pp, raw_conversion_p, holm_adjusted_conversion_p, holm_reject_5pct. These CI columns are **unadjusted** Newcombe–Wilson 95% CIs, and only p-values use Holm correction. To show chosen treatment plus control in a chart, add visual-level filter `[Show Control or Selected Treatment] = 1` to the ArmKPIs bar. The full three-arm chart on Page 1 must remain unchanged by this selector. Use the CI lower/upper **table as canonical display** even if native error-bar visuals are unavailable.

Expected selected Mens: +0.68050065 percentage points, CI [+0.50143447,+0.86407234] pp, Holm p=3.046447e-13, visit lift +7.658956 pp, spend/customer +$0.769827. Women: +0.31110575 pp, CI [+0.15016571,+0.47454713], p=0.000157105, visit lift +4.523311 pp, spend/customer +$0.424412.

## Page 3 — Exploratory Customer Segments

Slicers: Segments[dimension], Segments[value] with a clearly marked single active dimension. Show Segments[segment], [value], [assigned], [conversions], [conversion_rate], [visit_rate], [spend_per_assigned]. Only compute segmented rates within ONE selected dimension (e.g. channel, zip_code, newbie); each dimension duplicates a 64,000-assignment population. Never add all Segments[assigned] across dimensions. NO inferential significance from exploratory subgroups.

## Page 4 — Recommendation, Provenance and Limitations

Display the verified decision from `reports/business_decision_memo_actual.md`: Men's email has stronger observed conversion improvement; recommend a gated modern follow-up, NOT unqualified profitable deployment. Show `SourceMetadata` including public-mirror source SHA-256 `27bab8c5d3669f26ec08ebb50a0a78317542f29501156f2e2af6781fab4cd7e2`. Static SRM chi-square=0.202531, p=0.903693 at 0.001 flag threshold. Limitations: no known marginal sending cost, margin, unsubscribes or verified email delivery/open rates; original publisher checksum absent; 2008 generalization to modern customers not tested.

## Mandatory independent Windows verification

- [ ] Power Query refresh and M-type validation succeed: 3 arm rows, 2 contrasts, 93 exploratory segment rows, 6 metadata rows; all columns typed.
- [ ] Page 1 total customers=64000, conversions=578, gross spend=$67258.13, and arm conversion rates 0.5726087%, 1.2531093%, 0.8837144%.
- [ ] Men->Women slicer changes only selected contrast numbers; cannot mutate static full-population p-values or total-arm bars.
- [ ] No subtotal across Segments dimension; verify counts when filtering channel versus zip_code separately.
- [ ] Reopen after File > Save as `ExperimentIQ.pbix`; refresh all queries, inspect visual tooltips and filtered cards for correctness.
- [ ] Do not commit row-level data or claim Power BI Desktop visual validation before this manual check.

The CI screenshot of `dashboard/` validates the standalone **HTML dashboard**, not a Windows PBIX file.
