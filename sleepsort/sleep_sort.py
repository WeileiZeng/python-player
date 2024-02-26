import threading
import time
import sys

print('''
Program name: sleep sort
Author:       Weilei Zeng
Date:         Feb 21, 2024
Goal:         Sort a list of unordered numbers
Introduction: Loop through the list, for each item, print the number after sleep number of timesteps. Number with smaller values will wake up from the sleeping first, hence get printed first. As a result, the output will be an ordered list.
Tricks:       For large list and very small timesteps, the sleeping order may get interrupted by other tasks in the busy CPU. Take the output and rerun the program can solve this issue. Using larger timesteps is also a solution, but now one need to consider the trade off between timestep duration and number of trials.
''')

#def ENV
#n_total=5000*6+100

import os
cols, lins = os.get_terminal_size()
#71,39
if cols < 120:
        lins -= 2
n_total = cols*(lins-4) #print in the full screen
#n_total=8000
timestep=1/10000.0 # Sleep for 'num' timesteps (sec)
bench=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
icon =['0', '1', "\033[93m{}\033[00m" .format('<'), '3', '\033[91m{}\033[00m'.format('.'), '5', "\033[92m{}\033[00m" .format(':'), '7', "\033[93m{}\033[00m" .format('>'), '9'] #for print
int_min=1  #used range of icons
int_max=9
ratio_expected=16.5 #sample: 15.2 18.25, 16.7

# This function will be executed by each thread
def routine(num):
	# Sleeping time is proportional to the number
	time.sleep((0+num) * timestep) 
	print(num, end=" ")

# A function that performs sleep sort
def sleep_sort(arr):
	threads = []

	# Create a thread for each element in the input array
	for num in arr:
		thread = threading.Thread(target=routine, args=(num,))
		threads.append(thread)
		thread.start()
#		print(' ')
#                print('*')
                
                

	# Wait for all threads to finish
	for thread in threads:
		thread.join()

                
def str2int(str_arr): #for array
        int_arr=[]
        #list(range(len(str_arr)))
        for s in str_arr:
                int_arr.append(int(s))
        return int_arr


def pour(arr):
        s=''.join(["." if _ == 5 else str(_) for _ in arr])
        s=''.join([icon[_] for _ in arr])        
        print(s)


def step(arr):        
        sys.stdout = open('tmp.txt','w')
        sleep_sort(arr)
        print()
        sys.stdout = original
        with open('tmp.txt', 'r') as f:
            l=f.readline()
            a=l.split()
            #print(a)
            b=str2int(a)
            pour(b)
            #print('after sorting:',b)
            #print(l,file=original)
        return b
original = sys.stdout

import random
# return a list of random int
def get_arr(n):
        return [random.randint(int_min,int_max) for _ in range(n)]

# evaluated the order in current list
def eval(arr):
        n = len(arr)
        val = [0]*10
        for i in range(n):
                val[arr[i]] += i
        ratio = val[-1]/val[1]
#        ratio_expected = 18.25
        print('ratio={:.3f} {:.1f}%'.format(ratio,ratio/ratio_expected*100.0),end=' ')
        print('list =',val,end='\n')
'''
        #not useful
        ss=0.0
        for i in range(1,9):
                ss += (val[i+1]-val[i])**2
        ss=ss/8.0
        ss_expected = 81144753585.5
        print(ss/ss_expected,'ss=',ss,74199989977.5,81144753585.5)
'''
# check if the two arrayed are identical        
def match(arr1,arr2):
#        eval(arr1)
        n = len(arr1)
        for i in range(n):
                if arr1[i] != arr2[i]:
                        return False
        return True

if __name__ == "__main__":
        # Doesn't work for negative numbers
        arr = [34, 23, 122, 9]
        arr = [3,7,5,6,9,8,2,4,5,7,3,5,6]
        arr = [3,7,5,6,9,8,2,4,5,7,3,5,6,7,5,6,3,6,4,5,7,8,5,6,2]
        arr = get_arr(n_total)
#        print('initial arr:  ',arr)
        pour(arr)
#        for i in range(10):
        i = 0
        flag = 0
        while True:
                print()
                print(f'round {i}: ', end='')
                eval(arr)
                arr2=step(arr)
                if match(arr2,arr) :
                        print('match after round ', i)
                        flag += 1
                        if flag > 1:
                                break
                else:
                        arr = arr2
                i +=1

#Contributed by Aditi Tyagi
