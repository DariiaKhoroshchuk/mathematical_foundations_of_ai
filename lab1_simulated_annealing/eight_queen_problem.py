from random import randint, random
import math

N = 8
INITIAL_T = 30
FINAL_T = .5
ALPHA = .98  # coefficient for T reduction
EPOCH = 100  # how many moves do we make before reducing T

queens = [i for i in range(N)]
t = INITIAL_T


def compute_error(arr):  # how many queens are beaten each other, target -> error = 0
    cols = 0  # number of hits
    for i in range(N):
        x = i
        y = arr[i]
        for j in range(4):
            dx = 1 if j % 2 == 0 else -1
            dy = 1 if j < 2 else -1
            temp_x = x
            temp_y = y
            while True:
                temp_x += dx
                temp_y += dy
                if temp_x < 0 or temp_y < 0 or temp_x >= N or temp_y >= N:
                    break  # checking if we are within the board
                if arr[temp_x] == temp_y:  # if true, we found the queen that beats
                    cols = cols + 1
    return cols / 2


def flip():  # swap columns
    a = randint(0, N - 1)
    while True:
        b = randint(0, N - 1)
        if b != a:
            break
    flip_arr = [i for i in queens]
    flip_arr[a] = queens[b]
    flip_arr[b] = queens[a]
    return flip_arr


err = compute_error(queens)
found = False
while t > FINAL_T and not found:
    for _ in range(EPOCH):
        new_arr = flip()
        use_new = False
        new_err = compute_error(new_arr)
        use_new = (new_err <= err or math.exp((err - new_err) / t) > random())
        if use_new:
            queens = new_arr
            err = new_err
        if new_err == 0:
            found = True
            break

    t = t * ALPHA
# showing board
for i in range(N):
    print(' '.join(['Q' if queens[i] == j else '-' for j in range(N)]))
