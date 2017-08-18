from schema import *
import db


######################################Creation Functions
def create_account(username, name):
    # Create a Student and Account instance in the rd database.
    s = db.get_session()

    Acc =  Account(username, name)
    s.add(Acc)
    s.commit()
    i = Acc.id
    s.close()

    print(username, "added to the database")
    return i
def del_acc(aid):
    s = db.get_session()
    a = s.query(Account).get(aid)
    s.delete(a)
    s.commit()
    s.close()

def approve_admin(usernameAttempt):
    s = db.get_session()
    A = s.query('accounts').filter(Account.username==usernameAttempt).first()
    A.admin = True
    s.commit()
    s.close()

def approve_requesting(usernameAttempt):
    s = db.get_session()
    A = s.query('accounts').filter(Account.username==usernameAttempt).first()
    A.approved = True
    s.commit()
    s.close()

def open_request(student_id, amount, reason, title, anon, app):
    # Create a request instance in the rd database.
    s = db.get_session()
    if title == '': title = "Donate to a Reedie in needie"
    req = Request(student_id, amount, title, reason, anon, True)
    s.add(req)
    s.commit()
    i = req.id
    s.close()
    print(student_id, "request added to the database")
    return i

def del_req(rid):
    s = db.get_session()
    r = s.query(Request).get(rid)
    s.delete(r)
    s.commit()
    s.close()

def donate(request_id, amount):
    # Create and log the effects of a Donation in the database
    s = db.get_session()
    R = s.query(Request).get(request_id)
    AID = R.requested_by
    A = s.query(Account).get(AID)

    A.recieved += amount
    A.num_recieved += 1
    s.flush()
    R.amount_filled += amount
    s.flush()
    # check to see if the request has been completed    
    if R.amount_filled >= R.amount_needed:
        R.filled = True

    s.commit()
    s.close()

######################################Information Functions

def account_id(name):
    # Return the database Account id for an account from the username
    s = db.get_session()
    A = s.query(Account).filter(Account.username==name).first()
    s.close()
    
    return A.id


def request_id(posttitle):
    # Return the database Account id for an account from the username
    s = db.get_session()
    R = s.query(Request).filter(Request.title==posttitle).first()
    s.close()
    
    return R.id

def update_account_token(username, token):
    s = db.get_session()
    
    A = s.query(Account).filter(Account.username==usernameAttempt).first()
    A.account_token=token

    s.commit()
    s.close()

def confirm(email, code):
    s = db.get_session()
    q = s.query(Pending).filter(Pending.email==email)
    for p in q:
        if p.code == code: return True
    return False

def request_info(show_unapproved=False):
    # Returns a list of all active and approved requests as lists of their traits
    # requestlist = [row1List, ...] where
    # rowXList = rowX:name, rowX.amount_needed, rowX.amount_filled, rowX.description
    s = db.get_session()
    requestList = []
    if show_unapproved == False:
        q = s.query(Request).filter(Request.approved==True)
    else:
        q = s.query(Request).filter(Request.approved==False)
    for row in q:
        if row.filled == False:     
            if row.anon == False:
                acc = s.query(Account).get(row.id)
                name = acc.name
            else:
                name = "Anonymous"            
            rowList = [name, row.amount_needed, row.amount_filled, row.title, row.description, row.approved]
            requestList += [rowList]
    if requestList==[]: requestList = [[]]
    s.close()
    return requestList
def filled_reqs():
    # Returns a list of all active and approved requests as lists of their traits
    # requestlist = [row1List, ...] where
    # rowXList = rowX:name, rowX.amount_needed, rowX.amount_filled, rowX.description
    s = db.get_session()
    requestList = []
    
    for row in s.query(Request).filter(Request.filled==True):
        if row.approved == True:     
            acc = s.query(Account).get(row.id)
            name = acc.name            
            rowList = [name, row.amount_needed, row.amount_filled, row.title, row.description, row.approved, row.id, row.requested_by]
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
 

if __name__ =="__main__":
    start_db()