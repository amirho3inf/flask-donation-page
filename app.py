from flask import Flask
from config import Config
from webpay import WebpayAPI
from flask_migrate import Migrate
from importlib import import_module
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

webpay = WebpayAPI(app.config['WEBPAY_API_KEY'])
db = SQLAlchemy(app)
migrate = Migrate(app, db)


import_module('views')
import_module('models')
