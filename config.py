"""
Welcome to the ReeDistribute app
To Do:
    *Attempt to keep it PEP-8 style
    *write a better intro here
    *annotations
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))



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
ADMINS = ['d']

# pagination
POSTS_PER_PAGE = 50
MAX_SEARCH_RESULTS = 50

#test data
# RQST = [(title="test title",desc="this is a fake request", amtNeeded=100, author="me", published="today"), (title="testing again",desc="one more", amtNeeded=150, author="him", published="yesterday"), (title="this","another", amtNeeded=50, author="me", published="08-01-05")]
