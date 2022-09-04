from hashlib import new
from math import gcd
from string import ascii_letters
import string
import random # para los ejemplos


coprimos = [3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
inversos = [9, 21,15,3, 19, 7,  23, 11, 5 , 17, 25 ]
numerosModulo = list(range(26))
abecedario =list(string.ascii_uppercase)

def afinEncrypt(input:str, key=None): 
  # la clave la  recibo como una pareja de enteros separadps por espacio donde a es coprimo con 26, b solo entero

  if key is None:
    a = random.randint(coprimos)
    b = random.randint(0, len(abecedario))
  elif "".join(key.split()).isdigit():
    a = int(key.split()[0]) % 26
    b = int(key.split()[1]) % 26
    if a in coprimos:

      newPalabra = ""
      for letra in input:
        letra = abecedario[(a * abecedario.index(letra) + b) % 26]
        newPalabra = newPalabra + letra
      return((newPalabra,key)) #retorna tupla con mensaje encriptado y su clave

    else:
      return("keyError: Must be pair integers 'a b' separated by an space where 'a' is a positive integer coprime with 26 between 0 and 25")
  else:
   return("keyError: Must be pair integers 'a b' separated by an space where 'a' is a positive integer coprime with 26 between 0 and 25")


# ----------------- DESENCRIPTADO --------------------


def afinDeencrypt(input:str, key=None):
   #si la clave es nula hace por fuerza bruta, variando a entre los coprimos de 26 y b entre 0 y 25
  if key is None:
    posibles = []
    for a in coprimos:
      a1 = inversos[coprimos.index(a)]
      for b in numerosModulo:
        newPalabra = ""
        for letra in input:
          letra = abecedario[(a * (abecedario.index(letra) - b)) % 26]
          newPalabra = newPalabra + letra
        posibles.append((newPalabra, (a1,b)))
    return(posibles) # retorna una lista de tuplas los posibles mensajes y su clave, la cual es una tupla
    # Ejemplo [(mensajeDesencriptado1, (a1,b1)),(mensajeDesencriptado2, (a2,b2)) ]

  elif "".join(key.split()).isdigit():
    a = inversos[coprimos.index(int(key.split()[0]) % 26)]
    a1 = int(key.split()[0])
    b = int(key.split()[1]) % 26
    if a in coprimos:

      newPalabra = ""
      for letra in input:
        letra = abecedario[(a * (abecedario.index(letra) - b)) % 26]
        newPalabra = newPalabra + letra
      return((newPalabra, (a1,b))) # retorna una tupla con el mensaje desencriptado y la clave que es otra tupla
      # ejemplo : (mensajeDesencriptado, (a,b))

    else:
      return("keyError: Must be pair integers 'a b' separated by an space where 'a' is a positive integer coprime with 26 between 0 and 25")
  else:
   return("keyError: Must be pair integers 'a b' separated by an space where 'a' is a positive integer coprime with 26 between 0 and 25")