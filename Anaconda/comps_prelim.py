import pandas as pd

mydata = pd.read_csv('CompsPrelim.csv')

x = mydata['ptau']
y = mydata['rbans']

print(x.corr(y))
