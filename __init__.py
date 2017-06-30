"""
Welcome to the ReeDistribute app
To Do:
    *Attempt to keep it PEP-8 style
    *write a better intro here
    *annotations
"""
import os

from flask import Flask, render_template, request, jsonify, templating
import stripe

from controls import (create_student, create_donor, open_request,
                        authenticate, get_id, get_student_id,
                        get_donor_id, request_info, update_account_token)
import schema
import db
"""
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, \
    MAIL_PASSWORD
"""
import app