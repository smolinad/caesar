# Falta analysis
import random
from goodies import InputKeyError

"""
Tanto Encrypt como Decrypt 
reciben texto cualquiera y clave(con espacios)
retornan [texto, clave]
"""


def permutationEncrypt(t: str, k=None):
    """
    Recibe texto t cualquiera
    e.g. "HOLAMUNDOLUNES"

    Recibe clave k, permutación de range(1,n) separada por espacios
    e.g. "3 1 4 2"

    Retorna texto encriptado de longitud múltiplo de n
    e.g. ["LHAONMDUUONL","3 1 4 2"]
    """

    if k == None:
        k = randomKeyPermutation()
    text = t
    key = [int(x) for x in k.split(" ")]

    if not isNumberPermutation(key):
        return

    text = completeWithAs(text, len(key))
    encrypted_text = performPermutation(text, key)

    return [encrypted_text, k]


def permutationDecrypt(t: str, k: str):
    """
    Recibe texto t cualquiera
    e.g. "LHAONMDUUONL"

    Recibe clave k, texto separado por espacios permutación de range(1,n)
    e.g. "3 1 4 2"

    lista de texto desencriptado y clave
    e.g. ["HOLAMUNDOLUN","3 1 2 4"]
    """

    text = t
    key = [int(x) for x in k.split(" ")]

    if not isNumberPermutation(key):
        return
    if not len(text)%len(key) == 0:
        raise InputKeyError("Length of key must divide length of text")
        return

    inverse_key = inversePermutation(key)
    encrypted_text = performPermutation(text,inverse_key)
    k = " ".join([str(x) for x in inverse_key])

    return [encrypted_text,k]


# --------------------------->
# Funciones de Encrypt y Decrypt


def everyNumberJustOnce(s: list):
    for i in range(1, len(s) + 1):
        x: int = s.count(i)
        if 1 < x:
            raise InputKeyError("duplicated '" + str(i) + "' in key")
        elif x < 1:
            raise InputKeyError("'" + str(i) + "' is missing from the key")

    return True


def isNumberPermutation(s: list):
    if (not everyNumberJustOnce(s)):
        return False
    return True


def randomKeyPermutation():
    x = random.randint(4, 7)
    s = list(range(1, x))
    random.shuffle(s)
    if (s == list(range(1, x))):
        random.shuffle(s)
    s = [str(x) for x in s]
    s = " ".join(s)
    return s

def completeWithAs(text:list, period:int):
    total = len(text)
    if (total % period != 0):
        new_num = period - (total % period)
        text += 'A' * new_num
    return text

def performPermutation(text: list, key:list):
    total = len(text)
    period = len(key)

    encrypted_text = ""
    for i in range(int(total / period)):
        # A partir de text[i*periodo]

        for j in range(period):
            objective = key[j] - 1
            newElement = text[i * period + objective]
            encrypted_text += newElement

    return encrypted_text

def inversePermutation(key:list):
    inverse_key = [0]*len(key)
    for i in range(len(key)):
        value = key[i]
        inverse_key[value-1] = i+1
    return inverse_key

a = permutationEncrypt("XYZ", "2 4 3 1 5")
ax = permutationDecrypt("YAZXA", "2 4 3 1 5")
print(a)
print(ax)

b = permutationEncrypt("123456789")
print(b)
