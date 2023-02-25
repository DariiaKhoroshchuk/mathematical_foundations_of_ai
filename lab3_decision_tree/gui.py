from graphics import Line, GraphWin, Point, Circle

SIZE = 100  # cell width
PADDING = 20  # distance between icon and cell
WIDTH = 4  # line width

win = None  # window
items = []


# window initialization
def init():
    global win
    win = GraphWin('Tic Tac Toe', SIZE*3, SIZE*3)
    Line(Point(SIZE, 0), Point(SIZE, 3*SIZE)).draw(win)
    Line(Point(SIZE*2, 0), Point(SIZE*2, 3*SIZE)).draw(win)
    Line(Point(0, SIZE), Point(3*SIZE, SIZE)).draw(win)
    Line(Point(0, SIZE*2), Point(3*SIZE, SIZE*2)).draw(win)


# user's move
def get_turn(board):
    global win
    point = None
    while point is None:
        p = win.getMouse()
        x = int(p.getX() / SIZE)
        y = int(p.getY() / SIZE)
        p = 3*y+x
        if board[p] == 0:
            point = p
    draw_iks(x, y)
    return point


def draw_iks(x, y):
    global items
    line1 = Line(Point(x*SIZE+PADDING, y*SIZE+PADDING), Point((x+1)*SIZE-PADDING, (y+1)*SIZE-PADDING))
    line1.setWidth(WIDTH)
    line1.draw(win)
    items.append(line1)
    line2 = Line(Point(x*SIZE+PADDING, (y+1)*SIZE-PADDING), Point((x+1)*SIZE-PADDING, (y)*SIZE+PADDING))
    line2.setWidth(WIDTH)
    line2.draw(win)
    items.append(line2)


def draw_o(x, y):
    global items
    c = Circle(Point(x*SIZE+SIZE/2, y*SIZE+SIZE/2), SIZE/2 - PADDING)
    c.setWidth(4)
    c.draw(win)
    items.append(c)


def reset():
    global items
    for item in items:
        item.undraw()
