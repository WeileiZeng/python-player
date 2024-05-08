
light_white='\033[29m'
grey='\033[90m'
blue='\033[36m'
white='\033[0m'


def factor(n):#this is not the prime factor
    pairs=[]
    factors=[]
    for i in range(1,11):
        if n % i == 0:
            j = n//i
            if j < 11:
                pairs.append((i,j))
                factors.append(i)
    if len(pairs) == 0:
        print(n,'can not be factored by 1-10')
    return factors
    #return pairs
        
def factor_test():
    for n in range(100):
        print(n,factor(n))
        
#factor_test()

def common(fa,fb):
#def common(pairs_a,pairs_b):
    #return common factor of a and b
#    fa=[_[0] for _ in pairs_a]
#    fb=[_[0] for _ in pairs_b]
    fc=[]
    for f in fa:
        if f in fb:
            fc.append(f)
    return fc
            
def update_factor(fin,f):
    #update the factors using new constraint
    fout=f.copy()
    if fin == 0:
        return fout
    else:
        for i in f:
            if i not in fin:
                fout.rm(i)
    return fout

def exclude_factor(fin,f):
    #rm factor f from fin
    for i in f:
        if i in fin:
            fin.remove(i)
    return fin


def print_array(array):
    print('-------- array 10 x 10 --------')
    for row in array:
        _=''
        for i in row:
            _ = _ + f'{i:3d}'
        print(_)
    print('-------------------------------')

def print_puzzle(puzzle,doc=''):
    array=puzzle.array
    print('----------- puzzle 10 x 10 ---------- '+doc)
    #print row as header
    _='|'+blue + '           X         '
    for i in puzzle.row:
        t=f'{i}'
        _ = _ + f'{t:^12s}'
    _ = _ + white +''
    print(_)

    for j in range(10):
        row=array[j]
        t=f'{puzzle.col[j]}'
        _='|'+ blue+f'{t:^15s}' +white
        for i in row:
            _ = _ + f'{i:12d}'
        _ = _ +'  |'
        print(_)
    print('-------------------------------------')
    

    
    
def str2array(s):
    rows=s.split('\n')
    str_array=[ row.replace('\t','\t ').split('\t') for row in rows]            
    array=[ [0 for _ in range(10)] for _ in range(10)]
    for i in range(10):
        #print(str_array[i])
        for j in range(10):
            s=str_array[i][j]
            if s not in ['',' ']:
                array[i][j]=int(s)
    return array

def filename2array(filename):
    with open(filename,'r') as f:
        s=f.read()
        array = str2array(s)
    return array


class Puzzle:
    def __init__(self,data=None):
        print('init')
        if data:
            pass
        else:
            self.default()

    def default(self):        
        filename="puzzle1.dat"
        print(filename)
        array= filename2array(filename)
        print_array(array)
        self.array=array
        self.row=[0 for _ in range(10)]
        self.col=[0 for _ in range(10)]
    
    def solve(self):
        while(True):
            #update row and col
            for i in range(10):
                for j in range(10):
                    n= self.array[i][j]
                    if n:
                        f=factor(n)
                        #should update
                        self.col[i]=update_factor(self.col[i],f)
                        self.row[j]=update_factor(self.col[j],f)
            print('after first update')
            self.print()
            #check for the same row
            for i in range(10):
                a,b=0,0
                ai,aj,bi,bj=0,0,0,0
                for j in range(10):
                    n= self.array[i][j]
                    if n:#nonzero
                        if a==0:
                            a=n
                            ai,aj=i,j
                        else: #find two nonzero
                            b=n
                            bi,bj=i,j
                            break
                if b:
                    pair_a=factor(a)
                    pair_b=factor(b)
                    print(f'find two numbers in row {i}: {ai,aj},{a},{bi,bj},{b}')
                    print(a,pair_a,b,pair_b)
                    # common factor for i=ai=bi 
                    assert ai==bi
                    self.col[bi]=[6,9]
                    self.print()
                    
            #check for same column       
            for j in range(10):
                a,b=0,0
                ai,aj,bi,bj=0,0,0,0
                for i in range(10):
                    n= self.array[i][j]
                    if n:#nonzero
                        if a==0:
                            a=n
                            ai,aj=i,j
                        else: #find two nonzero
                            b=n
                            bi,bj=i,j
                            break
                if b:
                    pair_a=factor(a)
                    pair_b=factor(b)
                    print(f'find two numbers in col {j}: {ai,aj},{a},{bi,bj},{b}')
                    print(a,pair_a,b,pair_b)
                    # common factor for j=aj=bj
                    assert aj==bj
                    factors=common(pair_a,pair_b)
                    if len(factors)==1:
                        f=factors[0]
                        self.row[aj]=f
                        af=a//f
                        bf=b//f
                        self.col[ai]=af
                        self.col[bi]=bf
                        #exlcude
                        for k in range(10):                          
                            if type(self.row[k])==list:
                                if k != aj:
                                    if f in self.row[k]:
                                        print(f'now remove {f} from row {k}')
                                        print('before',k,self.row[k])
                                        self.row[k].remove(f)
                                        print('after',k,self.row[k])
                                        pass
                            if type(self.col[k])==list:
                                if k != ai:
                                    if af in self.col[k]:
                                        self.col[k].remove(af)
                                if k != bi:
                                    if bf in self.col[k]:
                                        self.col[k].remove(bf)
                            self.print(f' index {af,bf,f,k}')

                        
                    self.print()

            break
        pass

    def print(self,doc=''):
        print_puzzle(self,doc=doc)
    
def main():
    print('main')
    puzzle=Puzzle()
    puzzle.print()
    #print_puzzle(puzzle)
    puzzle.solve()
    


if __name__=="__main__":
    #factor_test()
    main()
    print('done')
