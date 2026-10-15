let
    CsvPath = ProjectDirectory & "\\reports\\arm_kpis_actual.csv",
    Raw = Csv.Document(File.Contents(CsvPath), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Raw, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"segment", type text}, {"assigned", Int64.Type}, {"conversions", Int64.Type}, {"visits", Int64.Type}, {"spend_total", type number}, {"conversion_rate", type number}, {"visit_rate", type number}, {"spend_per_assigned", type number}}, "en-US"),
    Checked = if Table.RowCount(Typed) <> 3 or List.Sum(Typed[assigned]) <> 64000 or List.Sum(Typed[conversions]) <> 578 or List.Sort(Typed[segment]) <> {"Mens E-Mail", "No E-Mail", "Womens E-Mail"} or List.AnyTrue(List.Transform(Table.ToRecords(Typed), each [conversions] > [assigned] or [visits] > [assigned] or Number.Abs([conversion_rate] - [conversions] / [assigned]) > 0.00000000001)) then error Error.Record("ExperimentIQ lineage error","Expected original verified three-arm 64000 cohort; refresh from audited reports.") else Typed
in
    Checked
