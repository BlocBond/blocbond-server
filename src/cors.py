from flask_cors import CORS
from src.app import app

CORS(app, supports_credentials=True)