import numpy as np
import matplotlib.pyplot as plt
from math import*
from time import time
import random
from scipy import integrate

x = []
y = []

a = 1.0
b = 2.0
N = 10000
points_x = []
points_y = []
num_of_points = 0
right_x = []
right_y = []
wrong_x = []
wrong_y = []
f0 = 0.0
f1 = 59.0

start = time()


def func(x):
    return pow(e, x*x)


# random by x
def rand_x(a, b):
    for _ in range(N):
        points_x.append(random.uniform(a, b))


# random by y
def rand_y(f0, f1):
    for _ in range(N):
        points_y.append(random.uniform(f0, f1))


def absolute_error(integral):
    return abs(integrate.quad(func, a, b)[0]-integral)


def relative_error(integral):
    return (absolute_error(integral)/integral)*100


rand_x(a, b)
rand_y(f0, f1)

i = a
while i <= b:
    x.append(i)
    y.append(func(i))
    i += 0.00001
plt.plot(x, y)

# monte carlo method
for i in range(N):
    if points_y[i] <= func(points_x[i]):
        right_x.append(points_x[i])
        right_y.append(points_y[i])
        # plt.scatter(points_x[i], points_y[i], c='blue', s=1)
        num_of_points += 1
    else:
        wrong_x.append(points_x[i])
        wrong_y.append(points_y[i])
        # plt.scatter(points_x[i], points_y[i], c='black', s=1)
plt.scatter(right_x, right_y, c='black', s=1.5)
plt.scatter(wrong_x, wrong_y, c='blue', s=1.5)
S = (b-a)*(f1-f0)
integral = S*(num_of_points/N)
plt.title(f"The exact value of the integral = {integrate.quad(func, a, b)[0]}\n"
          f"Integral by Monte Carlo = {integral}")


print(f"Integral = {integral}")

print(f"Абсолютна похибка основної задачi {np.around(absolute_error(integral), decimals=5)}")
print(f"Вiдносна похибка основної задачi {np.around(relative_error(integral), decimals=3)}%")
end = time()

print(f'Значення функцiї {func(2)}')
# print(f"Time of calculation is {int(end-start)} seconds")
plt.show()
