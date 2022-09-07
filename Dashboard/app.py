import dash
import dash_bootstrap_components as dbc

external_stylesheets = [
    'assets/style.css'
]

app = dash.Dash(__name__,suppress_callback_exceptions=True,
                external_stylesheets = [external_stylesheets,dbc.themes.BOOTSTRAP],
                meta_tags=[{
                    'name':'Network Analysis Dashboard',
                    'content': 'width=device-width,initial-scale=1.0'
                }]
                )
app.title = 'Social Network'
server = app.server