import string
import unicodedata
import random

ALPHABET = string.ascii_uppercase

def caesar(text:str, key:int=random.randint(0, len(ALPHABET))):
    cypher = ""
    normalized = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    lowercase = normalized.upper()
    for c in lowercase:
        if c != " ":
            cypher += ALPHABET[(ALPHABET.index(c) + key) % len(ALPHABET)]
    return cypher

def bruteForceCaesar(text:str):
  for i in range(len(ALPHABET)):
    decode = ""
    for c in text:
      decode += ALPHABET[(ALPHABET.index(c) - i) % len(ALPHABET)]
    print(f"Key # {i}: {decode}")