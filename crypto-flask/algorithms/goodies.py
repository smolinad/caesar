import string
import unicodedata

ALPHABET = string.ascii_uppercase

def processInput(text:str):
    text = ''.join(text.split())
    normalized = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    uppercase = normalized.upper().strip() 
    return uppercase