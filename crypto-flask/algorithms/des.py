
import math
import random as r
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
import os
from algorithms.goodies import InputKeyError, ALPHABET

dir_encr = 'web/static/uploads/encrypted/'

dir_des = 'crypto-flask/web/static/uploads/decrypted/'

def desEncrypt(nombre,mode, key, ivk):
    # if(key==""):
    #     key = get_random_bytes(8)
    # else:
    #     if not (all([isinstance(item, int) for item in key]) and len(key) == 8):
    #         raise InputKeyError("Key must be a binar number with length 8")

    # ivk = get_random_bytes(8)

    if(key==""):
        key = "".join(r.sample(ALPHABET, 8)).encode()
    elif (len(key)!=8):
        raise InputKeyError("Key must have a length of 8 letters.")
    
    if(ivk==""):
        ivk = "".join(r.sample(ALPHABET, 8)).encode()
    elif (len(ivk)!=8):
        raise InputKeyError("Initial vector must have a length of 8 letters.")

    if(mode == 'ECB'):
        mod = DES.MODE_ECB
    elif(mode == 'CBC'):
        mod = DES.MODE_CBC
    elif(mode == 'CFB'):
        mod = DES.MODE_CFB
    elif(mode == 'OFB'):
        mod = DES.MODE_OFB
    elif(mode == 'CTR'):
        mod = DES.MODE_CTR

    img_path = os.path.join(os.getcwd(), "web/static/uploads/uploaded", nombre)

    image = Image.open(img_path)
    size = image.size
    image = np.array(image)
    cipher = None

    if(mod != DES.MODE_ECB and mod != DES.MODE_CTR):
        cipher = DES.new(key, mod, ivk)
    elif mod == DES.MODE_CTR:
        cipher = DES.new(key, mod, nonce=b"")
    else:
        cipher = DES.new(key, mod)

    cripbytes = cipher.encrypt(pad(image.tobytes(), DES.block_size))
    imgData = np.frombuffer(cripbytes)
    im = Image.frombuffer("RGB", size, imgData)
    im.save(os.path.join(os.getcwd(), dir_encr, nombre))
        
    # file_out = open("key.txt", "wb")
    # file_out.write(key)
    # file_out.close()

    # file_out = open("ivk.txt", "wb")
    # file_out.write(ivk)
    # file_out.close()
    return {'key': key.decode()  , 'inicial_vector': ivk.decode() }


def desDecrypt(nombre,img_path,mode, key):
    if(mode == 'ECB'):
        mod = DES.MODE_ECB
    elif(mode == 'CBC'):
        mod = DES.MODE_CBC
    elif(mode == 'CFB'):
        mod = DES.MODE_CFB
    elif(mode == 'OFB'):
        mod = DES.MODE_OFB
    elif(mode == 'CTR'):
        mod = DES.MODE_CTR

    if(key == ""):
        try:
            file_in = open("key.txt", "rb")
            key = file_in.read()
            file_in.close()
        except:
            raise InputKeyError("we can not decrypt without a key :(")


    file_in = open("ivk.txt", "rb")
    ivk = file_in.read()
    file_in.close()

    image = Image.open("imagenCifrada.bmp")
    size = image.size
    image = np.array(image)
        
    cipher = None
    if(mod != DES.MODE_ECB and mod != DES.MODE_CTR):
        cipher = DES.new(key, mod, ivk)
    elif mod == DES.MODE_CTR:
        cipher = DES.new(key, mod, nonce=b"")
    else:
        cipher = DES.new(key, mod)

    imagebytes = image.tobytes()
    decrypbytes = cipher.decrypt(imagebytes)
    imgData = np.frombuffer(decrypbytes)
    Image.frombuffer("RGB", size, imgData).save("imagen.bmp")


#DesCifrar('2021-03-04 (1).png','ECB','')