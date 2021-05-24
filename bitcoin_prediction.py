# -*- coding: utf-8 -*-
"""bitcoin-prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1neobQacrCa0jf2eSCOOolxtkudmNqm4w
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/content/drive/')
# %cd /content/drive/My Drive/Colab Notebooks/

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from matplotlib import pyplot as plt

#Filtering the data to get the desired range
#Grouping the data using hourly timestamp and forward filling the NULL values

import datetime, pytz

def dateparse (time_in_secs):    
    return pytz.utc.localize(datetime.datetime.fromtimestamp(float(time_in_secs)))

data = pd.read_csv('bitstampUSD_1-min_data_2012-01-01_to_2021-03-31.csv',parse_dates=[0], date_parser=dateparse) 
data['Timestamp'] = data['Timestamp'].dt.tz_localize(None)
drop_row = data[ (data['Timestamp'] >= '2020-06-01 00:00:00') ].index
data.drop(drop_row, inplace = True)
drop_row = data[ (data['Timestamp'] < '2017-05-01 00:00:00')].index
data.drop(drop_row, inplace = True)



data = data.groupby([pd.Grouper(key='Timestamp', freq='H')]).first().reset_index()
data = data.set_index('Timestamp')
data = data[['Weighted_Price']]
data['Weighted_Price'].fillna(method='ffill', inplace=True)
data.head()
X1 = np.array(data.index)
X2 = np.array(data.iloc[:,0])
X1=X1.reshape(-1,1)
X2=X2.reshape(-1,1)

#print(X1)
#print(X2)

from sklearn.model_selection import train_test_split
input_vec_train,input_vec_test,output_label_y_train,output_label_y_test = train_test_split(X1,X2,test_size=0.1,random_state=0)
# print(input_vec_train)
# print(input_vec_test)
# print(output_label_y_train)
# print(output_label_y_test)

import matplotlib.pyplot as plt
fig = plt.figure(figsize=[20, 7])
plt.rc('font', size=18); plt.rcParams['figure.constrained_layout.use'] = True
plt.scatter(input_vec_train, output_label_y_train, color='red', marker='.', linewidth=0.1)

#Using KNN with uniform weight
from math import sqrt
from sklearn import metrics


fig = plt.figure(figsize=[20, 7])
plt.rc('font', size=18); plt.rcParams['figure.constrained_layout.use'] = True

from sklearn.neighbors import KNeighborsRegressor
model = KNeighborsRegressor(n_neighbors=7).fit(input_vec_train, output_label_y_train)
ypred = model.predict(input_vec_test)
#print(ypred)
RMSE = sqrt(metrics.mean_squared_error( output_label_y_test, ypred)) 
print('RMSE value of the KNN Model is:', RMSE)


MAPE = np.mean(np.abs((output_label_y_test - ypred)/output_label_y_test))*100
print('MAPE value of the KNN Model is:', MAPE)


import matplotlib.pyplot as plt
plt.rc('font', size=18); plt.rcParams['figure.constrained_layout.use'] = True
plt.scatter(input_vec_train, output_label_y_train, color='red', marker='.', linewidth=0.1)
plt.scatter(input_vec_test, ypred, color='blue', marker='.', linewidth=0.1)
plt.xlabel("input x"); plt.ylabel("output y")
plt.legend(['train','predictions'])



# Using Smoothing Splines
import rpy2.robjects as robjects
r_y = robjects.FloatVector(output_label_y_train)
r_x = robjects.FloatVector(input_vec_train)

r_smooth_spline = robjects.r['smooth.spline']
spline1 = r_smooth_spline(x=r_x, y=r_y, spar=0.5) # Changing the "spar" value effects how smooth the spline is => the larger the value the smoother (less accurate)

ySpline = np.array(robjects.r['predict'](spline1, robjects.FloatVector(input_vec_test)).rx2('y'))

from math import sqrt
from sklearn import metrics

RMSE = sqrt(metrics.mean_squared_error( output_label_y_test, ySpline))
print('RMSE value of the Smoothing Spline Model is:', RMSE)


MAPE = np.mean(np.abs((output_label_y_test - ySpline)/output_label_y_test))*100
print('MAPE value of the Smoothing Spline Model is:', MAPE)

import matplotlib.pyplot as plt
plt.rc('font', size=18); plt.rcParams['figure.constrained_layout.use'] = True
plt.scatter(input_vec_train, output_label_y_train, color='red', marker='.', linewidth=0.1)
plt.scatter(input_vec_test, ySpline, color='blue', marker='.', linewidth=0.1)
plt.xlabel("input x"); plt.ylabel("output y")
plt.legend(['train','predictions'])
plt.show()
