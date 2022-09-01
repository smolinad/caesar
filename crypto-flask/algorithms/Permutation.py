#Find inverse np.argsort(permutation)
import random


def toNumbersList(s:list):
    n = []
    for i in s:
        if(ord(i)< 48 or 57 < ord(i)):
            raise Exception("key must only have numbers")
        n.append(int(i))
    return n

def everyNumberJustOnce(s: list):
    for i in range(1,len(s)+1):
        x: int = s.count(i)
        if(x > 1):
            raise Exception("duplicated '"+str(i)+"' in key")
            return False
        elif(x < 1):
            raise Exception("'"+str(i)+"' is missing from the key")

    return True

def isNumberPermutation(s: list):
    if len(s) >= 10: #No reconoce '10' sino '1' y '0'
        raise Exception("Key is too long")
    if(not everyNumberJustOnce(s)):
        return False
    return True

def randomKeyPermutation():
    x = random.randint(4, 10)
    s = list(range(1,x))
    random.shuffle(s)
    random.shuffle(s)
    return s

def PermutationEncrypt(t: str, k = None ):

    text = list(t)
    if k  == None:
        key = randomKeyPermutation()
        print("key:", key) #Presentar más compacto
    else:
        key = toNumbersList(k)

    if(not isNumberPermutation(key)): return
    #len(k)/len(t)?

    total = len(text)
    period = len(key)

    encrypted_text = []
    for i in range(int(total/period)):
        #A partir de text[i*periodo]
        for j in range(period):
            objective = int(key[j])-1 #-1 por indexación desde 1
            newElement = text[i*period + objective]
            encrypted_text.append(newElement)

    #len(k)/len(t)?

    return encrypted_text

def PermutationDecrypt(): pass

a = PermutationEncrypt("1234123412341234","2431")
print(a)

b = PermutationEncrypt("123456789")
print(b)
