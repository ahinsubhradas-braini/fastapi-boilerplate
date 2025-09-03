import dash
from dash import html

def create_dash_app(requests_pathname_prefix="/dev_dash/"):
    dash_app = dash.Dash(
        __name__,
        requests_pathname_prefix=requests_pathname_prefix
    )

    dash_app.layout = html.Div([
        html.H1("Developer Dashboard")
    ])

    return dash_app