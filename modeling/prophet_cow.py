from prophet import Prophet
from prophet.serialize import model_to_json

import pandas as pd
import pymysql
import datetime

data = pd.read_csv('../pybo/static/소고기가격.csv', index_col=0)

mydb = pymysql.connect(
    host='localhost',
    user='root',
    password='0000',
    db='price',
    charset='utf8'
)

cursor = mydb.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * FROM price.cow ORDER BY 1 DESC LIMIT 5")
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
data.to_csv('../pybo/static/소고기가격.csv')

data = data[['date', '도매가격']]
data = data.rename(columns=({'date': 'ds', '도매가격': 'y'}))

Gujeyeok = pd.DataFrame({
    'holiday': 'Gujeyeok',
    'ds': pd.to_datetime(['2017-02-07', '2017-02-09', '2017-02-13',
                          '2017-02-14', '2018-03-27', '2018-04-03',
                          '2019-01-28', '2019-01-29', '2019-01-31'
                          ]),
    'lower_window': 0,
    'upper_window': 1,
})

m = Prophet(holidays=Gujeyeok, changepoint_range=0.9,
            changepoint_prior_scale=0.5, yearly_seasonality=20)
m.add_seasonality(name='monthly', period=30, fourier_order=5)
m.add_country_holidays(country_name='KR').fit(data)
future = m.make_future_dataframe(periods=28)
forecast = m.predict(future)

forecast["ds"] = forecast["ds"].dt.strftime("%Y-%m-%d")
forecast = forecast[['ds', 'yhat']].tail(28)
forecast.reset_index(drop=True, inplace=True)

# 데이터 저장
with open('../pybo/src/cow_model.json', 'w') as fout:
    fout.write(model_to_json(m))
forecast.to_csv('../pybo/src/predict_cow_price.csv')
forecast.to_json('./pybo/src/cow_predict_price.json',
                 orient='records', date_format='iso')
print(forecast)
