# ExperimentIQ — A/B Testing & Business Decision Intelligence

**Production-oriented portfolio code for analytics of the Hillstrom MineThatData Email Challenge**: reproducible processing, declarative SQL KPIs, randomized-inference decision engine, honest gross-spend impact analysis, a local interactive dashboard, Power BI authoring assets, and automated tests.

> **REAL-DATA ANALYSIS VERIFIED (2026-10-15):** 64,000 Hillstrom records from a documented public mirror; actual conversion, visits, spend, confidence intervals, Holm-adjusted p-values and guarded business memo generated. GitHub Actions on Python 3.12 + PostgreSQL 16: **39 passed**, including live SQL/Python parity for all 3 arms. Original publisher HTTPS failed certificate verification; mirror SHA-256 is recorded, but publisher-original identity is not independently certified. The source CSV and customer-level processed rows remain Git-excluded. **No native Power BI .pbix exists** (Windows Desktop unavailable); a verified aggregate-only rebuild ZIP and Chromium dashboard screenshot now exist. This is a verified historical analysis, NOT a deployed production service. See `docs/REAL_DATA_VERIFICATION.md` and `docs/FINAL_AUDIT.md`.

## Portfolio-ready real-data dashboard and Power BI rebuild package (15 October 2026)

![Chromium browser-verified real Hillstrom dashboard](docs/images/dashboard-real.png)

The screenshot above is from the **64,000-record actual-data report**, not the 900-record synthetic fixture. [Browser E2E source](scripts/verify_dashboard.py) checks exact control/treatment cards, 578 conversions, $67,258.13 gross spend, Holm-adjusted p, 95% CI, interactive treatment change, confidence chart and segments. An opt-in synthetic demo is generated **only for isolation testing** and is never included in the actual report.

- [View interactive HTML dashboard source](dashboard/index.html), [real report JSON](dashboard/data/report.json), [actual screenshot](docs/images/dashboard-real.png).
- [Download complete Power BI Desktop rebuild ZIP](powerbi/ExperimentIQ-PowerBI-Rebuild.zip): 20 files (typed M imports, DAX, visual blueprint, data CSV/analysis/memo, source provenance, manifest). **This is a reproducible authoring archive, NOT a PBIX file.**
- [Power BI four-page visual and validation blueprint](powerbi/desktop/VISUAL_BLUEPRINT.md), [DAX measures](powerbi/desktop/measures_aggregate.dax), [source-guarded Power Query M](powerbi/desktop/ArmKPIs.pq).
- [Portfolio demonstration guide](docs/PORTFOLIO_SHOWCASE.md).
- **Native PBIX remains unavailable:** the Linux runner cannot run Windows Power BI Desktop or certify PBIX authoring. The generated Power Query/DAX *source* has not been compiled in Power BI Desktop, so manually authoring, opening and visually checking a native PBIX on Windows is explicitly unfinished.
- Keep all source, screenshots, archive and tests in this repository's `master` branch; `main` remains the preserved bootstrap branch.

### Quick dashboard preview (using committed verified aggregates)

```bash
git clone --branch master https://github.com/sajib713/ExperimentIQ.git
cd ExperimentIQ
python -m http.server 8000 -d dashboard
# Visit http://localhost:8000
```

**Source path** `dashboard/data/report.json` is committed with verified actual results; no raw customer data is required merely to preview this report. To refresh the underlying analysis instead, follow the earlier Python acquisition/pipeline and PostgreSQL instructions. To rebuild on Windows, extract `powerbi/ExperimentIQ-PowerBI-Rebuild.zip` and follow `powerbi/desktop/VISUAL_BLUEPRINT.md`. Historical mirror SHA-256 remains fixed in `docs/REAL_DATA_VERIFICATION.md`.

## Verified real-data results (source: public Hillstrom mirror)

Run on GitHub Actions: **2026-10-15**, [real-data analysis workflow](https://github.com/sajib713/ExperimentIQ/actions), exact CSV SHA-256: `27bab8c5d3669f26ec08ebb50a0a78317542f29501156f2e2af6781fab4cd7e2`. Sample = 64,000 randomized customer assignments, **not synthetic**. Source publisher described the experiment, but no original publisher-provided checksum exists to independently certify the third-party mirror.

| Arm | Assigned | Conversions | Conversion rate | Visits | 2-week observed gross spend (USD) |
|---|---:|---:|---:|---:|---:|
| No E-Mail (control) | 21,306 | 122 | 0.5726% | 2,262 | 13,908.33 |
| Mens E-Mail | 21,307 | 267 | 1.2531% | 3,894 | 30,311.69 |
| Womens E-Mail | 21,387 | 189 | 0.8837% | 3,238 | 23,038.11 |

- **Mens vs control:** +0.6805 percentage points (unadjusted Newcombe 95% CI +0.5014 to +0.8641 pp); Holm-adjusted p = 3.05e-13.
- **Womens vs control:** +0.3111 percentage points (unadjusted Newcombe 95% CI +0.1502 to +0.4745 pp); Holm-adjusted p = 1.57e-4.
- **SRM diagnostic:** chi-square 0.2025, p = 0.9037 (threshold 0.001, not flagged).
- **Observed spend/customer uplift:** Mens +$0.7698 (bootstrap 95% CI +$0.4813 to +$1.0533), Womens +$0.4244 (CI +$0.1710 to +$0.6930). These are **gross-spend differences, not profit/ROI**.
- **Decision:** Mens E-Mail has the larger statistically supported conversion gain. Recommend a monitored, gated follow-up rollout/test, subject to delivery, marginal cost, contribution margin and unsubscribe information. Do not extrapolate a profit claim.
- **Actual deliverables:** [memo](reports/business_decision_memo_actual.md), [analysis JSON](reports/analysis_actual.json), [arm KPIs](reports/arm_kpis_actual.csv), [treatment contrasts](reports/control_comparisons_actual.csv), [profiling](reports/profile_actual.json), [real dashboard JSON](dashboard/data/report.json). Real summaries are separate from `data/synthetic/` and `dashboard/data/demo.json`.

**Branch note:** `master` contains the complete six-commit original project history plus verified releases; GitHub's separately preserved `main` branch is a bootstrap/transfer branch. Clone `--branch master` as above, not the default `main`.

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
git clone --branch master https://github.com/sajib713/ExperimentIQ.git ExperimentIQ
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
docker compose up -d postgres
python -m experimentiq.cli load-db     # uses transaction, staging, indexed table, views
python -m experimentiq.cli verify-db   # compares actual PostgreSQL vs Python KPI results
# Additional SQL via: psql "$DATABASE_URL" -f sql/003_quality_checks.sql
```

**Power BI Desktop**: The complete report has NOT been authored or visually validated as a `.pbix`. For a reproducible native report, follow [`powerbi/BUILD_GUIDE.md`](powerbi/BUILD_GUIDE.md) to create/verify the report from generated CSVs, import theme, Power Query and DAX. This build has **not** produced a PBIX artifact.

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

Raw source dataset redistribution rights; a publisher-confirmed CSV checksum or mirror authenticity; campaign profit, causal open-rate effect or ROI; long-term transportability; deployed production uptime; a native or user-validated Power BI report. GitHub Actions *did* verify temporary PostgreSQL 16 parity and 39 tests. These are documented and deliberately not fabricated.
