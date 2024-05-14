# crontab -e
# 30 * * * * python3 /Users/weileizeng/Documents/GitHub/python-player/email/check_ip.py
# run every hour at :30 mins


import json
import os

#get current info

ip=os.popen('curl https://api.ipify.org/').read()
user = os.popen('echo $USER').read()
hostname = os.popen('hostname').read()
date = os.popen('date').read()

import socket
## getting the hostname by socket.gethostname() method
socket_hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
socket_local_ip = socket.gethostbyname(socket_hostname)
## printing the hostname and ip_address
#print("Hostname: ",{hostname})
#print("IP Address: ",{ip_address})

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
socket_public_ip=s.getsockname()[0]
#print(s.getsockname()[0])
s.close()




info=dict(ip=ip,user=user,hostname=hostname,date=date,
          socket_hostname=socket_hostname,socket_local_ip=socket_local_ip,socket_public_ip=socket_public_ip)

print(info)

s=json.dumps(info,indent=2)
#print(s)

filename_current='data-latest.json'

data_new=info
#read previous data
with open(filename_current,'r') as f:
    data_old=json.load(f)

#compare data
for k in ['ip','user','hostname','socket_local_ip','socket_public_ip','socket_hostname','date']:
    if data_old[k] == data_new[k]:
        pass
    else:        
        print(k,'data changes. do something')
        from send import send_text
        ifconfig = os.popen('ifconfig').read()
        content=dict(log=k+' changes ',data_old=data_old, data_new=data_new)
        s=json.dumps(content,indent=2)
        s = s + '\n' + ifconfig
        send_text(s,note=socket_hostname+socket_public_ip)
        
#print(data_old)

#save data

from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
 
#print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%Y%m%d-%H%M%S")
filename_log='log/'+dt_string+'.json'
with open(filename_log,'w') as f:
    json.dump(info,f,indent=2)

#filename_old='data-'    
#os.popen('mv '+filename_current + ' ' + filename_old)
    
#print("date and time =", dt_string)

with open(filename_current,'w') as f:
    json.dump(info,f,indent=2)

print('done')
