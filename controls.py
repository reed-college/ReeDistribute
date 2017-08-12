from schema import *
import db


######################################Creation Functions
def create_account(username):
    # Create a Student and Account instance in the rd database.
    s = db.get_session()

    Acc =  Account(username)
    s.add(Acc)
    s.commit()
    s.close()

    print(username, "added to the database")

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

def open_request(student_id, amount, reason, title, anon):
    # Create a request instance in the rd database.
    s = db.get_session()
    if title == '': title = "Donate to a Reedie in needie"
    req = Request(student_id, amount, title, reason, anon, True)
    s.add(req)
    s.commit()
    s.close()
    print(student_id, "request added to the database")

def donate(request_id, amount):
    # Create and log the effects of a Donation in the database
    s = db.get_session()
    R = s.query(Request).get(request_id)
    AID = R.requested_by
    A = s.query(Account).get(AID)
    D = Donation(request_id, AID, amount)
    s.add(D)
    s.flush()

    A.recieved += amount
    s.flush()
    R.num_donors += 1
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


def request_info(show_unapproved=False):
    # Returns a list of all active and approved requests as lists of their traits
    # requestlist = [row1List, ...] where
    # rowXList = rowX:name, rowX.amount_needed, rowX.amount_filled, rowX.description
    s = db.get_session()
    requestList = []
    
    for row in s.query(Request):
        if row.filled == False:     
            if row.anon == False:
                name = get_student_name(row.requested_by)
            else:
                name = "Anonymous"            
            rowList = [name, row.amount_needed, row.amount_filled, row.title, row.description, row.approved]
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

#############################################HTML and LISTS
def account_table():
    s = db.get_session()
    q = s.query(Account)
    html = "<table name='Accounts'>" 
    headRow=" <tr> <th> ID </th> <th> Username </th> <th>approved</th> <th>admin</th> </tr>"
    html += headRow
    accounts = []
    for a in q:
        accounts += [a.id, a.username, a.approved, a.admin]
        row=' <tr>'
        row += ' <td> ' + str(a.id) + ' </td>'
        row += ' <td> ' + a.username + '</td>'        
        row += ' <td> ' + str(a.approved) + ' </td>'
        row += ' <td> ' + str(a.admin) + ' </td>'
        row += ' </tr> '
        html += row
    html += '</table>'
    print(accounts)
    return accounts, html  

def pending_table():
    s = db.get_session()
    q = s.query(Request)
    table = "<table name='Pending Requests'>" 
    headRow="<tr> <th>ID</th> <th>Title</th> <th>amount</th> <th>description</th> </tr>"
    table += headRow
    accounts = []
    for p in q:
        if ((p.filled==False) and (p.approved==False)):
            accounts += [p]
            row='<tr>'
            row += '<td>' + str(p.id) + '</td>'
            row += '<td>' + p.title + '</td>'        
            row += '<td>' + str(p.amount_needed) + '</td>'
            row += '<td>' + p.description + '</td>'
            row += '</tr>'
            table += row
    table += '</table>'    


def request_table():
    
    s = db.get_session()
    q = s.query(Request)
    table = "<table name='Requests'>" 
    headRow="<tr> <th>ID <\th> <th>Title</th> <th>amount</th> <th>description</th> </tr>"
    table += headRow
    requests = []
    for r in q:
        if ((r.filled==False) and (r.approved==True)):
            requests += [r]
            row='<tr>'
            row += '<td>' + str(r.id) + '</td>'
            row += '<td>' + r.title + '</td>'        
            row += '<td>' + str(r.amount_needed) + '</td>'
            row += '<td>' + r.description + '</td>'
            row += '</tr>'
            table += row
    table += '</table>'

    return requests, table   

