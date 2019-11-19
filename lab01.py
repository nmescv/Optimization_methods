from math import cos, tanh
import matplotlib.pyplot as plt	# Субмодуль для создания графиков
from numpy import arange  # Импортируем субмодуль создания массива

# Реализация метода пассивного поиска
def PassiveSearch(f, a, b, Nmax):

	print("Метод пассивного поиска")
	print("+-----+------------+")
	print('|  N  |    xMin    |')
	print("+-----+------------+")

	N = 1               # Стартовая точка
	inaccuracy = []     # Пока что пустой список неточностей
	N_list = []         # Пока что пустой список точек N

# Цикл для нахождения минимума
	while N <= Nmax:
		accuracy = (b - a) / (N + 1)       	# Шаг поиска
		inaccuracy.append(accuracy)       		  	# Добавляем неточность
		N_list.append(N)            		# Добавляем N
		xMin = a                    		# Считаем, что минимум находится в точке a
		x = a
		# Идём по всему интервалу
		while x <= b:
			if f(x) < f(xMin):  # Если очередное значение стало меньше,
				xMin = x        # то обновляем точку минимума
			x += accuracy              # Переходим на следующую точку
		print('| %*d | %*.4f |' % (3, N, 10, xMin))
		N += 1                  # Увеличиваем итерацию на 1
		# N *= 2                # Для ускорения нахождения минимума, т.е. каждый раз умножая на 2
	print("+-----+------------+")

# Рисуем график зависимостей неточности от числа точек N
	plt.plot(N_list, inaccuracy)    # Формируем график по осям
	plt.ylabel('Погрешность')       # Подписываем ось У
	plt.xlabel('N')                 # Подписываем ось Х
	plt.grid(True)					# Включаем сетку
	plt.show()                      # Оторбажаем график

	return xMin                     # Возвращщаем конечную точку минимума

# Реализация метода дихотомии
def Dichotomy(f, a, b, eps):
	delta = 0.01
	k = 1

	print("Метод дихотомии")
	print("+-----+------------+------------+------------+------------+------------+------------+------------+")
	print("|  k  |     ak     |     bk     |     lk     |     x1     |     x2     |   f(x1)    |    f(x2)   |")
	print("+-----+------------+------------+------------+------------+------------+------------+------------+")

	# Запускаем цикл. Пока интервал не сомкнётся...
	while b - a > eps:
		x = (a + b) / 2

		x_Left = x - delta
		x_Right = x + delta

		func_xLeft = f(x_Left)
		func_xRight = f(x_Right)

		print('| %*d | %*.3f | %*.3f | %*.3f | %*.3f | %*.3f | %*.3f | %*.3f |' % (3, k, 10, a, 10, b, 10, b - a, 10, x_Left, 10, x_Right, 10, func_xLeft, 10, func_xRight))
		# Выполняем процедуру исключения отрезка
		if func_xLeft >= func_xRight:
			a = x
		else:
			b = x

		k += 1

	print("+-----+------------+------------+------------+------------+------------+------------+------------+")

	return (a + b) / 2      # Возвращает вычисленный минимум

# Заданная унимодальная функция для поиска минимума
if __name__ == "__main__":
	UnimodalFunction = lambda x: cos(x) * tanh(x)

# Интервал поиска [-2, 0]
	a = -2
	b = 0
	eps = 0.1                   # Точность
	Nmax = (2*(b-a)/eps - 1)    # Максимально возможное число точек
	delta = 0.01
	xlist = arange(a, b, delta)
	ylistUni = [UnimodalFunction(x) for x in xlist]

	plt.plot(xlist, ylistUni)
	plt.title("Унимодальная функция")
	plt.grid(True)
	plt.show()

	xMin_ps = PassiveSearch(UnimodalFunction, a, b, Nmax)
	xMin_dic = Dichotomy(UnimodalFunction, a, b, eps)

print('Найденный методом пасс. поиска минимум:', xMin_ps)
print('Найденный методом дихотомии минимум:', xMin_dic)