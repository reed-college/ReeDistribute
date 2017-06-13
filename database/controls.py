from schema import *
import db


def create_student(username, name, password, email):
    # Create a Student and Account instance in the rd database.
    s = db.get_session()

    Acc =  Account(username = username, name = name, password=password, email = email)
    s.add(Acc)
    s.flush()

    Stu = Student(related_account=Acc.id)
    s.add(Stu)
    s.commit()
    s.close()


def create_donor(username, password, email):
    # Create a Donor and Account instance in the rd database
    s = db.get_session()

    Acc =  Account(username = username, password=password, email = email)
    s.add(Acc)
    s.flush()

    Don = Donor(related_account=Acc.id)
    s.add(Don)
    s.commit()
    s.close()


def open_request(student_id, amount, reason):
    # Create a request instance in the rd database.
    s = db.get_session()

    req = Request(requested_by=student_id, amount_needed=amount, description=reason)
    s.add(req)
    s.commit()
    s.close()   

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


def get_donor_id(usernameAttempt):
    # Return the database Donor id for an account from the username
    s = db.get_session()
    A = s.query(Account).filter(Account.username==usernameAttempt).first()
    acc = A.id
    D = s.query(Donor).filter(Donor.related_account==acc).first()
    s.close()
    return D.id
 

def donate(request_id, donor_id, amount):
    # Create and log the effects of a Donation in the database
    s = db.get_session()
    D = s.query(Donor).get(donor_id)
    R = s.query(Request).get(request_id)

    D.money_given += amount
    D.donations_given += 1
    R.amount_filled += amount

    if R.amount_needed >= R.amount_filled:
        R.filled = True

    d = Donation(to_request=request_id, from_donor=donor_id,amount_given = amount)

    s.add(d)
    s.commit()
    s.close()

def authenticate(usernameAttempt, passwordAttempt):
    # Check to see if a user is in the database
    s = db.get_session()
    A = s.query(Account).filter(Account.username==usernameAttempt).first()
    if A is None: ret = False
    elif (A.password == passwordAttempt): ret = True
    else: ret = False
    s.close()
    return ret



######################################################################################## TESTS

def test_donation():
    createStudent('Georgia', 'Pe@ch3s','On@my.mind')
    createDonor('Mr.Money-Bags', 'Ka-CH1NG!','monopolywinner@funny.money')
    openRequest(1,34,'I need money for Rent')
    donate(1,1,35.0)

def test_tables():
    
    # s = db.get_session()

    # Check Creation
    S = create_student('rubiesandemralds','jolene', 'mine', 'EMAIL' )
    D = create_donor('bananabread', 'MONEY', 'MAIL')
    R = Request(requested_by = 4, amount_needed = 60.00, description = "I NEED A TOAD. TRUST ME.")
    DM = Donation(to_request= 3, from_donor= 4,amount_given=55.9,charge_token='kEYKey')

    print(get_id('rubiesandemralds'), get_id('bananabread'))

    # s.close()
test_tables()

def test_authentication():
    A = Account(username = 'LonelyLady',name = 'Eleanor Rigby', password='ringoSTA**',email = 'doIbelong@here.where',account_token = 'MCKENZIE')
    s = db.get_session()
    s.add(A)
    s.commit()
    r1 = authenticate("LonelyLady", "ringoSTA**")
    r2 = authenticate("LonelyLaddie", "ringoSTA**")
    r3 = authenticate("LonelyLady", "YOKO")
    s.close()
    print(r1, r2, r3)
# test_authentication()
