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

    return render_template('index.html', chickennews=chickennews, cownews=cownews, porknews=porknews)
