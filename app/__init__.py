from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Allows localhost
allowed_origins = [
    'http://localhost:5173',
    'http://localhost:8080',
]

render_url = os.environ.get('RENDER_EXTERNAL_URL')
if render_url:
    allowed_origins.append(render_url)

CORS(app, supports_credentials=True, origins=allowed_origins)

from . import views, models