from flask import Blueprint, render_template, url_for
from ..models import Newschicken, Newscow, Newspork

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
