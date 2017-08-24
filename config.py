import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask, render_template, request, jsonify, templating
import stripe


import schema
import db


stripe_keys = {
  "secret_key": os.environ["SECRET_KEY"],
  "publishable_key": os.environ["PUBLISHABLE_KEY"]
}
activation_code = os.environ["CODE"]
api_key = stripe_keys["secret_key"]

app = Flask(__name__)

class Config(object):
    DEBUG = False
    TESTING = False
    CODE = activation_code
    

class Development(Config):
    DEBUG = True
    DATABASE = 'rd'
    USER = os.environ["USERNAME"]
    MODE = "DEV"

class Production(Config):
    DATABASE = 'production_db'
    MODE="PROD"

# Email account and server info

# administrator list

# pagination
POSTS_PER_PAGE = 50
MAX_SEARCH_RESULTS = 50
