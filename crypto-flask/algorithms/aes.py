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

#Recibe nombre de la imagen su path, el modo y una llave que es de 24 bits"

#"""ejemplo: aesEncrypt('sebas.png','crypto-flask\\uploads\\img\\sebas.png','ECB','')
#Nos va a guardar todo en la carpeta :
#crypto-flask\uploads\encrypted\sebas.png

#RETORNA LA LLAVE DE LA FORMA: b'\xc3\xba\x0c\x7f \xf7\x9b\x03\x97\rN(\xc3L?\xe8'
#
#aesEncrypt('sebas.png','crypto-flask\\uploads\\img\\sebas.png','ECB','')
#aesDecrypt('sebas.png','crypto-flask\\uploads\\encrypted\\sebas.png','ECB','')"""

p8_table = [6, 3, 7, 4, 8, 5, 10, 9]
p10_table = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
p4_table = [2, 4, 3, 1]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]
expansion = [4, 1, 2, 3, 2, 3, 4, 1]
s0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
s1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]] 

dir_encr = 'crypto-flask\\web\\static\\uploads\\encrypted\\'
dir_des = 'crypto-flask\\web\\static\\uploads\\decrypted\\'


def loadImageBlock(url):
    f = open('imagen.bmp', 'wb')
    f.write(requests.get(url).content)
    f.close()
    image = iio.imread('imagen.bmp')
    im = Image.fromarray(image)
    im = im.convert('RGB')
    im.save("imagen.bmp")

def loadImage2Block(a):
    if(a==0):
        image = iio.imread('imagen.bmp')
    elif(a==1):
        image = iio.imread('imagenCifrada.bmp')
    reshape = 1
    for i in image.shape:
        reshape *= i
    return image.reshape((1, reshape)), image.shape

def loadImage3Block(path):
    image = iio.imread(path)
    im = Image.fromarray(image)
    im = im.convert('RGB')
    im.save("imagen.bmp")


def aesEncrypt(nombre,img_path,mode, key, bt=16):
    if(key==""):
        key = get_random_bytes(bt)
    ivk = get_random_bytes(16)

    if(mode == 'ECB'):
        mod = AES.MODE_ECB
    elif(mode == 'CBC'):
        mod = AES.MODE_CBC
    elif(mode == 'CFB'):
        mod = AES.MODE_CFB
    elif(mode == 'OFB'):
        mod = AES.MODE_OFB

    image = Image.open(img_path)
    size = image.size
    image = np.array(image)
    cipher = None
    if(mod != AES.MODE_ECB):
        cipher = AES.new(key, mod,iv=ivk)
    else:
        cipher = AES.new(key, mod)
    cripbytes = cipher.encrypt(pad(image.tobytes(),AES.block_size))
    imgData = np.frombuffer(cripbytes)
    im = Image.frombuffer("RGB", size, imgData)
    im.save(dir_encr + nombre)

    file_out = open("key.txt", "wb")
    file_out.write(key)
    file_out.close()

    file_out = open("ivk.txt", "wb")
    file_out.write(ivk)
    file_out.close()

    return key


def aesDecrypt(nombre,img_path,mode, key, bt=16):
    if(mode == 'ECB'):
        mod = AES.MODE_ECB
    elif(mode == 'CBC'):
        mod = AES.MODE_CBC
    elif(mode == 'CFB'):
        mod = AES.MODE_CFB
    elif(mode == 'OFB'):
        mod = AES.MODE_OFB

    if(key == ""):
        file_in = open("key.txt", "rb")
        key = file_in.read()
        file_in.close()

    file_in = open("ivk.txt", "rb")
    ivk = file_in.read()
    file_in.close()

    image = Image.open(img_path)
    size = image.size
    image = np.array(image)
        
    cipher = None
    if(mod != AES.MODE_ECB):
        cipher = AES.new(key, mod, iv=ivk)
    else:
        cipher = AES.new(key, mod)

    imagebytes = image.tobytes()
    decrypbytes = cipher.decrypt(imagebytes)
    imgData = np.frombuffer(decrypbytes)
    Image.frombuffer("RGB", size, imgData).save(dir_des + nombre)
    return key

print(aesEncrypt('sebas.png','crypto-flask\\web\\static\\uploads\\img\\sebas.png','ECB',''))
#aesDecrypt('sebas.png','crypto-flask\\web\\static\\uploads\\img\\sebas.png','ECB','')