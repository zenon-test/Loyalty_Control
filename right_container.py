import dash
from dash import Input, Output, State, dcc, html, dash_table
from dash.dash_table.Format import Format, Scheme, Symbol, Group
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
    'fontSize': '14px',
    'cursor': 'pointer',
    'textDecoration': 'none',
    'marginLeft': '10px'  # Space between H5 and the button
}

def table_title(title, link_c, link_d):
    return html.Div([
        html.H5(title),
        html.A(
            html.Button('View Code', style=gh_button_style),
            href=link_c,  # Repository URL from the provided link
            target='_blank'
        ),
        html.A(
            html.Button('View File', style=gh_button_style),
            href=link_d,  # Repository URL from the provided link
            target='_blank'
        ),
    ], style={
        'display': 'flex',
        'alignItems': 'bottom',  # Vertically align the H5 and button
        'marginTop': '20px',
    })

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

lightred = 'rgba(240, 128, 128, 0.3)'
lightgreen = 'rgba(144, 238, 144, 0.3)'

comma_fmt = Format(group=Group.yes)
pct_fmt = {
    "specifier": "$,",
    "locale": {"symbol": ["", "%"]},
}

numeric_cols = {
    'Transaction Amount': comma_fmt,
    'Actual Points Awarded': comma_fmt,
    'Expected Points': comma_fmt,
    'Difference': comma_fmt,
    'Leakage': comma_fmt,
    'transactionAmount': comma_fmt,
    'expected_points': comma_fmt,
    'actual_points': comma_fmt,
    '% Difference': pct_fmt,
}

def num_align_right():
    return [{
        'if': {'column_id': col},
        'textAlign': 'right',
    } for col in numeric_cols]

style_cond_level_1 = [
    {
        'if': {'row_index': 2, 'column_id': 'Monitoring'},  # Specify the target cell
        'color': 'red',  # Apply the bold font weight
        'fontWeight': 'bold',
    },
    {
        'if': {'row_index': 2},  
        'backgroundColor': lightred,
    },
]
style_cond_level_1 = style_cond_level_1 + num_align_right()

style_cond_level_2 = [
    {
        'if': {'column_id': 'Leakage'},  # Specify the target cell
        'color': 'red',  # Apply the bold font weight
        'fontWeight': 'bold',
    },
    {
        'if': {'row_index': 0},  
        'backgroundColor': lightred,
    },
]
style_cond_level_2 = style_cond_level_2 + num_align_right()

style_cond_level_3 = [
    {
        'if': {'row_index': 0, 'column_id': 'actual_points'},  # Specify the target cell
        'color': 'red',  # Apply the bold font weight
        'fontWeight': 'bold',
    },
    {
        'if': {'row_index': 0},  
        'backgroundColor': lightred,
    },
    {
        'if': {'row_index': 1},  
        'backgroundColor': lightgreen,
    },
]
style_cond_level_3 = style_cond_level_3 + num_align_right()

style_cond_level_4_0 = [
    {
        'if': {'row_index': 0, 'column_id': 'Variable'},  # Specify the target cell
        'fontWeight': 'bold',
    },
    {
        'if': {'row_index': 0},  
        'backgroundColor': lightred,
    },
    {
        'if': {'column_id': 'col_value'},
        'color': 'red',
        'fontWeight': 'bold',
        'textAlign': 'center',
        'width': '60px',

    },
    {
        'if': {
            'column_id': 'col_value',
            'row_index': 0
        },
        'fontSize': '20px',
    },
    {
        'if': {
            'column_id': 'col_value',
            'row_index': 1
        },
        'color': 'green'
    },
]

