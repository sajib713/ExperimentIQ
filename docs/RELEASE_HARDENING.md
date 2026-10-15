# Release hardening and data-lineage policy

## Revisions after first offline build

- **Single PostgreSQL transaction**: schema SQL must not issue `BEGIN` or `COMMIT` inside the loader's connection-managed transaction. The loader locks `experiment_customers`, loads into a temporary table, verifies staging row count, replaces rows, and creates views before the connection context commits. If any command errors, PostgreSQL rolls back the load. `psql` manual migrations should use `--single-transaction -v ON_ERROR_STOP=1`.
- **Raw/processed lineage**: pipeline writes an atomic processed CSV and an associated `experiment_customers.manifest.json` with SHA-256 fingerprints for both the raw CSV and cleaned output. Database load, database parity and the standalone `analyze` command verify the manifest, expected row count and recomputed row-by-row content. Stale or edited inputs are rejected before accessing the database.
- **Precise types**: PostgreSQL numeric amount columns use `NUMERIC(22,8)` rather than silently rounding to two decimal places. This preserves more source precision; exact precision still depends on raw CSV input. Actual derived monetary inputs and outputs are verified against CSV and Python.
- **Safe outputs**: `data/raw/*.json` and `data/processed/*.json` are Git-ignored, as are actual CSVs; the dataset has no explicit redistribution license.
- **Experiment assignment integrity**: the validator rejects missing treatment groups in addition to invalid treatment labels.

## Operational caveats

- A raw SHA-256 fingerprint is only an **integrity/lineage check**, not independent proof that a third-party mirror is authentic. A freshly processed, compromised dataset could still have internally consistent hashes. Record the author URL, acquisition evidence and ideally cross-source checksum comparison separately.
- PostgreSQL loader **replaces** the table contents and acquires an exclusive lock; run only on a dedicated ExperimentIQ database in an approved maintenance window, not against a shared production table. The integration test deliberately targets a disposable test database.
- In this environment no PostgreSQL server, Docker daemon or Power BI Desktop was available. Therefore the new atomicity and row-parity behavior was tested through fixture-level guards and code review, **not** a live PostgreSQL transaction. GitHub Actions will run the real database test once pushed to a repository with working CI.
- The synthetic fixtures used in tests do not represent actual Hillstrom outcomes. Actual dataset acquisition and real-business memo are currently blocked by outbound DNS failure.

## Verification steps

```bash
python -m pytest -q
python -m experimentiq.cli acquire
python -m experimentiq.cli all
# When PostgreSQL and a legitimate CSV are present:
docker compose up -d postgres
python -m experimentiq.cli load-db
python -m experimentiq.cli verify-db
```

If the CSV changes, explicitly rerun `python -m experimentiq.cli pipeline` then `analyze`; do not edit processed files or manifests by hand. A matched fingerprint alone is insufficient to call the pipeline production-verified: run database integration and compare actual results, then open Power BI Desktop to validate report interactions and numerical consistency.
