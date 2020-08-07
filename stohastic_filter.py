import numpy as np
import pandas as pd
import random

# Метрика расстояния
def _manhattan_dist(f_arr, s_arr):
    res = np.subtract(f_arr, s_arr) # Поэлементное вычитание аргументов
    res = np.abs(res)
    return np.sum(res)

# Критерий зашумленности (&)
def manhattan_noise_c(arr):
    return _manhattan_dist(arr[1:], arr[:-1])

# Отличие
def manhattan_diff_c(f_arr, s_arr):
    assert len(f_arr) == len(s_arr)         # Проверка истинности утверждения
    result = _manhattan_dist(f_arr, s_arr)  #
    return result / len(f_arr)

# Случайный шум ??
def uniform_noise(func, amp, seed=42):
    assert amp > 0
    amp /= 2
    rd_gen = np.random.default_rng(seed=seed)
    return lambda x: np.add(func(x), rd_gen.uniform(-amp, amp, len(x)))


def sw_gen(sw_size=3, seed=42):
    assert sw_size > 1 and sw_size % 2 == 1
    random.seed(seed)
    while True:
        root = random.uniform(0, 1)
        w = []
        for _ in range(0, (sw_size - 1) // 2 - 1):
            w.append(0.5 * random.uniform(0, 1 - root - 2 * sum(w)))
        w.append(0.5 * (1 - root - 2 * sum(w)))
        yield [*reversed(w), root, *w]


def mean_geom_sw(y_noisy, weights):
    m = (len(weights) - 1) // 2
    y_padded = np.pad(y_noisy, (m, m), 'constant', constant_values=1)
    return [np.prod([y_padded[i + j] ** w
                     for j, w in enumerate(weights)])
            for i, _ in enumerate(y_noisy)]

# Число испытаний N
def get_tries(x_min, x_max, eps, proba):
    return int(np.log(1 - proba) / np.log(1 - eps / (x_max - x_min)))

# Случайный поиск
def random_search(y_noisy, weights_generator, tries, l):
    weights = [next(weights_generator)
               for _ in range(tries)]
    y_filtered = [mean_geom_sw(y_noisy, w)
                  for w in weights]
    noise_c = [manhattan_noise_c(y_a)
               for y_a in y_filtered]
    diff_c = [manhattan_diff_c(y_a, y_noisy)
              for y_a in y_filtered]
    lin_conv = [l * n_c + (1. - l) * d_c
                for n_c, d_c in zip(noise_c, diff_c)]
    ind = np.argmin(lin_conv, axis=0)
    return [weights[ind],
            noise_c[ind],
            diff_c[ind],
            lin_conv[ind]]

# Поиск весов
def find_weights(y_noisy, sw_size,
                 tries, arrangement,
                 seed=42):
    res = []
    sw_creator = sw_gen(sw_size, seed)
    for l in np.linspace(*arrangement):
        res.append([l, *random_search(y_noisy, sw_creator, tries, l)])
    res = pd.DataFrame(data=res,
                       columns=['Lambda', 'Alpha', 'W', 'D', 'J'])
    distance = np.abs(res['W'].values) + np.abs(res['D'].values)
    res['Distance'] = distance
    return np.argmin(distance), res