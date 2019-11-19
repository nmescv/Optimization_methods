from math import cos, tanh, ceil, log, sin  # Импортируем субмодули математических значений
from random import uniform  # Импортируем субмодуль для генерирования чисел согласно равномерному распределению
from numpy import arange  # Импортируем субмодуль создания массива
from prettytable import PrettyTable  # Импортируем субмодуль создания простых таблиц ASCII
from matplotlib import pyplot as plt  # Импортируем субмодуль для построения графиков

# Таблица зависимости N от P и q (опционально)
def Dependent():
    table = PrettyTable()  # Создание таблицы
    table.add_column("q\\P", list(map(lambda N: round(N, 3), arange(0.005, 0.105, 0.005))))  # Формируем столбцы таблицы
    for p in arange(0.9, 1, 0.01):  # Запускаем цикл:
        column = []
        for q in arange(0.005, 0.105, 0.005):
            N = ceil(log(1 - p) / log(1 - q))  # Формула вычисления количества случайных точек
            column.append(N)
        table.add_column(str(round(p, 2)), column)
    print(table)

# Реализация метода случайного поиска
def RandomSearchMethod(f, a, b):
    table = PrettyTable()            # Создание таблицы
    table.add_column("q\\P", list(map(lambda x: round(x, 3), arange(0.005, 0.105, 0.005))))  # Формируем столбцы таблицы
    for p in arange(0.9, 1, 0.01):  # Запускаем цикл для каждого столбца:
        column = []
        for q in arange(0.005, 0.105, 0.005):
            N = ceil(log(1 - p) / log(1 - q))       # Формула вычисления количества случайных точек
            x_value = [uniform(a, b) for i in range(N)]  # Возвращает случайное вещественное число в [a,b]
            y_value = list(map(f, x_value))
            cur_min = round(min(y_value), 5)
            column.append(cur_min)
        table.add_column(str(round(p, 2)), column)
    print(table)


if __name__ == "__main__":
    UnimodalFunction = lambda x: cos(x) * tanh(x)                       # Унимодальная функция
    MultimodalFunction = lambda x: UnimodalFunction(x) * sin(5 * x)     # Мультимодальная функция
    xBegin = -2.0
    xEnd = 0.0
    delta = 0.001
    xlist = arange(xBegin, xEnd, delta)
    ylistUni = [UnimodalFunction(x) for x in xlist]
    ylistMulti = [MultimodalFunction(x) for x in xlist]

    '''
    # Строим график с обеими функциями
    fig, axs = plt.subplots(2)
    axs[0].plot(xlist, ylistUni)
    axs[0].grid(True)
    axs[1].plot(xlist, ylistMulti)
    axs[1].grid(True)
    plt.show()
    '''
    # Построим графики для каждой функции
    plt.plot(xlist,ylistUni)
    plt.title("Унимодальная функция")
    plt.grid(True)
    plt.show()
    plt.plot(xlist, ylistMulti)
    plt.title("Мультимодальная функция")
    plt.grid(True)
    plt.show()

    Dependent()
    RandomSearchMethod(UnimodalFunction, -2, 0)
    RandomSearchMethod(MultimodalFunction, -2, 0)

