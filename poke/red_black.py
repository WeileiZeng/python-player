
'''
Classical game of guessing red and black
2 players
Author: Weilei Zeng, May 3rd, 2024
'''
import random

blue='\033[36m'
red='\033[31m'
dark='\033[30m'
light_white='\033[29m'
green='\033[32m'
grey='\033[90m'
white='\033[0m'

SPADE=0  #black
HEART=1  #red
CLUB=2
DIAMOND=3
COLOR=['spade','heart','club','diamond']
PRINT_COLOR=[grey,red,grey,red]
class Card:
    def __init__(self,color=SPADE,number=0,id=None):
        if id:#define from id; id=0 will jump to the default value
            self.id=id
            self.color=id//13
            self.number = id % 13
        else:#define from color and number
            self.color=color
            self.number=number
            self.id=self.color*13+number
    def get_pic(self):
        return f'assets/{self.id}.png'
    def is_red(self):
        if self.color in [HEART,DIAMOND]:
            return True
        else:
            return False
    def __repr__(self):
        
        return f'{PRINT_COLOR[self.color]}{COLOR[self.color]} {self.number} {white}'
    
def get_full_stack():
    stack=[]
    for i in range(52):
        card=Card(id=i)
        #print(card,end=',')
        stack.append(card)
    #print()
    return stack

def count_cards(cards):
    #count red and black        
    Nr,Nb=0,0
    for card in cards:
        if card.is_red():
            Nr += 1
        else:
            Nb +=1
    return Nr,Nb

class Player:
    def __init__(self,name,stack):
        self.name=name
        self.stack=stack
        #count red and black        
        self.Nr,self.Nb=count_cards(self.stack)
        assert self.Nr+self.Nb == len(self.stack)
        
    def __repr__(self):
        s=f'{self.name} has {red}{self.Nr}{white}+{grey}{self.Nb}{white}={len(self.stack)} cards'
        return s

    def draw(self):
        assert len(self.stack)>0


        #determine mode
        #d: mode flag, 0 for red, 1 for black, 2 for red and black
        if self.Nr == 0:#no red card
            d=1
        elif self.Nb == 0:#no black card
            d = 0
        else: #draw random card
            d=random.randint(0,2) 
        drawn=[]
        try:
            nr=random.randint(1,self.Nr)
            nb=random.randint(1,self.Nb)
        except:
            pass
        if d == 0 or d == 2:#red
            n=0
            for card in self.stack:
                if card.is_red():
                    drawn.append(card)
                    n += 1
                    if n == nr:
                        break
        if d == 1 or d == 2:#black
            n=0
            for card in self.stack:
                if not card.is_red():
                    drawn.append(card)
                    n +=1
                    if n == nb:
                        break
        print(f'{self.name} draw {len(drawn)} cards:{drawn}')
        assert len(drawn)>0
        return d, drawn
    def guess(self):
        d = random.randint(0,2)
        _=['red','black','red & black']
        print(f'{self.name} guesses for {_[d]}')
        return d

    def add_cards(self,cards):
        Nr,Nb=count_cards(cards)
        self.Nr +=Nr
        self.Nb +=Nb
        self.stack.extend(cards)
    def remove_cards(self,cards):
        Nr,Nb=count_cards(cards)
        self.Nr -=Nr
        self.Nb -=Nb
        for card in cards:
            self.stack.remove(card) #very inefficient but it works

def put(long_text,substitute,offset):
    s=long_text[:offset]+substitute
    if len(s)>=len(long_text):
        s=s[:len(long_text)]
    else:
        s = s+long_text[len(s):]
    return s

def put_middle(long_text,substitute):
    offset = (len(long_text)-len(substitute))//2
    return put(long_text,substitute,offset)

background='.' #' '
class Screen:
    def __init__(self):
        self.width=100
        self.height=20
        self.rows=[background*self.width for i in range(self.height)]
        #boarder
        self.rows[0]='-'*self.width
        self.rows[-1]='-'*self.width
        for i in range(0,self.height-1):
            self.rows[i] = put(self.rows[i],'|',0)
            self.rows[i] = put(self.rows[i],'|',-1)
        #head
        _='* Red and Black *'
        #l=(self.width-len(_))//2
        self.rows[0]=put_middle(self.rows[0],_)
        #background*l+_+background*l
        left='Alice'
        right='Bob'
        self.rows[3]=put(self.rows[3],left,15)
        self.rows[3]=put(self.rows[3],right,self.width-15)
        
        
    def __repr__(self):
        #s='\n'.join(['.'*self.width for i in range(self.height)])
        s='\n'.join(self.rows)
        return s
    def put_cards(self,cards, left=True):
        offset=10
        if not left:
            offset += self.width//2
            
        for card in cards:
            c = card.color * 10 + offset
            r = card.number+5
            self.rows[r]= put(self.rows[r],str(card.number),c)

def screen_test():
    screen=Screen()
    stack=get_full_stack()
    print(stack)
    screen.put_cards(stack,False)
    print(screen)

    


        
    
def main():    
    print('''
    Game begins!
    ''')
    stack=get_full_stack()
    print('full stack:',stack)
    random.shuffle(stack)
    print(stack[:26])
    print(stack)
    alice=Player('Alice',stack[:26])
    bob= Player('Bob',stack[26:])                
    print(alice)
    print(bob)

    #game loop
    players=[alice,bob]
    round = 0
    while True:
        print()
        print('~'*30+' Round '+str(round)+' '+'~'*30)
        print(players)
        p1,p2=players    
        d,drawn=p1.draw()
        d2=p2.guess()
        print(d,d2)
        if d==d2:#p2 wins
            print(f'{p2.name} win the cards')
            p2.add_cards(drawn)
            p1.remove_cards(drawn)
            if len(p1.stack) == 0:
                print(f'{p1.name} loses all cards. {p2.name} win the game!')
        else:
            print(f'Wrong guess, {p2.name} got nothing.')
            pass
        input('Click for next step...')
        players.reverse()
        round +=1

if __name__=="__main__":
    screen_test()        
    #main()
