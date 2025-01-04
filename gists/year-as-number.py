
def square(n:int) -> int:
    result=0
    for i in range(n):
        result += i*i
    return result

def cube(n):
    result=0
    for i in range(n):
        result += i*i*i
    return result

def square_and_cube(n):
    return square(n) + cube(n)

def sum(n):
    result=0
    for i in range(n):
        result += i
    return result
    
def poly(n):
    return sum(n) + square(n) + cube(n)

def main():
    n=12
    years=[]
    for i in range(n):
        years.extend([sum(i),square(i),cube(i),square_and_cube(i),poly(i)])
        #print(square(i))
        #print(cube(i))
    years.sort()
    print(years)

main()

    
