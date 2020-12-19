import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
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

df = pd.read_csv("C:\\Users\\samar\\OneDrive\\Desktop\\Samarth\\Assignment\\sample.csv", encoding="utf-8")
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
    html.Label("Unlabeled_Data",style={
        'textAlign': 'center',
        'display': 'inline-block','margin':'10',
        'color' : colors['page_bgcolor'],
    }),
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
                'title': "A simple chart",

            },

        }
    ),



    #here user can input the name to labels and also save the data
    html.Div(dcc.Input(id='input-on-submit',type="text")),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-basic-button',children='Give the name of label of and press submit'),

    #Here by using this button we can save changes and see a new graph
    html.Button('Save_Data',id='save-data',n_clicks=0),

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
        ], className='three columns'),



    ]),

])
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
    }
}

second_plot_color={
    'text' : '#ff0000',
    'plot_1bgcolor':'#990033',
    'page_2bgcolor':'#CC0000'
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
    Output('container-basic-button','children'),
    [Input('submit-val','n_clicks')],
    [State('input-on-submit','value')]
)
def update_output(n_clicks,value):
    return 'The label you have given is of name : {}'.format(
        value,
        n_clicks
    )


#here we will finally render our graph with updated value

@app.callback(
    Output('selected-data', 'children'),
    Input('basic-interactions', 'selectedData'),
    [State('input-on-submit','value')]
)

def display_selected_data(selectedData,value):
    result = ""
    if selectedData is not None:
        x_1 = list(map(lambda pt: pt.get("x"), selectedData.get("points")))
        # print(x_1)
        y_1 = list(map(lambda pt: pt.get("y"), selectedData.get("points")))
        # print(y_1)

        # sel_df=pd.DataFrame(list(zip(x_1,y_1)),
        #                   columns=['Active_Power','Reactive_Power'])
        # frames=[df,df_1]
        # data_a = pd.concat(frames)
        # a = 'Given_label - {}'.format(value)
        # print(a)

        # print(s)

        #Take the help of looping to match the data and make a new graph.
        df["label"] = "unlabeled"
        for idx in df.index:
            if df.at[idx, "active_power"] in x_1 and df.at[idx, "reactive_power"] in y_1:
                df.at[idx, "label"] = value
        print(df)
        fig_2 = px.scatter(df,x="active_power",y="reactive_power",color='label')
        #making the second graph

        app.layout=html.Div([

            html.Label("Labeled_Data", style={
                'display': 'inline-block', 'margin': '10',
                'color': '#808000',
            }),
            dcc.Graph(
                id='second-interaction',
                figure=fig_2,
                style={
                    'layout': {
                        'plot_bgcolor': second_plot_color["plot_1bgcolor"],
                        'page_color': second_plot_color["page_2bgcolor"],
                        'font': {
                            'color': '#FFFF00',

                        },
                        'hover_data': '',
                        'hovermode': 'closest',
                        'title': "A simple chart"
                    }
                }

            ),
            html.Label("Selected Active_Power", style={
                'display': 'inline-block', 'margin': '10',
                'color': '#808000',
            }),
            dcc.Dropdown(
                id='dropdown-1',
                options=[
                    {'label': i, 'value': i} for i in df['active_power']
                ]
            ),
            html.Label("Selected Reactive_Power", style={
                'display': 'inline-block', 'margin': '10',
                'color': '#808000',
            }),
            dcc.Dropdown(
                id='dropdown-1',
                options=[
                    {'label': i, 'value': i} for i in df["reactive_power"]
                ]
            ),
        ])
        # df[df["active_power"].isin(x_1) & df["reactive_power"].isin(y_1)]["label"] = value
        # for idx in df.index:
        #     if df_1["Active_Power"] in df["active_power"] :
        #         df.at[3,'Type']= value
        #         return df

    return json.dumps(selectedData, indent=4)


@app.callback(
    Output('relayout-data', 'children'),
    Input('basic-interactions', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)
