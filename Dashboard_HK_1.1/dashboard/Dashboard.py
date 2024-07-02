import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the data
df = pd.read_csv('/home/pumet/Desktop/Year 3/Term_1/Ai_eco/Dashboard_HK_1.1/dashboard/data.csv')
geojson_path = '/home/pumet/Desktop/Year 3/Term_1/Ai_eco/Dashboard_HK_1.1/dashboard/thailand-provinces.geojson'
# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Graduates Dashboard"),
    
    # Dropdown for province selection
    dcc.Dropdown(
        id='province-dropdown',
        options=[{'label': province, 'value': province} for province in df['schools_province'].unique()],
        value='กระบี่',  # Default value (change as needed)
        clearable=False
    ),
    
    # Bar chart showing number of graduates by gender
    dcc.Graph(id='bar-chart'),
    
    # Interactive map showing provinces
    html.H2("Interactive Map"),
    dcc.Graph(id='map')
])

# Callback to update bar chart based on province selection
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
    Output('map', 'figure'),
    [Input('province-dropdown', 'value')]
)
def update_map(province):
    fig = px.choropleth(
    df,
    geojson=geojson_path,
    locations='schools_province',  # Column in your CSV that contains province names
    color='totalstd',  # Column in your CSV that you want to visualize
    color_continuous_scale="Viridis",
    range_color=(0, df['totalstd'].max()),  # Adjust color scale range as needed
    featureidkey="properties.name",  # Key in GeoJSON file that matches province names
    projection="mercator",
    title="Total Students per Province in Thailand"
)

    fig.update_geos(fitbounds="locations", visible=False)
    return fig

# Callback to update map based on province selection
# @app.callback(
#     Output('map', 'figure'),
#     [Input('province-dropdown', 'value')]
# )
# def update_map(province):
#     # Replace with actual latitude and longitude data from your dataset
#     fig = px.scatter_mapbox(df, lat=[13.736717], lon=[100.523186],
#                             text='schools_province', zoom=4, height=300)
#     fig.update_layout(mapbox_style="open-street-map")
#     return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
