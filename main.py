import dash
from dash import Input, Output, State, dcc, html
import dash_bootstrap_components as dbc
import os
import right_container
from right_container import right_container_layout

#---
# 0. Initialize APP
#---
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True) # suppress to allow dynamic layout

server = app.server

#---
# 1. DATA FUNCTIONS
#---
# imported from hg_goals

#---
# 2. LAYOUT FUNCTIONS
#---

def title_div(title):
    return html.Div(
        html.H2(title),
        style={"text-align": "center", "margin-top": "200px", "margin-bottom": '20px'}
        )
    
def label_div(label):
    return html.Div(
        [
            html.Label(label)
        ],
        style={"margin-bottom": '5px'}
    )

def input_div(id,type):
    return html.Div(
        [
            dcc.Input(id=id,type=type)
        ],
        style={"margin-bottom": '10px'}
    )

button_style = {
    'background': 'linear-gradient(to bottom, #FFA500, #FF8C00)',
    'border': 'none',
    'color': 'white',
    'padding': '3px 3px',
    'text-align': 'center',
    'text-decoration': 'none',
    'display': 'inline-block',
    'font-size': '16px',
    'cursor': 'pointer',
    'border-radius': '5px',
    'width': '185px',
    "margin": '10px 5px',
}

toggle_button_style = {
    'background-color': '#333',  #/* Dark gray, but not as dark as the black background */
    'color': 'white',  #/* Text color */
    'border': 'none',  #/* Removes the default button border */
    'padding': '3px 5px',  #/* Vertical and horizontal padding */
    'border-radius': '5px',  #/* Rounded corners */
    'cursor': 'pointer',  #/* Hand cursor on hover */
    'transition': 'background-color 0.3s',
}

banner_style = {
    'height': '60px', 
    'width': '100%',
    'background-color': 'black',
    'color': 'white',
    'padding': '10px 30px'
}

#---
# 3. CALLBACK FUNCTIONS
#---


#---
# 4. Create Data
#---

#---
# 5. Create Layout
#---

TL_layout = html.Div(
    children=[
        # banner
        html.Div(
            [
                html.Button("<>", id="toggle-button", n_clicks=0, style=toggle_button_style),
                "Loyalty Control Center"
            ], 
            style=banner_style # height 60px
        ),
        # Left column - shown on laptops/desktops but hidden on smaller screens
        html.Div(
            html.Button("Top Level", id="TL-button", style=button_style),
            className="col-md-2 d-none d-md-block", #"col-md-2 d-none d-md-block",  # Bootstrap classes for responsiveness
            style={"background-color": "black", "height": "calc(100vh - 60px)"},
            id='col_id-0',
        ),
        # Main content
        html.Div(
            right_container_layout(),
            className="col-md-10 col-12",  # Takes up full width on small screens, 9 columns on larger screens
            id='col_id-1',
        ),
    ],
    className="row",  # Bootstrap class for a row
    style={'height': '100vh'}
)

login_layout = html.Div(
    children=[
        title_div(title="Loyalty Control Center"),
        label_div(label="Username"),
        input_div(id="username-input", type="text"),
        label_div(label="Password"),
        input_div(id="password-input", type="password"),

        html.Button("Login", id="login-button", style=button_style),
        html.Div(id="login-result"),
    ],
    id="login-div",
    style={"text-align": "center", "margin-top": "200px"}, # put login-div text in center
)

app.layout = html.Div(
    [
        login_layout,
    ],
    id='app_layout_div'
)

#---
# 6. Register Callbacks
#---

# Toggle Left Col
@app.callback(
    [Output("col_id-0", "className"),
     Output("col_id-1", "className"),
    ],
    Input("toggle-button", "n_clicks")
)
def toggle_left_column(n_clicks):
    # worry about small screen later.. shall store the toggle status instead of using n_clicks
    if n_clicks and n_clicks % 2:  # Toggle the column visibility based on odd or even number of clicks
        return "col-md-2 d-none", "col-md-12"
    else:
        return "col-md-2 d-block", "col-md-10"

# TL: click TL-button, get back to TL layout
@app.callback(
    Output('col_id-1', 'children', allow_duplicate=True),  # UPDATE right container
    [Input('TL-button', 'n_clicks')],
    prevent_initial_call=True   
)
def update_TL(n_clicks,):
    if n_clicks :
        return "TL Layout" # Todo
    
    else:
        return dash.no_update

# Click Login, Update app_layout_div (Whole App)
@app.callback(
    Output('app_layout_div', 'children'),  # UPDATE WHOLE APP
    [Input('login-button', 'n_clicks')],
    [State('username-input', 'value'), State('password-input', 'value')]
)
def update_layout_02A(n_clicks, username, password):
    if n_clicks and username == "admin" and password == "123":
        return TL_layout 
    elif n_clicks:
        error_message = html.Div("Incorrect username or password", style={'color': 'red'})
        return html.Div([error_message,])
    else:
        return dash.no_update

# local callback
right_container.register_drilldown_callbacks(app)

#----
# 7. Run the App
#----

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    server.run(host='0.0.0.0', port=port, debug=True)