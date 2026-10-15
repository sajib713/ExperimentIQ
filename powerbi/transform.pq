// In Power BI Desktop, create a text parameter called ProjectDirectory, e.g. C:\work\ExperimentIQ
// Change ProjectDirectory when cloning the repo; never hard-code someone else's path.
let
    Source = Csv.Document(File.Contents(ProjectDirectory & "\data\processed\experiment_customers.csv"),
           [Delimiter=",", Columns=13, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {
      {"source_row_number", Int64.Type}, {"recency", Int64.Type}, {"history_segment", type text},
      {"history", type number}, {"mens", Int64.Type}, {"womens", Int64.Type},
      {"zip_code", type text}, {"newbie", Int64.Type}, {"channel", type text},
      {"segment", type text}, {"visit", Int64.Type}, {"conversion", Int64.Type},
      {"spend", type number}})
in Types
