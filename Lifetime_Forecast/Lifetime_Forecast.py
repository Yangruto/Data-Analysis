import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# features
def features_preparation(data, column):
    data['diff'] = data[column].diff()
    data['moving_avg'] = data[column].rolling(5, center=True, min_periods=1).mean()
    data['cumulate'] = data[column].cumsum()
    return data    

# get the diff >= 0
def partial_max(data, col, diff_col):
    partial_y = data.loc[data[diff_col] >= 0, col].to_list()
    partial_x = data.loc[data[diff_col] >= 0, col].index
    return partial_x, partial_y

def equation(x, a, b):
    return -(a * x + b * x * x)

def forecast(train_x, train_y):
    (a, b), pcov = curve_fit(equation, train_x, train_y)
    forecast_x = np.arange(len(data))
    forecast_y = equation(forecast_x, a, b)
    return forecast_x, forecast_y