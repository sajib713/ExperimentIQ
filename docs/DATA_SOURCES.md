# Dataset origin, acquisition, license, provenance

- **Original author:** Kevin Hillstrom / MineThatData, *The MineThatData E-Mail Analytics and Data Mining Challenge*, 20 March 2008.
- **Original announcement:** https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html
- **Original CSV:** https://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv
- **Third-party fallback mirror (not publisher; verify provenance):** https://raw.githubusercontent.com/W-Tran/uplift-modelling/master/data/hillstrom/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv
- **Independent catalog listing:** https://www.tensorflow.org/datasets/catalog/hillstrom

Author describes 64,000 customers, randomly assigned approximately 1:1:1 to mens merchandise email, womens merchandise email, and no-email holdout. Outcomes follow two weeks after assignment. No source customer ID or exact per-customer assignment timestamp is supplied.

## License and restrictions

The 2008 author invited public download and analysis for a challenge. **No explicit standard dataset redistribution license or warranty was identified during this implementation.** The published availability is NOT equivalent to CC0/MIT licensing. To avoid asserting rights we do not have, we **exclude the raw dataset from Git**. Obtain the data independently from the author or a legally usable mirror. Do not resell, republish, embed in a public Power BI report, or distribute data as licensed without checking terms/obtaining permission. Repository code is independently licensed MIT; that license **does not apply** to Hillstrom data.

## Acquire and verify

From repo root, using an Internet-enabled terminal:

```bash
python -m experimentiq.cli acquire
# if original fails, and terms/provenance are acceptable to you:
python -m experimentiq.cli acquire --mirror
# or download manually to data/raw/hillstrom.csv (do not rename any columns)
python -m experimentiq.cli profile
```

`acquire` downloads to a temporary `.download` file, checks all 12 column names, types, categories and **exact 64,000 rows**, then atomically renames to `data/raw/hillstrom.csv`; logs URL and SHA-256 to `data/raw/hillstrom.source.json`. It **never overwrites existing raw data**. After manual placement, `profile` generates SHA and validation output but source origin remains *unverified* if you have no acquisition manifest. A matching published row count alone is insufficient to verify provenance.

## Integrity and limitation

In the original local sandbox, DNS prevented dataset download. On 2026-10-15, **GitHub Actions successfully acquired a 64,000-row source from the documented third-party mirror**, validated it, and recorded SHA-256 `27bab8c5d3669f26ec08ebb50a0a78317542f29501156f2e2af6781fab4cd7e2`. Original publisher HTTPS download failed certificate verification in that environment. The checksum is a verifiable mirror-file fingerprint, NOT independently authenticated against the publisher. There is no approved publisher-supplied cryptographic SHA-256 reference available here to compare a third-party mirror with the original. Treat mirrors as unverified versions unless compared against the original.

Transformations applied **only after** full validation: assign a 1-based technical row number; change published misspelling `Surburban` to canonical `Suburban` in processed CSV. No deduplication, imputation, filtering, winsorization, post-treatment adjustment, row deletion or random splitting. Exact duplicates of features/outcomes cannot be assumed duplicate people in absence of a customer ID.
