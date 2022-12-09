from flask import Flask, render_template, jsonify, request
# from model import test_model as model
from flask_migrate import Migrate   
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_cors import CORS, cross_origin
from flask_ngrok import run_with_ngrok

# from apscheduler.schedulers.background import BackgroundScheduler
# from crawling import cow_week_crawling, pork_week_crawling, chicken_week_crawling

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)
    
    run_with_ngrok(app)
    
    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models
    
    # Blueprint
    from .views import main_views
    app.register_blueprint(main_views.bp)

    if __name__ == '__main__':
        app.run(debug=True)

    return app

# sched = BackgroundScheduler(daemon=True, timezone="Asia/Seoul")
# sched.add_job(func=chicken_week_crawling, trigger='interval', seconds=3)
# sched.add_job(func=cow_week_crawling, trigger='interval', seconds=3)
# sched.add_job(func=pork_week_crawling, trigger='interval', seconds=3)
# sched.start()

# app = Flask(__name__)

# # database
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@localhost:3306/test"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)
# db.init_app(app)

# @app.route('/hello')
# def hello_pybo():
#     return 'Hello, Pybo!'

# @app.route('/')
# def index():
#     return 'Pybo index'

# @app.route('/all')
# def select_all():
#     members = Members.query.all()
#     return render_template('templates/db.html', members=members)

# import pymysql
# pymysql.install_as_MySQLdb()