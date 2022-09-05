import random
import string
from goodies import InputKeyError

abecedario = list(string.ascii_uppercase)

"""
Tanto Encrypt como Decrypt reciben texto y clave(opcional)
Y devuelven lista [texto, clave]

Cryptoanalysis recibe texto
Y devuelve lista [lista_frecuencia_de_letras, dict_frecuencia_de_digramas]
"""


def substitutionEncrypt(t: str, k=None):
    """
    Recibe texto t de solo letras mayúsculas
    e.g. HOLAMUNDO

    Puede recibir clave k permutación del abecedario en mayúsculas
    e.g. BACDEFGHIJKLMNOPQRSTUVWXYZ

    Devuelve lista de texto encriptado y clave
    [texto,clave]
    e.g. HOLBMUNDO
    """
    encrypted_text = ""
    text = list(t)

    if k is None:
        key = randomKey()
        print("key:", "".join(key))
    else:
        key = list(k)

    if not isPermutation(key):
        print("invalid key")
    if not onlyUppercase_letters(text):
        print("invalid text")
        return

    for i in text:
        place: int = ord(i) - ord('A')
        b = key[place]
        encrypted_text += key[place]
    return [str(encrypted_text), key]


def substitutionDecrypt(t: str, k=" "):
    """
    Recibe texto t de solo letras mayúsculas
    e.g. HOLBMUNDO
    Recibe clave k permutación del abecedario en mayúsculas
    e.g. BACDEFGHIJKLMNOPQRSTUVWXYZ

    Devuelve lista de texto desencriptado y clave
    e.g. [HOLAMUNDO,BACDEFGHIJKLMNOPQRSTUVWXYZ]
    """

    decrypted_text = ""
    text = list(t)

    if k == " ":
        key = abecedario.copy()
        random.shuffle(key)
        print("key:", key)
    else:
        key = list(k)
    if (not isPermutation(key) or not onlyUppercase_letters(text)):
        return

    for i in text:
        place: int = key.index(i)
        decrypted_text += chr(place + ord('A'))
    return [str(decrypted_text), key]


def substitutionCryptoanalysis(text: str):
    return [frequencyOfLetters(text), mostCommon(frequencyOfDigraphs(text))]


# --------------------------->
# Funciones de Encrypt y Decrypt


def onlyUppercase_letters(s):
    for i in s:
        if (ord(i) < 65 or 91 < ord(i)):
            raise InputKeyError("key and text must contain only uppercase letters")
            return False
    return True


def everyElementJustOnce(s: list):
    for i in abecedario:
        x: int = s.count(i)
        if (x > 1):
            raise InputKeyError("duplicated '" + i + "' in key")
            return False
        elif (x < 1):
            raise InputKeyError("letter '" + i + "' is missing from key")

    return True


def isPermutation(s: list):
    if len(s) != 26:
        raise InputKeyError("key must contain every letter just once")
        return False
    if onlyUppercase_letters(s) and everyElementJustOnce(s):
        return True
    return False


def randomKey():
    s = abecedario.copy()
    random.shuffle(s)
    return s


# --------------------------->
# Funciones de criptoanalisis

def numberOfTimesALetterAppears(t: str):
    dict = {}
    for i in abecedario:
        if dict.get(digraph) == None:
            dict[digraph] = 1
        else:
            dict[digraph] += 1
    return dict


def frequencyOfDigraphs(t: str):
    # List of 10 most common pairs
    # 1 time doesnt count
    dict = {}
    for i in range(len(t) - 1):
        digraph = t[i:i + 2]
        if dict.get(digraph) == None:
            dict[digraph] = 1
        else:
            dict[digraph] += 1

    return dict


# a = substitutionEncrypt("XUA", "VKWBXLYFZMDNOCPHGERISATJUQ")
# b = subtitutionEncrypt("XA")
# ax = substitutionDecrypt(a[0], a[1])
# ay = substitutionCryptoanalysis("DTNNBUBXNJ")

