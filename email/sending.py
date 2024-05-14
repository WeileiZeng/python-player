#!python3.5
# use python to send gmail
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print('This script use gmail to send emails. The body can be text or html')

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "ProgressBar20XX@gmail.com"  # Enter your address
receiver_email = "240155787@qq.com"  # Enter receiver address
#password = input("Type your password and press enter: ")
password="kzoyvjckjltatdgt"

message = MIMEMultipart("alternative")
message["Subject"] = "Cherenkov Report"
message["From"] = sender_email
message["To"] = receiver_email



#get ip
import os
req=os.popen('curl https://api.ipify.org/')
ip=req.read()
req=os.popen('date')
d=req.read()

local_ip = os.popen('ifconfig |grep 138.23').read()
ifconfig = os.popen('ifconfig').read()
#print(req)
#print(ip)


import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)
## printing the hostname and ip_address
print("Hostname: ",{hostname})
print("IP Address: ",{ip_address})

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
public_ip=s.getsockname()[0]
#print(s.getsockname()[0])
s.close()



# Create the plain-text and HTML version of your message
text=''
text = text + "The ip of cherenkov is "+ip+'\n'
text = text + d +'\n'
text = text + 'python socket: local ip = '+ ip_address +'\n'
text = text + 'public ip = '+public_ip +'\n'
text = text + 'local ip:'+local_ip+'\n' 
text = text + ifconfig

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
print(part1)

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)

context_ssl = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context_ssl) as server:
    print('login into', sender_email)
    server.login(sender_email, password)
    print('sending to',receiver_email)
    server.sendmail(sender_email, receiver_email, message.as_string() )


print("done")
                    
