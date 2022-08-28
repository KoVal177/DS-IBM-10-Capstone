import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

site_dropdown_options = [
    {'label': 'All sites', 'value': 'All'},
]
for site in spacex_df['Launch Site'].unique():
    site_dropdown_options.append(
        {'label': site, 'value': site}
    )

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={
                'textAlign': 'center',
                'color': '#503D36',
                'font-size': 40,
            },
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id='site-dropdown',
                    options=site_dropdown_options,
                    value='All',
                    placeholder='Select a Launch Site',
                    searchable=True,
                    style={
                        'width': '80%',
                        'padding': '2px',
                        'font-size': '20px',
                        'text-align-last': 'center',
                    }
                ),

            ],
            style={'display':'flex'}
        ),
        html.Br(),
        html.Div(
            [ ], id='success-pie-chart'
        ),

        html.Br(),

        html.P("Payload range (Kg):"),
        html.Div(
            dcc.RangeSlider(
                id='payload-slider',
                min=0,
                max=10000,
                step=1000,
                marks={
                    0: '0',
                    1000: '1000',
                    2000: '2000',
                    3000: '3000',
                    4000: '4000',
                    5000: '5000',
                    6000: '6000',
                    7000: '7000',
                    8000: '8000',
                    9000: '9000',
                    10000: '10000',
                },
                value=[
                    min_payload,
                    max_payload,
                ]
            )
        ),
        html.Div(
            [ ], id='success-payload-scatter-chart'
        ),
    ],
)

@app.callback( 
    [
        Output(component_id='success-pie-chart', component_property='children'),
    ],
    [
        Input(component_id='site-dropdown', component_property='value'),
    ],
    [
    ],
)
def get_pie_chart(site):
    filtered_df = spacex_df
    if site == 'All':
        data = filtered_df.groupby(by='Launch Site')['class'].agg('sum').reset_index()
        fig = px.pie(
            data,
            values='class',
            names='Launch Site',
            title='Total Success Launches by Site',
        )
        return [
            dcc.Graph(figure=fig),
        ]
    else:
        data = filtered_df.loc[
            filtered_df['Launch Site'] == site
        ].groupby(by='class')['Flight Number'].agg('count').reset_index()
        fig = px.pie(
            data,
            values='Flight Number',
            names='class',
            title='Total Success Launches for Site {}'.format(site),
        )
        return [
            dcc.Graph(figure=fig),
        ]

@app.callback( 
    [
        Output(
            component_id='success-payload-scatter-chart',
            component_property='children'
        ),
    ],
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value'),
    ],
    [
    ],
)
def get_scatter_chart(site, payload):
    filtered_df = spacex_df
    data = filtered_df.loc[
        (filtered_df['Payload Mass (kg)'] >= payload[0]) &
        (filtered_df['Payload Mass (kg)'] <= payload[1]),
    ]
    if site == 'All':
        fig = px.scatter(
            data,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for all Sites',
        )
        return [
            dcc.Graph(figure=fig),
        ]
    else:
        data = data.loc[data['Launch Site'] == site]
        fig = px.scatter(
            data,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for Site {}'.format(site),
        )
        return [
            dcc.Graph(figure=fig),
        ]


if __name__ == '__main__':
    app.run_server()
