import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def activation_email(to,code):
    fro = "reedistributesds@gmail.com"
    msg=MIMEMultipart()
    msg['From'] = fro
    msg['To'] = to
    msg['Subject'] = "ReeDistribute Activation Code"
    url = "reed.edu/reedistribute"

    body = "Welcome! You are invited to join ReeDistribute, an online communtiy for Reed College student monetary gifting!"
    body += "\n"
    body += "To activate you account please go to " + url + " and use this email address along with the following activation code: " + code
    msg.attach(MIMEText(body,'plain'))

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(fro,"pipinstallreed")
    text = msg.as_string()
    server.sendmail(fro,to,text)
    server.quit()