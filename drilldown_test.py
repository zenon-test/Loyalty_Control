import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd

app = dash.Dash(__name__)
server = app.server

# 1. Data Func

# 2. Layout Func
def top_level_table_layout():
    return dash_table.DataTable(
            id='top-level-table',
            columns=[{"name": i, "id": i} for i in df_top_level.columns],
            data=df_top_level.to_dict('records'),
            row_selectable='single'
        )

# 3. Callback Func

# 4. Create Data
# Sample DataFrames for demo
df_top_level = pd.DataFrame({'prin': range(1, 6)})
df_level_2 = pd.DataFrame({'prin': [1, 1, 2, 2, 3], 'txn_id': range(1, 6)})
df_level_3 = pd.DataFrame({'txn_id': [1, 2, 3, 3, 4], 'program_cd': list('ABCDE')})
df_level_4 = pd.DataFrame({'txn_id': [1, 2, 3, 4, 4], 'program_cd': list('ABCDE'), 'info': list('ijklm')})

# 5. Create Layout
app.layout = html.Div([
    top_level_table_layout(),
    html.Div(id='level-2-div'),
    html.Div(id='level-3-div'),
    html.Div(id='level-4-div')
])

# 6. Register Callback
@app.callback(
    Output('level-2-div', 'children'),
    Input('top-level-table', 'selected_rows'),
    State('top-level-table', 'data')
)
def display_level_2(selected_rows, data):
    if selected_rows:
        prin_selected = data[selected_rows[0]]['prin']
        df_filtered = df_level_2[df_level_2['prin'] == prin_selected]
        return dash_table.DataTable(
            id='level-2-table',
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            data=df_filtered.to_dict('records'),
            row_selectable='single'
        )
    return ''

# 7. Run App
if __name__ == '__main__':
    app.run_server(debug=True)
