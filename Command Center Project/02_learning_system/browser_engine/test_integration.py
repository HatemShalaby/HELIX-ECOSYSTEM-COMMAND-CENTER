import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from path_config import RECORDS_DIR

OUTPUT_FILE = RECORDS_DIR / "engine_test_status.md"

def run_test():
    RECORDS_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Targeting directory: {RECORDS_DIR}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.google.com")
        title = page.title()
        browser.close()

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"# Engine Test Successful\n- Status: Browser engine connected.\n- Test: Retrieved title '{title}'")
        
        print(f"SUCCESS: Record saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    run_test()