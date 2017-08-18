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


api_key = stripe_keys["secret_key"]

app = Flask(__name__)

class Config(object):
    DEBUG = False
    TESTING = False

class Development(Config):
    DEBUG = True
    DATABASE = 'rd'

class Production(Config):
    DATABASE = 'production_db'

# Email account and server info

# administrator list
ADMINS = ['d']

# pagination
POSTS_PER_PAGE = 50
MAX_SEARCH_RESULTS = 50
