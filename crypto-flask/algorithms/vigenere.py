from string import ascii_letters
import random
import string

abecedario = list(string.ascii_uppercase)

def vigenere(frase:str, clave=None):

    if clave is None:
        clave = ''.join(random.choices(abecedario, k=random.randint(2, len(input))))
    
    clave_list = []
    for letra in clave.upper():
        clave_list.append(abecedario.index(letra))

    newFrase = ""

    contador = 0

    for letra in frase:
        letra = abecedario[(abecedario.index(letra) + clave_list[contador]) % len(abecedario)]
        newFrase = newFrase + letra
        contador = (contador + 1) % len(clave)
        

    return(newFrase)