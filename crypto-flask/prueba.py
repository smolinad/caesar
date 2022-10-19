from Cryptodome.Random import get_random_bytes
 
print(get_random_bytes(24))

num = [0, 'l', 0, 1, 1, 1]

a = bytes(num)
print(a)