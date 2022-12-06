from flask import Blueprint, render_template, url_for
from ..models import Newschicken, Newscow, Newspork, Disease_current
from sqlalchemy import func
import json
from pybo.functions import predict_price, GetAiCnt, GetAiData, GetCnt, GetData

bp = Blueprint('main', __name__, url_prefix='/')



# 메인페이지------------------------------------------------------------------------------------
@bp.route('/',  methods=["GET"])
def main():

    chicken_path = "pybo\static\json\chicken_predict_price.json"
    cow_path = "pybo\static\json\cow_predict_price.json"
    pork_path = "pybo\static\json\pork_predict_price.json"

    chicken_price = predict_price(chicken_path, 'p9_10')
    cow_price = predict_price(cow_path, 'yhat')
    pork_price = predict_price(pork_path, 'yhat')

    return render_template('base_index.html', chicken_price=chicken_price, cow_price=cow_price, pork_price=pork_price)



# 닭고기 페이지------------------------------------------------------------------------------------
@bp.route('/chicken',  methods=["GET"])
def base_generic1():
    case_cnt = GetAiCnt(Disease_current)
    showfive = GetAiData(Disease_current)
    
    return render_template('base_generic1.html', showfive=showfive, case_cnt=case_cnt)



# 소고기 페이지------------------------------------------------------------------------------------
@bp.route('/cow',  methods=["GET"])
def base_generic2():
    case_cnt = GetCnt(Disease_current,'소')
    showfive = GetData(Disease_current,'소')
   

    return render_template('base_generic2.html', showfive=showfive, case_cnt=case_cnt)



# 돼지고기 페이지------------------------------------------------------------------------------------
@bp.route('/pig',  methods=["GET"])
def base_generic3():
    case_cnt = GetCnt(Disease_current,'돼지')
    showfive = GetData(Disease_current,'돼지')

    return render_template('base_generic3.html', showfive=showfive, case_cnt=case_cnt)





# 닭고기 뉴스
@bp.route('/predictchicken', methods=['GET'])
def predictChicken():
    news_chicken = Newschicken.query.all()

    # return render_template('predictChicken.html', news_chicken=news_chicken)
    return render_template('predictChicken.html', news_chicken=news_chicken)

# 소고기 뉴스
@bp.route('/predictcow', methods=['GET'])
def predictCow():
    news_cow = Newscow.query.all()

    return render_template('predictCow.html', news_cow=news_cow)

# 돼지고기 뉴스
@bp.route('/predictpork', methods=['GET'])
def predictPork():
    news_pork = Newspork.query.all()

    return render_template('predictPork.html', news_pork=news_pork)




# 백엔드에서 base.html 접근용
@bp.route('/base', methods=["GET"])
def base():
    return render_template('base.html')