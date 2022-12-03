# import os

# BASE_DIR = os.path.dirname(__file__)

# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
# SQLALCHEMY_TRACK_MODIFICATIONS = False

# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@localhost:3306/test"
# SQLALCHEMY_TRACK_MODIFICATIONS = False

db = {
    'user'     : 'root',
    'password' : '0000',
    'host'     : '127.0.0.1',
    'port'     : '3306',
    'database' : 'price'
}

SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8" 
SQLALCHEMY_TRACK_MODIFICATIONS = False