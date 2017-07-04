from schema import *
import db
def create_student(username, name, password, email):
    s = db.get_session()

    Acc =  Account(username = username, name = name, password=password, email = email)
    s.add(Acc)
    s.flush()

    Stu = Student(related_account=Acc.id)
    s.add(Stu)
    s.commit()
    s.close()
create_student("it_is_me","Moi","mypassword143","example@ex.com")
create_student("test_person","New Person","pass","exex@ex.com")
def create_donor(username, password, email):
    s = db.get_session()

    Acc =  Account(username = username, password=password, email = email)
    s.add(Acc)
    s.flush()

    Don = Donor(related_account=Acc.id)
    s.add(Don)
    s.commit()
    s.close()
create_donor("it_is_me","mypassword143","example@ex.com")


def open_request(student_id, amount, reason):
    s = db.get_session()
    req = Request(requested_by=student_id, amount_needed=amount, description=reason)
    s.add(req)
    s.commit()
    s.close()
open_request(1,100,"need")  
open_request(3,75.5,"I'm booooororred")   
def donate(request_id, donor_id, amount):

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
    s = db.get_session()
    A = s.query(Account).filter(Account.username==usernameAttempt).first()
    if A is None: ret = False
    elif (A.password == passwordAttempt): ret = True
    else: ret = False
    s.close()
    return ret
# authenticate("it_is_me","mypassword143")
