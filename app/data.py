from flask import Flask, Response, abort
import pandas as pd
import os

app = Flask(__name__)


def get_data_path():
	"""Return absolute path to axp.us.txt located in project root.

	Assumes the project layout has the file at the repository root next to `app/`.
	"""
	root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
	candidate = os.path.join(root, 'axp.us.txt')
	if os.path.exists(candidate):
		return candidate
	# fallback: try current working directory
	candidate = os.path.join(os.getcwd(), 'axp.us.txt')
	if os.path.exists(candidate):
		return candidate
	return None


@app.route('/')
def index():
	return "AXP data API. Visit /table to view the data as an HTML table."


@app.route('/table')
def table():
	path = get_data_path()
	if not path:
		abort(404, description='axp.us.txt not found')

	# Try to read the text file as CSV-like. We'll try common delimiters.
	# If the file is a plain text log, show it as a single-column table.
	try:
		# Try comma first, then tab, then whitespace
		for sep in [',', '\t', r'\s+']:
			try:
				df = pd.read_csv(path, sep=sep, engine='python')
				# If dataframe has only one column but the separator wasn't whitespace,
				# try the next separator as it may have failed to split.
				if df.shape[1] == 1 and sep != '\s+':
					continue
				break
			except Exception:
				df = None
		if df is None:
			# As a fallback, read the file as plain text into one column
			with open(path, 'r', encoding='utf-8', errors='replace') as f:
				lines = [line.rstrip('\n') for line in f]
			df = pd.DataFrame({'line': lines})
	except Exception as e:
		abort(500, description=f'Error reading data file: {e}')

	html = df.to_html(classes='dataframe table table-striped', index=False, escape=False)
	return Response(html, mimetype='text/html')


if __name__ == '__main__':
	# For local development only. Use gunicorn/uvicorn for production.
	app.run(debug=True, host='127.0.0.1', port=5000)

