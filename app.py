import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask, render_template, request, jsonify, templating, redirect, url_for
from flask_environments import Environments
import stripe

from controls import (create_account, approve_admin, approve_requesting, 
                    open_request,donate, account_id, update_account_token, 
                    request_info, request_info_who, approve_request, confirm)
 
import db
import schema
import json

from config import app, stripe_keys
from forms import PostForm


app = Flask(__name__)
env = Environments(app)
app.config.from_object('config.Development')
stripe.api_key = stripe_keys["secret_key"]

def current_user():
    m = app.config["MODE"]
    if m == "DEV": u = app.config["USER"]
    elif m == "PROD": u = request.env["REMOTE_USER"]
    
    return u

@app.route("/", methods=["POST"])
def main():
    return render_template("basic.html")


@app.route("/", methods=["GET", "POST"])
def make_cards():
    info=request_info()
    post = PostForm()
    return render_template("feed.html",post=post,key=stripe_keys["publishable_key"])


@app.route("/account_info", methods=["GET","POST"])
def account_info():
    info=request_info()
    name=current_user()
    post=PostForm()
    post2=PostForm()
    post2.filled()
    
    return render_template("test.html", name=name, post=post, post2=post2)

@app.route("/donate")
def get_donation_info(ID=None):
    return render_template("donation.html")

    
@app.route("/create_account")
def create_account():
    return render_template("addform.html")


@app.route("/record_account", methods=["POST"])
def add_account():
    username = current_user()

    activation_code=request.form["code"]
    name =request.form["name"]
    email=request.form["email"]
    res = confirm(email,activation_code)


    if res:
        create_student(username, name)
        return render_template("loginsuccess.html")
    else:
        return render_template("loginFailure") 



@app.route("/login")
# Since we as of now are not implementing user sessions, this is not needed
def log_in():
    return render_template("login.html")


@app.route("/are-you-real", methods=["POST"])
def check_credentials():
    u = request.form["uname"]
    # return render_template("basic.html")

    if (account_id(u) != None): 
        return redirect(url_for("make_cards"))
    else: 
        return render_template("login.html")


@app.route("/pay", methods=["POST"])
def index():
    return render_template("index.html",key=stripe_keys["publishable_key"])

@app.route("/charge", methods=["POST"])
def charge():
    bill=request.form.get("amount")
    email=request.form.get("source.customer.name")
    customer = stripe.Customer.create(
        source=request.form.get("stripeToken"),
        email=email
    )

    dollars_cents=bill.split(".")
    #amount comes in as a string, this is to make sure we can process amounts with or without decimals without ValueError
    if len(dollars_cents) > 2:
        #not yet sure what to do if this happens, but this would mean there is more than one decimal point which doesn't work
        print(dollars_cents)
    elif len(dollars_cents) == 2:
        #the length of the list we create from splitting will have 2 items if there is a decimal 
        dollars=int(dollars_cents[0])*100
        cents=int(dollars_cents[1])
        amount=dollars+cents
    else:
        amount=int(dollars_cents[0])*100

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency="usd",
        description="Donation"
    )

    #DB FUNCTIONS
    return render_template('charge.html', amount=str(amount), stripeEmail=email)

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
