# Database:     
## Start making sense 
## Set up for running ReeDistribute
### In English:
1. Open and activate a venv
2. Install stripe, flask, sqlalchemy, flask-sqlalchemy, psycopg2
3. In psql create a database named rd.
4. Set the Private and public keys
5. Set the enviornent variable FLASK_APP to app.py
6. Run!
	* to be able to run you must remember to include the lines to start the session, "s = db.get\_session()" and the line to create the database and schema, "schema.start\_db()".
    * also remember to import db, controls and schema! After that you can call any function as you would a normal python function (no session work)

### In Powershell:
1. python -m venv ReeDistribute
2. scripts/activate
3. psql -U postgres
 * DROP DATABASE rd;
 * CREATE DATABASE rd;
 * \q;  
4. python -m install stripe
5. python -m install flask
6. python -m install sqlalchemy
7. python -m install flask-sqlalchemy
8. python -m install psycopg2
9. $env:PUBLISHABLE_KEY='pk_test_6pRNASCoBOKtIshFeQd4XMUh'
10. $env:SECRET_KEY='sk_test_BQokikJOvBiI2HlWgH4olfQ2'
11. $env:FLASK_APP='app.py'
12. python -m flask run

### In OS:
1. I am sorry, Macs scare me
2. Please someone who speaks Mac write this

## The Controls

#### create_student(username, name, password, email, token)
>This function takes 5 strings, opens a session, creates student and related account for the student, and finally closes the session. 
>Token defaults to "".
>No return value

#### create_donor(username, password, email, token)
>This function takes 5 strings, opens a session, creates a donor and related account for the donor, and finally closes the session.
>Token defaults to "".
>No return value

#### open\_request(student\_id, amount, reason, title, anon)
>This function takes an integer, a float, two strings and a boolean (in that order), opens a database session to create the request and then closes the session.
>title defaults to "Donate to a Reedie in needie", anon defaults to True.
>No return value

#### donate(request\_id, donor\_id, amount, account\_token)
>This function takes the integer id of the request, then the donor, a float of how much the donor wishes to donate and the account token of the donor to update the database.
>No defaults
>No return value

#### get\_id(username)
>This function takes a username and returns the id of the account which the username belongs to.
> Returns the integer account.id

#### get\_student\_id(username)
>This function takes a username and returns the id of the student which the username belongs to.
> Returns the integer student.id

#### get\_donor\_id(username)
>This function takes a username and returns the id of the donor which the username belongs to.
> Returns the integer donor.id

#### get\_student\_name(student.id)
>This function takes a student's id and returns the associated username.
> Returns the string student.name

#### update\_account\_token(username, token)
>This function takes the username and stripe token as strings and updates the account to hold the new account token
>No return value

#### request_info()
>This returns a list of lists which enables us to create the html for the request cards.
>Returns a list of lists in the following form [[L1],...,[Ln]] for a list of n elements where Lx = [name, amount\_needed, amount\_filled, title, description, id] for the xth row.

#### Authenticate(usernameAttempt, passwordAttempt)
>This function takes two strings and authenticates the user if they are stored in our database
>Returns a boolean, True if the user exists, False otherwise


### Tests  
#### I will not bother explaining the test functions since they should be removed before the final product and do not need to be accessed except (obviously) for testing purposes

### If more functions need to be written
The format of these functions is as follows:

def function_name(var1, ...):

* s = db.get_session()
* object = s.query(ObjectType).get(id)
* do things to object
* s.flush()   (optional)  
* do another thing to object?
* s.commit()
* s.close

#### Notice:
1. You must open and close the session. Otherwise things _will_ get confusing.
2. You must commit the session before you close it. Flush will push the changes to the database, but not save them outside of the session. A commit will save to the session.
3. Queries are annoying. You can format them a few ways, the ones I have had success with are: 

> s.query(className).get(object.id)
> to retrieve a specific object for which you have the id
> or
> s.query(class\_name).filter(object.variable == desired\_variable).first()
> used to find an entry with the specific trait defined in the filter parenthesis (it can be any boolean statement about the desired object, but will return whichever first makes the boolean statement True.


Just make sure you actually have the object for the row or you may not be changing things
4. Attributes from objects are accessed by the normal object syntax of object.attribute

## The Schema:
>To make database use easier, the following is an overview of the database's schema.  
>There are two types of classes, the Mixin classes and the table classes. Mixins always end with Mixin, these are basic types which act as parent classes to all of the table classes. The rest of the classes are Tabels to store information in the database.
### Mixins
#### IdPrimaryKeyMixin
>This Mixin creats a unique id key for each object to make them accessible to the database. The unique database key enables us to more easily execute queries, and prevents any table from having repetitivly named rows (ex. two accounts may store the same name, password, etc. but NEVER the same id).
#### DateTimeMixin  
>This Mixin stores the time of creation for each object and the time it was last updated. These will be especially helpful for putting requests in an order and quering them by time.
### Tables
#### accounts: the Account table
>This table will be used to store account data for both the donors and LSES student accounts.
  
##### Columns:

 * username: a string
 * password: a string
 * name: any string, does not need to be your legal name
 * email: a string, mandatory
 * account_token: a string of the stripe account token, stored after first donation 
 * admin: a boolean to grant admin privileges 

#### students: the Student table
>This table will be used to store the LSES student data.

##### Columns:

 * related_account: Integer which holds the ID of the account which stores this users account information.
 * open_requests: Integer, the number of current open requests from the student. This can be used to see if student need is being met.
 * closed requests: Integer, the number of current closed requests from the student. This can be used to see if student need is being met.
 * gained\_money: Float, the amount of money that this student has received through this account. Can be used to see how much money is going through the _ReeDistribute_ webapp.
 * approved: a boolean which will show if the student account has been approved to collect donations from the website (if false, funds should be withheld).
 
#### donors: the Donor table
>This table will store information about the accounts which donate to the _ReeDistribute_ webapp.

##### Columns:
 
  * related_account: Integer which holds the ID of the account which stores this users account information.
  * donations_given: Integer which stores the number of donations the donor has given
  * money_given: Float which represents how much money this donor has donated.

#### requests: the Request table
>This tables stores all of the request information to enable us to display requests so money can be given.

###### Columns:

  * requested\_by: Integer which holds the ID of the student (_not the account_)which created the request
  * amount_needed: a Float, of how much money is needed, displayed on the request
  * title: String, which will be displayed on the request
  * description: String, which will be displayed on the request
  * amount_filled: Float, used to see how much left of the request needs to be filled
  * anon: boolean, to see if we should post the request anonymously
  * filled: boolean which is true after the request has been fully covered

#### donations: the Donation table
>This table is used to store all of the donation information to help transfer money and help prove the validity of our transactions

##### Columns:

* to_request: Integer for the id of the request which the donor hopes to give to.
* from_donor: Integer referring to id of the donor who is giving money 
* amount_given: Float of the total which os being given
* charge_token: Stripe token to complete transaction
* anon: boolean to represent if the user wants to give anonymously or not.

