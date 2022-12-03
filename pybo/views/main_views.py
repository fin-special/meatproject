from flask import Blueprint, render_template
from ..models import Newschicken, Newscow, NewsPork
from prophet.serialize import model_from_json

import pandas as pd


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def home():
    chickennews = Newschicken.query.all()
    cownews = Newscow.query.all()
    porknews = NewsPork.query.all()

    # 닭고기 가격 예측 모델 api
    size = ["5_6", "7_8", "9_10", "11", "12", "13_16"]
    for i in size:
        with open(f'./pybo/src/chicken_{i}_model.json', 'r') as fin:
            model_chicken = model_from_json(fin.read())
        future_chicken = model_chicken.make_future_dataframe(periods=28)
        pred_chicken = model_chicken.predict(future_chicken)
        if i == "5_6":
            data1 = pred_chicken[['ds', 'yhat']][-28:]
            data1["ds"] = data1["ds"].dt.strftime("%Y-%m-%d")
            data1.rename(columns={"yhat": f"p{i}"}, inplace=True)
        else:
            data2 = pred_chicken[['ds', 'yhat']][-28:]
            data2["ds"] = data2["ds"].dt.strftime("%Y-%m-%d")
            data2.rename(columns={"yhat": f"p{i}"}, inplace=True)

            data1 = pd.merge(data1, data2, on="ds")
    data1.to_json('./pybo/src/chicken_price.json',
                  orient='records', date_format='iso')
    
    

    return render_template('index.html', chickennews=chickennews, cownews=cownews, porknews=porknews)
