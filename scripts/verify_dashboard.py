"""Real-only Chromium E2E & reproducible screenshot. No test fixtures in the actual-data view."""
from __future__ import annotations
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
if __name__ == '__main__':
    report=ROOT/'dashboard/data/report.json'
    assert report.is_file(), 'Real report JSON required: never screenshot synthetic demo as real'
    handler=partial(SimpleHTTPRequestHandler,directory=str(ROOT/'dashboard'))
    server=ThreadingHTTPServer(('127.0.0.1',0), handler)
    Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as engine:
            browser=engine.chromium.launch(headless=True,args=['--no-sandbox'])
            page=browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
            root_url=f'http://127.0.0.1:{server.server_port}/'
            page.goto(root_url,wait_until='networkidle')
            page.locator('#status.ready').wait_for(timeout=20000)
            assert 'Observed data' in page.locator('#status').inner_text()
            assert page.locator('#assigned').inner_text() == '64,000'
            assert page.locator('#conversions').inner_text() == '578'
            assert page.locator('#spend').inner_text() == '$67,258.13'
            assert page.locator('#detailAbs').inner_text() == '+0.681 pp'
            assert page.locator('#detailRelative').inner_text() == '+118.842%'
            assert page.locator('#detailP').inner_text() == '3.05e-13'
            assert page.locator('#detailCI').inner_text().startswith('95% CI: [+0.501, +0.864]')
            page.locator('#treatmentSelect').select_option('Womens E-Mail')
            assert page.locator('#detailAbs').inner_text() == '+0.311 pp'
            assert page.locator('#detailP').inner_text() == '0.000157'
            assert page.locator('#detailVisit').inner_text() == '+4.523 pp'
            page.locator('#treatmentSelect').select_option('Mens E-Mail')
            page.locator('#metric').select_option('visit_rate')
            assert '18.28%' in page.locator('#performanceChart').inner_text()
            page.locator('#metric').select_option('conversion_rate')
            assert page.locator('#segmentTable table').count() == 1
            assert page.locator('#confidenceChart svg').count() == 1
            assert 'SYNTHETIC' not in page.locator('#data-notice').inner_text()
            screenshot=ROOT/'docs/images/dashboard-real.png'
            screenshot.parent.mkdir(parents=True,exist_ok=True)
            page.screenshot(path=str(screenshot),full_page=True,animations='disabled')
            print('REAL_BROWSER_VERIFIED: 64000 assignments, 578 conversions, $67258.13 spend, 2 treatment selections, CI, p, visits and segments; screenshot:',screenshot)
            page.goto(root_url+'?demo=1',wait_until='networkidle')
            assert 'SYNTHETIC DEMO' in page.locator('#data-notice').inner_text()
            assert 'SYNTHETIC DEMO' in page.locator('#status').inner_text()
            print('SYNTHETIC_ISOLATION_VERIFIED')
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
