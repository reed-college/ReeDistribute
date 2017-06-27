
"""
Welcome to the ReeDistribute app

To Do:
    *Attempt to keep it PEP-8 style
    *write a better intro here
    *annotations
"""
import os

from flask import Flask, render_template, request, jsonify
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

stripe.api_key = stripe_keys["secret_key"]

app = Flask(__name__)

@app.route("/")
def home():
    """Display the homepage"""
    return render_template("basic.html")


@app.route("/log_donation")
def get_donation_info():
    return render_template("donation.html")


@app.route("/donate", methods=["POST"])
def submit_donation():
    amount=request.form["amt"]*100 #multiply by 100 or stripe thinks we are talking cents
    usernameAttempt=request.form["uname"]
    passwordAttempt=request.form["psw"]
    result = authenticate(usernameAttempt, passwordAttempt)
    if result: 
        return render_template("LSESdonation.html", amount=amount )
    else: return render_template("loginFailure.html")
    
@app.route("/create_account")
def create_account():
    return render_template("addform.html")


@app.route("/record_account", methods=["POST"])
def add_account():
    username=request.form["username"]
    name =request.form["name"]
    email=request.form["email"]
    pw1 =request.form["pw1"]
    pw2 =request.form["pw2"]
    

    if (pw1 == pw2):
        create_student(username, name, pw1, email)

        return render_template("frontpage.html") 
    else: 
        return render_template("addform.html")


@app.route("/login")
def log_in():
    return render_template("login.html")


@app.route("/are-you-real", methods=["POST"])
def check_credentials():
    usernameAttempt = request.form["uname"]
    passwordAttempt = request.form["psw"]
    result = authenticate(usernameAttempt, passwordAttempt)
    if result: return render_template("loginsuccess.html")
    else: return render_template("loginFailure.html")

@app.route("/pay", methods=["POST"])
def index():
    return render_template("index.html",key=stripe_keys["publishable_key"])

@app.route("/charge", methods=["POST"])
def charge():
    amount=request.form["amount"]
    customer = stripe.Customer.create(
        source=request.form["stripeToken"]
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency="usd",
        description="Donation"
    )

    return render_template('charge.html', amount=amount)

@app.route("/open_request")
def make_request():
    return render_template("request.html")

@app.route("/submit-request", methods=["POST"])
def check_request():
    requiredmoney = request.form["amt"]
    reason = request.form["dscrp"]
    usernameAttempt = request.form["uname"]
    passwordAttempt = request.form["psw"]
    result = authenticate(usernameAttempt, passwordAttempt)
    if result: 
        ID = get_id(usernameAttempt)
        open_request(ID, amt, reason)
        return render_template("loginsuccess.html")
    else: return render_template("loginFailure.html") 

@app.route("/TEST")
def make_cards():
    # THough this is truly a mess
    # I wanted to show how request_info could be used
    start = '<html>\n<head>\n    <title>home</title>\n'
    card = '<div class="card"> \n     <div class="container"> \n    <h4><b> %s </b></h4>\n    <p> %d</p>\n     <p> %s </p>\n  </div>'
    end = '</body></html>'
    allCards = ''
    info = request_info()
    for request in info:
        allCards += card % (request[0], request[1], request[3])
    return start+allCards+end
    


if __name__ == "__main__":
    schema.start_db()
    
    app.run(debug=True)

