
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import os

def prediction(model):

  #Read data and analyze closing price from dataframe
  data = pd.read_csv("./assets/NSE-TATA.csv")

  #Spliting Data as Train and Validation
  length_data = len(data)     # rows that data has
  split_ratio = 0.8          # %80 train + %20 validation
  length_train = round(length_data * split_ratio)  
  length_validation = length_data - length_train
  
  data.index=data['Date']
  data=data.sort_index(ascending=True,axis=0)

  #Training data 
  train_data=pd.DataFrame(index=range(0,length_train),columns=['Date','Close'])
  for i in range(0,length_train):
      train_data["Date"][i]=data['Date'][i]
      train_data["Close"][i]=data["Close"][i]
    
  train_data['Date'] = pd.to_datetime(train_data['Date'])  # converting to date time object
  train_data

  #Validation data
  validation_data=pd.DataFrame(index=range(length_train,len(data)),columns=['Date','Close'])
  for i in range(length_train,len(data)):
      validation_data["Date"][i]=data['Date'][i]
      validation_data["Close"][i]=data["Close"][i]
  validation_data['Date'] = pd.to_datetime(validation_data['Date'])  # converting to date time object
  validation_data

  #Creating Train Dataset from Train split
  dataset_train = train_data.Close.values
  dataset_train.shape
  dataset_train = np.reshape(dataset_train, (-1,1))
  dataset_train.shape

  #Normalization / Feature Scaling
  from sklearn.preprocessing import MinMaxScaler
  scaler = MinMaxScaler(feature_range = (0,1))
  # scaling dataset
  dataset_train_scaled = scaler.fit_transform(dataset_train)
  dataset_train_scaled.shape

  #Creating X_train and y_train from dataset_train_scaled
  X_train = []
  y_train = []
  time_step = 50
  for i in range(time_step, length_train):
      X_train.append(dataset_train_scaled[i-time_step:i,0])
      y_train.append(dataset_train_scaled[i,0])
      
  # convert list to array
  X_train, y_train = np.array(X_train), np.array(y_train)

  X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1],1))
  y_train = np.reshape(y_train, (y_train.shape[0],1))


  #Load yourmodel
  regressor=load_model(model)

  #Creating Test Dataset from Validation Data
  #Converting array and scaling
  dataset_validation = validation_data.Close.values  # getting "close" column and converting to array
  dataset_validation = np.reshape(dataset_validation, (-1,1))  # converting 1D to 2D array
  scaled_dataset_validation =  scaler.fit_transform(dataset_validation)  # scaling open values to between 0 and 1

  #Creating X_test and y_test
  X_test = []
  y_test = []

  for i in range(time_step, length_validation):
      X_test.append(scaled_dataset_validation[i-time_step:i,0])
      y_test.append(scaled_dataset_validation[i,0])

  # Converting to array
  X_test, y_test = np.array(X_test), np.array(y_test)

  X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))  # reshape to 3D array
  y_test = np.reshape(y_test, (-1,1))  # reshape to 2D array

  # predictions with X_test data
  y_pred_of_test = regressor.predict(X_test)
  # scaling back from 0-1 to original
  y_pred_of_test = scaler.inverse_transform(y_pred_of_test) 

  
  return train_data, validation_data, y_pred_of_test