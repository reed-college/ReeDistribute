"""
Welcome to the ReeDistribute app
To Do:
    *Attempt to keep it PEP-8 style
    *write a better intro here
    *annotations
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask, render_template, request, jsonify, templating
import stripe

from controls import (create_student, create_donor, open_request,
                        authenticate, get_id, get_student_id,
                        get_donor_id, request_info, update_account_token)
import schema
import db


stripe_keys = {
  "secret_key": os.environ["SECRET_KEY"],
  "publishable_key": os.environ["PUBLISHABLE_KEY"]
}

api_key = stripe_keys["secret_key"]

app = Flask(__name__)

# email server for later vvv
"""
MAIL_SERVER = ''  # our mailserver???
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
"""

# administrator list
ADMINS = ['example@example.com']

# pagination
POSTS_PER_PAGE = 50
MAX_SEARCH_RESULTS = 50