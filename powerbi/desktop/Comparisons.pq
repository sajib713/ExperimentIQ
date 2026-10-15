let
    CsvPath = ProjectDirectory & "\\reports\\control_comparisons_actual.csv",
    Raw = Csv.Document(File.Contents(CsvPath), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Raw, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"treatment", type text}, {"control", type text}, {"conversion_lift_pp", type number}, {"conversion_ci_low_pp", type number}, {"conversion_ci_high_pp", type number}, {"relative_conversion_lift", type number}, {"raw_conversion_p", type number}, {"holm_adjusted_conversion_p", type number}, {"holm_reject_5pct", type logical}, {"visit_lift_pp", type number}, {"revenue_per_assigned_lift", type number}, {"bootstrap_spend_ci_low", type number}, {"bootstrap_spend_ci_high", type number}, {"incremental_spend_estimate_on_arm", type number}}, "en-US"),
    Checked = if Table.RowCount(Typed) <> 2 or List.Sort(Typed[treatment]) <> {"Mens E-Mail","Womens E-Mail"} or List.AnyTrue(List.Transform(Table.ToRecords(Typed), each [control] <> "No E-Mail" or [holm_adjusted_conversion_p] < [raw_conversion_p] or [conversion_ci_low_pp] > [conversion_lift_pp] or [conversion_ci_high_pp] < [conversion_lift_pp])) then error Error.Record("ExperimentIQ inference error","The verified treatment contrasts are missing or inconsistent.") else Typed
in
    Checked
