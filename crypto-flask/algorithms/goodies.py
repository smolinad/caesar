import string
import re 
import unicodedata
import os

ALPHABET = string.ascii_uppercase

def processInput(text:str):
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ''.join(text.split())
    normalized = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    no_digits = re.sub(r'[0-9]+', '', normalized)
    uppercase = no_digits.upper().strip() 
    return uppercase

class InputKeyError(Exception):
    def __init__(self, message:str):
        self.message = message

    def __str__(self):
        return self.message

def deleteImages(list_dir):
    for dir in list_dir:
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
