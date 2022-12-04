import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import pymysql
import datetime
from prophet import Prophet
from prophet.serialize import model_to_json

data = pd.read_csv('../pybo/static/돼지고기가격.csv', index_col=0)
data['date'] = pd.to_datetime(data['date'])

mydb = pymysql.connect(
    host='localhost',
    user='root',
    password='0000',
    db='price',
    charset='utf8'
)

cursor = mydb.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * FROM price.pork ORDER BY 1 DESC LIMIT 5")
result = cursor.fetchall()

df = pd.DataFrame(result)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date', ascending=True)

days_1 = pd.DataFrame(df['date'][-1:] + datetime.timedelta(days=1))
days_2 = pd.DataFrame(df['date'][-1:] + datetime.timedelta(days=2))
days = pd.concat((days_1, days_2))

df = pd.merge(df, days, on='date', how='outer')
df = df.fillna(method='ffill')

data = pd.concat((data, df), axis=0)
data['date'] = pd.to_datetime(data['date'])
data = data.sort_values(by='date', ascending=True)
data = data[-2220:]
data.to_csv('../pybo/static/돼지고기가격.csv')

data = data[['date', '도매가격']]
data = data.rename(columns=({'date': 'ds', '도매가격': 'y'}))

m = Prophet(changepoint_range=0.9, changepoint_prior_scale=0.25)
# m.add_seasonality(name='monthly', period=30.5, fourier_order=5)
m.add_country_holidays(country_name='KR').fit(data)
future = m.make_future_dataframe(periods=28)
forecast = m.predict(future)

forecast["ds"] = forecast["ds"].dt.strftime("%Y-%m-%d")
forecast = forecast[['ds', 'yhat']].tail(28)
forecast.reset_index(drop=True, inplace=True)

# 데이터 저장
with open('../pybo/src/pork_model.json', 'w') as fout:
    fout.write(model_to_json(m))
forecast.to_csv('../pybo/src/predict_pork_price.csv')
forecast.to_json('./pybo/src/pork_predict_price.json',
                 orient='records', date_format='iso')
print(forecast)
