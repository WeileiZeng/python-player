import os


ip='cherenkov.dyn.ucr.edu'
r=os.popen('ping -c 1 '+ip).read()
#print(r)

if r=='':
    print('the ip '+ip+' is not availble')
elif r[:4]=='PING':
    print('the ip '+ip+' is available')
else:
    print('unknown case for '+ip)

    
ip='138.23.11.240'
r=os.popen('ping -c 1 '+ip).read()
#print(r)

if r[:4]=='ping':
    print('the ip '+ip+' is not availble')
elif r[:4]=='PING':
    print('the ip '+ip+' is available')
else:
    print('unknown case for '+ip)
#r=os.popen('ping -c 1 138.23.11.240').read()




#ping cherenkov.dyn.ucr.edu
