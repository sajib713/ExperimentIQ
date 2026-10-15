# Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `FileNotFoundError: Dataset is absent` | Obtain original CSV using `acquire` in an Internet-enabled environment; do not substitute test fixture |
| `ConnectionError / DNS` on acquire | Environment has outbound network restrictions; download manually from cited author/mirror after rights check |
| Raw rows != 64,000 | Wrong/incomplete file. Guard intentionally stops analysis; inspect CSV rather than dropping records |
| Missing/unknown raw column | Dataset revision/mirror may have changed; compare source and schema before editing code |
| `Surburban` appears in raw | Expected in published CSV; only processed output canonicalizes to `Suburban` |
| Existing raw file not overwritten | Intentional immutable source protection. Back up/remove file manually after independent review |
| `DATABASE_URL required` | Supply connection string via `.env` and shell export (`set -a; source .env; set +a`) |
| No `psycopg` installed | Install `pip install ".[postgres]"` in online development environment |
| PostgreSQL connection refused | Docker must be installed and running; `docker compose up -d postgres`; wait healthcheck |
| PostgreSQL SQL syntax differs from SQLite | Expected. SQLite is only lightweight fixture parity; test actual Postgres separately |
| Power BI file missing | No Windows Power BI Desktop in environment. Complete `powerbi/BUILD_GUIDE.md` manually |
| Blank browser dashboard | Expected until `all` creates `dashboard/data/report.json`; run local HTTP server (file:// blocks fetch) |
| Dashboard Power BI KPI disagreement | Verify local filters, whether outcomes were used as filters, currency formatting, denominator and source SHA |
| GitHub remote absent | Add your own repository with `git remote add origin ...` and push only after review; don't commit restricted data or `.env` |
