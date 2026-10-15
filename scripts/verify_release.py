"""Read-only QA manifest. Does not fake successful integration or live data outputs."""
import json
import os
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CORE=['README.md','LICENSE','pyproject.toml','Dockerfile','docker-compose.yml','.env.example',
'rs', 'src/experimentiq/data.py','src/experimentiq/stats.py','src/experimentiq/business.py',
'src/experimentiq/database.py','src/experimentiq/report.py','src/experimentiq/cli.py',
'sql/001_schema.sql','sql/002_views.sql','sql/003_quality_checks.sql','dashboard/index.html',
'dashboard/app.js','dashboard/style.css','powerbi/theme.json','powerbi/measures.dax',
'powerbi/transform.pq','powerbi/BUILD_GUIDE.md','docs/ARCHITECTURE.md',
'docs/DATA_SOURCES.md','docs/DATA_DICTIONARY.md','docs/KPI_SPEC.md','docs/STATISTICAL_METHOD.md',
'docs/TROUBLESHOOTING.md','.github/workflows/ci.yml']
CORE=[x for x in CORE if x!='rs']
report={'core_files':{'found':[x for x in CORE if (ROOT/x).is_file()],
                     'missing':[x for x in CORE if not (ROOT/x).is_file()]},
        'raw_dataset_present':(ROOT/'data/raw/hillstrom.csv').exists(),
        'processed_dataset_present':(ROOT/'data/processed/experiment_customers.csv').exists(),
        'real_analysis_present':(ROOT/'reports/analysis_actual.json').exists(),
        'real_memo_present':(ROOT/'reports/business_decision_memo_actual.md').exists(),
        'real_dashboard_data_present':(ROOT/'dashboard/data/report.json').exists(),
        'power_bi_binary_present':any((ROOT/'powerbi').glob('*.pbix')),
        'postgres_cli_present':shutil.which('psql') is not None,
        'docker_cli_present':shutil.which('docker') is not None,
        'git_cli_present':shutil.which('git') is not None,
        'env_file_present_untracked_ignored':(ROOT/'.env').exists(),
        'disclosure':'Presence of a file is NOT evidence of its validity; run tests and actual integration parity.'}
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'reports/release_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if report['core_files']['missing']:
    raise SystemExit(1)
