from string import ascii_letters
import random
import string

abecedario = list(string.ascii_uppercase)

def vigenereEncrypt(frase:str, clave=None):

    if clave is None:
        clave = ''.join(random.choices(abecedario, k=random.randint(2, len(input))))
    elif "".join(clave.split()).isalpha():
    
      clave_list = []
      for letra in clave.upper():
          clave_list.append(abecedario.index(letra))

      newFrase = ""

      contador = 0

      for letra in frase:
          letra = abecedario[(abecedario.index(letra) + clave_list[contador]) % len(abecedario)]
          newFrase = newFrase + letra
          contador = (contador + 1) % len(clave)
          

      return(newFrase) #retorna la tupla (Mensaje_Encriptado, clave)
    else:
      return("keyError: Must be a word or a phrase made up of letters")
  
  
  # --------- DECIFRADO --------------- 
  # METODO PAULINA  
from itertools import product

from string import ascii_letters
import random
import string

abecedario = list(string.ascii_uppercase)


def vigenereDeencryptKey(frase:str, clave): # Esta función no te importa, la que tiene el caso con y sin clave está más abajo

    if "".join(clave.split()).isalpha():
    
      clave_list = []
      for letra in clave.upper():
          clave_list.append(abecedario.index(letra))

      newFrase = ""

      contador = 0

      for letra in list(frase):
          letra = abecedario[(abecedario.index(letra) - clave_list[contador]) % len(abecedario)]
          newFrase = newFrase + letra
          contador = (contador + 1) % len(clave)
          

      return(newFrase) 
    else:
      return("keyError: Must be a word or a phrase made up of letters")

def letrasMásfrecuentes(texto):
  letras = [0]*26

  for letter in texto:
    x = abecedario.index(letter)
    letras[x] += 1

  indices = [index for index, value in enumerate(letras) if value == max(letras)]
  masFrecuentes = list(map(lambda x: abecedario[x], indices))
  return(masFrecuentes)

def particiona_en_bloques(texto , tamano):
  texto_particionado = [ texto[ y - tamano : y ] for y in range( tamano, len(texto) + tamano , tamano) ]
  return(texto_particionado)

# ESTA ES LA FUNCION IMPORTANTE
def vigenereDeencrypt(text:str, key=None):
  if key==None:
    posibles_mensajes = []
    for longitud in range(4,7):
      simbolos = {} 
      variables_frecuentes = {}
      chunks = particiona_en_bloques(text,longitud)


      # divide los bloques por la letra i-esima 
      for i in range(longitud):
        simbolos[ i ] = []



      for bloque in chunks: #separa por orden de los simbolos, ai: primer simbolo segundo simbolo
        for i in range(longitud):
          try:
            simbolos[i].append(bloque[i])
          except:
            pass


      for n in range(len(simbolos)): #crea un diccionario con numbre i = [a,b,c] las letras más frecuentes de ese bloque i
        variables_frecuentes[n]  = letrasMásfrecuentes(simbolos[n])

      listas_letras = []
      posibles_claves = []

      for key in variables_frecuentes.keys():
          listas_letras.append( list(map(lambda x: abecedario[ (abecedario.index(x)- 4) % 26],variables_frecuentes[key]) ) )
      


      for items in product(*listas_letras):
          posibles_claves.append(("".join(items)))



      for clave in posibles_claves:
        posibles_mensajes.append((vigenereDeencryptKey(text, clave),clave))
    return(posibles_mensajes) #Retorna una lista con tuplas con el posible mensaje encriptado y la posible clave
# Ejmplo [("GRACIASPOR", "BETA"), ("AYUDARMEA", "OMEGA"),("APRENDER", "ALPHA")]

  elif "".join(key.split()).isalpha():
    return(vigenereDeencryptKey(text, key),key)  #Si la función recibe clave retorna una tupla con mensaje encriptado y la clave
# Ejmplo ("HOLAMUNDO", "ALPHA")
  else:
    return("keyError: Must be a word or a phrase made up of letters")
  
  