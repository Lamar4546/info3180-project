import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    _db_url = os.environ.get('DATABASE_URL', 'sqlite:///driftdater.db')
    SQLALCHEMY_DATABASE_URI = _db_url.replace('postgres://', 'postgresql://')
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False