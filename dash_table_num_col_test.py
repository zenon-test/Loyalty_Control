import dash
from dash import html, dash_table
from dash.dash_table.Format import Format, Group
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'Text Column': ['A', 'B', 'C'],
    'Number Column': [1000, 23000, 4560000]
})

# Dictionary to classify columns and set their format
numeric_cols = {
    'Number Column': Format(group=Group.yes)
}

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[
            {"name": col, "id": col, "type": "numeric", "format": numeric_cols[col]} if col in numeric_cols else {"name": col, "id": col}
            for col in df.columns
        ],
        data=df.to_dict('records'),
        style_data_conditional=[
            {
                'if': {'column_type': 'numeric'},
                'textAlign': 'right'  # Align right for numeric columns
            }
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
