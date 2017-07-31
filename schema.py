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
    approved = Column(Boolean, default=True) #False if request rights are revoked
    recieved = Column(Float, default = 0.00) #How much money has this account recieved
    num_recieved = Column(Integer, default=0) #How many individual donations has this account recieved
    given = Column(Float, default = 0.00) #How much money has this account given
    num_given = Column(Integer, default=0) #How many individual donations has this accouunt given

    

    def __repr__(self):
        ret = {'user':self.username, 'token':self.account_token, 'admin':self.admin, 'approved': self.approved}
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
    approved = Column(Boolean, default=False) #admin approval is needed for the request to be shown
    
    def __repr__(self):
        need = self.amount_needed - self.amount_filled
        ret = {'user':self.requested_by, 'need': need, 'title':self.title, 'anon': self.anon, 'filled':self.filled, 'approved':self.approved}
        return ret
    def __str__(self):
        ret = self.title + "\n" + self.description
        return ret


    
#####################################################
def start_db():
    Base.metadata.create_all(db.engine)
