# #!python3.5

# use python to send gmail
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print('This script use gmail to send emails. The body can be text or html')


def send_text(text):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "ProgressBar20XX@gmail.com"  # Enter your address
    receiver_email = "240155787@qq.com"  # Enter receiver address
    #password = input("Type your password and press enter: ")
    password="kzoyvjckjltatdgt"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Host Info Report"
    message["From"] = sender_email
    message["To"] = receiver_email


    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)


    context_ssl = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context_ssl) as server:
        print('login into', sender_email)
        server.login(sender_email, password)
        print('sending to',receiver_email)
        server.sendmail(sender_email, receiver_email, message.as_string() )
    print('finish sending email to',receiver_email ,'with the following text')
    print(message)
    #print(text)
    

if __name__=="__main__":
    
    #get ip
    import os
    req=os.popen('curl https://api.ipify.org/')
    ip=req.read()
    req=os.popen('date')
    d=req.read()
    user = os.popen('echo $USER $HOSTNAME').read()
    #print(req)
    #print(ip)

    # Create the plain-text version of your message
    text=''
    text = text + "The ip is "+ip+'\n'
    text = text + d
    text = text + user

    print('send the following info')
    print(text)

    send_text(text)
    print("done")
