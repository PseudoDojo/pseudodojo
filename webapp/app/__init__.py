from flask import Flask
from .config import Config

app = Flask(__name__)

# Not used currently, TODO delete?
# from flask_restful import Api
# from .api import create_api
# api = Api(app)
# create_api(api)

app.config.from_object(Config)

# Load dynamic configurations
Config.load_dynamic_config(app)

from app import routes
