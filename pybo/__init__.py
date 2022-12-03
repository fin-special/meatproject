from flask import Flask, render_template, jsonify, request
# from model import test_model as model
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_cors import CORS, cross_origin

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)
    
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