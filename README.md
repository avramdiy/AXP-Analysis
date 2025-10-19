# TRG Week 46

## $AXP (American Express Company)

- Global financial-services firm best known for issuing consumer and commercial charge/credit cards, processing merchant payments, and providing travel and expense-management services. 

- https://www.kaggle.com/borismarjanovic/datasets

### 1st Commit

- Implemented a small Flask data inspection tool and supporting artifacts:
	- Added a clean server entrypoint `app/server.py` (Flask) that locates `axp.us.txt`, parses it (tries CSV, TSV, or whitespace), and serves an HTML table at `/table`.
	- Saved the rendered HTML table to `app/table.html` (full dataset exported from the running server).
	- Created `app/screenshot.py` (Playwright-based) to capture a PNG of `/table` (note: Playwright was added but running it in this environment hung; instructions to run locally are below).
	- Fixed parsing/escape issues and improved path resolution for robust local runs.

	Quick notes on running locally:

	- Install deps: `pip install flask pandas` and, if you want to use the screenshot tool, `pip install playwright` then `python -m playwright install chromium`.
	- Start server: `python .\app\server.py` and visit `http://127.0.0.1:5000/table` or open `app/table.html` directly.
	- Run screenshot (optional): `python .\app\screenshot.py` (after installing Playwright and browsers).

### 2nd Commit

### 3rd Commit

### 4th Commit

### 5th Commit