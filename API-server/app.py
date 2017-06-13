import os
from flask import Flask, render_template, request
import stripe

stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)

# Token is created using Stripe.js or Checkout!
# Get the payment token submitted by the form:
# token = POST['stripeToken'] # Using Flask


@app.route('/')
def index():
    return render_template('index.html',key=stripe_keys['publishable_key'])
    #index is an .html file which will give us the literal "donate" button
    #the information from index will be given to this file and passed thru server
@app.route('/charge', methods=['POST'])
def charge():
  amount=999
  #amt in cents
# Create a Customer:
  customer = stripe.Customer.create(
    anonymous = True ,
    #I'll look into this more, but will hopefully be able to make the stripe button so you can be anon 
    email="paying.user@example.com",
    source=request.form['stripeToken']
    )

# Charge the user's card, we do this thru server:
  charge = stripe.Charge.create(
    customer=customer.id,
    amount=amount,
    currency='usd',
    description="ReeDistribute Charge"
  )
# # receive Charge(???), no service, writing this blindly 
#   receive = stripe.???.create(
#     source = customer.source
#       #from which request
#     receive_acct = "routing number + acct number"
#       #idk, but recipient account 
#     amount = amount,

#     )
#   #########################################
  invoice = stripe.Invoice.create(
    anonymous = False,
    email = customer.email,
    description = charge.description
#   )
  # hannah, take a look at this print function, we can see how we want to actually send it to the database
  with open("database3.txt","w+") as f:
      f.write("Customer ID: " + str(customer.id) + '\n' + "Amount Charged (cents): " + str(charge.amount)
       +'\n' + "email: " + str(customer.email))
      print(f)
      #this prints any information we may want to store onto a .txt file
      #right now, customer-id,amount,email
      #would like to also use this to print simple thank you email 
  
  return render_template('charge.html',amount=amount)


if __name__ == '__main__':
    app.run(debug=True)


