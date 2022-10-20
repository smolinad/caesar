# import math
import random as r
#from readline import append_history_file
from PIL import Image
import numpy as np
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
from base64 import b64encode
# import imageio as iio
# import requests
from Cryptodome.Cipher import DES3
from Cryptodome.Cipher import DES
from algorithms.goodies import InputKeyError, ALPHABET

import os

dir_encr = 'web/static/uploads/encrypted/'
dir_des = 'web/static/uploads/decrypted/'

"Recibe nombre de la imagen su path, el modo y una llave que es de 24 bits"

#"""ejemplo: Des3Cifrar(fractal.png,crypto-flask\uploads\img\fractal.png,'ECB', '') 
#Nos va a guardar todo en la carpeta :
#crypto-flask\uploads\encrypted\fractal.png
#RETORNA LA LLAVE DE LA FORMA: b'\xc3\xba\x0c\x7f \xf7\x9b\x03\x97\rN(\xc3L?\xe8'
#PARA DESENCRIPTAR LA IMAGEN DEBE ESTAR EN ENCRYPTED


#"""


def des3Encrypt(nombre, mode, key, ivk):
    if(key==""):
        key = "".join(r.sample(ALPHABET, 24)).encode() 
    elif (len(key)!=24):
        raise InputKeyError("Key must have a length of 24 letters.")
    
    if(ivk==""):
        ivk = "".join(r.sample(ALPHABET, 8)).encode()
    elif (len(ivk)!=8):
        raise InputKeyError("Initial vector must have a length of 8 letters.")

    # key = get_random_bytes(24)
    # else:
    #     if not (all([isinstance(item, int) for item in key]) and len(key) == 24):
    #         raise InputKeyError("Key must be a binary number with length 24")
    
    # ivk = get_random_bytes(8)
    # file_out = open("key.txt", "wb")
    # file_out.write(key)
    # file_out.close()

    if(mode == 'ECB'):
        mod = DES3.MODE_ECB
    elif(mode == 'CBC'):
        mod = DES3.MODE_CBC
    elif(mode == 'CFB'):
        mod = DES3.MODE_CFB
    elif(mode == 'OFB'):
        mod = DES3.MODE_OFB
    elif(mode == 'CTR'):
        mod = DES3.MODE_CTR

    img_path = os.path.join(os.getcwd(), "web/static/uploads/uploaded", nombre)

    image = Image.open(img_path)
    size = image.size
    image = np.array(image)
    cipher = None
    if(mod != DES3.MODE_ECB and mod != DES3.MODE_CTR):
        cipher = DES3.new(key, mod, ivk)
    elif mod == DES3.MODE_CTR:
        cipher = DES3.new(key, mod, nonce=b"")
    else:
        cipher = DES3.new(key, mod)


    cripbytes = cipher.encrypt(pad(image.tobytes(), DES3.block_size))
    imgData = np.frombuffer(cripbytes)
    im = Image.frombuffer("RGB", size, imgData)
    im.save(os.path.join(os.getcwd(), dir_encr, nombre))
    # im.save(dir_encr+nombre)
    # file_out = open("ivk.txt", "wb")
    # file_out.write(ivk)
    # file_out.close()

    return {'key': key.decode(), 'inicial_vector': ivk.decode()}




def des3Decrypt(nombre, mode, key, ivk):
    if (len(key)!=24):
        raise InputKeyError("Key must have a length of 24 letters.")
    if (len(ivk)!=8):
        raise InputKeyError("Initial vector must have a length of 8 letters.")

    if(mode == 'ECB'):
        mod = DES3.MODE_ECB
    elif(mode == 'CBC'):
        mod = DES3.MODE_CBC
    elif(mode == 'CFB'):
        mod = DES3.MODE_CFB
    elif(mode == 'OFB'):
        mod = DES3.MODE_OFB
    elif(mode == 'CTR'):
        mod = DES3.MODE_CTR

    # if(key == ""):
    #     file_in = open("key.txt", "rb")
    #     key = file_in.read()
    #     file_in.close()

    #ivk = get_random_bytes(8)
    # file_in = open("ivk.txt", "rb")
    # ivk = file_in.read()
    # file_in.close()
    # img_path = dir_encr + nombre
    img_path = os.path.join(os.getcwd(), "web/static/uploads/uploaded", nombre)
    image = Image.open(img_path)
    size = image.size
    image = np.array(image)
        
    cipher = None
    if(mod != DES3.MODE_ECB):
        cipher = DES3.new(key, mod, iv=ivk)
    else:
        cipher = DES3.new(key, mod)

    imagebytes = image.tobytes()
    decrypbytes = cipher.decrypt(imagebytes)
    imgData = np.frombuffer(decrypbytes)
    # Image.frombuffer("RGB", size, imgData).save(dir_des + nombre)
    im = Image.frombuffer("RGB", size, imgData)
    im.save(os.path.join(os.getcwd(), dir_des, nombre))

    return {'key': key.decode(), 'inicial_vector': ivk.decode()}

# des3Encrypt('fractal.png','ECB','')
# des3Decrypt('fractal.png','ECB','')
