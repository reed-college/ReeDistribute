from schema import *
from controls import *
import db
from random import randint, choice

"""
Run this files to fill up your database
Feel free to add more names/reasons/etc. to make it more interesting.
"""

booleans = [True, False]
# Random Choices for accounts
usernames = ['HannahBanana','Floralicious','Emtastic','Krogerdile','OvertheMoon','xifmij','tacoslayer',"BigBen"]
names = ["Hannah","Flora","Emily","John","Luna","JIM","Tacotaco","Benjiman"]
account_token=["TOKEN"]
# Random Request choices
titles = ["Donate to a Reedie in Needie","Groceries","Horcrux","Toads (for science)","Lunch Money","Sick Day"]
reasons = ["I am a LSES student who really needs help.","I want to buy this so I can live forever","Driving question: Are they actually part of the illuminati?","I spent too much and now I need some extra funds to buy my food","I was sick and now need some money to cover the day I took off"]

def TESTIT():
    # Create Accounts
    IDs = []
    for username in usernames:
        name = choice(names)
        create_account(username, name)
        i = account_id(username)
        IDs += [i]
    # Create Requests
    RIDs = []
    for reason in reasons:
        i = choice(IDs)
        amount = randint(1,100)
        title = choice(titles)
        anon = choice(booleans)
        app = choice(booleans)
        r = open_request(i,amount,reason,title,anon,app)
        RIDs += [r]
    # Donate
    for r in RIDs:
        amount = randint(0,75)
        donate(r, amount)

TESTIT()


        