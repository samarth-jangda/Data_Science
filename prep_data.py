import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from flask import request

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
    }
}
colors = {
    'text' : '#ff0000',
    'plot_bgcolor':'#D3D3D3',
    'page_bgcolor':'#00FFFF'
}
red_button_style={
    'color':'#D3D3D3'
}

df = pd.read_csv("C:\\Users\\samar\\OneDrive\\Desktop\\Samarth\\Assignment\\sample.csv")
x = df["active_power"]
y = df["reactive_power"]


fig = px.scatter(df, x=x, y=y)


fig.update_layout(clickmode='event+select')

fig.update_traces(marker_size=6)

app.layout = html.Div([
    html.H1("Data Science App",
            style={
                'textAlign': 'center',
                'color': colors['text']
            }),
    html.Label("Consider the following graph",
               style={
                  'textAlign': 'center',
                   'color': '#00FFFF',
               }),
    html.Label("Below is the data for active power",
               style={
                   'color': '#FF5733 '
               }),
    dcc.Dropdown(
        id="dropdown",
        options=[
            {'label':i ,'value':i} for i in x
        ]
    ),
    html.Label("Below is the data for reactive power",
               style={
                   'color': '#B933FF ',
               }),
    dcc.Dropdown(
        id='dropdown-1',
        options=[
            {'label':i, 'value':i} for i in y
        ]
    ),
    dcc.Graph(
        id='basic-interactions',
        figure=fig,
        style={
            'layout':{
                'plot_bgcolor':colors['plot_bgcolor'],
                'paper_bgcolor':colors['page_bgcolor'],
                'font':{
                    'color':'#ff0000',

                },
                'hover_data': '',
                'hovermode':'closest',
                'title': "A simple chart"
            }
        }
    ),
    html.Button("Save_Data",id='SaveData'),

    html.Div(className='row', children=[
        html.Div([

            dcc.Markdown("""
                **Hover Data**

                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data', style=styles['pre']),

        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data',style=styles['pre']),
        ], className='three columns'

        ),

        html.Div([
            dcc.Markdown("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.

                Note that if `layout.clickmode = 'event+select'`, selection data also
                accumulates (or un-accumulates) selected data if you hold down the shift
                button while clicking.
            """),



            html.Pre(id='selected-data', style=styles['pre']),
        ], className='three columns'),




        html.Div([
            dcc.Markdown("""
                **Zoom and Relayout Data**

                Click and drag on the graph to zoom or click on the zoom
                buttons in the graph's menu bar.
                Clicking on legend items will also fire
                this event.
            """),
            html.Pre(id='relayout-data', style=styles['pre']),
        ], className='three columns')

    ])
])
styles_1 = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
    }
}

second_plot_color={
    'text' : '#ff0000',
    'plot_bgcolor':'#990033',
    'page_bgcolor':'#CC0000'
}


@app.callback(
    Output('hover-data', 'children'),
    Input('basic-interactions', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(
    Output('click-data', 'children'),
    Input('basic-interactions', 'clickData'))
def display_click_data(clickData):

    return json.dumps(clickData, indent=2)



@app.callback(
    Output('selected-data', 'children'),
    Input('basic-interactions', 'selectedData'))
def display_selected_data(selectedData):
    result = ""
    if selectedData is not None:
        x_1 = list(map(lambda pt: pt.get("x"), selectedData.get("points")))
        print(x_1)
        y_1 = list(map(lambda pt: pt.get("y"), selectedData.get("points")))
        print(y_1)

        df_1=pd.DataFrame(list(zip(x_1,y_1)),
                          columns=['Active_Power','Reactive_Power'])
        frames=[df,df_1]
        result=pd.concat(frames)
        fig_2=px.scatter(df_1,x=x_1,y=y_1)
        print(result)


        app.layout=html.Div[{
            dcc.Graph(
                id='second-interaction',
                figure=fig_2,
                style={
                    'layout':{
                    'plot_bgcolor': second_plot_color["plot_bgcolor"],
                    'page_color': second_plot_color["page_bgcolor"],
                    'font': {
                        'color': '#FF0000',

                  },
                    'hover_data': '',
                    'hovermode': 'closest',
                    'title': "A simple chart"
               }
            }

        ),
        dcc.Dropdown(
            id='dropdown-1',
            options=[
                {'label': i, 'value': i} for i in x_1
            ]
        ),
        dcc.Dropdown(
            id='dropdown-1',
            options=[
                {'label': i, 'value': i} for i in y_1
            ]
        ),


    }]

    return selectedData


@app.callback(
    Output('relayout-data', 'children'),
    Input('basic-interactions', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)
