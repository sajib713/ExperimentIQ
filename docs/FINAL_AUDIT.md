# ExperimentIQ release audit — 15 October 2026

## Overall judgement

**PARTIALLY IMPLEMENTED, NOT ACCEPTANCE COMPLETE.** Local repository implementation, fixture-based tests, SQL/Python analytic code, dashboard UI and Power BI source assets are prepared. Actual dataset acquisition and consequent real-data analysis/decision memo are **BLOCKED** by no external DNS/network access. PostgreSQL, Docker and Power BI Desktop were unavailable. No source CSV, statistical p-value, screenshot of a populated real dashboard or `.pbix` is fabricated.

## Verified toolchain

- Python 3.13.5; pandas 2.2.3; NumPy 2.3.5; SciPy 1.17.0; statsmodels 0.14.6; pytest 9.0.2; Node.js 22.16.0; Git 2.47.3.
- PostgreSQL CLI/server: **NOT INSTALLED / NOT RUN**; Docker CLI: **NOT INSTALLED / NOT RUN**; Power BI Desktop: **NOT AVAILABLE** (Linux host).
- `python -m pytest -q` latest execution: **38 passed, 1 skipped** (the skip is live PostgreSQL integration because `TEST_DATABASE_URL` was not configured). Synthetic fixture tested the data pipeline, memo exporter, dashboard JSON, statistical formulas, SQL-derived relational views in SQLite and reproducibility. These are not actual Hillstrom experimental results.
- `node --check dashboard/app.js`: **exit 0 / syntax valid**, not a verified Chromium GUI acceptance test.
- `python -m experimentiq.cli acquire`: **exit 2** (`URLError`, DNS name resolution failure), no dataset acquired.
- `python -m experimentiq.cli profile`: **exit 2** (`FileNotFoundError` missing source CSV).
- `python -m experimentiq.cli all`: **exit 2** (`FileNotFoundError` missing source CSV).
- `scripts/verify_release.py` verifies checked-in structure and reports **presence** of deliverables; it does not substitute for runtime integrations.

## Acceptance checklist, requirement by requirement

| Requirement | State | Evidence / missing validation |
|---|---|---|
| Dataset publisher, source, schema and terms documented | COMPLETE (documentation) | `docs/DATA_SOURCES.md`, `docs/DATA_DICTIONARY.md` (rights unspecified) |
| Original CSV obtained and independently profiled | BLOCKED | Network DNS failure; no raw data in repo |
| Cleaning, validation, missing/duplicates checking | IMPLEMENTED / FIXTURE VERIFIED | `data.py`, test suite; real row statistics unavailable |
| Deterministic row-preserving pipeline | IMPLEMENTED / FIXTURE VERIFIED | SHA-256 fixture repeatability; 64k source not verified |
| PostgreSQL schema and transactional loader | IMPLEMENTED / UNVERIFIED ON POSTGRESQL | SQL/psycopg code and dedicated server integration test, skipped locally |
| Reusable SQL views, business KPIs and denominators | IMPLEMENTED / FIXTURE VERIFIED | SQLite relational view checks vs pandas; actual PostgreSQL parity pending |
| Randomized treatment / SRM / covariate balance | IMPLEMENTED / FIXTURE VERIFIED | `stats.py`, `balance.py`; actual SRM unavailable |
| Valid statistical tests, CIs and multiplicity | IMPLEMENTED / FIXTURE VERIFIED | scipy/statsmodels, 2-arm Holm correction, Newcombe intervals, Welch/bootstrap |
| Actual conversion lift, p-values, impact estimates | BLOCKED | No original CSV; no raw results invented |
| No unsupported ROI / profits | COMPLETE | ROI explicitly uncomputed; guardrails in report generator and docs |
| Dashboard interactive visuals and source code | IMPLEMENTED / STATIC VERIFIED | `dashboard/`; JS syntax checked; real-data population pending |
| Native Power BI `.pbix` / `.pbit` | NOT PRODUCED | Desktop unavailable; explicit M/DAX/theme/report blueprint shipped |
| Business memo with actual findings | BLOCKED | `report.py` implementation; `reports/STATUS.md` is honest blocker report |
| Automated test execution | COMPLETE (local fixture coverage) | pytest 38 passed, 1 skipped; test log included |
| Docker PostgreSQL run verified | BLOCKED | Docker unavailable |
| README, architecture, data dictionary, KPI, methodology | COMPLETE | `README.md`, docs files |
| Git local repository | COMPLETE | Locally initialized and committed; remote GitHub target authenticated, source push not completed |
| GitHub CI workflow | CONFIGURED / NOT RUN | `.github/workflows/ci.yml`; not pushed, so no Actions run |
| Real-data end-to-end execution | BLOCKED | Missing source CSV |
| SQL/Python results consistent on real data | NOT VERIFIED | `verify-db` requires PostgreSQL + source; fixture view parity passed |

## Synthetic demo for UI testing

`python -m experimentiq.cli demo` creates a clearly marked 900-row synthetic CSV and `dashboard/data/demo.json`, displayed only at `/?demo=1`. Neither output is used as the real Hillstrom source or its derived analysis. Synthetic demo outputs are **not real results**, and the dashboard makes this explicit. Four added tests verify deterministic generation, invalid inputs, source isolation and clear labeling. Local total: 38 passed, 1 PostgreSQL integration skipped.

## GitHub publication status

The private target is `sajib713/ExperimentIQ`. The authenticated `sajib713` GitHub integration can now read its metadata and sees an installed GitHub App with all-repository selection. An attempted `create_blob` on the entirely empty repository returned HTTP 409 (`Git Repository is empty`), not a successful write. Direct `git push` remains inaccessible from this execution container because DNS resolution of `github.com` fails. No publication is claimed until GitHub's remote commit and repository files are verified.

## Best next action

Obtain `hillstrom.csv` legally on an Internet-connected Windows/Linux machine, run `python -m experimentiq.cli all`, then Docker PostgreSQL integration, SQL parity, dashboard inspection, and Power BI Desktop verification. Record resulting source SHA and actual metrics before claiming this project as a completed analytical portfolio artifact.
