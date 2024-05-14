print("""
This script collect ip information and email it.
Author: Weilei Zeng
Dated: May 14, 2024

To run it automatically for given peorid, add it into cron jobs
cmd to edit cron job is `crontab -e`
sample cmd
30 * * * * python3 /Users/weileizeng/Documents/GitHub/python-player/email/check_ip.py
run every hour at :30 mins
""")

import json
import os

#get current info
ipify_ip=os.popen('curl https://api.ipify.org/').read()

#use shell to get info
#shell_user = os.popen('echo $USER').read()
shell_user = os.popen('whoami').read()
shell_hostname = os.popen('hostname').read()
shell_date = os.popen('date').read()
shell_cron_cmd = os.popen('crontab -l |grep check_ip.py').read()

#use socket to get info
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

from datetime import datetime
# datetime object containing current date and time
now = datetime.now() 
#print("now =", now)
# YYmmdd-HHMMSS
python_date = now.strftime("%Y%m%d-%H%M%S")



data_new=dict(ipify_ip=ipify_ip,
              shell_user=shell_user,shell_hostname=shell_hostname,shell_date=shell_date,shell_cron_cmd=shell_cron_cmd,
              socket_hostname=socket_hostname,socket_local_ip=socket_local_ip,socket_public_ip=socket_public_ip,
              python_date=python_date)

print('data_new',data_new)
#print('all info',info)

#s=json.dumps(info,indent=2)
#print(s)


filename_current='data-latest.json'
#read previous data
with open(filename_current,'r') as f:
    data_old=json.load(f)

#compare data
for k in ['ipify_ip','shell_user','shell_hostname','shell_cron_cmd','socket_local_ip','socket_public_ip','socket_hostname','python_date']:
    changed=False
    if k not in data_new:
        changed=True
    elif k not in data_old:
        changed=True    
    elif data_old[k] != data_new[k]:
        changed=True
    if changed:
        print(k,'data changes. do something')
        from send import send_text
        ifconfig = os.popen('ifconfig').read()
        #content=dict(data_old=data_old, data_new=data_new)
        s = k + ' changed. \n'
        s = s + 'data_new:\n'+json.dumps(data_new,indent=2) + '\n'
        s = s + 'data_old:\n'+json.dumps(data_old,indent=2) + '\n'        
        #s=json.dumps(content,indent=2)
        s = s + '\n' + ifconfig
        send_text(s,note=' '+socket_hostname+' '+socket_public_ip)
        break #only send email once
#print(data_old)

#save data
#only save after succeeding sendint the email out

filename_log='log/'+python_date+'.json'
with open(filename_log,'w') as f:
    json.dump(data_new,f,indent=2)
    print('write into file',filename_log)
#filename_old='data-'    
#os.popen('mv '+filename_current + ' ' + filename_old)
    
#print("date and time =", dt_string)

with open(filename_current,'w') as f:    
    json.dump(data_new,f,indent=2)
    print('write into file',filename_current)

print('done')
