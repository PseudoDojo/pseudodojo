from flask import Flask
from flask_restful import Api
from .api import create_api

app = Flask(__name__)

api = Api(app)

create_api(api)

from app import routes
