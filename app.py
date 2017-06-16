"""
Welcome to the ReeDistribute app

To Do:
    *Attempt to keep it PEP-8 style
    *write a better intro here
    *annotations
"""
import os

from flask import Flask, render_template, render_template_string, request
import stripe

from controls import (create_student, create_donor, open_request,
                        authenticate, get_id, get_student_id,
                        get_donor_id, request_info, update_account_token)
import Schema
import db


app = Flask(__name__)
# app.debug = True 

stripe_keys = {
  "secret_key": os.environ["SECRET_KEY"],
  "publishable_key": os.environ["PUBLISHABLE_KEY"]
}

stripe.api_key = 'sk_test_FVIT9u4L0pYiMHguHr3aL5ZK'



@app.route("/", methods=["GET"])
def make_cards():
    # Front page, displays the request cards
    # If there is a better way to do this, please show me -H
    start = '{% extends "basic.html" %} {% block content %} '
    card = '<div class="card"><div class="container"><h4><b> %s, </b> %s</h4><p>$ %d</p><div id="myProgress"><div id="myBar" style="width: %f">%f</div></div> <p> %s </p><a href="/log_donation/%d"> HELP OUT</a></div></div>'
    end = '{% endblock %}'
    allCards = ''
    info = request_info()
    for request in info:
        percent_filled = (request[2]/request[1])*100
        if percent_filled >= 100: percent_filled = 100
        allCards += card % (request[3], request[0], request[1], percent_filled, percent_filled, request[4], request[5])
    return render_template_string(start+allCards+end)


@app.route("/log_donation/<ID>", methods=["POST", "GET"])
@app.route("/log_donation")
def get_donation_info(ID=None):
    if ID: message = "For Request # %s" %(ID)
    else: message = "For the Low SES community" 
    return render_template("donation.html", info=message)

    
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
# Since we as of now are not implementing user sessions, this is not needed
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
def charge():
    howMuch=request.form["amt"] #multiply by 100 or stripe thinks we are talking cents
    usernameAttempt=request.form["uname"]
    passwordAttempt=request.form["psw"]
    result = authenticate(usernameAttempt, passwordAttempt)
    howMuch += '.00'
    if result: 
        # Create a Customer:
        customer = stripe.Customer.create(
            email="paying.user@example.com",
            # source=request.form["stripeToken"]
            )

        # Charge the user's card:
        charge = stripe.Charge.create(
            # customer=customer.id,
            amount=howMuch,
            currency="usd",
            description="ReeDistribute Charge"
        )
        # update_account_token(usernameAttempt, customer)
        
        # eventually replace with donate and a stripe confirmation
        # with open("database3.txt","w+") as f:
        #     f.write("Customer ID: " + str(customer.id) + "\n" + "Amount Charged: " + str(charge.amount)
        #     +"\n" + "email: " + str(customer.email))
        #     print(f)
        #     #this prints any information we may want to store onto a .txt file
        #     #right now, customer-id,amount,email
        return render_template("LSESdonation.html", amount=howMuch )
        
    else: return render_template("loginFailure.html")


@app.route("/charge")
def payment():
    return render_template("charge.html")  

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


    


if __name__ == "__main__":
    schema.start_db()
    
    app.run(debug=True)
