import random


def mod(a, m):
    """
    Взятие числа по модулю с бинарным поиском
    Бинарным поиском находится минимальное частное от деления a / m,
    при котором (a - q * m) < m
    Тогда a - q * m = r (остаток)
    :param a: Число
    :type a: int
    :param m: Модуль
    :type m: int
    :return: Число по модулю
    :rtype: int
    """
    #
    if m == 0:
        raise ValueError("Деление на 0!")
    if m == 1 or a == 0:
        return 0

    negative_dividend = False
    if a < 0:
        a = abs(a)
        negative_dividend = True

    negative_divisor = False
    if m < 0:
        m = abs(m)
        negative_divisor = True

    left = 0
    right = a
    while left < right:
        q = int((left + right) / 2)
        if a - q * m >= m:
            left = q + 1
        else:
            right = q
    res = a - left * m

    if negative_dividend and negative_divisor:
        return -res
    elif negative_dividend and not negative_divisor:
        return m - res
    elif not negative_dividend and negative_divisor:
        return res - m
    else:
        return res


def gcd(a, b):
    """
    НОД алгоритмом Евклида
    :param a: Первое число
    :type a: int
    :param b: Второе число
    :type b: int
    :return: НОД
    :rtype: int
    """
    if a == b == 0:
        raise ValueError("НОД(0, 0) не определен!")

    a = abs(a)
    b = abs(b)

    if a < b:
        a, b = b, a

    if b == 0:
        return a

    while b != 0:
        a, b = b, mod(a, b)
    return int(a)


def lcm(a, b):
    """
    Нахождение НОК с помощью НОД
    :param a: Первое число
    :type a: int
    :param b: Второе число
    :type b: int
    :return: НОК
    :rtype: int
    """
    if a == b == 0:
        raise ValueError("НОК(0, 0) не определен!")
    if a == 0 or b == 0:
        return 0

    a = abs(a)
    b = abs(b)

    res = int(a * (b / gcd(a, b)))
    return res


def fast_pow(a, b, m):
    """
    Быстрое возведение в степень по модулю
    :param a: Основание степени
    :type a: int
    :param b: Показатель степени
    :type b: int
    :param m: Модуль
    :type m: int
    :return: Результат возведения в степень
    :rtype: int
    """
    if b < 0:
        raise ValueError(
            "Показатель степени должен быть натуральным числом или 0!")
    if b == 0:
        return 1
    if b == 1:
        return mod(a, m)

    a = mod(a, m)
    if mod(b, 2) == 0:
        res = fast_pow(a, int(b / 2), m)
        product = mod(res * res, m)
        return product
    else:
        res = fast_pow(a, b - 1, m)
        product = mod(a * res, m)
        return product


def prime_test_fermat(p, precision):
    """
    Тест Ферма на простоту числа
    :param p: Проверяемое число
    :type p: int
    :param precision: Количество чисел, которые будут использованы при проверке
    Чем больше чисел, тем больше точность
    :type precision: int
    :return: Является ли число простым?
    :rtype: bool
    """
    if p < 0:
        raise ValueError("Показатель степени должен быть натуральным числом!")
    if p == 2 or p == 3:
        return True
    if mod(p, 2) == 0:
        return False

    for i in range(precision):
        a = random.randint(2, p - 2)
        if gcd(a, p) != 1:
            continue
        if fast_pow(a, p - 1, p) != 1:
            return False
    return True


def carmichael_func(p, q):
    """
    Функция Кармайкла
    Для числа n = p * q находится как НОК(p - 1, q - 1)
    :param p: Первое простое число
    :type p: int
    :param q: Второе простое число
    :type q: int
    :return: Значение функции Кармайкла
    :rtype: int
    """
    lam = lcm(p - 1, q - 1)
    return lam


def ext_euclidean_alg(a, b):
    """
    Расширенный алгоритм Евклида
    :param a: Первое число
    :type a: int
    :param b: Второе число
    :type b: int
    :return: НОД, корни уравнения ax + by = НОД(a, b)
    :rtype: tuple
    """
    a = abs(a)
    b = abs(b)

    if a < b:
        a, b = b, a

    x2 = 1
    x1 = 0
    y2 = 0
    y1 = 1

    while b != 0:
        q = int(a / b)
        r = a - q * b
        x = x2 - q * x1
        y = y2 - q * y1

        a = b
        b = r
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y

    d = a
    x = x2
    y = y2
    return d, x, y


def inverse_mod(a, m):
    """
    Нахождение обратного по модулю через расширенный алгоритм Евклида
    :param a: Число, к которому ищется обратное
    :type a: int
    :param m: Модуль
    :type m: int
    :return: Обратное
    :rtype: int
    """
    a = mod(a, m)
    d, x, y = ext_euclidean_alg(m, a)

    if d != 1:
        raise ValueError("НОД(a, m) = 1, обратного значения не существует!")
    else:
        return mod(y, m)
