import random
import string

abecedario = list(string.ascii_uppercase)

def onlyUppercase_letters(s):
    for i in s:
        if (ord(i)<65 or 91 <ord(i)):
            raise Exception("key and text must contain only uppercase letters")
            return False
    return True

def everyElementJustOnce(s: list):
    for i in abecedario:
        x: int = s.count(i)
        if(x > 1):
            raise Exception("duplicated '"+i+"' in key")
            return False
        elif(x < 1):
            raise Exception("letter '"+i+"' is missing from the key")

    return True

def isPermutation(s: list):
    if(len(s)>30 or len(s)<15):
        raise Exception("key must contain every letter just once")
        return False
    if(not onlyUppercase_letters(s)): return False
    if(not everyElementJustOnce(s)): return False
    return True

def randomKey():
    s = abecedario.copy()
    random.shuffle(s)
    return s

def substitutionEncrypt(t:str, k = None):
    #Recibe texto t de solo letras mayúsculas
    #e.g. HOLAMUNDO

    #Recibe clave k permutación del abecedario en mayúsculas
    #e.g. BACDEFGHIJKLMNOPQRSTUVWXYZ

    #Devuelve texto encriptado
    #e.g. HOLBMUNDO
    encrypted_text = ""
    text = list(t)

    if k  == None:
        key = randomKey()
        print("key:", "".join(key))
    else:
        key = list(k)

    if(not isPermutation(key)):
        print("invalid key")
    if(not onlyUppercase_letters(text)):
        print("invalid text")
        return

    for i in text:
        place: int = ord(i)-ord('A')
        b = key[place]
        encrypted_text += key[place]
    return str(encrypted_text)

def substitutionDecrypt(t:str, k=" "):
    #Recibe texto t de solo letras mayúsculas
    #e.g. HOLBMUNDO
    #Recibe clave k permutación del abecedario en mayúsculas
    #e.g. BACDEFGHIJKLMNOPQRSTUVWXYZ

    #Devuelve texto encriptado
    #e.g. HOLAMUNDO
    decrypted_text = ""
    text = list(t)

    if k == " ":
        key = abecedario.copy()
        random.shuffle(key)
        print("key:", key)
    else:
        key = list(k)

    if(not isPermutation(key) or not onlyUppercase_letters(text)):
        return

    for i in text:
        place: int = key.index(i)
        decrypted_text += chr(place +ord('A'))
    return str(decrypted_text)

def count(i, t:str): return t.count(i)

def numberOfTimesALetterAppears(t: str):
    s = []
    for i in abecedario:
        s.append(t.count(i))
    return zip(t,s)

def mostCommon(t: str): pass

def substitutionCryptoanalysis(text: str):
    #To be implemented
    numberOfTimesALetterAppears(text)
    mostCommon(text)

# a = subtitutionEncrypt("XUA","VKWBXLYFZMDNOCPHGERISATJUQ")
# ax = substitutionDecrypt(a,"VKWBXLYFZMDNOCPHGERISATJUQ")
# print(a, ax) #ax ==XUA

# b = subtitutionEncrypt("XA")
# print(b)
# substitutionCryptoanalysis("XADSFA")
