from graphics import *

win = GraphWin("My Test", 100, 100)

my_object = Circle(Point(50, 50), 10)

my_object.draw(win)

dx, dy = 10, 0

while True:
    k = win.checkKey()

    if k == 'Left':
        my_object.move(-dx, dy)
    elif k == 'Right':
        my_object.move(dx, dy)
    elif k == 'period':
        break
    print('*')

win.close()
