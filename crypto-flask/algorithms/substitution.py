import string

abecedario = list(string.ascii_uppercase)

def only_uppercase_letters(s):
    for i in s:
        if (ord(i)<65 or 91 <ord(i)):
            raise Exception("key and text must contain only uppercase letters")
            return False
    return True

def no_duplicates(s):
    for i in abecedario:
        x: int = s.count(i)
        if(x > 1):
            raise Exception("duplicated '"+i+"' in key")
            return False
        elif(x < 1):
            raise Exception("letter '"+i+"' is missing from the key")

    return True

def is_permutation(s):
    if(len(s)>30):
        raise Exception("key must contain every letter just once")
        return False
    if(only_uppercase_letters(s) == False): return False
    if(no_duplicates(s) == False): return False
    return True

def subtitutionEncrypt(t:str, k:str):

    text = list(t)
    key = list(k)
    encrypted_text = ""
    if(is_permutation(key)==False or only_uppercase_letters(text)==False):
        print("invalid key")
        return
    for i in text:
        place: int = ord(i)-ord('A')
        b = key[place]
        encrypted_text += key[place]
    return str(encrypted_text)

def substitutionDecrypt(t:str, k:str):
    text = list(t)
    key = list(k)
    decrypted_text = ""
    if(is_permutation(key)==False):
        return

    for i in text:
        place: int = key.index(i)
        decrypted_text += chr(place +ord('A'))
    return str(decrypted_text)

a = subtitutionEncrypt("XUA","VKWBXLYFZMDNOCPHGERISATJUQ")
print(a)
print(substitutionDecrypt(a,"VKWBXLYFZMDNOCPHGERISATJUQ"))
