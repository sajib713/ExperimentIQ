let
    CsvPath = ProjectDirectory & "\\reports\\segment_kpis_actual.csv",
    Raw = Csv.Document(File.Contents(CsvPath), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Raw, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"dimension", type text}, {"value", type text}, {"assigned", Int64.Type}, {"conversions", Int64.Type}, {"visits", Int64.Type}, {"spend_total", type number}, {"conversion_rate", type number}, {"visit_rate", type number}, {"spend_per_assigned", type number}, {"segment", type text}}, "en-US"),
    Checked = if Table.RowCount(Typed) < 90 or List.AnyTrue(List.Transform(Table.ToRecords(Typed), each [assigned] <= 0 or [conversions] > [assigned] or [visits] > [assigned])) then error Error.Record("ExperimentIQ segments error","Missing or inconsistent exploratory cohort partitions.") else Typed
in
    Checked
