import random
import string

abecedario = list(string.ascii_uppercase)

def only_uppercase_letters(s):
    for i in s:
        if (ord(i)<65 or 91 <ord(i)):
            raise Exception("key and text must contain only uppercase letters")
            return False
    return True

def no_duplicates(s: list):
    for i in abecedario:
        x: int = s.count(i)
        if(x > 1):
            raise Exception("duplicated '"+i+"' in key")
            return False
        elif(x < 1):
            raise Exception("letter '"+i+"' is missing from the key")

    return True

def is_permutation(s: list):
    if(len(s)>30 or len(s)<15):
        raise Exception("key must contain every letter just once")
        return False
    if(only_uppercase_letters(s) == False): return False
    if(no_duplicates(s) == False): return False
    return True

def randomKey():
    s = abecedario.copy()
    random.shuffle(s)
    return s

def subtitutionEncrypt(t:str, k = " "):
    encrypted_text = ""
    text = list(t)

    if k  == " ":
        key = randomKey()
        print("key:", "".join(key))
    else:
        key = list(k)

    if(is_permutation(key)==False):
        print("invalida key")
    if(only_uppercase_letters(text)==False):
        print("invalid text")
        return

    for i in text:
        place: int = ord(i)-ord('A')
        b = key[place]
        encrypted_text += key[place]
    return str(encrypted_text)

def substitutionDecrypt(t:str, k=" "):
    decrypted_text = ""
    text = list(t)

    if k == " ":
        key = abecedario.copy()
        random.shuffle(key)
        print("key:", key)
    else:
        key = list(k)

    if(is_permutation(key)==False or only_uppercase_letters(text)==False):
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
    numberOfTimesALetterAppears(text)
    mostCommon(text)

#a = subtitutionEncrypt("XUA","VKWBXLYFZMDNOCPHGERISATJUQ")
#b = subtitutionEncrypt("XA")
#ax = substitutionDecrypt(a,"VKWBXLYFZMDNOCPHGERISATJUQ")
substitutionCryptoanalysis("XADSFA")
