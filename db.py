"""
This is the database for the webapp ReeDistribute
All information collected by this program remains anonymous
Everything that is stored is either for functionality or statistics to prove the site's valaccount_idity
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Boolean
from sqlalchemy import create_engine

Base = declarative_base() #Make it an OOP
engine = create_engine('postgresql://@localhost:5432/myDB', echo = True)

class Account(Base):
    """
    The main user class for ReeDistribute Login.abs
    Attributes: account_id (int), name (str), email (str), consumer_key (str), anon (int), admin (int)
    """
    __tablename__='accounts' #Store all account objects in accounts

    account_id = Column(Integer, primary_key=True, nullable = False) #The key value for account account_identification
    username = Column(String, nullable = False) #Account's chosen name, used for site personalization
    email = Column(String, nullable = False) #Account's email for contacting
    consumer_key = Column(String) #Account's Stripe coustomer key
    anon = Column(Integer) #If 0 then the account does not wish to remain anonymous for actions on the website
    admin = Column(Integer) #If 0 then this account is not an admin
    def __init__(self, account_id, username, email, consumer_key, anon = 1, admin = 0):
        # Initialize account to the input values
        self.account_id = account_id
        self.username = username
        self.consumer_key = consumer_key 
        self.anon = anon
        self.admin = admin

    def __repr__(self):
        # When called, accounts return the user's name
        return self.username

class Student(Base):
    """
    The class for LSES students
    Attributes: account_id, open_requests (int), closed_requests (int), gained_money (int)
    """
    __tablename__ = 'students' #store all student Objects in students

    account_id = Column(Integer, primary_key=True, nullable = False) #The key value for account identification
    open_requests = Column(Integer) #The number of open requests by the student
    closed_requests = Column(Integer) #The number of requests which the student opened that are now closed (filled)
    gained_money = Column(Float) #The total amount of money this Student has gained (used for statistics)

    def __init__(self, account_id):
        # Initializes the student with the account id and all other attributes set to 0
        self.account_id = account_id
        self.open_requests = 0
        self.closed_requests = 0
        self.gained_money = 0
    def __repr__(self):
        # Formats the student's information to be easily read
        s = "<ID: %d, Opened Requests: %d, Closed Requests: %d, Money Gained: %d>" % (self. account_id, self.open_requests, self.closed_requests, self.gained_money)
        return s

class Donor(Base):
    """
    The class for Donors
    Attributes:  account_id (int), closed_requests (Int), money_given (int)
    """
    __tablename__= 'donors' #Store all donor objects in the table donors

    account_id = Column(Integer, primary_key=True, nullable = False) #The key value for account identification
    closed_requests = Column(Integer) #The number of requests this donor has closed (been the last one to donate to)
    money_given = Column(Float) #The total amount of money this donor has donated

    def __init__(self, account_id):
        # Initializes the donor with the account id and all other attributes set to 0
        self.account_id =  account_id
        self.closed_requests = 0
        self.money_given = 0
    def __repr__(self):
        #Formats the donor's information to be easily read
        s = "<ID: %d, closed_requests: %d, money_given: %d>" % (self. account_id, self.closed_requests, self.money_given)
        return s

class Request(Base):
    """
    The object class for donation requests
    Attributes: 
    """
    __tablename__='requests' #store all the request objects in a table called requests

    request_id = Column(Integer, primary_key=True, nullable = False)
    account_id = Column(Integer, primary_key = True, nullable = False)
    amount_needed = Column(Float)
    amount_filled = Column(Float)
    description = Column(String)
    filled = Column(Boolean)

    def __init__(self, request_id, account_id, amount_needed, description):
        self.request_id = request_id
        self.account_id = account_id
        self.amount_needed = amount_needed
        self.description = description
        self.amount_filled = 0
        self.filled = False
    def __repr__(self):
        s = "<Request ID: %d, Requested: %d, Filled: %d, Reason: %s>" % (self.request_id, self.amount_needed, self.amount_filled, self.description)
        return s
class Donation(Base):
    """
    The object class for donation donations
    Attributes: 
    """
    __tablename__='donations' #store all the request objects in a table called requests

    request_id = Column(Integer, primary_key=True, nullable = False)
    account_id = Column(Integer, primary_key = True, nullable = False)
    amount_given = Column(Float)
    charge_key = Column(String)
    filled = Column(Boolean)

    def __init__(self, request_id, account_id, amount_given, charge_key, filled):
        self.request_id = request_id
        self.account_id = account_id
        self.amount_given = amount_given
        self.charge_key = charge_key
        self.filled = filled

    def __repr__(self):
        s = '<Donation Key: %s, donated: %f, from account: %s' % (self.request_id, self.amount_given, self.account_id)
        return s


# Base.metadata.create_all(engine)
 #################################################Testing 
def Test():
    A = Account(1, 'JOE','Joeyjoe@joesph.com','555XTZ', 0, 0)
    S = Student(1)
    D = Donor(2)
    R = Request(3,4,60.00, "I NEED A TOAD")
    DM = Donation(3,4,55.9,'JKS', False)
    print(A, A.__table__)
    print(S, S.__table__)
    print(D, D.__table__)
    print(R, R.__table__)
    print(DM, DM.__table__)
Test()