import math_functions as mfunc
import helper_functions as hfunc

user_num = 10
print(f"Количество пользователей - {user_num}\n")

message = "Hello, world!"
byte_message = message.encode("utf-8")
print(f"Сообщение: {message}")
hash_message = hfunc.get_hash_md5(byte_message)
print(f"Хеш-значение сообщения: {hash_message}\n")

p, q = hfunc.generate_prime_nums(150, 10000, 2)
n = p * q
lam = mfunc.carmichael_func(p, q)
pq = lam / 2
d = hfunc.generate_private_key(lam)
e = mfunc.inverse_mod(d, lam)
print(f"p = {p}, q = {q}, n = p * q = {n}, λ(n) = {lam}\n"
      f"e = {e}, d = {d}\n")

hash_message_mod = hash_message % n
print(f"Хеш-значение сообщения по модулю n: {hash_message_mod}\n")

key_shares = hfunc.get_key_shares(user_num, d, lam)
print(f"Доли секрета: {key_shares}")

partial_signs = hfunc.get_partial_signs(key_shares, hash_message_mod, n)
print(f"Доли подписи: {partial_signs}\n")

sign = hfunc.get_sign(partial_signs, n)
print(f"Подпись: {sign}\n")

message_new = hfunc.get_message(sign, e, n)
print(f"Исходное хеш-значение: {hash_message_mod}\n"
      f"Расшифрованное хеш-значение: {message_new}")
