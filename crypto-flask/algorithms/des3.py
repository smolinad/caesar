# import math
# import random
from readline import append_history_file
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

dir_up = 'crypto-flask/web/static/uploads/uploaded/'
dir_encr = 'crypto-flask/web/static/uploads/encrypted/'
dir_des = 'crypto-flask/web/static/uploads/decrypted/'

"Recibe nombre de la imagen su path, el modo y una llave que es de 24 bits"

#"""ejemplo: Des3Cifrar(fractal.png,crypto-flask\uploads\img\fractal.png,'ECB', '') 
#Nos va a guardar todo en la carpeta :
#crypto-flask\uploads\encrypted\fractal.png
#RETORNA LA LLAVE DE LA FORMA: b'\xc3\xba\x0c\x7f \xf7\x9b\x03\x97\rN(\xc3L?\xe8'
#PARA DESENCRIPTAR LA IMAGEN DEBE ESTAR EN ENCRYPTED


#"""


def des3Encrypt(nombre,mode, key):
    if(key==""):
        key = get_random_bytes(24)
    ivk = get_random_bytes(8)
    file_out = open("key.txt", "wb")
    file_out.write(key)
    file_out.close()

    if(mode == 'ECB'):
        mod = DES3.MODE_ECB
    elif(mode == 'CBC'):
        mod = DES3.MODE_CBC
    elif(mode == 'CFB'):
        mod = DES3.MODE_CFB
    elif(mode == 'OFB'):
        mod = DES3.MODE_OFB
    img_path = dir_up + nombre
    print(img_path)
    image = Image.open(img_path)
    size = image.size
    image = np.array(image)
    cipher = None
    if(mod != DES3.MODE_ECB):
        cipher = DES3.new(key, mod, ivk)
    else:
        cipher = DES3.new(key, mod)


    cripbytes = cipher.encrypt(pad(image.tobytes(), DES3.block_size))
    imgData = np.frombuffer(cripbytes)
    im = Image.frombuffer("RGB", size, imgData)
    path_ = os.path.join(curr_dir, dir_encr + nombre)
    print(path_)
    im.save(path_)
        
    

    # file_out = open("ivk.txt", "wb")
    # file_out.write(ivk)
    # file_out.close()
    return {"key": key, "ivk": ivk}





def des3Decrypt(nombre,mode, key):
    if(mode == 'ECB'):
        mod = DES3.MODE_ECB
    elif(mode == 'CBC'):
        mod = DES3.MODE_CBC
    elif(mode == 'CFB'):
        mod = DES3.MODE_CFB
    elif(mode == 'OFB'):
        mod = DES3.MODE_OFB

    if(key == ""):
        file_in = open("key.txt", "rb")
        key = file_in.read()
        file_in.close()

    #ivk = get_random_bytes(8)
    file_in = open("ivk.txt", "rb")
    ivk = file_in.read()
    file_in.close()
    img_path = dir_encr + nombre
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
    Image.frombuffer("RGB", size, imgData).save(dir_des + nombre)

    return key

des3Encrypt('fractal.png','ECB','')
des3Decrypt('fractal.png','ECB','')
