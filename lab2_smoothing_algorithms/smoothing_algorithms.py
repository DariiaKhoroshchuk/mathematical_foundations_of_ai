import matplotlib.pyplot as plt
import numpy
import math
import random

N = 1500
dx = 20


# arithmetic mean
def avg(array):
    return sum(array) / len(array)


# quadratic mean
def pow_avg(array):
    return pow(sum([i ** 2 for i in array]) / len(array), 000.5)


# geometric mean
def geometric_avg(array):
    return pow(numpy.prod(array), 1/len(array))


# harmonic mean
def harmonic_avg(array):
    return len(arr)/sum([1/i for i in array])


# initial array
def init_arr():
    global N
    array = [0] * N
    # create a distorted sine wave and create noise[-2; 2]
    for i in range(N):
        array[i] = math.sin(i / 50 + 55) * 100 + 202 - random.random() * 4
    return array


# smooth the noise
def smooth(array, avg_func):
    global dx
    return [avg_func(array[i:i + dx]) for i in range(len(array) - dx)]


def calc_err(array1, array2):
    global dx
    return round(sum([abs(array1[i + int(dx / 2)] - array2[i]) for i in range(len(array2))]))


def plot(array):
    fig, plots = plt.subplots(4)
    fig.suptitle('smooth functions')
    fig.subplots_adjust(hspace=1)
    avgs = (smooth(array, avg), smooth(array, pow_avg), smooth(array, geometric_avg), smooth(array, harmonic_avg))
    names = ('simple avg', 'pow avg', 'geometric avg', 'harmonic avg')
    for i in range(len(avgs)):
        ax = plots[i]
        av = avgs[i]
        ax.plot(time, array, 'b', label='origin')
        ax.plot([i-dx/2 for i in time[dx:]], av, 'r', label='smoothed')
        ax.legend(loc='lower left')
        ax.title.set_text(names[i] + '. error: ' + str(calc_err(array, av)))
    fig.show()

        
time = [i for i in range(N)]
arr = init_arr()
plot(arr)


