import random
import aritmeticaModular as myAm

# 1. **Generación de Claves RSA:**

# https://mathworld.wolfram.com/Rabin-MillerStrongPseudoprimeTest.html
def is_prime(n: int, k: int) -> bool:

    if n <= 1:
        return False

    if n == 2:
        return True
    
    if myAm.calcularMódulo(n,2) == 0:
        return False
    
    # n - 1 = 2^r * s
    r = 0
    s = n - 1
    while s % 2 == 0:
        s //= 2
        r += 1

    for i in range(k):
        a = random.randint(2, n-1) #random integer a with 1 <= a <= n-1
        strong_prime  = False # Strong prime in base a

        if myAm.calcularMódulo(a**s,n) == 1: # a^s (mod n) = 1
            strong_prime = True

        else: 
            for j in range(r):
                exponent = (2**j) * s
                if myAm.calcularMódulo(a**exponent ,n) == (n-1): # a^(2^j * s) (mod n) = -1
                    strong_prime = True
                    break   

        if not strong_prime:
            return False
        
    return True  

def generate_prime(bits: int) -> int:
    while True:
        n = random.getrandbits(bits)
        if is_prime(n, 5):
            return n

def generate_e(phi_n: int) -> int:
    while True:
        e = random.randint(2, phi_n-1)
        if myAm.coprimos(e, phi_n):
            return e

p = generate_prime(8)
q = generate_prime(8)
n = p * q
phi_n = (p-1) * (q-1) # Euler's totient function
# https://www.uninorte.edu.co/documents/13942513/27035260/prueba-IV-problemas-grupales-2015.pdf/ce8be0d1-9570-183c-fdd8-3b88c4620fb3?t=1654881264146
e = generate_e(phi_n)
d = myAm.inversoModular(e, phi_n)

print('\n------------')
print('Claves RSA: ')
print(f'numero primo <p>           : {p}')
print(f'numero primo <q>           : {q}')
print(f'n = p*q                    : {n}')
print(f'totiente Euler -> phi_n    : {phi_n}')
print(f'entero coprimo <e>         : {e}')
print(f'inverso multiplicativo <d> : {d}')

# 2. **Cifrado de Mensajes:**

def string_to_numbers(s: str):
    # https://www.w3schools.com/python/ref_func_ord.asp
    numbers = []
    for c in s:
        numbers.append(ord(c))
    return numbers

def encrypt_block(block, e ,n):
    # https://www.w3schools.com/python/ref_func_pow.asp
    return pow(block, e, n)

def encrypt_message(message: str, e, n):
    numbers = string_to_numbers(message)
    encrypted_blocks = []
    for num in numbers:
        encrypted_blocks.append(encrypt_block(num, e, n))
    return encrypted_blocks

print("\n-----------------------------------------")
message = input('Ingrese el mensaje a cifrar: ')
encrypted_message = encrypt_message(message, e, n)
print('Mensaje cifrado: ')
print(encrypted_message)

# 3. **Descifrado de Mensajes:**

def numbers_to_string(numbers):
    strings = ''
    for num in numbers:
        strings += chr(num)
    return strings

def decrypt_block(block, d, n):
    return pow(block, d, n)

def decrypt_message(encrypted_blocks, d, n): # encrypted_blocks is the list that function 'encrypt_message' returns
    decrypted_blocks = []
    for block in encrypted_blocks:
        decrypted_blocks.append(decrypt_block(block, d, n))
    return numbers_to_string(decrypted_blocks)

print("\n-----------------------------------------")
decrypted_message = decrypt_message(encrypted_message, d, n)
print('Mensaje descifrado: ')
print(decrypted_message)

# 4. **Optimización con el Teorema del Resto Chino (CRT):**

def crt_decrypt_block(block, d, p, q):
    dp = d % (p - 1)
    dq = d % (q - 1)
    q_inv = myAm.inversoModular(q, p)
    
    m1 = pow(block, dp, p)
    m2 = pow(block, dq, q)
    
    h = (q_inv * (m1 - m2)) % p
    m = m2 + h * q
    return m

def crt_decrypt_message(encrypted_blocks, d, p, q):
    decrypted_numbers = []
    for block in encrypted_blocks:
        decrypted_numbers.append(crt_decrypt_block(block, d, p, q))
    return numbers_to_string(decrypted_numbers)

print("\n-----------------------------------------")
crt_decrypted_message = crt_decrypt_message(encrypted_message, d, p, q)
print('Mensaje descifrado con CRT: ')
print(crt_decrypted_message)