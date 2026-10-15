"""CLI is intentionally fail-closed when the 64k-row source is unavailable."""
import argparse
import json
import sys
from .config import RAW,PROCESSED,REPORTS,DASHBOARD_DATA
from .data import acquire,load_raw,run_pipeline,clean,verify_processed_input
from .report import export_results
from .database import load_postgres,verify_postgres

def main(argv=None):
    p=argparse.ArgumentParser(prog='experimentiq',description='Auditable Hillstrom experiment analytics')
    sp=p.add_subparsers(dest='cmd',required=True)
    a=sp.add_parser('acquire');a.add_argument('--mirror',action='store_true');a.add_argument('--source',default=None)
    sp.add_parser('profile');sp.add_parser('pipeline');sp.add_parser('analyze');sp.add_parser('all')
    sp.add_parser('load-db');sp.add_parser('verify-db')
    args=p.parse_args(argv)
    try:
        if args.cmd=='acquire': result=acquire(source=args.source,use_mirror=args.mirror)
        elif args.cmd=='profile':
            from .data import validate_raw,sha256
            raw=load_raw()
            result={'raw_sha256':sha256(RAW),'profile':validate_raw(raw)}
        elif args.cmd=='pipeline': result=run_pipeline()
        elif args.cmd=='analyze':
            if not PROCESSED.exists(): raise FileNotFoundError('Run pipeline after obtaining real dataset first')
            if not RAW.exists(): raise FileNotFoundError('Raw dataset required for results fingerprint')
            # Recheck raw and processed fingerprints before publishing inference.
            validation=verify_processed_input()
            res=export_results(validation);result={'n':res['n'],'memo':'reports/business_decision_memo_actual.md','dashboard':str(DASHBOARD_DATA)}
        elif args.cmd=='all':
            pipeline_result=run_pipeline()
            res=export_results(clean(load_raw()))
            REPORTS.mkdir(exist_ok=True,parents=True)
            (REPORTS/'profile_actual.json').write_text(json.dumps(pipeline_result,indent=2)+'\n',encoding='utf8')
            result={'pipeline':pipeline_result,'summary':res['groups'],'srm':res['srm'],
                    'memo':'reports/business_decision_memo_actual.md', 'dashboard':str(DASHBOARD_DATA)}
        elif args.cmd=='load-db': result=load_postgres()
        elif args.cmd=='verify-db': result=verify_postgres()
        print(json.dumps(result,indent=2,allow_nan=False))
        return 0
    except (ValueError,FileNotFoundError,RuntimeError,AssertionError,OSError) as err:
        print(f'FAILED ({type(err).__name__}): {err}',file=sys.stderr)
        return 2
if __name__=='__main__': sys.exit(main())
