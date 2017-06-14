"""
Welcome to the ReeDistribute app

To Do:
    *Attempt to keep it PEP-8 style
    *write a better intro here
    *annotations
"""
import os

from flask import Flask, render_template, request
import stripe

from controls import create_student, create_donor, open_request, authenticate, get_id, get_student_id, get_donor_id, request_info
import schema
import db


app = Flask(__name__)
app.debug = True 

stripe_keys = {
  "secret_key": os.environ["SECRET_KEY"],
  "publishable_key": os.environ["PUBLISHABLE_KEY"]
}

stripe.api_key = stripe_keys["secret_key"]


@app.route("/")
def home():
    """Display the homepage"""
    return render_template("basic.html")


@app.route("/log_donation")
def get_donation_info():
    return render_template("donation.html")


@app.route("/donate", methods=["POST"])
def submit_donation():
    amount=request.form["amt"]
    usernameAttempt=request.form["uname"]
    passwordAttempt=request.form["psw"]
    result = authenticate(usernameAttempt, passwordAttempt)
    if result: 
        return render_template("LSESdonation.html")
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

@app.route("/charge", methods=["POST"])
def charge():
  amount=999
  #amt in cents
# Create a Customer:
  customer = stripe.Customer.create(
    email="paying.user@example.com",
    source=request.form["stripeToken"]
    )

# Charge the user's card:
  charge = stripe.Charge.create(
    customer=customer.id,
    amount=amount,
    currency="usd",
    description="ReeDistribute Charge"
  )
  with open("database3.txt","w+") as f:
      f.write("Customer ID: " + str(customer.id) + "\n" + "Amount Charged (cents): " + str(charge.amount)
       +"\n" + "email: " + str(customer.email))
      print(f)
      #this prints any information we may want to store onto a .txt file
      #right now, customer-id,amount,email
  
  return render_template("charge.html",amount=amount)

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
    start = '{% extends "basic.html" %}\n{% block content %}'
    card = '<div class="card"> \n     <div class="container"> \n    <h4><b> %s </b></h4>\n    <p> %d</p>\n     <p> %s </p>\n  </div>\n <\div>\n'
    end = '{% endblock %}'
    allCards = ''
    info = request_info()
    for request in info:
        allCards += card % (request[0], request[1], request[3])
    return start+allCards+end
    


if __name__ == "__main__":
    schema.start_db()
    
    app.run(debug=True)
