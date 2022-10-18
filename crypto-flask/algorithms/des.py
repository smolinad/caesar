
import math
import random
from PIL import Image
import numpy as np
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
from base64 import b64encode
import imageio as iio
import requests
from Cryptodome.Cipher import DES3
from Cryptodome.Cipher import DES 

dir_encr = 'crypto-flask/web/static/uploads/encrypted/'
dir_des = 'crypto-flask/web/static/uploads/decrypted/'

def DesCifrar(nombre,img_path,mode, key):
    if(key==""):
        key = get_random_bytes(8)
    ivk = get_random_bytes(8)

    if(mode == 'ECB'):
        mod = DES.MODE_ECB
    elif(mode == 'CBC'):
        mod = DES.MODE_CBC
    elif(mode == 'CFB'):
        mod = DES.MODE_CFB
    elif(mode == 'OFB'):
        mod = DES.MODE_OFB

    image = Image.open(img_path)
    size = image.size
    image = np.array(image)
    cipher = None
    if(mod != DES.MODE_ECB):
        cipher = DES.new(key, mod,iv=ivk)
    else:
        cipher = DES.new(key, mod)
    cripbytes = cipher.encrypt(pad(image.tobytes(), DES.block_size))
    imgData = np.frombuffer(cripbytes)
    im = Image.frombuffer("RGB", size, imgData)
    im.save("imagenCifrada.bmp")
        
    file_out = open("key.txt", "wb")
    file_out.write(key)
    file_out.close()

    file_out = open("ivk.txt", "wb")
    file_out.write(ivk)
    file_out.close()


def DesDescifrar(nombre,img_path,mode, key):
    if(mode == 'ECB'):
        mod = DES.MODE_ECB
    elif(mode == 'CBC'):
        mod = DES.MODE_CBC
    elif(mode == 'CFB'):
        mod = DES.MODE_CFB
    elif(mode == 'OFB'):
        mod = DES.MODE_OFB

    if(key == ""):
        file_in = open("key.txt", "rb")
        key = file_in.read()
        file_in.close()

    file_in = open("ivk.txt", "rb")
    ivk = file_in.read()
    file_in.close()

    image = Image.open("imagenCifrada.bmp")
    size = image.size
    image = np.array(image)
        
    cipher = None
    if(mod != DES.MODE_ECB):
        cipher = DES.new(key, mod, iv=ivk)
    else:
        cipher = DES.new(key, mod)

    imagebytes = image.tobytes()
    decrypbytes = cipher.decrypt(imagebytes)
    imgData = np.frombuffer(decrypbytes)
    Image.frombuffer("RGB", size, imgData).save("imagen.bmp")