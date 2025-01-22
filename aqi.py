from dash import dcc, html  # Use updated imports
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

data = {
    'City': ['City A', 'City B', 'City C', 'City D', 'City E'] * 10,
    'AQI': np.random.randint(50, 200, 50),
    'Temperature': np.random.randint(15, 35, 50),
    'Humidity': np.random.randint(40, 80, 50),
    'Date': pd.date_range(start='2024-01-01', periods=50, freq='D')
}

df = pd.DataFrame(data)

def classify_aqi(aqi):
    if aqi <= 50:
        return 'Good'
    elif aqi <= 100:
        return 'Moderate'
    elif aqi <= 150:
        return 'Unhealthy for Sensitive Groups'
    elif aqi <= 200:
        return 'Unhealthy'
    else:
        return 'Very Unhealthy'

df['AQI Classification'] = df['AQI'].apply(classify_aqi)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    children=[
  
        html.Div(
            children=[
                html.H1("Advanced AQI Dashboard", style={
                    'text-align': 'center',
                    'font-size': '3rem',
                    'color': '#2c3e50',
                    'font-weight': 'bold',
                    'margin-bottom': '10px'
                }),
                html.H3("Visualizing Air Quality with Dynamic Analytics", style={
                    'text-align': 'center',
                    'color': '#34495e',
                    'font-size': '1.5rem',
                    'margin-bottom': '20px'
                }),
                html.H4("- By Aman Giri", style={
                    'text-align': 'center',
                    'color': '#34495e',
                    'font-size': '1.5rem',
                    'margin-bottom': '20px'
                })
            ],
            style={'background-color': '#ecf0f6', 'padding': '30px', 'border-radius': '8px'}
        ),

        html.Div(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            dcc.Dropdown(
                                id='city-filter',
                                options=[{'label': city, 'value': city} for city in df['City'].unique()],
                                placeholder="Select a City",
                                multi=True,
                                style={'width': '100%'}
                            ),
                            width=6
                        ),
                        dbc.Col(
                            dcc.DatePickerRange(
                                id='date-filter',
                                start_date=df['Date'].min(),
                                end_date=df['Date'].max(),
                                display_format='YYYY-MM-DD'
                            ),
                            width=6
                        ),
                    ],
                    style={'margin-bottom': '20px'}
                )
            ],
            style={'padding': '20px', 'background-color': '#bdc3c7', 'border-radius': '8px'}
        ),

        html.Div(
            children=[
                dbc.Row(
                    children=[
                        # Scatter Plot with AQI and Temperature
                        dbc.Col(dcc.Graph(id='scatter-plot'), width=6),
                        # Heatmap
                        dbc.Col(dcc.Graph(id='heatmap'), width=6)
                    ]
                ),
                dbc.Row(
                    children=[
                        # Sunburst Chart
                        dbc.Col(dcc.Graph(id='sunburst-chart'), width=6),
                        # Parallel Coordinates
                        dbc.Col(dcc.Graph(id='parallel-coordinates'), width=6)
                    ]
                ),
                dbc.Row(
                    children=[
                        # Histogram
                        dbc.Col(dcc.Graph(id='histogram'), width=6),
                        # Area Chart
                        dbc.Col(dcc.Graph(id='area-chart'), width=6)
                    ]
                ),
                dbc.Row(
                    children=[
                        # Line Chart
                        dbc.Col(dcc.Graph(id='line-chart'), width=6),
                        # Pie Chart
                        dbc.Col(dcc.Graph(id='pie-chart'), width=6)
                    ]
                ),
                dbc.Row(
                    children=[
                        # Box Plot
                        dbc.Col(dcc.Graph(id='box-plot'), width=6),
                        # Violin Plot
                        dbc.Col(dcc.Graph(id='violin-plot'), width=6)
                    ]
                ),
            ]
        )
    ],
    style={'font-family': 'Arial, sans-serif'}
)

@app.callback(
    [
        Output('scatter-plot', 'figure'),
        Output('heatmap', 'figure'),
        Output('sunburst-chart', 'figure'),
        Output('parallel-coordinates', 'figure'),
        Output('histogram', 'figure'),
        Output('area-chart', 'figure'),
        Output('line-chart', 'figure'),
        Output('pie-chart', 'figure'),
        Output('box-plot', 'figure'),
        Output('violin-plot', 'figure')
    ],
    [
        Input('city-filter', 'value'),
        Input('date-filter', 'start_date'),
        Input('date-filter', 'end_date')
    ]
)
def update_graphs(selected_cities, start_date, end_date):
    # Filter data based on input
    filtered_df = df.copy()
    if selected_cities:
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]
    filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]

    # Scatter Plot
    scatter_fig = px.scatter(filtered_df, x='Temperature', y='AQI', color='City', title='AQI vs Temperature',
                             template='plotly_dark')

    # Heatmap
    heatmap_fig = px.imshow(
        pd.crosstab(filtered_df['City'], filtered_df['AQI Classification']),
        labels=dict(x="AQI Classification", y="City", color="Count"),
        title='Heatmap: AQI Classification by City',
        template='plotly_dark'
    )

    # Sunburst Chart
    sunburst_fig = px.sunburst(filtered_df, path=['City', 'AQI Classification'], title='AQI Classification Distribution',
                               template='plotly_dark')

    # Parallel Coordinates Plot
    parallel_fig = px.parallel_coordinates(
        filtered_df,
        dimensions=['AQI', 'Temperature', 'Humidity'],
        color='AQI',
        title='Parallel Coordinates Plot',
        template='plotly_dark'
    )

    # Histogram
    hist_fig = px.histogram(filtered_df, x='AQI', nbins=10, title='AQI Distribution', template='plotly_dark')

    # Area Chart
    area_fig = px.area(filtered_df, x='Date', y='AQI', color='City', title='Cumulative AQI Trends Over Time',
                       template='plotly_dark')

    # Line Chart
    line_fig = px.line(filtered_df, x='Date', y='AQI', color='City', title='AQI Trends Over Time', template='plotly_dark')

    # Pie Chart
    pie_fig = px.pie(filtered_df, names='City', values='AQI', title='AQI Distribution by City', template='plotly_dark')

    # Box Plot
    box_fig = px.box(filtered_df, x='City', y='AQI', color='City', title='AQI Box Plot by City', template='plotly_dark')

    # Violin Plot
    violin_fig = px.violin(filtered_df, x='City', y='AQI', color='City', title='AQI Violin Plot by City', template='plotly_dark')

    return scatter_fig, heatmap_fig, sunburst_fig, parallel_fig, hist_fig, area_fig, line_fig, pie_fig, box_fig, violin_fig

if __name__ == '__main__':
    app.run_server(debug=True)
