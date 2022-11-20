from sympy import randprime, isprime
import random
import math
from algorithms.goodies import InputKeyError, ALPHABET,primos


def generatePrime(a=0):
    if a!=0:
        return randprime(2**(a-2),2**(a-1))
    return randprime(2**(256),2**(512))

def gcd(p,q):
    while q != 0:
        p, q = q, p%q
    return p

def generateRsaData(p,q):
    n=p*q
    phi = (p-1)*(q-1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    pub_key=e
    d = 0
    d =multiplicative_inverse(pub_key,phi)
    priv_key = d
    return ({'public_key' : str(pub_key), 'private_key':str(priv_key)})

def rsaEncrypt(message, p="", q=""): # rsaEncrypt
    try:
        p = int(p)
        q = int(q)
    except:
        pass
    
    if p == "" or q == "":
        p,q = generatePrime(50),generatePrime(50)
    elif type(p) != int or type(q) != int or not isprime(p) or not isprime(q):
        raise InputKeyError("p and q must be primes numbers")

    n=p*q
    keys = generateRsaData(p,q)
    pub_key = int(keys['public_key'])
    priv_key = int(keys['private_key'])
    encrypt_text = []
    for letter in message:
        m = ord(letter)
        cipher_text = pow(m,pub_key,n)#(m**pub_key)%n
        encrypt_text.append(str(cipher_text))
    
    return((encrypt_text,[p,q,priv_key,0]))

def rsaDecrypt(message, p="", q="",priv_key=""):
    if message == "":
        raise InputKeyError("The message is not a encrypted text")
    try:
        p = int(p)
        q = int(q)
    except:
        pass 
    if p == "" or q == "" or priv_key=="":
        raise InputKeyError("For decrypt must have p,q and the prived key")
    elif type(p) != int or type(q) != int or not isprime(p) or not isprime(q):
        raise InputKeyError("p and q must be primes numbers")

    if type(priv_key) != int:
        raise InputKeyError(f"prived key must be a number be an integer \n between 1 and  {(p-1)*(q-1)}")

    
    n=p*q
 #   keys = generateRsaData(p,q)
  #  priv_key = int(keys['private_key'])
    decrypt_text = ""
    for letter in message:
        c = int(letter)
        decrypt_letter = pow(c,priv_key,n)#(c**priv_key)%n
        ascii_convert = chr(decrypt_letter)
        decrypt_text = decrypt_text + ascii_convert
    return((decrypt_text,[p,q,priv_key,0]))

def multiplicative_inverse(e, phi):
    d, x1, x2, y1 = 0, 0, 1, 1
    temp_phi = phi
    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    if temp_phi == 1:
        return d + phi

# encrypt_text,pub_key,priv_key,p,q = rsaEncrypt("biscozho","","")
# print(encrypt_text,pub_key,priv_key,p,q )
#print(rsaDecrypt([146822, 148160, 55407, 112487],439,443,159025 ))
