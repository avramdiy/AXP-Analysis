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

- Dropped the "OpenInt" column from the dataset for clarity and relevance (it was always zero and not useful for analysis).
- Split the data into 4 separate dataframes by timeframe:
	1. 1972-01-07 to 1985-12-31
	2. 1986-01-01 to 1999-12-31
	3. 2000-01-01 to 2009-12-31
	4. 2010-01-01 to 2017-11-10
- Each split is served at `/table/1`, `/table/2`, `/table/3`, and `/table/4` for focused inspection.

**Reasoning:**
- Splitting by timeframes enables targeted analysis of macro trends, market cycles, and company evolution across distinct periods (e.g., pre-1986, late 20th century, early 21st century, and post-2010).
- This approach helps highlight changes in trading volume, price behavior, and external events (such as regulatory shifts or financial crises) that may have impacted American Express differently in each era.

### 3rd Commit

- Added a Flask route `/volume_chart` that visualizes a bar chart of the average monthly volume for each of the four timeframes (splits).
- The chart is generated using matplotlib and returned as a PNG image for quick visual comparison.
- This helps users spot differences in trading activity across eras, identify periods of higher/lower liquidity, and contextualize macro trends in American Express stock volume.

### 4th Commit

### 5th Commit