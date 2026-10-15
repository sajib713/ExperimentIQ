from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW = PROJECT_ROOT / 'data/raw/hillstrom.csv'
PROCESSED = PROJECT_ROOT / 'data/processed/experiment_customers.csv'
REPORTS = PROJECT_ROOT / 'reports'
DASHBOARD_DATA = PROJECT_ROOT / 'dashboard/data/report.json'
ORIGINAL_URL = ('https://www.minethatdata.com/'
    'Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv')
PUBLIC_MIRROR = ('https://raw.githubusercontent.com/W-Tran/uplift-modelling/master/'
    'data/hillstrom/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv')
ARMS = ('No E-Mail', 'Mens E-Mail', 'Womens E-Mail')
INPUT_COLUMNS = ('recency', 'history_segment', 'history', 'mens', 'womens',
                 'zip_code', 'newbie', 'channel', 'segment', 'visit',
                 'conversion', 'spend')
ZIP_CLASSES = ('Urban', 'Surburban', 'Suburban', 'Rural')
CHANNELS = ('Web', 'Phone', 'Multichannel')
