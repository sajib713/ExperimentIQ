# Architecture & trust boundary

```mermaid
flowchart TD
  A[Publisher Hillstrom CSV] -->|HTTPS download or verified manual copy| B[data/raw/hillstrom.csv]
  B --> C[SHA-256 + strict validation + profiling]
  C -->|Reject errors| X[Stop / error / audit]
  C --> D[Deterministic cleaning, no deleted rows]
  D --> E[data/processed/experiment_customers.csv]
  E --> F[PostgreSQL transactional load]
  F --> G[SQL views and reconciliation]
  E --> H[Python analysis / statsmodels]
  H --> I[JSON, CSV metrics, memo]
  I --> J[Local browser dashboard]
  E --> K[Power BI Desktop authoring]
  I --> K
  F --> L[Compare SQL vs Python KPIs]
```

Design principles: raw source bytes immutable; generated `source_row_number` is **not** a real customer ID. Configuration via environment variables only. No database password in Git. All data-changing database operations are atomic. Primary inference is carried out by Python and is not re-estimated inside Power BI slicers.

**Trust boundaries:** Raw dataset is publicly described by its original author, but the license is unspecified. External sources should be treated as untrusted. The database is only bound to local host in Compose. No remote dashboard analytics and no external JavaScript CDN.
