import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
from stock_prediction import prediction

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#define model prediction
LSTM, RNN, XGBoot = "./model/lstm.model.h5", "", "./model/xgb_model.h5"

#call api model prediction
train, valid = prediction(LSTM)


#print(train)
#print(valid)


#===================================LAYOUT====================================================#
app.layout = html.Div([

    html.H1("Stock Price Analysis Dashboard", style={"textAlign": "center"}),
   
    dcc.Tabs(id="tabs", children=[
       
      dcc.Tab(label='NSE-TATAGLOBAL Stock Data',children=[
				html.Div([
					html.H2("Stock Price Prediction Using LSTM Method",style={"textAlign": "center"}),
					dcc.Dropdown(id='lstm-dropdown',
                       options=[{'label': 'Close Price', 'value': 1},
                       {'label': 'Price Rate of Change','value': 2},], 
                        multi=True,value=[1],
                        style={}),
				  dcc.Graph(
						id="Actual Data",
						style={'width':'100%'},
						figure={
						"data":[
							go.Scatter(
								x=train.index,
								y=train["Close"],
								#mode='markers',
								name="train data"
							),

							go.Scatter(
								x=valid.index,
								y=valid["Close"],
								#mode='markers',
								name="valid data"
							),

							go.Scatter(
								x=valid.index,
								y=valid["Predictions"],
								#mode='markers',
								name="predict data"
							),
						],
						"layout":go.Layout(
							xaxis={'title':'Date'},
							yaxis={'title':'Closing Rate'},
						)
					}
				),
			])        		
    ]),
        # dcc.Tab(label='Facebook Stock Data', children=[
        #     html.Div([
        #         html.H1("Stocks High vs Lows", 
        #                 style={'textAlign': 'center'}),
              
        #         dcc.Dropdown(id='my-dropdown',
        #                      options=[{'label': 'Tesla', 'value': 'TSLA'},
        #                               {'label': 'Apple','value': 'AAPL'}, 
        #                               {'label': 'Facebook', 'value': 'FB'}, 
        #                               {'label': 'Microsoft','value': 'MSFT'}], 
        #                      multi=True,value=['FB'],
        #                      style={"display": "block", "margin-left": "auto", 
        #                             "margin-right": "auto", "width": "60%"}),
        #         dcc.Graph(id='highlow'),
        #         html.H1("Stocks Market Volume", style={'textAlign': 'center'}),
         
        #         dcc.Dropdown(id='my-dropdown2',
        #                      options=[{'label': 'Tesla', 'value': 'TSLA'},
        #                               {'label': 'Apple','value': 'AAPL'}, 
        #                               {'label': 'Facebook', 'value': 'FB'},
        #                               {'label': 'Microsoft','value': 'MSFT'}], 
        #                      multi=True,value=['FB'],
        #                      style={"display": "block", "margin-left": "auto", 
        #                             "margin-right": "auto", "width": "60%"}),
        #         dcc.Graph(id='volume')
        #     ], className="container"),
        # ])
    ])
])





#==============================CALL BACK ENVENT AND FUNCTION============================#

@app.callback(
    dash.dependencies.Output("lstm-dropdown", "options"),
    [dash.dependencies.Input("lstm-dropdown", "search_value")],
    [dash.dependencies.State("lstm-dropdown", "value")],
)
def update_multi_options(search_value, value):
	  print(value)

    return true


# @app.callback(Output('highlow', 'figure'),
#               [Input('my-dropdown', 'value')])
# def update_graph(selected_dropdown):
#     dropdown = {"TSLA": "Tesla","AAPL": "Apple","FB": "Facebook","MSFT": "Microsoft",}
#     trace1 = []
#     trace2 = []
#     for stock in selected_dropdown:
#         trace1.append(
#           go.Scatter(x=df[df["Stock"] == stock]["Date"],
#                      y=df[df["Stock"] == stock]["High"],
#                      mode='lines', opacity=0.7, 
#                      name=f'High {dropdown[stock]}',textposition='bottom center'))
#         trace2.append(
#           go.Scatter(x=df[df["Stock"] == stock]["Date"],
#                      y=df[df["Stock"] == stock]["Low"],
#                      mode='lines', opacity=0.6,
#                      name=f'Low {dropdown[stock]}',textposition='bottom center'))
#     traces = [trace1, trace2]
#     data = [val for sublist in traces for val in sublist]
#     figure = {'data': data,
#               'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
#                                             '#FF7400', '#FFF400', '#FF0056'],
#             height=600,
#             title=f"High and Low Prices for {', '.join(str(dropdown[i]) for i in selected_dropdown)} Over Time",
#             xaxis={"title":"Date",
#                    'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
#                                                        'step': 'month', 
#                                                        'stepmode': 'backward'},
#                                                       {'count': 6, 'label': '6M', 
#                                                        'step': 'month', 
#                                                        'stepmode': 'backward'},
#                                                       {'step': 'all'}])},
#                    'rangeslider': {'visible': True}, 'type': 'date'},
#              yaxis={"title":"Price (USD)"})}
#     return figure


# @app.callback(Output('volume', 'figure'),
#               [Input('my-dropdown2', 'value')])
# def update_graph(selected_dropdown_value):
#     dropdown = {"TSLA": "Tesla","AAPL": "Apple","FB": "Facebook","MSFT": "Microsoft",}
#     trace1 = []
#     for stock in selected_dropdown_value:
#         trace1.append(
#           go.Scatter(x=df[df["Stock"] == stock]["Date"],
#                      y=df[df["Stock"] == stock]["Volume"],
#                      mode='lines', opacity=0.7,
#                      name=f'Volume {dropdown[stock]}', textposition='bottom center'))
#     traces = [trace1]
#     data = [val for sublist in traces for val in sublist]
#     figure = {'data': data, 
#               'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
#                                             '#FF7400', '#FFF400', '#FF0056'],
#             height=600,
#             title=f"Market Volume for {', '.join(str(dropdown[i]) for i in selected_dropdown_value)} Over Time",
#             xaxis={"title":"Date",
#                    'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
#                                                        'step': 'month', 
#                                                        'stepmode': 'backward'},
#                                                       {'count': 6, 'label': '6M',
#                                                        'step': 'month', 
#                                                        'stepmode': 'backward'},
#                                                       {'step': 'all'}])},
#                    'rangeslider': {'visible': True}, 'type': 'date'},
#              yaxis={"title":"Transactions Volume"})}
#     return figure



if __name__=='__main__':
	app.run_server(debug=True)