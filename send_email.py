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

    html = """\
    <html>
    <head></head>
    <body style='text-align:center'>
    <h1> Welcome! </h1>
    <h3> You are invited to join ReeDistribute, an online communtiy for Reed College student monetary gifting! </h3>
    <h2> To activate you account please go to %s and use this email address along with the following activation code: %s
    </body>
    </html>
    """ %(url, code)
    msg.attach(MIMEText(html,'html'))
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(fro,"pipinstallreed")
    text = msg.as_string()
    server.sendmail(fro,to,text)
    server.quit()
