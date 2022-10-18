import math_functions as mfunc
import helper_functions as hfunc


user_num = 10
print(f"Количество пользователей - {user_num}\n")

p, q = hfunc.generate_prime_nums(150, 100000, 2)
n = p * q
lam = mfunc.carmichael_func(p, q)
pq = lam / 2
e = hfunc.generate_public_key(lam)
d = mfunc.inverse_mod(e, lam)
print(f"p = {p}, q = {q}, n = p * q = {n}, λ(n) = {lam}\n"
      f"e = {e}, d = {d}\n")

message = 123423425
message_mod = mfunc.mod(message, n)
print(f"Сообщение: {message}")
print(f"Сообщение по модулю n: {message_mod}\n")

key_shares = hfunc.get_key_shares(user_num, d, lam)
print(f"Доли секрета: {key_shares}")

partial_signs = hfunc.get_partial_signs(key_shares, message_mod, n)
print(f"Доли подписи: {partial_signs}\n")

sign = hfunc.get_sign(partial_signs, n)
print(f"Подпись: {sign}\n")

message_new = hfunc.get_message(sign, e, n)
print(f"Исходное сообщение: {message_mod}\n"
      f"Расшифрованное сообщение: {message_new}")
