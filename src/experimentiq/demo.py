"""Opt-in SYNTHETIC example only, entirely isolated from real Hillstrom processing."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from .config import ARMS, INPUT_COLUMNS, PROJECT_ROOT
from .data import validate_raw, sha256
from .business import subgroup_rows
from .stats import analyze

DEMO_CSV = PROJECT_ROOT / 'data/synthetic/demo_customers.csv'
DEMO_JSON = PROJECT_ROOT / 'dashboard/data/demo.json'


def make_synthetic(seed: int = 20261015, rows_per_arm: int = 300) -> pd.DataFrame:
    """Fabricated customer records for exercising code, NEVER real experiment evidence."""
    if isinstance(rows_per_arm, bool) or not isinstance(rows_per_arm, int) or rows_per_arm < 20:
        raise ValueError('rows_per_arm must be an integer >= 20')
    rng = np.random.default_rng(seed)
    n = 3 * rows_per_arm
    arm = np.repeat(ARMS, rows_per_arm)
    arm = arm[rng.permutation(n)]
    recency = rng.integers(1, 13, n)
    history = np.round(rng.lognormal(mean=4.2, sigma=0.85, size=n), 2)
    purchase_prob = np.clip(0.055 + (arm == 'Mens E-Mail') * .015 + (arm == 'Womens E-Mail') * .01, 0, 1)
    conversion = (rng.random(n) < purchase_prob).astype(int)
    visit = np.maximum(conversion, (rng.random(n) < .20).astype(int))
    spend = np.where(conversion, np.round(rng.gamma(shape=2.5, scale=30, size=n), 2), 0.)
    hist_bins = np.digitize(history, [100, 200, 350, 500, 750, 1000]) + 1
    hist_names = [f'{i}) Synthetic history band {i}' for i in hist_bins]
    frame = pd.DataFrame({
        'recency': recency, 'history_segment': hist_names, 'history': history,
        'mens': rng.binomial(1, .48, n), 'womens': rng.binomial(1, .42, n),
        'zip_code': rng.choice(['Urban', 'Surburban', 'Rural'], n),
        'newbie': rng.binomial(1, .27, n),
        'channel': rng.choice(['Web', 'Phone', 'Multichannel'], n),
        'segment': arm, 'visit': visit, 'conversion': conversion, 'spend': spend,
    })
    frame = frame[list(INPUT_COLUMNS)]
    validate_raw(frame, expected_rows=None)
    return frame


def make_demo(csv_path: Path = DEMO_CSV, json_path: Path = DEMO_JSON) -> dict:
    """Generate obvious demo assets; NEVER write to raw/hillstrom.csv or report.json."""
    csv_path, json_path = Path(csv_path), Path(json_path)
    from .config import RAW, PROCESSED, DASHBOARD_DATA
    protected = {x.resolve() for x in (RAW, PROCESSED, DASHBOARD_DATA)}
    if csv_path.resolve() in protected or json_path.resolve() in protected or csv_path.resolve() == json_path.resolve():
        raise ValueError('Demo output must not overwrite real-data files or each other')
    df = make_synthetic()
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    result = analyze(df, bootstrap_iterations=150)
    output = {
        'metadata': {'kind': 'SYNTHETIC_DEMO_ONLY', 'source_sha256': sha256(csv_path),
                     'observed_sample': len(df),
                     'warning': 'FABRICATED TEST DATA. NOT Hillstrom. NO real business decisions or causal claims.'},
        'analysis': result, 'segments': subgroup_rows(df),
        'recommendation': 'SYNTHETIC DEMO ONLY — do not use these invented metrics for business decisions.',
    }
    json_path.write_text(json.dumps(output, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    return {'synthetic_rows': len(df), 'csv': str(csv_path), 'dashboard_data': str(json_path),
            'kind': 'SYNTHETIC_DEMO_ONLY'}
