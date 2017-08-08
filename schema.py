from sqlalchemy import (Column, ForeignKey, DateTime, Boolean, Integer, Float, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, select
from datetime import datetime
import db


"""
This is the database for the webapp ReeDistribute
All information collected by this program defaults to anonymous 
"""
Base = declarative_base() #Make it an OOP

class IdPrimaryKeyMixin(object):
    #An ID column we wish to add to all rows,
    #  it will be unique to the table and given incrementaly
    id = Column(Integer, primary_key=True, nullable = False)


class DateTimeMixin(object):
    #To Record the time each object was created and last updated
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now,
                        onupdate=datetime.now)


class Account(Base, IdPrimaryKeyMixin, DateTimeMixin):
    """
    accounts is the table for the Account objects which hold the user information 
    """
    __tablename__="accounts" #Store all account objects in accounts

    # Columns:
    username = Column(String, nullable=False) #The reed id
    account_token = Column(String) #Account's Stripe coustomer key
    admin = Column(Boolean, default=False) #True for admins
    approved = Column(Boolean, default=False) #False if request rights are revoked
    recieved = Column(Float, default = 0.00) #How much money has this account recieved

    def __init__(self, username):
        self.username = username
        self.account_token = 'TOKEN'
        self.admin = False
        self.approved = False
        self.recieved = 0.00

    def as_dict(self):
        ret = {'user':self.username,
        'token':self.account_token,
        'admin':self.admin,
        'approved': self.approved}
        return ret
    def __str__(self):
        ret = self.username
        return ret
    def make_admin(self):
        s = db.get_session()
        self.admin = True
        s.commit()
        s.close()
    def revoke_requests(self):
        s = db.get_session()
        self.approved = False
        s.commit()
        s.close()



class Request(Base, IdPrimaryKeyMixin, DateTimeMixin):
    """
    requests is the table which holds all the requests represented by Request objects
    """
    __tablename__="requests"

    # Columns:
    requested_by = Column(Integer, ForeignKey("accounts.id")) #who gave the request
    amount_needed = Column(Float) #How much money do you need
    title = Column(String) #Give it a title
    description = Column(String) #Why the user needs money or requests for physical goods
    amount_filled = Column(Float, default=0.0) #How much money has been raised
    anon = Column(Boolean, default=True) #Will the request be posted anonymously
    filled = Column(Boolean, default=False) #After the request is filled, it no longer needs to be donated to
    num_donors = Column(Integer, default=0) #How many donors   
    approved = Column(Boolean, default=False) #admin approval is needed for the request to be shown
    
    def __init__(self, user_id, amount, title, description, anon, approved):
        self.requested_by = user_id
        self.amount_needed = amount
        self.title = title 
        self.description = description
        self.amount_filled = 0
        self.num_donors = 0
        self.approved = approved
        

    def as_dict(self):
        ret = {"requested_by":self.requested_by,
        "amount":self.amount,
        "needed":self.amount_needed,
        "filled":self.amount_filled,
        "title":self.title,
        "description":self.description,
        "numDonors":self.num_donors,
        "approved":self.approved}
        return ret
    def __str__(self):
        ret = self.title + "\n" + self.description
        return ret


class Donation(Base, IdPrimaryKeyMixin, DateTimeMixin):
    """
    donations is the table of Donation objects
    """
    __tablename__="receipt"

    # Columns:
    to_request = Column(Integer, ForeignKey("requests.id")) #which request is being filled
    to_user = Column(Integer, ForeignKey("accounts.id")) #who is donating
    amount_given = Column(Float) #how much money is being donated
    charge_token = Column(String) #stripey?

    def __init__(self, for_request, for_user, amount, token=""):
        self.to_request = for_request
        self.to_user = for_user
        self.amount_given = amount
        self.token = token
        

    def as_dict(self):
        ret = {"request":self.to_request,
        "user":self.to_user,
        "amount":self.amount_given
        }
        return ret
    def __str__(self):
        ret = "User %d was given %f for request %d" % (self.to_user, self.amount_given, self.to_request)
        return ret



    
#####################################################
def start_db():
    engine = create_engine('postgresql://postgres@localhost/rd')
    Base.metadata.create_all(engine)
###################################################
if __name__ == "__main__":
    start_db()