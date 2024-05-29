import time
import copy
import random

# config constant
IDLE=0
UP=1
DOWN=-1
MAINTAIN=2
speed_str=["idle","up","down"]

# config parameter
FLOOR_MAX = 20

class People:
    def __init__(self):
        self.floor=1
        self.destination=7
        self.in_elevator=False
        self.elevator=None
        
class Elevator:
    def __init__(self,index):
        self.index=index
        self.floor=1
        self.num_up=0
        self.num_down=0
        self.speed = UP #up down idle maintain
        self.destinations=[]
        self.passengers=[]
        self.cd=0 #cooling delay
        
    def check(self, peoples):
        # send off people one by one
        for p in self.passengers:
            if p.destination == self.floor:
                self.passengers.remove(p)
                if self.speed != IDLE:
                    self.previous_speed = self.speed
                    self.speed == IDLE
                self.cd += 1
                return
        # all/no people sent off, continue
        
        # load people
        if len(peoples[self.floor]) > 0 :
            if self.speed != IDLE:
                # stay idle and check in next timestep
                self.previous_speed = self.speed
                self.speed = IDLE
                return
            else: #already IDLE,
                # add one people one time
                p = peoples[self.floor][0]                
                #for p in peoples[self.floor]:
                self.passengers.append(p)
                peoples[self.floor]=peoples[self.floor][1:]
                self.cd += 3
                return
        if self.speed == IDLE:
            if self.cd:
                self.cd -= 1
                return
            #recover speed
            self.speed = self.previous_speed

        if self.speed != IDLE:
            # flip direction
            if self.floor == FLOOR_MAX :
                self.speed = DOWN
            if self.floor == 1:
                self.speed = UP

            
    def move(self):
        self.floor += self.speed
        if self.speed != IDLE:
            assert self.cd ==0
        




class Building:
    def __init__(self):
        self.height=FLOOR_MAX
        self.width=80
        self.num_elevators=4
#        self.screen= ["#"+"|_____|"*self.num_elevators+"#"]*(self.height+2)
        self.screen= ["#"+"."*self.width+"#"]*(self.height+2)        
        self.screen[0]="#"*(self.width+2)
        self.screen[-1]="#"*(self.width+2)
        self.screen_base = copy.copy(self.screen)

        self.screen_base = [ self.screen_base[i] + ' ' + str(  i  ) + '\t'  for i in range( len(self.screen_base))] 
        self.elevators=[]
        for i in range(self.num_elevators):
            e=Elevator(i)
            self.elevators.append(e)

        self.peoples=[ [] for i in range(self.height + 2) ]
        #p = People()
        #self.peoples[1].append(p)
        self.add_people(15)

        
    def add_people(self,n=1): #add random people
        p = People()
        p.floor = random.randint(3,self.height)
        p.destination = random.randint(1,self.height)
        while p.floor == p.destination:
            p.destination = random.randint(1,self.height)
        self.peoples[p.floor].append(p)

        if n > 1:
            self.add_people(n-1)
        
    def flush(self):
        print(' ')
        for i in range(self.height+2):
            floor = self.height - i + 1
            print(self.screen[floor])
#        for _ in self.screen):
#            print(_)
        print(' ')
            
    def draw_elevator(self):
        for e in self.elevators:
            row=e.floor #self.height-e.floor+1
            s=self.screen[row]
            pos=1+20*e.index
            passengers = ','.join([ str(p.destination) for p in e.passengers ])
            info = f'{e.floor} {speed_str[e.speed]} cd{e.cd} {passengers}'
            
            _ = (".|"+ info + "________________") [:18] + "|."
            #s=s[:pos]+".|______|."+s[pos+10:]
            s=s[:pos]+_+s[pos+20:]
            #s[10*e.index,10*e.index+10]=".|______|."
            self.screen[row]=s
    def run(self):
        for e in self.elevators:
            e.check(self.peoples)
            e.move()
        #move one time step

        #add and clean people
        
        #decide direction of elevator
        #update all people

        #move

        #draw
        self.screen = copy.copy(self.screen_base)
        self.draw_elevator()

        #draw people
        for i in range(self.height):
            floor = i+1
            people_on_floor = self.peoples[floor]
            for p in  people_on_floor:
                #print(p)
                self.screen[floor] = self.screen[floor] + f'p{p.floor}->{p.destination},'
            
        self.flush()

def main():
    building=Building()
    building.flush()
    #input()
    for i in range(1000):
        print(i)
        building.run()
        input()
        #time.sleep(1)



if __name__=="__main__":
    main()

        
