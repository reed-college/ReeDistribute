# Stripe API Notes and Planning
## Things we need to do, look into, questions, etc...

### integrate checkout
    [CHECKOUT TUTORIAL](https://stripe.com/docs/checkout/tutorial)
    - enable HTTPS on checkout page
    [ENABLING HTTPS](https://stripe.com/docs/checkout#does-checkout-require-https)
    - stripe returns token to Checkout or error message. Takes returned token and stores it in pages **PRIMARY FORM** (the one surrounding the script tag in the checkout-tutorial link)
    - checAkout then submits the form to the server 
    - the **SERVER** uses the posted token to charge the card
        - [CHARGES DOCUMENTATION](https://stripe.com/docs/charges)

### create charges 
    [CHARGES DOCUMENTATION](https://stripe.com/docs/charges)
    - happens after you have securely _collected_ and _tokenized_ customers credit card using **CHECKOUT**
    - charge attempts are made from your **SERVER **
        - normally using one of their **CLIENT LIBRARIES**
        [SEE: LIBRARIES](https://stripe.com/docs/libraries)
        - we have `pip install stripe`
        - this will be done on **python** then
    - from there, do a simple **API call** to charge the card (check [here](https://stripe.com/docs/charges) to see python code)
    - you automatically receive money in TWO DAYS(**?**)

####  SAVING CREDIT CARD DETAILS FOR LATER 
        - STRIPE TOKENS CAN ONLY BE USED **ONCE**
        - stripe provides a `CUSTOMER OBJECT TYPE` that will let us save this info for later use 
        - ALLOW CUSTOMERS TO UPDATE CARD INFO
        [API UPDATE CARD DOCS](https://stripe.com/docs/api#update_card)
            - to CHANGE CARD provide a token as a value for source and update the `CUSTOMER OBJECT`
            https://stripe.com/docs/api#update_customer
            - you can also [DELETE CARD](https://stripe.com/docs/api#delete_card)
 #####  STORING METADATA 
        - any metadata we choose to include will be viewable in the _Dashboard_ 
        - _example:_ Store's order ID can be attached to the charge used to pay for the order 

 #####  CAPTURING/AUTHORIZING 
        - don't completely understand but:
        - to authorize a payment without "capturing" it, make a charge request that also includes the `CAPTURE` parameter with a value of **FALSE**
            - tells Stripe to only authorize the amount on the customer's card
            - to settle an authorized charge, make a capture charge request
            [API CAPTURE CHARGE](https://stripe.com/docs/api#capture_charge)
            - the total authorized amount is captured by default and can't capture more than this
    - DYNAMIC STATEMENT DESCRIPTOR 
        - not _that_ important for right now but I'll get into that later 

###SOME NEXT STEPS:
    - [getting paid](https://stripe.com/docs/payouts)
    - [managing stripe account](https://stripe.com/docs/dashboard)
    - declines and failed payment
    - disputes overview
    - subscriptions quickstart


GETTING PAID
[PAYOUT DOCUMENTATION](https://stripe.com/docs/payouts)
    - your bank account info is required when activating your account
        - can update these details at any time at payout settings
        https://dashboard.stripe.com/account/payouts
    - make a payout schedule on dashboard 
    - look into payout failures 

MANAGING STRIPE ACCOUNT
https://stripe.com/docs/dashboard
    - managing multiple accounts
        - might be good for multiple requests and stuff, give LSES people access to main account and can make requests via multiple accounts 
    - can make additional Stripe accounts at any time, each of which operates independently from one another
    https://support.stripe.com/questions/stripe-account-for-multiple-projects



### GOING LIVE CHECKLIST!!
- steps to take
    - one related to the Stripe account
    [STRIPE ACCT CHECKLIST](https://stripe.com/docs/checklist#account)
    - one related to the Stripe integration
    [STRIPE INTEGRATION CHECKLIST](https://stripe.com/docs/checklist#integration)
- literally just look through [here](https://stripe.com/docs/checklist)

### QUESTIONS:
- what is [webhooks](https://dashboard.stripe.com/account/webhooks)
    - do we need it? 

### REPORTING:
[REPORTING DOCUMENTATION](https://stripe.com/docs/reporting)


### Applying filters
> "The balance history and account activity can be filtered to display results within a specified criteria. Use the Filter option, located at the top-left of the results, to view and apply the available filter options. Account activity with filtered results can also be exported to a CSV file, reducing the amount of data you need to work with.""






