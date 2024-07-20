import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('/home/pumet/Desktop/Year 3/Term_1/Ai_eco/Dashboard_HK_1.1/dashboard/data_with_coords.csv')

total_students = df['totalstd'].sum()
total_province = df['schools_province'].nunique()
total_boy = df["totalmale"].sum()
total_girl = df["totalfemale"].sum()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

sidebar = dbc.Col(
    [
        html.H2("Dashboard", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [

            ],
            vertical=True,
            pills=True,
        ),
    ],
    width=2,
)

content = dbc.Col(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(f"{total_students}", className="card-title"),
                                html.P("Total Students"),
                                dbc.Button("More info", color="primary"),
                            ]
                        )
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(f"{total_province}", className="card-title"),
                                html.P("Total Provinces"),
                                dbc.Button("More info", color="success"),
                            ]
                        )
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(f"{total_boy}", className="card-title"),
                                html.P("Total Boys"),
                                dbc.Button("More info", color="warning"),
                            ]
                        )
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(f"{total_girl}", className="card-title"),
                                html.P("Total Girls"),
                                dbc.Button("More info", color="danger"),
                            ]
                        )
                    ),
                    width=3,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='province-dropdown',
                        options=[{'label': province, 'value': province} for province in df['schools_province'].unique()],
                        value=df['schools_province'].unique()[0], 
                        clearable=False,
                        style={'margin-bottom': '10px'}
                    ),
                    width=12
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='bar-chart'), width=6),
                dbc.Col(dcc.Graph(id='pie-chart'), width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.H2("Interactive Map"), className="mb-2"),
                dbc.Col(dcc.Graph(id='map', style={'height': '80vh'}), width=12),
            ]
        ),
    ],
    width=10,
)

app.layout = dbc.Container(
    [
        dbc.Row([sidebar, content])
    ],
    fluid=True,
)

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('province-dropdown', 'value')]
)
def update_bar_chart(province):
    filtered_df = df[df['schools_province'] == province]
    fig = px.bar(filtered_df, x='schools_province', y=['totalfemale', 'totalmale'],
                 labels={'value': 'Number of Graduates', 'variable': 'Gender'},
                 title=f'Number of Graduates in {province} (Year 2566)',
                 barmode='group')
    return fig

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('province-dropdown', 'value')]
)
def update_pie_chart(province):
    filtered_df = df[df['schools_province'] == province]
    data = {
        'Gender': ['Boys', 'Girls'],
        'Count': [filtered_df['totalmale'].sum(), filtered_df['totalfemale'].sum()]
    }
    fig = px.pie(data, names='Gender', values='Count',
                 title='Total Students by Gender')
    return fig

@app.callback(
    Output('map', 'figure'),
    [Input('province-dropdown', 'value')]
)
def update_map(province):
    filtered_df = df[df['schools_province'] == province]

    if filtered_df.empty:
        return go.Figure()  

    fig = px.scatter_mapbox(
        filtered_df,
        lat='latitude',
        lon='longitude',
        size='totalstd',
        color='totalstd',
        color_continuous_scale='reds', 
        size_max=15,
        hover_name='schools_province',
        hover_data={'latitude': False, 'longitude': False},
        title=f"Students Distribution in {province}"
    )

    lat_center = filtered_df['latitude'].mean()
    lon_center = filtered_df['longitude'].mean()
    
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=lat_center, lon=lon_center),
            zoom=10  
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        title=f"Map of {province}"
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8055)