style_cond_level_4_1 = [
    {
        'if': {'row_index': 0, 'column_id': 'Variable'},  # Specify the target cell
        'fontWeight': 'bold',
    },
    {
        'if': {'row_index': 0},  
        'backgroundColor': lightgreen,
    },
    {
        'if': {'column_id': 'col_value'},
        'color': 'green',
        'fontWeight': 'bold',
        'textAlign': 'center',
        'width': '60px',
    },
    {
        'if': {
            'column_id': 'col_value',
            'row_index': 0
        },
        'fontSize': '20px',
    },
]

def my_table(title,link_c,link_d,id,df,style_cond):

    tooltip_header = {col: {'value': col, 'use_with': 'header'} for col in df.columns}

    def num_col(col):
        return {
            "name": col, 
            "id": col, 
            "type": "numeric",
            "format": numeric_cols[col],
        }
    
    def oth_col(col):
        return {
            "name": col, 
            "id": col,
        } 
    
    columns = [num_col(col) if col in numeric_cols else oth_col(col) for col in df.columns]

    return html.Div([
        dcc.Store(id='selected-cell'),
        table_title(title, link_c, link_d),
        dash_table.DataTable(
            id=id,
            data=df.to_dict('records'),
            columns=columns,
            style_header=style_header,
            style_data=style_data,
            style_cell=style_cell,
            fixed_rows={'headers': True}, # set this will limit table max height
            style_table={'height': '100%'}, #'overflowY': 'auto'
            style_data_conditional=style_cond,
            tooltip_header=tooltip_header,
            # This is necessary to enable tooltips
            tooltip_delay=0,
            tooltip_duration=None
        ),
        html.Hr(),
    ]
    )


def right_container_layout():
    base_url = 'https://github.com/zenon-test/Loyalty_Control/blob/main/data'
    link_1c = f'{base_url}/level_1.sql'
    link_1d = f'{base_url}/level_1.csv'
    return html.Div(
            [
                my_table(
                    title='Level 1: All Partners', 
                    link_c=link_1c, 
                    link_d=link_1d, 
                    id='level-1-table', 
                    df=df_level_1, 
                    style_cond=style_cond_level_1),
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
df_level_1['% Difference'] = df_level_1['% Difference'] * 100
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
    base_url = 'https://github.com/zenon-test/Loyalty_Control/blob/main/data/partner_466'
    level_dict = {
        '2': {
            'div': 'level-2-div',
            'table': 'level-2-table',
            'title': 'Level 2: Partner=466',
            'link_c' : f'{base_url}/level_2.sql',
            'link_d' : f'{base_url}/level_2.csv',
            'df': df_level_2,
            'style_cond': style_cond_level_2,
        },
        '3': {
            'div': 'level-3-div',
            'table': 'level-3-table',
            'title': 'Level 3: Txn_ID=29',
            'link_c' : f'{base_url}/txn_29/level_3.sql',
            'link_d' : f'{base_url}/txn_29/level_3.csv',
            'df': df_level_3,
            'style_cond': style_cond_level_3,
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
                return my_table(
                    title=out['title'], 
                    link_c=out['link_c'], 
                    link_d=out['link_d'], 
                    id=out['table'], 
                    df=out['df'],
                    style_cond=out['style_cond'])
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
        base_url = 'https://github.com/zenon-test/Loyalty_Control/blob/main/data/partner_466/txn_29'
        link_0c = f'{base_url}/program_1565160/level_4.py'
        link_0d = f'{base_url}/program_1565160/level_4.csv'
        link_1c = f'{base_url}/program_1565159/level_4.py'
        link_1d = f'{base_url}/program_1565159/level_4.csv'

        if row == 0:
            return my_table(
                title='Level 4: Program Code=1565160', 
                link_c=link_0c, 
                link_d=link_0d, 
                id='level-4-table-60', 
                df=df_level_4_60,
                style_cond=style_cond_level_4_0)
        elif row == 1:
            return my_table(
                title='Level 4: Program Code=1565159', 
                link_c=link_1c, 
                link_d=link_1d, 
                id='level-4-table-59', 
                df=df_level_4_59,
                style_cond=style_cond_level_4_1)
    