import random
import math_functions as mfunc


def generate_prime_nums(start, end, amount):
    """
    Генерация простых чисел
    Сгенеированное число проверяется на простоту с помощью теста Ферма
    :param start: Левая граница генерации
    :type start: int
    :param end: Правая граница генерации
    :type end: int
    :param amount: Количество чисел, которое требуется получить
    :type amount: int
    :return: Простые числа
    :rtype: list
    """
    generated_nums = []
    prime_nums = []

    while amount > 0:
        num = random.randint(start, end)
        if num not in generated_nums:
            generated_nums.append(num)
            if mfunc.prime_test_fermat(num, 100):
                prime_nums.append(num)
                amount -= 1

    return prime_nums


def generate_public_key(lam):
    """
    Генерация открытого ключа
    Генерируется число, которое проверяется на взаимную простоту с λ(n)
    Если взаимная простота не выполняется, функция вызывает саму себя
    :param lam: Значение функции Кармайкла
    :type lam: int
    :return: Открытый ключ
    :rtype: int
    """
    e = random.randint(2, lam - 1)
    if mfunc.gcd(e, lam) != 1:
        e = generate_public_key(lam)
    return e


def get_key_shares(user_num, d, lam):
    """
    Получение долей секретного ключа
    Сумма долей секрета по модулю λ(n) равна секрету
    Генерируется user_num - 1 случайных чисел, последнее число вычисляется как
    разность d и суммы сгенерированных чисел по модулю λ(n)
    :param user_num: Количество пользователей
    :type user_num: int
    :param d: Секретный ключ
    :type d: int
    :param lam: Значение функции Кармайкла
    :type lam: int
    :return: Доли секретного ключа
    :rtype: list
    """
    key_shares = []
    summary = 0
    for i in range(user_num - 1):
        a = random.randint(1, lam - 1)
        key_shares.append(a)
        summary += a
        # summary = summary % lam
        summary = mfunc.mod(summary, lam)
    # key_shares.append((d - summary) % lam)
    key_shares.append(mfunc.mod(d - summary, lam))
    return key_shares


def get_partial_signs(key_shares, message, n):
    """
    Получение подписей пользователей
    Подпись рассчитывается по формуле s = m**d (mod n)
    :param key_shares: Доли ключей пользователей
    :type key_shares: list
    :param message: Подписываемое сообщение
    :type message: int
    :param n: Модуль
    :type n: int
    :return: Подписи пользователей
    :rtype: list
    """
    signs = []
    for share in key_shares:
        sign = mfunc.fast_pow(message, share, n)
        signs.append(sign)
    return signs


def get_sign(partial_signs, n):
    """
    Получение подписи из подписей пользователей
    Подпись вычисляется как произведение частей подписи
    :param partial_signs: Подписи пользователей
    :type partial_signs: list
    :param n: Модуль
    :type n: int
    :return: Подпись сообщения
    :rtype: int
    """
    sign = 1
    for partial_sign in partial_signs:
        sign *= partial_sign
        sign = mfunc.mod(sign, n)
    return sign


def get_message(sign, e, n):
    """
    Получение сообщения из подписи
    Сообщение рассчитывается по формуле s = m**e (mod n)
    :param sign: Подпись
    :type sign: int
    :param e: Открытый ключ
    :type e: int
    :param n: Модуль
    :type n: int
    :return: Сообщение
    :rtype: int
    """
    message = mfunc.fast_pow(sign, e, n)
    return message
