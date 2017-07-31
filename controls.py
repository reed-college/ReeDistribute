from schema import *
import db

start_db()


######################################Creation Functions
def create_account(username, admin, approved, token = ''):
    # Create a Student and Account instance in the rd database.
    s = db.get_session()

    Acc =  Account(username=username, admin=admin, approved=approved, account_token=token)
    s.add(Acc)
    s.commit()
    s.close()

    print(username, "added to the database")

def approve_admin(username):
    s = db.get_session()
    A = s.query(Account).filter(Account.username==usernameAttempt).first()
    A.admin = True
    s.commit()
    s.close()

def approve_requesting(username):
    s = db.get_session()
    A = s.query(Account).filter(Account.username==usernameAttempt).first()
    A.approved = True
    s.commit()
    s.close()

def open_request(student_id, amount, reason, title="Donate to a Reedie in needie", anon=True, amount_filled=0.0):
    # Create a request instance in the rd database.
    s = db.get_session()
    req = Request(requested_by=student_id, amount_needed=amount, title=title, amount_filled=amount_filled, description=reason, anon=anon)
    s.add(req)
    s.commit()
    s.close()
    print(student_id, "request added to the database")
       

def donate(username, request_id, amount):
    # Create and log the effects of a Donation in the database
    s = db.get_session()
    A = s.query(Account).filter(Account.username==usernameAttempt).first()
    R = s.query(Request).filter(request.id==request_id).first()

    A.given += amount
    A.num_given += 1
    s.flush()
    R.amount_filled += amount

    # check to see if the request has been completed
    if R.amount_needed >= R.amount_filled:
        R.filled = True


    s.commit()
    s.close()

######################################Information Functions

def get_id(usernameAttempt):
    # Return the database Account id for an account from the username
    s = db.get_session()
    
    A = s.query(Account).filter(Account.username==usernameAttempt).first()
   
    s.close()
    return A.id



def update_account_token(username, token):
    s = db.get_session()
    
    A = s.query(Account).filter(Account.username==usernameAttempt).first()
    A.account_token=token

    s.commit()
    s.close()


def request_info(show_unapproved=False):
    # Returns a list of all active and approved requests as lists of their traits
    # requestlist = [row1List, ...] where
    # rowXList = rowX:name, rowX.amount_needed, rowX.amount_filled, rowX.description
    s = db.get_session()
    requestList = []
    
    for row in s.query(Request):
        if row.filled == False:     
            if row.anon == True:
                name = "Anonymous"
            else:
                name = get_student_name(row.requested_by)
            
            rowList = [name, row.amount_needed, row.amount_filled, row.title, row.description, row.id, row.approved]
            requestList += [rowList]
    if requestList==[]: requestList = [[]]
    s.close()
    return requestList

    


def request_info_who(post_n,type_n):
    s = db.get_session()
    requestList = request_info()
    data = requestList[post_n][type_n]
    s.close()
    return data
# print(request_info()[1][0])


def approve_request(id):
    s = db.get_session()
    R = s.query(Request).filter(Request.id == id).first()
    R.approved = True
    s.commit()
    s.close()

    

######################################################################################## TESTS

def test_accounts():
    s = db.get_session()
    A = Account(username='HannahBanana')
    B = Account(username='DarkLordVold')
    C = Account(username='Krogerdile')
    s.add(A)
    s.add(B)
    s.add(C)
    s.commit()
    s.close()

def test_requests():
    s = db.get_session()
    R1 = Request(requested_by=1, amount_needed=20.87, title="For Books",description="I would like to but the LOTR trillogy in paperback")
    R2 = Request(requested_by=2,amount_needed=6.66, title='Horcrux', description='keep me alive forever')
    s.add(R1)
    s.add(R2)
    s.commit()
    s.close()

def TEST():
    test_accounts()
    test_requests()
# TEST()
