let
 Raw = Json.Document(File.Contents(ProjectDirectory & "\\reports\\analysis_actual.json")),
 Check = if Raw[n] <> 64000 or Record.Field(Record.Field(Raw, "groups"), "No E-Mail")[assigned] <> 21306 then error Error.Record("ExperimentIQ source mismatch","Full verified sample missing.") else
 #table(type table [record_type = text, value = text], {
 {"sample", "64000 Hillstrom 2008 randomized assignments"},
 {"window", "2 weeks"},
 {"source", "Third-party public mirror, no publisher-provided checksum"},
 {"raw_sha256", "27bab8c5d3669f26ec08ebb50a0a78317542f29501156f2e2af6781fab4cd7e2"},
 {"inference", "Full cohort; p-values do not respond to exploratory slicers"},
 {"business_limit", "No email send cost, contribution margin, or ROI"}
 })
in
 Check
