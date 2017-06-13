# Stripe Subscriptions #
- _this will show how to set up basic recurring bill for donors_
	[sub quickstart](https://stripe.com/docs/subscriptions/quickstart)
	[sub FAQ](https://support.stripe.com/search?q=subscriptions)
## Steps ##
1. **define a plan**: how much should be billed, what interval
2. **create a customer** in stripe account
3. **subscribe** customer to plan 

- You only need to *define the plan* once, steps **2** and **3** will be executed for each new customer 

############################################

### 1.) Define a plan ### 
- the plans will be objects 
	* representing a set _cost, currency, billing cycle_
- we may need to set up different plans
	* __look into maybe making it so people can make their own plans?__
- this is what a basic plan from the API will look like:
~~~~
- _Set your secret key: remember to change this to your live secret key in production
- _See your keys here: https://dashboard.stripe.com/account/apikeys_

stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

plan = stripe.Plan.create(
  name="Basic Plan",
  id="basic-monthly",
  interval="month",
  currency="usd",
  amount=0,
)

~~~~

- each plan requires a **unique ID**
- we will provide the ID value in API requests when we subscribe a customer to the plan 

### 2.) Create a customer ###
- **customers as _Stripe_ objects** represent the actual customers
	* provide easy way to process their payments
	* we will probably store metadata on customer object, ie _email address_
- we can create the customers with or without stored payment method, like  a credit card or bank acount 
- this code creates **customer obj** via the API _without_ stored payment method:
~~~~
# Set your secret key: remember to change this to your live secret key in production
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

customer = stripe.Customer.create(
  email="jenny.rosen@example.com",
)
~~~~

- Then _Stripe_ will return a new **Customer** object with details of Customer:
~~~~
{
  "id": "cus_4fdAW5ftNQow1a",
  "object": "customer",
  "account_balance": 0,
  "created": 1497386064,
  "currency": null,
  ...
  "livemode": false,
  "email": "jenny.rosen@example.com",
  ...
}
~~~~

- Once we have created the customer, we can store the **id** value in our **database** (hannah?)
	* this is where the email address will definitely be stored, whether secret or not, we can look more into that
	* this particular call shows that this **Customer** object doesn't have payment source or a sub. 


### 3.) Subscribe the customer to the plan ###
- Here, we will createt he subscription by associating the plan with the customer, like so:
~~~~
# Set your secret key: remember to change this to your live secret key in production
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

stripe.Subscription.create(
  customer=customer.id,
  plan="basic-monthly",
)
~~~~ 
- _note the plan is now set to basic monthly, and we are using Stripe object for customer IDs_ 
- This code shows that we now have a customer subscribed to a plan, yay! 
	* "behind the scenes" _Stripe_ creates an [invoice](https://stripe.com/docs/api#retrieve_invoice) for every billing cycle
		- that means what the customer owes, what they are charged, tracks payment status etc...
		- stuff that the customer should be told every time they pay basically 
		- we can also add a ton of other [info](https://stripe.com/docs/api#create_invoiceitem) to the invoice 
- Now, since subscription stuff happens automatically (usually monthly) we will have to establish something called [webhooks](https://stripe.com/docs/subscriptions/webhooks) which I will create a .md for later
	* seems to be mostly used to be notified of events as they occur


### The subscription object! ###
- **Attributes** _some of these we will not use, but it is good to know what is accesible 
	* 'id' _string_
		- unique identifier for the **object**
	* 'objects' _string where value is "subscription"
		- reps the objects type. Objects of same type have same value
	* 'application_fee_percent' _decimal_
		- btwn 0-100
		- represents percentage of sub invoice subtotal that will be transferred to application owner's _Stripe_ account
		- _I would like to look further into what exactly this means_	
	* 'cancel_at_period_end' _boolean_
		- if `at_period_end` flag set to `True` then `cancel_at_period_end` on sub will be true.
		- we use this attribute to determine whether a subscription with a status of active is scheduled to be canceled at end of current period	
	* 'canceled_at' _timestamp_
		- if sub has been canceled, this shows when then happened	
	* 'created' _timestamp_
		- when object was created
		- measured in seconds	
	* 'current_period_end' _timestamp_
		- end of the current period that the subscription has been invoiced for
		- at the end of this period a **new invoice will be created**	
	* 'current_period_start' _timestamp_
		- start of current period that subscription has been invoiced for	
	* 'customer' _string_
		- ID of customer who owns the subscription
		- this is _**expandable**_	
	* 'items' _list_
		- _there are many child attributes for this which I will get into later_
	* 'metadata' _hash_
		- set the key/value pairs that you can attach to an object
		- useful for storing additional info about object in structured format	
	* 'plan' _hash_ (see plan object)
		- hash describing the plan the customer is subscribed to (database this??)	
	* 'quantity' _integer_
		- ex: $10 a month 
		- this is a bit more complicated than that and once again, I'll go into further detail with 	
	* 'start' _timestamp_
		- date of most recent update to this sub
	* 'status' _string_
		- possible values:
			* `trialing`
			* `active`
			* `past_due`
			* `canceled`
			* `unpaid`
			* `trialing` when in trial, and
			* `active` when trial period is over

### Create a subscription ###
__this creates a new sub on existing customer__
- **definition:**
~~~~
stripe.Subscription.create()
~~~~
- **example request**
~~~~
import stripe
stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

stripe.Subscription.create(
  customer="cus_Aq2WzpEWn7CA5T",
  plan="diamond-freelance-396"
)
~~~~
- **Arguments**
	* 'customer' (**required**)
	* 'metadata' (**optional**)
		- set of key/value pairs that you can attach to a sub object
		- useful for storing addtl. info about sub format 
		- you can unset an individual key by setting its value to `None` and saving
		- to clear all keys, set metadate to `None`
	* 'plan' (**optional**)
		- identifier of the plan to subscribe the customer to
		- obviously optional because subs are optional 
	*  quantity (**optional**)
		- a little confusing so I'm just gonna copy and past what _Stripe_ says:
		>> The quantity you’d like to apply to the subscription you’re creating. For example, if your plan is 10/user/month, and your customer has 5 users, you could pass 5 as the quantity to have the customer charged 50 (5 x 10) monthly. If you update a subscription but don’t change the plan ID (e.g. changing only the trial_end), the subscription will inherit the old subscription’s quantity attribute unless you pass a new quantity parameter. If you update a subscription and change the plan ID, the new subscription will not inherit the quantity attribute and will default to 1 unless you pass a quantity parameter.
	* source (**optional _dictionary_**)
		- source can be a **token** like the ones returned by **Elements** or a **dictionary** containing a user's credit card details (with more options)
		- you must provide a source if customer does not already have a valud source attached and you are subscribing customer for a plan that isn't free
		- passing `source` will create new source _object_, make it customers default source, and delete old customer default if it exists 
		- many more arguments that go into this which I can talk about later

#### Returns ####
-_newly created sub object if the call succeeded_
- if customer has no card, this call raises an error
	* error handling is a whole other issue

#### Retrieve a subscription ####
- **Arguments**
	*id (**required**)
		- ID of sub to retrieve
	* **example request**
	~~~~
	import stripe
	stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

	stripe.Subscription.retrieve("sub_AHqpku1ywVSpkL")
	~~~~
- **Returns**
	* returns the subscription object
	* **example response**

	~~~~
<StripeObject subscription id=sub_AHqpku1ywVSpkL at 0x00000a> JSON: {
  "id": "sub_AHqpku1ywVSpkL",
  "object": "subscription",
  "application_fee_percent": null,
  "cancel_at_period_end": false,
  "canceled_at": 1489503617,
  "created": 1489503614,
  "current_period_end": 1521039614,
  "current_period_start": 1489503614,
  "customer": "cus_AHqpPMOMwJLp0j",
  "discount": null,
  "ended_at": 1489503617,
  "items": {
    "object": "list",
    "data": [
      {
        "id": "si_19xH8E2eZvKYlo2CR1u1heAY",
        "object": "subscription_item",
        "created": 1489503614,
        "plan": {
          "id": "44bbf6da-0b63-4f54-bb2a-7988a6fbeeb6",
          "object": "plan",
          "amount": 665830,
          "created": 1489503611,
          "currency": "chf",
          "interval": "year",
          "interval_count": 1,
          "livemode": false,
          "metadata": {
          },
          "name": "test plan",
          "statement_descriptor": null,
          "trial_period_days": null
        },
        "quantity": 1
      }
    ],
    "has_more": false,
    "total_count": 1,
    "url": "/v1/subscription_items?subscription=sub_AHqpku1ywVSpkL"
  },
  "livemode": false,
  "metadata": {
  },
  "plan": {
    "id": "44bbf6da-0b63-4f54-bb2a-7988a6fbeeb6",
    "object": "plan",
    "amount": 665830,
    "created": 1489503611,
    "currency": "chf",
    "interval": "year",
    "interval_count": 1,
    "livemode": false,
    "metadata": {
    },
    "name": "test plan",
    "statement_descriptor": null,
    "trial_period_days": null
  },
  "quantity": 1,
  "start": 1489503614,
  "status": "canceled",
  "tax_percent": null,
  "trial_end": null,
  "trial_start": null
}
	~~~~









