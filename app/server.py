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



def load_and_split_data():
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

    # Drop OpenInt column if present
    if 'OpenInt' in df.columns:
        df = df.drop(columns=['OpenInt'])

    # Ensure Date column is datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Define timeframes
    splits = [
        ('1972-01-07', '1985-12-31'),
        ('1986-01-01', '1999-12-31'),
        ('2000-01-01', '2009-12-31'),
        ('2010-01-01', '2017-11-10'),
    ]
    dfs = []
    for start, end in splits:
        mask = (df['Date'] >= start) & (df['Date'] <= end)
        dfs.append(df.loc[mask].copy())
    return dfs


@app.route('/table/<int:split_id>')
def table_split(split_id):
    dfs = load_and_split_data()
    if not (1 <= split_id <= 4):
        abort(404, description='Invalid split index')
    df = dfs[split_id - 1]
    html = df.to_html(classes='dataframe table table-striped', index=False, escape=False)
    return Response(html, mimetype='text/html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
