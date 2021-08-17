import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
import lstm_method as lstm
import xgboost_method as xgboost
import rnn_method as rnn

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#define model prediction
LSTM, RNN = "./model/lstm.model.h5", "./model/rnn_model.h5"
XGBoot = "./model/xgb_model.h5"

#call api model prediction
#xgb_train, xgb_valid = xgboost.xgboost_prediction()

train_lstm, valid_lstm = lstm.prediction(LSTM)
train_rnn, valid_rnn ,y_predic_rnn = rnn.prediction(RNN)

# print(valid_rnn.Close)
# print(y_predic_rnn)
# print("train lstm")
# print(train_lstm.index)

# print("train rnn")
# print(train_rnn["Date"])
# print("valid rnn")
# print(valid_rnn)
# print("predic_rnn")
# print(predic_rnn)

#===================================LAYOUT====================================================#
app.layout = html.Div([

    html.H1("Stock Price Analysis Dashboard", style={"textAlign": "center"}),
   
    dcc.Tabs(id="tabs", children=[
       
      dcc.Tab(label='Long Short Temp Memory Method',children=[
				html.Div([
					html.H2(
            "Stock Price Prediction Using LSTM Method",
            style={
              "textAlign": "center",
              "color":"blue",
            }
          ),
					dcc.Dropdown(
                       id='lstm-dropdown',
                       options=[
                        {'label': 'Close Price', 'value': 1},
                        {'label': 'Price Rate of Change','value': 2},
                       ], 
                       multi=True,value=[1],
                       style={}),
				  dcc.Graph(
						id="lstm-graph",
						style={'width':'100%'},
				  ),
			  ]),        		
      ]),

      dcc.Tab(label='RNN Method',children=[
				html.Div([
					html.H2("Stock Price Prediction Using RNN Method",style={"textAlign": "center"}),
					dcc.Dropdown(
                       id='RNN-dropdown',
                       options=[
                        {'label': 'Close Price', 'value': 1},
                        {'label': 'Price Rate of Change','value': 2},
                       ], 
                       multi=True,value=[1],
                       style={}),
				  dcc.Graph(
						id="RNN-graph",
						style={'width':'100%'},
				  ),
			  ]),        		
      ]),
      
      dcc.Tab(label='XGBoots Method',children=[
				html.Div([
					html.H2("Stock Price Prediction Using XGBoots Method",style={"textAlign": "center"}),
					dcc.Dropdown(
                       id='Xgboots-dropdown',
                       options=[
                        {'label': 'Close Price', 'value': 1},
                        {'label': 'Price Rate of Change','value': 2},
                       ], 
                       multi=True,value=[1],
                       style={}),
				  dcc.Graph(
						id="Xgboots-graph",
						style={'width':'100%'},
				  ),
			  ]),        		
      ]),
    ])
])


#==============================CALL BACK ENVENT AND FUNCTION============================#

## Event for update lstm tab
@app.callback(Output('lstm-graph', 'figure'),
              [Input('lstm-dropdown', 'value')])
def update_graph(selected_dropdown):
  data = [
    go.Scatter(
      x=train_lstm.index,
      y=train_lstm["Close"],
      name="train data"
    ),
    go.Scatter(
      x=valid_lstm.index,
      y=valid_lstm["Close"],
    )
  ]
  for typepred in selected_dropdown:
    if typepred == 1:
      data.append(
        go.Scatter(
          x=valid_lstm.index,
          y=valid_lstm["Predictions"],
          name="predict data by closing price"
        )
      )
    if typepred == 2:
      print(2)

  figure = {
    "data": data,
    "layout": go.Layout(
      xaxis={"title":"Date"},
      yaxis={"title":"Price"}
    )
  }

  return figure


# Event for update XGBoots tab

# Event for update RNN tab
@app.callback(Output('RNN-graph', 'figure'),
              [Input('RNN-dropdown', 'value')])
def update_graph(selected_dropdown):
  data = [
    go.Scatter(
      x=train_rnn.Date,
      y=train_rnn.Close,
      name="train data"
    ),
    go.Scatter(
      x=valid_rnn.Date,
      y=valid_rnn.Close,
      name="valid data"
    )
  ]
  for typepred in selected_dropdown:
    if typepred == 1:
      data.append(
        go.Scatter(
          x=valid_rnn.Date.iloc[50:],
          y=y_predic_rnn,
          name="predict data by closing price"
        )
      )
    if typepred == 2:
      print(2)

  figure = {
    "data": data,
    "layout": go.Layout(
      xaxis={"title":"Date"},
      yaxis={"title":"Price"}
    )
  }
  return figure



if __name__=='__main__':
	app.run_server(debug=True)