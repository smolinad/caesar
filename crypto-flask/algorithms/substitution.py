def only_letters(s):
    return True

def no_duplicates(s):
    return True

def is_permutation(s):
    if(len(s)!=26): return False
    if(only_letters(s) == False): return False
    if(no_duplicates(s) == False): return False
    return True

def subtitutionEncrypt(t:str, k=None):
    if k is None:
        pass #Generate key

    text = list(t)
    key = list(k)
    encrypted_text = ""
    if(is_permutation(key)==False):
        print("invalid key")
        return
    for i in text:
        place: int = ord(i)-97
        b = key[place]
        encrypted_text += key[place]
    return str(encrypted_text)

def substitutionDecrypt(t:str, k:str):
    text = list(t)
    key = list(k)
    decrypted_text = ""
    if(is_permutation(key)==False):
        print("invalid key")
        return

    for i in text:
        place: int = key.index(i)
        decrypted_text += chr(place +97)
    return str(decrypted_text)

# a = encrypt("xuh","vkwbxlyfzmdngocphqerisatju")
# print(a)
# print(decrypt(a,"vkwbxlyfzmdngocphqerisatju"))