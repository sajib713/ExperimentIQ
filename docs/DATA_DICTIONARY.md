# Data dictionary (Hillstrom published CSV)

| Column | Expected type | Description / timing |
|---|---|---|
| `recency` | integer 1–12 | Months since prior purchase, PRE-treatment |
| `history_segment` | category 1–7 | Previous 12-month spend band, PRE-treatment |
| `history` | nonnegative money | Previous 12-month spend, PRE-treatment |
| `mens` | binary 0/1 | Previously bought mens merchandise, PRE-treatment, **not** email assignment |
| `womens` | binary 0/1 | Previously bought womens merchandise, PRE-treatment, **not** email assignment |
| `zip_code` | class Urban/Surburban/Rural | Area classification, PRE-treatment; original spelling `Surburban` |
| `newbie` | binary 0/1 | New customer flag, PRE-treatment |
| `channel` | Web/Phone/Multichannel | Historical purchase channel, PRE-treatment |
| `segment` | Mens E-Mail / Womens E-Mail / No E-Mail | Randomly assigned **TREATMENT ARM** |
| `visit` | binary 0/1 | Visited during following two weeks, OUTCOME |
| `conversion` | binary 0/1 | Purchased during following two weeks, OUTCOME |
| `spend` | nonnegative money | Observed spend during following two weeks, OUTCOME; reported currency is USD in challenge commentary/usage |
| `source_row_number` | 1-based positive integer | Added by pipeline, position in original CSV, **not real source key** |

A `conversion=1` but `visit=0` combination or other apparent anomaly is profiled, not silently deleted: the data owner may have channel-specific rules; do not impose unjustified consistency constraints. Customer-level deduplication is impossible with the given fields.
