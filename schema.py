from sqlalchemy import (Column, ForeignKey, DateTime, Boolean, Integer, Float, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, select
from datetime import datetime
import db


"""
This is the database for the webapp ReeDistribute
All information collected by this program remains anonymous
Everything that is stored is either for functionality or statistics to prove the site's validity

"""
Base = declarative_base() #Make it an OOP

class IdPrimaryKeyMixin(object):
    id = Column(Integer, primary_key=True, nullable = False)


class DateTimeMixin(object):
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Account(Base, IdPrimaryKeyMixin, DateTimeMixin):
    """
    The main user class for ReeDistribute Login.abs
    Attributes: account_id (int), name (str), email (str), account_token (str), anon (int), admin (int)
    """
    __tablename__='accounts' #Store all account objects in accounts

    username = Column(String, nullable = False) #Account's chosen name, used for site personalization
    password = Column(String, nullable = False) #Account's chosen name, used for site personalization
    email = Column(String, nullable = False) #Account's email for contacting
    account_token = Column(String) #Account's Stripe coustomer key
    admin = Column(Boolean, default = False) #If 0 then this account is not an admin

    def __repr__(self):
        ret = "<ID: %d, username: %s, email: %s, admin: %d>" % (self.id, self.username, self.email, self.admin)
        return ret

class Student(Base, IdPrimaryKeyMixin, DateTimeMixin):
    """
    The class for LSES students
    Attributes: account_id, open_requests (int), closed_requests (int), gained_money (int)
    """
    __tablename__ = 'students' #store all student Objects in students

    related_account = Column(Integer, nullable = False) #So we can easily locate the user information
    open_requests = Column(Integer, default=0) #The number of open requests by the student
    closed_requests = Column(Integer, default=0) #The number of requests which the student opened that are now closed (filled)
    gained_money = Column(Float, default=0) #The total amount of money this Student has gained (used for statistics)

    def __repr__(self):
        # Formats the student's information to be easily read
        ret = "<ID: %d, Opened Requests: %d, Closed Requests: %d, Money Gained: %d>" % (self.id, self.open_requests, self.closed_requests, self.gained_money)
        return ret


class Donor(Base, IdPrimaryKeyMixin, DateTimeMixin):
    """
    The class for Donors
    Attributes:  account_id (int), closed_requests (Int), money_given (int)
    """
    __tablename__= 'donors' #Store all donor objects in the table donors

    related_account = Column(Integer, nullable = False) #So we can easily locate the user information
    closed_requests = Column(Integer, default=0) #The number of requests this donor has closed (been the last one to donate to)
    money_given = Column(Float, default=0) #The total amount of money this donor has donated

    def __repr__(self):
        #Formats the donor's information to be easily read
        ret = "<ID: %d, closed_requests: %d, money_given: %d>" % (self.id, self.closed_requests, self.money_given)
        return ret

class Request(Base, IdPrimaryKeyMixin, DateTimeMixin):
    """
    The object class for donation requests
    Attributes: 
    """
    __tablename__='requests' #store all the request objects in a table called requests

    requested_by = Column(Integer)
    amount_needed = Column(Float)
    description = Column(String)
    amount_filled = Column(Float, default=0.0)
    anon = Column(Boolean, default=True) #If 0 then the account does not wish to remain anonymous for actions on the website
    filled = Column(Boolean, default=False)
    # add anon
    def __repr__(self):
        ret = "<Request ID: %d, Requested: %d, Filled: %d, Reason: %s>" % (self.id, self.amount_needed, self.amount_filled, self.description)
        return ret
    # def recieve(self, amount):
    #     self.amount_filled += amount
    #     if self.amount_needed <= self.amount_filled:
    #         self.filled = True
    #     pass

    
class Donation(Base, IdPrimaryKeyMixin, DateTimeMixin):
    """
    The object class for donation donations
    Attributes: 
    """
    __tablename__='donations' #store all the request objects in a table called donations
    to_request = Column(Integer, nullable = False) #make a foreign key?
    from_donor = Column(Integer, nullable = False)
    amount_given = Column(Float)
    charge_token = Column(String)
    anon = Column(Boolean, default = True) #If 0 then the account does not wish to remain anonymous for actions on the website   

    def __repr__(self):
        ret = '<Donation Key: %d, donated: %f, from account: %s' % (self.id, self.amount_given, self.from_donor)
        return ret
#####################################################
Base.metadata.create_all(db.engine)
    


######################################Actions
# def readoff(catagory):
#     for thing in catagory:
#         print(thing)
# def change(thing, attribute, now_is):
#     thing.attribute = now_is
#     session.commit
# def remove(thing):
#     session.delete(thing)
#     session.commit()
# #######################################Actions


    



#     # Check Donation
#     donate(3,2,40.98,'keykeykey')
#     print(A)
#     print(S)
#     print(D)
#     print(R)
#     print(DM)

# # Test()
 
