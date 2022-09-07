import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app
from app import server
from assets import facebook
from assets import sentiment
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import networkx as nx

upper_body = html.Div([
    dbc.Row(
        dbc.Col([html.H4('Select Social Platform'), dcc.Dropdown(['FaceBook', 'YouTube', 'Twitter'], id='items')],
                className='drop_outer_box')
    )
])

degs = facebook.degs
frq = facebook.frq
degree_size = facebook.degree_size
node_sizes = [d / 10 for d in degree_size]
colors = facebook.node_color

df = pd.DataFrame(np.column_stack([degs, frq]), columns=['degree', 'frequency'])
fig = px.scatter(df, x='degree', y='frequency')
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    legend_font_color = 'rgba(255,255,255,255)',
    plot_bgcolor='#121212'
)
list_board_layout = html.Div(
    [
        # html.H2(facebook.df_size),
        # html.H2(facebook.sample_size)
        dbc.Card(
            [
                dbc.CardBody([
                    html.P("Overall Size", className="card-title"),
                    html.H1(facebook.df_size, className="card-body")])], className='card'
        ),
        dbc.Card(
            [
                dbc.CardBody([
                    html.P("Sample Size", className="card-title"),
                    html.H1(facebook.sample_size, className="card-body")])], className='card'
        ),
        dbc.Card(
            [
                dbc.CardBody([
                    html.P("Sample Percentage", className="card-title"),
                    html.H1(facebook.frack_p, className="card-body")])], className='card'
        ),
        dbc.Card(
            [
                dbc.CardBody([
                    html.P("Company", className="card-title"),
                    html.H1("CNN", className="card-body")])], className='card'
        ),
    ], className="listBoard"
)


# Plotly figure
def networkGraph(EGDE_VAR):
    graph = facebook.G
    pos = nx.spring_layout(graph)

    # edges trace
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(color='gray', width=1),
        hoverinfo='none',
        showlegend=False,
        mode='lines')

    # nodes trace
    node_x = []
    node_y = []
    text = []
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y, text=text,
        mode='markers',
        showlegend=False,
        hoverinfo='none',
        marker=dict(
            color=colors,
            size=node_sizes,
            line=dict(color='black', width=1)))
    # layout
    l = dict(plot_bgcolor='white',
             paper_bgcolor='white',
             margin=dict(t=10, b=10, l=10, r=10, pad=0),
             xaxis=dict(linecolor='black',
                        showgrid=False,
                        showticklabels=False,
                        mirror=True),
             yaxis=dict(linecolor='black',
                        showgrid=False,
                        showticklabels=False,
                        mirror=True))

    # figure
    fig = go.Figure(data=[edge_trace, node_trace], layout=l)
    return fig

figImg = px.imshow(sentiment.wordcloud)
figImg.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
)
Content = html.Div([
    list_board_layout,
    dbc.Row([
       dbc.Col([
            html.Div([
            html.H4("Degree Distribution"),
            dcc.Graph(figure=fig),
            ],className="degreebox"),
       ],id="col1"),
        dbc.Col([
            html.Div([
            html.H4("Text Summary"),
            dcc.Graph(figure=figImg),
            ],className="degreebox")
        ],id="col2")
    ]),

    dcc.Loading(
        id="loading-2",
        children=[
            html.Div(children=[], id="layoutNetwork"),
        ],
        type="circle",
    ),

], className='page_content')

Header = html.Div([
    html.H1('Social Network Analysis Dashboard'),
    upper_body
], className='page_header')

app.layout = html.Div([
    Header,
    Content
], className='container-fluid')


@app.callback(
    Output(component_id='layoutNetwork', component_property='children'),
    Input(component_id='items', component_property='value')
)
def update_output(value):
    if value is None:
        return None
    if value == "FaceBook":
        return dcc.Graph(figure=networkGraph(" "), id="gNetwork")
    else:
        ans = "{} data not available yet..".format(value)
        return html.H1(ans)


if __name__ == "__main__":
    app.run_server(debug=True)
