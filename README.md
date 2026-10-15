# ExperimentIQ — A/B Testing & Business Decision Intelligence

**Production-oriented portfolio code for analytics of the Hillstrom MineThatData Email Challenge**: reproducible processing, declarative SQL KPIs, randomized-inference decision engine, honest gross-spend impact analysis, a local interactive dashboard, Power BI authoring assets, and automated tests.

> **CURRENT BUILD STATUS — PARTIALLY COMPLETE / DATA BLOCKED (fixture-based tests pass; live PostgreSQL test skipped (see local run log)).** The initial execution sandbox had no outbound DNS/network to download Hillstrom CSV, no PostgreSQL/Docker server and no Windows Power BI Desktop. Therefore **no actual experimental findings, verified PostgreSQL integration or Power BI binary are claimed**. Synthetic fixture tests are exclusively unit tests, not real Hillstrom results. See `docs/FINAL_AUDIT.md`.

## Why this is more than a notebook

- Source immutable + fingerprinted; expected schema/64k row checks; row-preserving processing; processed CSV lineage manifest and SHA/row-level checks before database loads.
- Arm assignment kept in its original 3-category form; ITT conversions and spend divided by **all** assigned customers.
- SQL KPI/reporting views plus Python exact-denominator parity fixture tests; transaction-controlled replacement of the dedicated PostgreSQL table; actual database parity command provided.
- Pre-specified *two* primary conversion vs control tests, Holm multiplicity correction, Newcombe CIs, SRM alert, spend bootstrap sensitivity.
- Automated, evidence-gated recommendation: won't invent ROI, campaign spend or margin.
- Responsive, zero-CDN interactive browser dashboard with metric selection, confidence interval plot and customer-segment filters.
- Power BI DAX, M, JSON theme, and four-page report build instructions. No fake `.pbix`.

## Quick start (Python 3.10+, Internet-enabled machine)

```bash
git clone <YOUR-REPO-URL> ExperimentIQ
cd ExperimentIQ
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\\Scripts\\Activate.ps1
python -m pip install -e '.[dev,postgres]'
python -m experimentiq.cli acquire            # published-source attempt
# If original is offline, legally obtain a copy or: python -m experimentiq.cli acquire --mirror
python -m experimentiq.cli profile            # source and quality report to console
python -m experimentiq.cli all                # clean + KPI + statistics + memo + dashboard JSON
python -m pytest -q
python -m http.server 8000 -d dashboard       # open http://localhost:8000
```

**Existing raw file policy:** Acquisition refuses to overwrite. If you manually download, place the exact original source as `data/raw/hillstrom.csv`, then run `profile` and `all`. Manual source provenance will remain *unverified* unless you independently record/verify source metadata. No sample data are automatically substituted.

## Optional synthetic demonstration (NOT Hillstrom data)

```bash
python -m experimentiq.cli demo
python -m http.server 8000 -d dashboard
# Open http://localhost:8000/?demo=1
```

The synthetic output is deliberately separate from all real-data paths. It is generated only for testing the software/UI; simulated metrics **must never** be interpreted as real experimental results. See `data/synthetic/README.md`.

## Optional PostgreSQL integration

Docker Desktop/Engine + Compose required; the Git-tracked `.env.example` is a template only.

```bash
cp .env.example .env
# EDIT .env POSTGRES_PASSWORD; make DATABASE_URL use the SAME secret. Do NOT commit .env.
set -a; source .env; set +a           # bash/zsh only; PowerShell: set env vars manually
# Start database; Docker must be installed
# docker compose up -d postgres
python -m experimentiq.cli load-db     # uses transaction, staging, indexed table, views
python -m experimentiq.cli verify-db   # compares actual PostgreSQL vs Python KPI results
# Additional SQL via: psql "$DATABASE_URL" -f sql/003_quality_checks.sql
```

**Power BI Desktop**: follow [`powerbi/BUILD_GUIDE.md`](powerbi/BUILD_GUIDE.md) to create/verify the report from generated CSVs, import theme, Power Query and DAX. This build has **not** produced a PBIX artifact.

## Repository layout

```text
ExperimentIQ/
  src/experimentiq/   # extraction, validations, SQL load, KPIs, inference, memo, CLI
  sql/                # PostgreSQL DDL, reusable views, quality queries
  tests/              # synthetic fixture-only tests + SQLite SELECT parity
  dashboard/          # interactive local HTML/CSS/JS, data/ generated from real CSV
  powerbi/            # theme, M, DAX measures, build instructions
  docs/               # sources/licensing, data dictionary, KPIs, stats, architecture, audit
  data/raw/           # user-supplied source CSV ignored by Git
  data/processed/     # deterministic cleaned CSV ignored by Git
  reports/            # actual results (created when dataset available), status and audit
  .github/workflows/  # GitHub Actions continuous integration
  Dockerfile, docker-compose.yml, Makefile, pyproject.toml, .env.example
```

## CLI reference

| Command | Output / effect |
|---|---|
| `python -m experimentiq.cli acquire` | original source HTTPS attempt; fail closed |
| `... acquire --mirror` | opt-in unendorsed GitHub source; provenance labeled mirror |
| `... profile` | raw fingerprint + profiling and anomalous-outcome diagnostics |
| `... pipeline` | validated CSV in `data/processed/` |
| `... analyze` | validates processed vs raw content and exports inference + memo |
| `... all` | all offline local analysis steps and report assets |
| `... load-db` | load validated processed CSV into PostgreSQL with one commit |
| `... verify-db` | actual server-side KPI reconciliation vs Python |
| `... demo` | Generate labeled, reproducible synthetic CSV and isolated dashboard demo JSON |

See [`docs/RELEASE_HARDENING.md`](docs/RELEASE_HARDENING.md), [`docs/KPI_SPEC.md`](docs/KPI_SPEC.md) and [`docs/STATISTICAL_METHOD.md`](docs/STATISTICAL_METHOD.md) before interpreting any difference. If data license/provenance are disputed, remove generated external distributions. The MIT license applies to project code only.

## What is **not** claimed

Raw source dataset redistribution rights; a verified published-source checksum; actual conversion lift/p-values; campaign profit, causal open-rate impact or ROI; deployed production uptime; independently verified Docker/PG/PBIX within the original sandbox. These are documented and deliberately not fabricated.
