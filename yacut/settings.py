import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    FLASK_APP = os.getenv('FLASK_APP', 'yacut')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    SECRET_KEY = os.getenv('SECRET_KEY', '1|adlib_air-max*-2')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        'SQLALCHEMY_TRACK_MODIFICATIONS', 'False',
    ).lower() == 'true'
