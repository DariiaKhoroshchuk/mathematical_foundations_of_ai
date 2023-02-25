import gui as gui
from game_tree import create_game_tree, make_choice

origin = create_game_tree()
gui.init()

while True:
    gui.reset()
    state = origin
    while state.get("win") == 0:
        p = gui.get_turn(state.get("board"))
        for child in state.get("children"):
            if child.get("board")[p] == -1:
                state = child
                break
        children = state.get("children")
        if len(children) == 0:
            break
        i = make_choice(state)
        pos = 0
        for j in range(len(state.get("board"))): 
            if state.get("board")[j] != children[i].get("board")[j]:
                pos = j
                break
        gui.draw_o(pos % 3, pos//3)
        state = children[i]
    gui.win.getMouse()
