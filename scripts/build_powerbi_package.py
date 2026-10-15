"""Deterministic aggregate-only Power BI Desktop rebuild archive; never a native PBIX."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import hashlib, json
ROOT=Path(__file__).resolve().parents[1]
SOURCE='27bab8c5d3669f26ec08ebb50a0a78317542f29501156f2e2af6781fab4cd7e2'
FILES=[
 'powerbi/desktop/ArmKPIs.pq','powerbi/desktop/Comparisons.pq',
 'powerbi/desktop/Segments.pq','powerbi/desktop/SourceMetadata.pq',
 'powerbi/desktop/measures_aggregate.dax','powerbi/desktop/VISUAL_BLUEPRINT.md',
 'powerbi/desktop/ProjectDirectory_PARAMETER.md','powerbi/BUILD_GUIDE.md',
 'powerbi/theme.json','reports/arm_kpis_actual.csv',
 'reports/control_comparisons_actual.csv','reports/segment_kpis_actual.csv',
 'reports/analysis_actual.json','reports/profile_actual.json',
 'reports/business_decision_memo_actual.md',
 'docs/REAL_DATA_VERIFICATION.md','docs/KPI_SPEC.md','docs/STATISTICAL_METHOD.md']
DEST=ROOT/'powerbi/ExperimentIQ-PowerBI-Rebuild.zip'
def add(z,name,data):
    meta=ZipInfo(name,date_time=(2026,10,15,0,0,0))
    meta.compress_type=ZIP_DEFLATED
    meta.external_attr=0o644<<16
    z.writestr(meta,data)
def main():
    missing=[p for p in FILES if not (ROOT/p).is_file()]
    if missing: raise RuntimeError('Refusing incomplete real-data archive; files missing: '+repr(missing))
    a=json.loads((ROOT/'reports/analysis_actual.json').read_text())
    profile=json.loads((ROOT/'reports/profile_actual.json').read_text())
    if a['n']!=64000 or profile['raw_sha256']!=SOURCE or sum(x['conversions'] for x in a['groups'].values())!=578:
        raise RuntimeError('Dataset fingerprint or analyzed arm totals mismatch')
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in FILES}
    manifest={'dataset':'Hillstrom 2008 third-party mirror','sha256_source':SOURCE,'sample':64000,
      'native_pbix':False,'desktop_visual_validation':False,'files_sha256':hashes}
    start='''ExperimentIQ Power BI Desktop rebuild package (NOT A PBIX).

1. Extract archive to C:\\ExperimentIQ-PowerBI.
2. In Windows Power BI Desktop make a blank report.
3. Set text parameter ProjectDirectory to extracted folder without trailing slash.
4. Follow powerbi/desktop/VISUAL_BLUEPRINT.md exactly.
5. Load 4 Power Query M files, create DAX measures, validate 3 arms/2 contrasts/93 segments.
6. Save and reopen ExperimentIQ.pbix ONLY in Power BI Desktop after verifying measures/slicers.

Contains only verified REAL aggregates: no row-level customers, synthetic demo or secret credentials.
Public-mirror source file cannot be cryptographically verified against publisher original.
'''
    with ZipFile(DEST,'w',ZIP_DEFLATED) as z:
        for path in sorted(FILES): add(z,path,(ROOT/path).read_bytes())
        add(z,'MANIFEST.json',(json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode())
        add(z,'START_HERE.txt',start.encode())
    with ZipFile(DEST) as z:
        assert len(z.namelist())==len(FILES)+2
        for path,expected in hashes.items():assert hashlib.sha256(z.read(path)).hexdigest()==expected
    print('REAL_AGGREGATES_POWERBI_ZIP_VERIFIED',DEST,DEST.stat().st_size,hashlib.sha256(DEST.read_bytes()).hexdigest())
if __name__=='__main__':main()
