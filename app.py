import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask, render_template, request, jsonify, templating
import stripe

from controls import (create_student, create_donor, open_request,
                        authenticate, get_id, get_student_id,
                        get_donor_id, request_info, request_info_who, update_account_token)
import db
import schema
import json

from config import app, stripe_keys, app
from forms import PostForm
"""
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS...
"""
from urllib.parse import urlparse, urljoin
from werkzeug.contrib.atom import AtomFeed


stripe.api_key = stripe_keys["secret_key"]



@app.route("/", methods=["POST"])
def main():
    return render_template("basic.html")


@app.route("/", methods=["GET", "POST"])
def make_cards():
    info=request_info()
    post = PostForm()
    return render_template("feed.html",post=post,key=stripe_keys["publishable_key"])


@app.route("/log_donation/<ID>", methods=["POST", "GET"])
@app.route("/log_donation")
def get_donation_info(ID=None):
    if ID: message = "For Request # %s" %(ID)
    else: message = "ignor this page" 
    return render_template("donation.html", info=message)

    
@app.route("/create_account")
def create_account():
    return render_template("addform.html")


@app.route("/record_account", methods=["POST"])
def add_account():
    username=request.form["username"]
    name =request.form["name"]
    email=request.form["email"]
    pw1 =request.form["psw1"]
    pw2 =request.form["psw2"]
    

    if (pw1 == pw2):
        create_student(username, name, pw1, email)
        return render_template("loginsuccess.html") 
    else: 
        return render_template("addform.html")


@app.route("/login")
# Since we as of now are not implementing user sessions, this is not needed
def log_in():
    return render_template("login.html")


@app.route("/are-you-real", methods=["POST"])
def check_credentials():
    usernameAttempt = request.form["uname"]
    passwordAttempt = request.form["psw"]
    result = authenticate(usernameAttempt, passwordAttempt)
    # return render_template("basic.html")
    if result: 
        return render_template("loginsuccess.html")
    else: 
        return render_template("loginFailure.html")


@app.route("/pay", methods=["POST"])
def index():
    return render_template("index.html",key=stripe_keys["publishable_key"])

@app.route("/charge", methods=["POST"])
def charge():
    amount=request.form.get("amount")
    email=request.form.get("source.customer.name")
    customer = stripe.Customer.create(
        source=request.form.get("stripeToken"),
        email=email
    )


    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency="usd",
        description="Donation"
    )
    return render_template('charge.html', amount=amount, stripeEmail=email)

@app.route("/open_request")
def make_request():
    return render_template("request.html")

@app.route("/submit-request", methods=["POST"])
def check_request():
    title = request.form["title"]
    requiredmoney = request.form["amount"]
    usernameAttempt = request.form["username"]
    passwordAttempt = request.form["psw"]
    reason = request.form["description"]
    result = authenticate(usernameAttempt, passwordAttempt)
    if result:    
        ID = get_id(usernameAttempt)
        open_request(ID,requiredmoney,reason,title)
        return render_template("loginsuccess.html")
    else: 
        return render_template("loginFailure.html") 


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
    

if __name__ == "__main__":
    schema.start_db()
    
    app.run(debug=True)
