import os

SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL', 'mysql+pymysql://user:pass@localhost/db')
SECRET_KEY = 'secretkey'
SQLALCHEMY_TRACK_MODIFICATIONS = False
