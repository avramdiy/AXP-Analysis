from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:5000/table"
OUT = "app/table.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1400, "height": 1000})
    page.goto(URL)
    page.wait_for_load_state("networkidle")
    page.screenshot(path=OUT, full_page=True)
    browser.close()
    print(f"Saved screenshot to {OUT}")
