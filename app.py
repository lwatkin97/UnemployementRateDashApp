# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import pandas as pd
#read data
df = pd.read_csv('a.csv')

#style sheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

states = df['state'].unique()

colors ={
    'background': 'white',
    'text': '#54575c'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children="Unemployment rate in US states by average Income", style={
            'font-weight': 'bold',
            'font-family': 'arial',
            'textAlign': 'center',
            'color': colors['text']
        }),
      
html.Div([
        dcc.Graph(id='slider'),
        dcc.Slider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            value=df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()},
            step=None,

    )
], style={'backgroundColor': colors['background']}),

 html.Div([
        dcc.Graph(id='rate-time-series'),
        dcc.Graph(id='rev-time-series'),
    ], style={'display': 'inline', 'width': '49%', 'backgroundColor': colors['background']}),

  
])

@app.callback(
    dash.dependencies.Output('rate-time-series', 'figure'),
    [dash.dependencies.Input('slider', 'hoverData')])
def update_y_timeseries(hoverData):
    #print(hoverData['points'][0])
    if hoverData is None:
        raise PreventUpdate
    state_name = hoverData['points'][0]['text']
    dff = df[df['state'] == state_name]
    #dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b>'.format(state_name)
    return create_time_series(dff, 'rate', title)

@app.callback(
    dash.dependencies.Output('rev-time-series', 'figure'),
    [dash.dependencies.Input('slider', 'hoverData')])
def update_y_timeseries(hoverData):
    if hoverData is None:
        raise PreventUpdate
    state_name = hoverData['points'][0]['text']
    dff = df[df['state'] == state_name]
    #dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b>'.format(state_name)
    return create_time_series(dff, 'value', title)


@app.callback(
    Output('slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
   

    return {
        'data': [dict(
            x=filtered_df['value'],
            y=filtered_df['rate'],
            text=filtered_df['state'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': colors['background']}
            },
        )],
        'layout': dict(
            xaxis={'title': 'Average Income',
                   },
            yaxis={'title': 'Unemployment Rate'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},

        )
    }

def create_time_series(dff, axis, title):
        return {
        'data': [dict(
            x=dff['year'],
            y=dff[axis],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear', },
            'xaxis': {'showgrid': False}
        }
    }








if __name__ == '__main__':
    app.run_server(debug=True)

"""
@app.callback(
    dash.dependencies.Output('rev-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)

  html.Div([
        dcc.Dropdown(
                id='state_drop',
                options=[{'label': i, 'value': i} for i in states],
                #value='Life expectancy at birth, total (years)'
            )
        ]),
    """






  