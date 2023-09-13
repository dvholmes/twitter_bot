import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
import os


def run_linearRegression(x_input,y_outcomes,predicted_x_value):


    # split the data into test and training
    X_train, X_test, y_train, y_test = train_test_split(x_input, y_outcomes, test_size = 0.15)
    reg_mod = LinearRegression()
    
    # fit/train the data using linear regression
    reg_mod.fit(X_train,y_train)

    print(reg_mod.score(X_test,y_test))

    #predict the y, based on the x input
    predicted_y_value = reg_mod.predict(predicted_x_value)

    print(predicted_y_value)
    return predicted_y_value[0][0]


def randomForestAlgroithm(dataframe,input_dataframe,x_columns,y_value_string,algoType):

    randFor_object = 0

    if algoType == 0:
        randFor_object = RandomForestClassifier(n_estimators= 200, min_samples_split=30,random_state=1)
    else:
        randFor_object = RandomForestRegressor(n_estimators= 200, min_samples_split=30,random_state=1)

    randFor_object.fit(dataframe[x_columns],dataframe[y_value_string])

    return randFor_object.predict(input_dataframe[x_columns])


def predict_openPrice(dataframe):    

    #get the last closing day to predict the nexts days opening.

    previous_dayClosing = np.array(dataframe['close'].iloc[len(dataframe) -1]).reshape(-1,1)

    # shift the closed column down one row, the close data should match the nexts day open data
    dataframe['close'] = dataframe['close'].shift(1)

    # get the last close date. This well be the input we use to predict the next days open price

    #remove the first row and last row.
    adjusted_dataframe = dataframe[1:len(dataframe)]
    

    x_values = np.array(adjusted_dataframe['close']).reshape(-1,1)
    y_values = np.array(adjusted_dataframe['open']).reshape(-1,1)
 
    return run_linearRegression(x_values,y_values,previous_dayClosing)

  
    
def predict_HighPrice(dataframe, current_openPrice):

    openPrice_array = np.array(current_openPrice).reshape(-1,1)
    
    #convert the x input rows of data fram into 2d array
    x_input = np.array(dataframe['open']).reshape(-1,1)
    y_output = np.array(dataframe['high']).reshape(-1,1)

    return run_linearRegression(x_input,y_output,openPrice_array)


def predict_lowPrice(dataframe,current_open,current_high):
    
    predict_x_val = np.column_stack((current_open, current_high))
    #convert the x input rows of data fram into 2d array
    x_values = np.array(dataframe[['open','high']])
    y_values =  np.array(dataframe['low']).reshape(-1,1)

    return run_linearRegression(x_values, y_values,predict_x_val)


def replace_zeros(df):
    average_volume = df[df['volume'] != 0]['volume'].mean()
    df['volume'] = df['volume'].replace(0, average_volume)

    return df

def predict_volume(dataframe,open_price,high_price, low_price):

    # create a dataframe to predict the volume for today
    input_dataframe = {
        "open":[open_price],
        "high":[high_price],
        "low":[low_price]}
    input_dataframe = pd.DataFrame(input_dataframe)


    x_input_list = ['open','high','low']
    y_input = 'volume'
   
    predicted_volume =  randomForestAlgroithm(dataframe,input_dataframe,x_input_list,y_input,0)

    if predicted_volume < 5:
        return randomForestAlgroithm(dataframe,input_dataframe,x_input_list,y_input,1)
    

    return predicted_volume


def predict_close_price(dataframe,open_price,high_price,low_price,volume_total):

    #convert the x input rows of data fram into 2d array
    x_values = np.array(dataframe[['open','high','low','volume']])
    predict_close_x = np.column_stack((open_price,high_price,low_price,volume_total))

    # convert the y input rows into a 2d array
    y_values = np.array(dataframe['close']).reshape(-1,1)
    return run_linearRegression(x_values,y_values,predict_close_x)


def predict_prices():

    current_dir = os.path.dirname(__file__)
    monthlycsv_path = os.path.join(current_dir, "monthly_data.csv")


    data = pd.read_csv(monthlycsv_path)
    daily_dataFrame = pd.DataFrame(data)

    # flip the dataframe
    reversed_dataFrame = daily_dataFrame[::-1].reset_index()

    copy_dataframe = reversed_dataFrame.copy()

    #predict the open price
    curr_openPrice = predict_openPrice(copy_dataframe)
    
    #predict the highest price
    todays_high_price = predict_HighPrice(reversed_dataFrame,curr_openPrice)
    
   # predict the lowest price
    todays_low_price = predict_lowPrice(reversed_dataFrame,curr_openPrice,todays_high_price)

    #predict the total volume
    todays_volume = predict_volume(reversed_dataFrame,curr_openPrice,todays_high_price,todays_low_price)

    #predict the closing price    
    todays_closing = predict_close_price(reversed_dataFrame,curr_openPrice,todays_high_price,todays_low_price,todays_volume)

    return curr_openPrice, todays_high_price,todays_low_price,todays_volume[0],todays_closing
