import dash
from dash import Input, Output, State, dcc, html, dash_table
import pandas as pd

#---
# 2. LAYOUT FUNCTIONS
#---

gh_button_style = {
    'backgroundColor': 'lightgrey',  
    'color': 'grey',
    'border': 'none',
    'borderRadius': '5px',
    'padding': '1px 20px',
    'fontSize': '16px',
    'cursor': 'pointer',
    'textDecoration': 'none',
    'marginLeft': '10px'  # Space between H5 and the button
}

def table_title(title, link):
    return html.Div([
        html.H5(title),
        html.A(
            html.Button('View Code', style=gh_button_style),
            href=link,  # Repository URL from the provided link
            target='_blank'
        ),
        html.A(
            html.Button('View File', style=gh_button_style),
            href=link,  # Repository URL from the provided link
            target='_blank'
        ),
    ], style={
        'display': 'flex',
        'alignItems': 'bottom',  # Vertically align the H5 and button
        'marginTop': '10px',
    })


def my_table(title,link,id,df):

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
        table_title(title, link),
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
    link_1 = 'https://github.com/zenon-test/Loyalty_Control/blob/main/data/level_1.csv'
    return html.Div(
            [
                my_table(title='Level 1', link=link_1, id='level-1-table', df=df_level_1),
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

df_level_1 = pd.read_excel('data/level_1.xlsx')
df_level_2 = pd.read_excel('data/partner_466/level_2.xlsx')
df_level_3 = pd.read_excel('data/partner_466/txn_29/level_3.xlsx')
df_level_4_60 = pd.read_excel('data/partner_466/txn_29/program_1565160/level_4.xlsx')
df_level_4_59 = pd.read_excel('data/partner_466/txn_29/program_1565159/level_4.xlsx')

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
            'link' : 'https://github.com/zenon-test/Loyalty_Control/blob/main/data/partner_466/level_2.csv',
            'df': df_level_2
        },
        '3': {
            'div': 'level-3-div',
            'table': 'level-3-table',
            'title': 'Level 3',
            'link' : 'https://github.com/zenon-test/Loyalty_Control/blob/main/data/partner_466/txn_29/level_3.csv',
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
                return my_table(title=out['title'], link=out['link'], id=out['table'], df=out['df'])
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
        link_0 = 'https://github.com/zenon-test/Loyalty_Control/blob/main/data/partner_466/txn_29/program_1565160/level_4.csv'
        link_1 = 'https://github.com/zenon-test/Loyalty_Control/blob/main/data/partner_466/txn_29/program_1565159/level_4.csv'

        if row == 0:
            return my_table(title='Program Code: 60', link=link_0, id='level-4-table-60', df=df_level_4_60)
        elif row == 1:
            return my_table(title='Program Code: 59', link=link_1, id='level-4-table-59', df=df_level_4_59)
    