import random
from collections import defaultdict
from copy import deepcopy
import numpy as np

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
classes = ["A", "B", "C"]
subjects = ["Maths", "English", "Writing", "Art", "Sport", "Music", "Dance", "Informatics"]
min_num_of_subjects = [3, 3, 3, 2, 1, 1, 1, 3]
max_num_of_subjects = [5, 5, 5, 4, 3, 3, 3, 5]
teachers = [3, 3, 3, 3, 1, 1, 1, 1]

subjects_with_one_teacher = ["Sport", "Music", "Dance", "Informatics"]

MAX_POPULATIONS = 300
MEMBERS_PER_POPULATION = 10


def init_time_table():
    random.seed()
    week_table = {"Monday": {}, "Tuesday": {}, "Wednesday": {}, "Thursday": {}, "Friday": {}}
    for day in days:
        day_table = defaultdict(list)
        for c in classes:
            for _ in range(5):
                day_table[c].append(subjects[random.randint(0, len(subjects) - 1)])
        week_table[day] = day_table
    return week_table


def init_populations(n=5):
    tables = list()
    for _ in range(n):
        tables.append(init_time_table())
    return tables


def get_score_days(population):
    sum_d = [0] * 5
    for day in days:
        for i1 in range(len(classes)):
            for i2 in range(i1 + 1, len(classes)):
                c1 = classes[i1]
                c2 = classes[i2]
                if c1 != c2:
                    for j in range(5):
                        if population[day][c1][j] == population[day][c2][j] \
                                and population[day][c1][j] in subjects_with_one_teacher:
                            sum_d[j] += 10
    for day in days:
        for c in classes:
            sum_d[j] += (5 - len(set(population[day][c]))) * 1
    return sum_d


def get_score_day(day_table):
    sum_d = 0
    for i1 in range(len(classes)):
        for i2 in range(i1 + 1, len(classes)):
            c1 = classes[i1]
            c2 = classes[i2]
            if c1 != c2:
                for j in range(5):
                    if day_table[c1][j] == day_table[c2][j] and day_table[c1][j] in subjects_with_one_teacher:
                        sum_d += 10
    for c in classes:
        sum_d += (5 - len(set(day_table[c]))) * 1
    return sum_d


def get_score_population(population):  
    sum_d = 0
    for day in days:
        for i1 in range(len(classes)):
            for i2 in range(i1 + 1, len(classes)):
                c1 = classes[i1]
                c2 = classes[i2]
                if c1 != c2:
                    for j in range(5):
                        if population[day][c1][j] == population[day][c2][j] \
                                and population[day][c1][j] in subjects_with_one_teacher:
                            sum_d += 10
    # Обчислення для вищезгаданих предметів за один день
    for day in days:
        for c in classes:
            sum_d += (5 - len(set(population[day][c]))) * 1

    # Обчислення кількості тих же уроків за тиждень
    for c in classes:
        for i in range(len(subjects)):
            num_of_lessons = 0
            for day in days:
                for j in range(5):
                    if population[day][c][j] == subjects[i]:
                        num_of_lessons += 1
            if min_num_of_subjects[i] > num_of_lessons:
                sum_d += abs(num_of_lessons - min_num_of_subjects[i]) * 5
            elif num_of_lessons > max_num_of_subjects[i]:
                sum_d += abs(num_of_lessons - max_num_of_subjects[i]) * 5
    return sum_d


def get_scores(populations):
    res_arr = list()
    for i in range(len(populations)):
        res_arr.append(get_score_population(populations[i]))
    return res_arr


def get_best(scores, k=3):
    saved = scores[:]
    scores.sort()
    res = list()
    for i in range(k):
        res.append(saved.index(scores[i]))
    return res


def cross_over_populations(populations, scores):
    best_scores = get_best(scores)
    best_populations = [populations[best_scores[0]], populations[best_scores[1]], populations[best_scores[2]]]
    result_arr = list()
    result_arr.append(cross_over(best_populations[0], best_populations[1]))
    result_arr.append(cross_over(best_populations[0], best_populations[2]))
    result_arr.append(cross_over(best_populations[1], best_populations[2]))
    return result_arr


def cross_over(population1, population2):
    result_population = dict()
    errors1 = get_score_days(population1)
    errors2 = get_score_days(population2)
    for i in range(len(days)):
        if errors1[i] < errors2[i]:
            result_population[days[i]] = deepcopy(population1[days[i]])
        elif errors2[i] < errors1[i]:
            result_population[days[i]] = deepcopy(population2[days[i]])
        else:
            mutated = mutate(deepcopy(population1[days[i]]))
            error = int(get_score_day(mutated))
            if int(error - errors1[i]) < 0:
                result_population[days[i]] = mutated
            else:
                result_population[days[i]] = population1[days[i]]
    return result_population


def mutate(day_schedule):
    for cl in day_schedule:
        if random.randint(0, 9) < 7:
            day_schedule[cl][random.randint(0, 4)] = subjects[random.randint(0, len(subjects)-1)]
    return day_schedule


def print_time_table(timetable):
    for cl in classes:
        print("{:<15}".format(cl), end=" ")
    print()
    for day in days:
        print("Day: ", day)
        for i in range(5):
            for cl in classes:
                print("{:<15}".format(timetable[day][cl][i]), end=" ")
            print()
        print()


if __name__ == "__main__":
    best_population = []
    best_score = 9999
    prev_population = 999999999
    populations = init_populations(MEMBERS_PER_POPULATION)
    scores = get_scores(populations)
    avg_score = np.mean(scores)
    for i in range(MAX_POPULATIONS):
        populations = cross_over_populations(populations, scores)
        
        scores = get_scores(populations)
        avg_score = np.mean(scores)

        if avg_score < best_score:
            best_score = avg_score
            best_population = populations

        if scores[0] == 0 or scores[1] == 0 or scores[2] == 0:
            break
        prev_population = avg_score

    print("Кінцеві оцінки:", scores)
    
    scores = get_best(scores)
    print("Найкраща популяція: ", best_score)
    print_time_table(best_population[0])
