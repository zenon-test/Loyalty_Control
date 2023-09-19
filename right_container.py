import dash
from dash import Input, Output, State, dcc, html, dash_table
import pandas as pd

#---
# 2. LAYOUT FUNCTIONS
#---

def my_table(title,id,df):

    style_header={
        'text-align': 'center',
        'backgroundColor': '#FFA500',  # Orange background
        'color': 'white',  # White font color
        'fontWeight': 'bold',  # Bold font weight
    }  # Center-align the column headers

    style_data={
        'text-align': 'left'
    }  # Center-align the text in cells

    style_cell={
        'fontFamily': 'Arial, sans-serif',  # Set the font family
        'fontSize': '14px',  # Set the font size
        'whiteSpace': 'pre-line', # new line, wrap
    }

    style_data_conditional_fail = [
        {
            'if': {'row_index': 2, 'column_id': 'Monitoring'},  # Specify the target cell
            'color': 'red',  # Apply the bold font weight
            'fontWeight': 'bold'
        },
        {
            'if': {'row_index': 2},  
            'backgroundColor': 'yellow'  # Set the background color to yellow
        },
    ]

    tooltip_header = {col: {'value': col, 'use_with': 'header'} for col in df.columns}

    return html.Div([
        dcc.Store(id='selected-cell'),
        html.H5(title),
        dash_table.DataTable(
            id=id,
            data=df.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in df.columns],
            style_header=style_header,
            style_data=style_data,
            style_cell=style_cell,
            fixed_rows={'headers': True}, # set this will limit table max height
            style_table={'height': '100%'}, #'overflowY': 'auto'
            style_data_conditional=style_data_conditional_fail,
            tooltip_header=tooltip_header,
            # This is necessary to enable tooltips
            tooltip_delay=0,
            tooltip_duration=None
        ),
    ]
    )


def right_container_layout():
    return html.Div(
            [
                my_table(title='Level 1', id='level-1-table', df=df_level_1),
                html.Div(id='level-2-div'),
                html.Div(id='level-3-div'),
                html.Div(id='level-4-div'),
            ],
            style={
                "height": "calc(100vh - 60px)",
                'overflow-y': 'auto'    # Enable vertical scrolling when content overflows
                },
            id='right_container',
        )

#---
# 4. Create Data
#---

df_level_1 = pd.read_excel('data/Top_Level.xlsx')
df_level_2 = pd.read_excel('data/Prin_0466.xlsx')
df_level_3 = pd.read_excel('data/tran_prog.xlsx')
df_level_4_60 = pd.read_excel('data/df_dl_1565160_.xlsx')
df_level_4_59 = pd.read_excel('data/df_dl_1565159_.xlsx')

#---
# 5. Create Layout
#---


#---
# 6. Register Callbacks (used in main.py)
#---
def register_drilldown_callbacks(app):

    level_dict = {
        '2': {
            'div': 'level-2-div',
            'table': 'level-2-table',
            'title': 'Level 2',
            'df': df_level_2
        },
        '3': {
            'div': 'level-3-div',
            'table': 'level-3-table',
            'title': 'Level 3',
            'df': df_level_3
        }
        # Add more levels here as needed
    }
    # func
    def show_next_level_callback(in_table, out):
        @app.callback(
            Output(out['div'], 'children'),
            Input(in_table, 'selected_cells'),
            State(in_table, 'data')
            )
        def display_next_level(selected_cells, data):
            if selected_cells:
                return my_table(title=out['title'], id=out['table'], df=out['df'])
            return ''
    
    show_next_level_callback(in_table='level-1-table', out=level_dict['2'])
    show_next_level_callback(in_table='level-2-table', out=level_dict['3'])

    @app.callback(
        Output('level-4-div', 'children'),
        Input('level-3-table', 'selected_cells')
    )
    def display_selected_table(selected_cells):
        if not selected_cells:
            return ''

        row = selected_cells[0]['row']

        if row == 0:
            return my_table(title='Program Code: 60', id='level-4-table-60', df=df_level_4_60)
        elif row == 1:
            return my_table(title='Program Code: 59', id='level-4-table-59', df=df_level_4_59)
    