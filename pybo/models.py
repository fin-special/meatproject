# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()
from pybo import db

class Newschicken(db.Model):
    __tablename__ = 'news_chicken'
    # __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(500, 'utf8mb4_unicode_ci'), nullable=False)
    url = db.Column(db.String(200, 'utf8mb4_unicode_ci'), nullable=False)
    
    def __init__(self, title, url):
        self.title = title
        self.url = url

class Newscow(db.Model):
    __tablename__ = 'news_cow'
    # __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(500, 'utf8mb4_unicode_ci'), nullable=False)
    url = db.Column(db.String(200, 'utf8mb4_unicode_ci'), nullable=False)
    
    def __init__(self, title, url):
        self.title = title
        self.url = url

class Newspork(db.Model):
    __tablename__ = 'news_pork'
    # __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(500, 'utf8mb4_unicode_ci'), nullable=False)
    url = db.Column(db.String(200, 'utf8mb4_unicode_ci'), nullable=False)
    
    def __init__(self, title, url):
        self.title = title
        self.url = url

# 질병현황 테이블
class Disease_current(db.Model):
    __tablename__ = 'disease_current'
    date = db.Column(db.String(500, 'utf8mb4_unicode_ci'), nullable=False, primary_key=True)
    farm_nm = db.Column(db.String(500, 'utf8mb4_unicode_ci'), nullable=False, primary_key=True)
    addr = db.Column(db.String(500, 'utf8mb4_unicode_ci'), nullable=False)
    ds_nm = db.Column(db.String(500, 'utf8mb4_unicode_ci'), nullable=False)
    animal = db.Column(db.String(500, 'utf8mb4_unicode_ci'), nullable=False)

    def __init__(self, date, farm_nm, addr, ds_nm ,animal):
        self.date = date
        self.farm_nm = farm_nm
        self.addr = addr
        self.ds_nm = ds_nm
        self.animal = animal