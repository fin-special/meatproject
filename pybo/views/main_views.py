from flask import Blueprint, render_template, url_for
from ..models import Newschicken, Newscow, Newspork, Disease_current
from sqlalchemy import func
bp = Blueprint('main', __name__, url_prefix='/')

# 메인화면


@bp.route('/')
def home():

    return render_template('index.html')

# 닭고기 가격 예측 api


@bp.route('/predictchicken', methods=['GET'])
def predictChicken():
    news_chicken = Newschicken.query.all()

    # return render_template('predictChicken.html', news_chicken=news_chicken)
    return render_template('generic.html', news_chicken=news_chicken)

# 소고기 가격 예측 api


@bp.route('/predictcow', methods=['GET'])
def predictCow():
    news_cow = Newscow.query.all()

    return render_template('predictCow.html', news_cow=news_cow)

# 돼지고기 가격 예측 api


@bp.route('/predictpork', methods=['GET'])
def predictPork():
    news_pork = Newspork.query.all()

    return render_template('predictPork.html', news_pork=news_pork)

@bp.route('/ai_current_css', methods=["GET"])
def ai_current_css():
    case_cnt = Disease_current.query.filter(Disease_current.date >= func.ADDDATE(func.NOW(), -30)).count()
    showfive = Disease_current.query.filter(Disease_current.animal.like('닭%')).order_by(Disease_current.date.desc()).limit(5)
    return render_template('disease_current_css.html', showfive=showfive, case_cnt=case_cnt)

@bp.route('/base_test1',  methods=["GET"])
def base_test1():

    return render_template('base_test1.html')


@bp.route('/base_test2',  methods=["GET"])
def base_test2():
    case_cnt = Disease_current.query.filter(Disease_current.date >= func.ADDDATE(func.NOW(), -30)).count()
    showfive = Disease_current.query.filter(Disease_current.animal.like('닭%')).order_by(Disease_current.date.desc()).limit(5)
    return render_template('base_test2.html', showfive=showfive, case_cnt=case_cnt)