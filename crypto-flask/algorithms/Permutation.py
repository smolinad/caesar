#Find inverse np.argsort(permutation)

def PermutationEncrypt(t: str, k = None ):

    #key solo num
    #key permutation
    #len(k)/len(t)?
    text = list(t)
    key = list(k)
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

print(PermutationEncrypt("1234123412341234","2431"))
