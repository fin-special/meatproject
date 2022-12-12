from flask import Blueprint, render_template, url_for
from ..models import Newschicken, Newscow, Newspork, Disease_current
from sqlalchemy import func
import json
from pybo.functions import predict_price, GetAiCnt, GetAiData, GetCnt, GetData, predict_price_all
from crawling import cow_week_crawling, pork_week_crawling, chicken_week_crawling
from apscheduler.schedulers.background import BackgroundScheduler    # apscheduler 라이브러리 선언
import atexit
import time


bp = Blueprint('main', __name__, url_prefix='/')



# 메인페이지------------------------------------------------------------------------------------
@bp.route('/',  methods=["GET"])
def main():

    chicken_path = "pybo\static\json\chicken_predict_price.json"
    cow_path = "pybo\static\json\cow_predict_price.json"
    pork_path = "pybo\static\json\pork_predict_price.json"

    chicken_price = format(predict_price(chicken_path, 'p9_10'), ',d')
    cow_price = format(predict_price(cow_path, 'yhat'), ',d')
    pork_price = format(predict_price(pork_path, 'yhat'), ',d')

    return render_template('base_index.html', chicken_price=chicken_price, cow_price=cow_price, pork_price=pork_price)

# About Us 페이지----------------------------------------------------------------------------------
@bp.route('/aboutus', methods=["GET"])
def aboutus():
    return render_template('aboutus.html')


# 닭고기 페이지------------------------------------------------------------------------------------
@bp.route('/chicken',  methods=["GET"])
def base_generic1():
    case_cnt = GetAiCnt(Disease_current)
    showfive = GetAiData(Disease_current)
    news_chicken = Newschicken.query.all()
    chicken_path = 'pybo\static\json\chicken_predict_price.json'

    chicken_price_5_6 = predict_price_all(chicken_path, 'p5_6')
    chicken_price_7_8 = predict_price_all(chicken_path, 'p7_8')
    chicken_price_9_10 = predict_price_all(chicken_path, 'p9_10')
    chicken_price_11 = predict_price_all(chicken_path, 'p11')
    chicken_price_12 = predict_price_all(chicken_path, 'p12')
    chicken_price_13_16 = predict_price_all(chicken_path, 'p13_16')
    
    return render_template('base_generic1.html', showfive=showfive, case_cnt=case_cnt, news_chicken=news_chicken,
    chicken_price_5_6=chicken_price_5_6, chicken_price_7_8=chicken_price_7_8, chicken_price_9_10=chicken_price_9_10,
    chicken_price_11=chicken_price_11, chicken_price_12=chicken_price_12, chicken_price_13_16=chicken_price_13_16)



# 소고기 페이지------------------------------------------------------------------------------------
@bp.route('/cow',  methods=["GET"])
def base_generic2():
    case_cnt = GetCnt(Disease_current,'소')
    showfive = GetData(Disease_current,'소')
    news_cow = Newscow.query.all()
    cow_path = 'pybo\static\json\cow_predict_price.json'

    cow_price = predict_price_all(cow_path, 'yhat')

    return render_template('base_generic2.html', showfive=showfive, case_cnt=case_cnt, news_cow=news_cow, cow_price=cow_price)



# 돼지고기 페이지------------------------------------------------------------------------------------
@bp.route('/pig',  methods=["GET"])
def base_generic3():
    case_cnt = GetCnt(Disease_current,'돼지')
    showfive = GetData(Disease_current,'돼지')
    news_pork = Newspork.query.all()
    pork_path = 'pybo\static\json\pork_predict_price.json'

    pork_price = predict_price_all(pork_path, 'yhat')

    return render_template('base_generic3.html', showfive=showfive, case_cnt=case_cnt, news_pork=news_pork, pork_price=pork_price)



# 백엔드에서 base.html 접근용-------------------------------------------------------------------------
@bp.route('/base', methods=["GET"])
def base():
    return render_template('base.html')


# 테스트용 페이지------------------------------------------------------------------------------------
@bp.route('/test',  methods=["GET"])
def test():
    case_cnt = GetAiCnt(Disease_current)
    showfive = GetAiData(Disease_current)
    news_chicken = Newschicken.query.all()
    
    chicken_path = 'pybo\static\json\chicken_predict_price.json'

    chicken_price_5_6 = predict_price_all(chicken_path, 'p5_6')
    chicken_price_7_8 = predict_price_all(chicken_path, 'p7_8')
    chicken_price_9_10 = predict_price_all(chicken_path, 'p9_10')
    chicken_price_11 = predict_price_all(chicken_path, 'p11')
    chicken_price_12 = predict_price_all(chicken_path, 'p12')
    chicken_price_13_16 = predict_price_all(chicken_path, 'p13_16')
    
    return render_template('structure_test.html', showfive=showfive, case_cnt=case_cnt, news_chicken=news_chicken,
    chicken_price_5_6=chicken_price_5_6, chicken_price_7_8=chicken_price_7_8, chicken_price_9_10=chicken_price_9_10,
    chicken_price_11=chicken_price_11, chicken_price_12=chicken_price_12, chicken_price_13_16=chicken_price_13_16)


#백엔드에서 가축발병현황 자동 크롤링
@bp.route("/backend", methods=["GET", "POST"])
def now():
    return time.strftime("%A, %d. %B %Y %I:%M:%S %p")

def crawl_interval():


    sched = BackgroundScheduler(daemon=True, timezone="Asia/Seoul")

#     sched.add_job(func=chicken_week_crawling, trigger='interval', seconds=3)
#     sched.add_job(func=cow_week_crawling, trigger='interval', seconds=3)
#     sched.add_job(func=pork_week_crawling, trigger='interval', seconds=3)

    sched.add_job(func=chicken_week_crawling, trigger='cron', week='1-53', day_of_week='6', hour='21')
    sched.add_job(func=cow_week_crawling, trigger='cron', week='1-53', day_of_week='6', hour='21')
    sched.add_job(func=pork_week_crawling, trigger='cron', week='1-53', day_of_week='6', hour='21')
#     sched.start()
#     atexit.register(lambda: sched.shutdown())




 











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



