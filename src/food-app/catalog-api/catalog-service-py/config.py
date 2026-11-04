import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "food.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH_ENABLED = os.getenv('AUTH_ENABLED', 'False').lower() == 'true'
    USE_SQLITE = os.getenv('USE_SQLITE', 'True').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
