
import random


#get a list of random names
namelist=None
with open('1000namelist.txt','r') as f:
    s=f.readlines()
    namelist=[name[:-1] for name in s]
#    print(namelist)
    
    
def poisson(p):
    n = 1000000
    s = 0
    for i in range(n):
        v=0
        while (random.random()>p):
            v +=1
        s +=v
#        print(v)
    average = 1.0*s/n
    print('p={:.1f}, {:.3f}, average = {:.3f} over {} instances'.format(p,(1-p)**2, average,n))
#    print(f'p={p}, average = {average} over {n} instances')

def get_prob(birth_rate):
    pass


def poisson_test():
    for i in range(1,10):
        p = 0.1 * i
        poisson(p)


class People:
    male=1
    female=2
    def __init__(self,name=None,sex=None):
        self.name=name
        self.sex=sex
        self.partner=None
        self.children=[]
        pass
    def __repr__(self):
        s='People: '
        if self.name:
            s = s +self.name
        def sex_str(sex):
            if sex == People.male:
                return "boy"
            else:
                return "girl"
        if self.sex:
            s = s +' ('+ sex_str(self.sex)+')'
        return s
        
    #def __str__(self):
        return 'haha'
'''
        self.name
        self.id
        self.generation
        self.sex
        self.age
        self.dad
        self.mom
        self.partner
        self.children
'''
def marry(husband,wife):
    husband.partner=wife
    wife.partner=husband
    #print(f"{husband.name} gets married to {wife.name}")

def born(dad):
    baby=People()
    baby.sex=People.male if random.random() <0.5 else People.female
    baby.name=namelist[random.randint(0,1000-1)] #get random name
    dad.children.append(baby)
    return baby

#return a group of n people
def get_random_people(n):
    peoples=[]
    men=[]
    women=[]
    for i in range(n):
        people = People()
        people.sex=People.male if random.random() <0.5 else People.female
        people.name=namelist[random.randint(0,1000-1)] #get random name
        if people.sex==People.male:
            men.append(people)
        else:
            women.append(people)
        peoples.append(people)
    return peoples,men,women

#hard to use discarded
def init():
    adam = People()
    adam.name='adam'
    adam.generation=0
    adam.sex=People.male
    
    eve = People()
    eve.name='eve'
    eve.sex=People.female
    eve.generation=0

    generation=[adam,eve]
    print('The 0th generation:',generation)
    men=[adam]
    women=[eve]    
    marry(adam,eve)

def report(g,men,women):
    print(f"The {g}th generations has {len(men)} boys and {len(women)} girls")
    return
    print('boys:',','.join([man.name for man in men]))
    print("girls:",','.join([woman.name for woman in women]))

#@n, number of initial people
def populate(n,num_generations,birth_rate):
#    print('The world begins...')
    #init the first generation
#    n = 2000
    peoples,men,women =  get_random_people(n)
    
    #now population to next generation
#    num_generations=20
    generations=[peoples]
    mens=[men]
    womens=[women]
#    report(0,men,women)
    for i in range(num_generations):
        generation=generations[i]
        generation_new=[]
        men,women = mens[i],womens[i]
        men_new=[]
        women_new=[]
        #now consider marridge
        random.shuffle(men)
        random.shuffle(women)
        min = len(men) if len(men) <len(women) else len(women)
#        print(f'{min} couples get married')
        for j in range(min):
            man, woman = men[j], women[j]
            marry(man,woman)


        
        for man in men:
            if man.partner: #if married
                while (random.random()*2<birth_rate):
                    baby = born(man)
                    generation_new.append(baby)
#                    print('hello',baby.name)
                    if baby.sex ==People.male:
                        men_new.append(baby)
                    else:
                        women_new.append(baby)                        
#        print(f'The {i+1}st generation',generation_new)
#        report(i+1,men_new,women_new)
        #  print(generation_new)
        generations.append(generation_new)
        mens.append(men_new)
        womens.append(women_new)
        if len(generation)==0:
            break
        
#    print('End of program')
    return len(generations[-1])

def lin(min,max,points):
    step = 1.0*(max-min)/points
    return [min+step*i for i in range(points)]

def main():
    n=1000
    num_generations=20
    birth_rate=1.35 #the population ratio between two generations
    rates=lin(1.340,1.344,10)
    rates=lin(1.341,1.342,10)
    for rate in rates:
        repeat = 200
        m=0
        flag=0
        for _ in range(repeat):
            p = populate(n,num_generations,rate)
            m += p
            if p >n :
                flag +=1
            else:
                flag -=1
        flag = flag*1.0/repeat
        m = m*1.0/repeat
        print('rate={:.5f}, n={},m={:.1f},ratio={:.3f},flag={:.3f}'
              .format(rate,n,m,1.0*m/n,flag))
#        print(n,m,rate)

    
main()
    
