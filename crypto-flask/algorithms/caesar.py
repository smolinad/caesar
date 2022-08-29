from algorithms.goodies import ALPHABET
import random

def encryptCaesar(text:str, key=None):
  if key is None:
    key = random.randint(0, len(ALPHABET))
  elif key.isdigit():
    key = int(key)
  if isinstance(key, int):
    cypher = ''
    for c in text:
      cypher += ALPHABET[(ALPHABET.index(c) + key) % len(ALPHABET)]
    return cypher
  else:
    print("keyError")

def bruteForceCaesar(text:str):
  for i in range(len(ALPHABET)):
    decode = ""
    for c in text:
      decode += ALPHABET[(ALPHABET.index(c) - i) % len(ALPHABET)]
    print(f"Key # {i}: {decode}")