# crontab -e
# 30 * * * * python3 /Users/weileizeng/Documents/GitHub/python-player/email/check_ip.py
# run every hour at :30 mins


import json
import os

#get current info

ip=os.popen('curl https://api.ipify.org/').read()
user = os.popen('echo $USER').read()
hostname = os.popen('echo $HOSTNAME').read()
date = os.popen('date').read()

info=dict(ip=ip,user=user,hostname=hostname,date=date)

print(info)

s=json.dumps(info,indent=2)
#print(s)

filename_current='data-latest.json'

data_new=info
#read previous data
with open(filename_current,'r') as f:
    data_old=json.load(f)

#compare data
for k in ['ip','user','hostname','date']:
    if data_old[k] == data_new[k]:
        pass
    else:        
        print(k,'data changes. do something')
        from send import send_text
        content=dict(log=k+' changes ',data_old=data_old, data_new=data_new)
        #info['log']=k+' changes'
        s=json.dumps(content,indent=2)
        send_text(s)
        
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
