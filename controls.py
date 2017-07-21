from schema import *
import db

start_db()


######################################Creation Functions
def create_student(username, name, password, email, token=""):
    # Create a Student and Account instance in the rd database.
    s = db.get_session()

    Acc =  Account(username=username, name=name, password=password, email=email, account_token=token)
    s.add(Acc)
    s.flush()

    Stu = Student(related_account=Acc.id)
    s.add(Stu)
    s.commit()
    s.close()
    print(username, "added to the database")

def create_donor(username, password, email, token=""):
    # Create a Donor and Account instance in the rd database
    s = db.get_session()

    Acc =  Account(username=username, password=password, email=email, account_token=token)
    s.add(Acc)
    s.flush()

    Don = Donor(related_account=Acc.id)
    s.add(Don)
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
       

def donate(request_id, donor_id, amount, account_token):
    # Create and log the effects of a Donation in the database
    s = db.get_session()
    D = s.query(Donor).get(donor_id)
    A = s.query(Account).get(D.related_account)
    R = s.query(Request).get(request_id)


    A.account_token = account_token
    D.money_given += amount
    D.donations_given += 1
    R.amount_filled += amount

    # check to see if the request has been completed
    if R.amount_needed >= R.amount_filled:
        R.filled = True

    d = Donation(to_request=request_id, from_donor=donor_id,amount_given = amount)

    s.add(d)
    s.commit()
    s.close()

######################################Information Functions

def get_id(usernameAttempt):
    # Return the database Account id for an account from the username
    s = db.get_session()
    
    A = s.query(Account).filter(Account.username==usernameAttempt).first()
   
    s.close()
    return A.id


def get_student_id(usernameAttempt):
    # Return the database Student id for an account from the username
    s = db.get_session()
    A = s.query(Account).filter(Account.username==usernameAttempt).first()
    
    acc = A.id
    S = s.query(Student).filter(Student.related_account==acc).first()
    
    s.close()
    return S.id

def get_student_name(studentID):
    # Return the database Student id for an account from the username
    s = db.get_session()
   
    S = s.query(Student).get(studentID)
    accountID = S.related_account
   
    A = s.query(Account).get(accountID)
    who = A.name
   
    s.close()
    return who


def get_donor_id(usernameAttempt):
    # Return the database Donor id for an account from the username
    s = db.get_session()
   
    A = s.query(Account).filter(Account.username==usernameAttempt).first()
    acc = A.id
    D = s.query(Donor).filter(Donor.related_account==acc).first()
   
    s.close()
    return D.id

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

def authenticate(usernameAttempt, passwordAttempt):
    # Check to see if a user is in the database
    # returns True/False
    s = db.get_session()
    
    A = s.query(Account).filter(Account.username==usernameAttempt).first()
    if A is None:
        ret = False
    elif (A.password == passwordAttempt): 
        ret = True
    else:
        ret = False
   
    s.close()
    return ret
########################################################################## Untested
# def update_password(userName, oldPass, newPass1, newPass2):
#     s = db.get_session()
#     A = s.query(Account).filter(Account.username==userName).first()
#     if A is None: 
#         Return False
#     elif A.password == oldPass:
#         if newPass1 == newPass2:
#             A.password = newPass1
#             return True
#         return False
#     return False
#     s.commit()
#     s.close()

def approve_request(id):
    s = db.get_session()
    R = s.query(Request).filter(Request.id == id).first()
    R.approved = True
    s.commit()
    s.close()

    

######################################################################################## TESTS

def test_donation():
    # Tests the donate function
    create_student("Peachy","Georgia", "Pe@ch3s","On@my.mind")
    create_donor("Mr.Money-Bags", "Ka-CH1NG!","monopolywinner@funny.money")
    open_request(1,34,"I need money for Rent")
    donate(3,2,15.0, "token")
# test_donation()
    


def test_tables():
    # Test table creation and insertion
    # Check Creation
    S = create_student("rubiesandemralds","jolene", "mine", "EMAIL" )
    S = create_student("KIKI","Kendra", "WITCH", "EMAIL" )
    S = create_student("Moonshine","Jordan", "brewer", "EMAIL" )
    D = create_donor("bananabread", "MONEY", "MAIL")
    D = create_donor("moneybagz", "richy", "MAIL")
    D = create_donor("Curtis", "Day", "MAIL")
    

    # print(get_id("rubiesandemralds"), get_id("bananabread"))

# test_tables()


def test_authentication():
    # Test a few cases to see if authentication works
    A = Account(username = "LonelyLady",name = "Eleanor Rigby", password="ringoSTA**",email = "doIbelong@here.where",account_token = "MCKENZIE")
    s = db.get_session()
    s.add(A)
    s.commit()
    r1 = authenticate("LonelyLady", "ringoSTA**")
    r2 = authenticate("LonelyLaddie", "ringoSTA**")
    r3 = authenticate("LonelyLady", "YOKO")
    s.close()
    print(r1, r2, r3)
# test_authentication()
def test_approval():
    approve_request(2)
# test_approval()

def test_requests():
    # Test to see if we can return all the request info needed for posting
    create_student("bananana","HANNAH","phone", "EMAIL@MAILMAIL.MAIL")
    open_request(1, 55, "WOOOOOOOOOOOOOOOOOOW", False)
    open_request(1, 22, "I need more cake, it was a lie")
    # print(request_info())
# test_requests()
    
    
def TEST():
    start_db()
    test_tables()
    open_request(1, 60.00, "I NEED A TOAD. TRUST ME.", "TOADZ")
    donate(1, 1, 5.35, "kEYKey")
    # test_donation()
    s = db.get_session()

    for row in s.query(Account):
        print(row)
    for row in s.query(Request):
        print(row)

    s.close()
# TEST()
