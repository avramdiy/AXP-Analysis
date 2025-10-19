from flask import Flask, Response, abort
import pandas as pd
import os

app = Flask(__name__)


def get_data_path():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    candidate = os.path.join(root, 'axp.us.txt')
    if os.path.exists(candidate):
        return candidate
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

    try:
        whitespace_sep = r'\s+'
        for sep in [',', '\t', whitespace_sep]:
            try:
                df = pd.read_csv(path, sep=sep, engine='python')
                if df.shape[1] == 1 and sep != whitespace_sep:
                    continue
                break
            except Exception:
                df = None
        if df is None:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                lines = [line.rstrip('\n') for line in f]
            df = pd.DataFrame({'line': lines})
    except Exception as e:
        abort(500, description=f'Error reading data file: {e}')

    html = df.to_html(classes='dataframe table table-striped', index=False, escape=False)
    return Response(html, mimetype='text/html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
