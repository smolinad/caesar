import cv2 as cv
import numpy as np
import os
from algorithms.goodies import InputKeyError
#from goodies import InputKeyError

dir = 'hill-images\\'
img_dir = 'img\\'
key_dir = 'key-img\\'
enc_dir = 'encrypted-img\\'
dec_dir = 'decrypted-img\\'

"""
hillEncrypt recibe (s: str, k="") donde s es el nombre de la imagen a encriptar  y k es el nombre de la imagen clave
no devuelve nada, en lugar de ello guarda las imagenes encrypted y key en la carpeta hill-images
hillDecrypt recibe (s: str, k: str) donde s y k son los descritos arriba.
no devuelve nada, en lugar de ello guarda las imagenes decrypted y key en la carpeta hill-images
"""

def hillImgEncrypt(s: str, k=""):
    mod = 256
    colored_img = read(img_dir+s)

    n = min(colored_img.shape[0], colored_img.shape[1])
    if n % 2 != 0:
        n = n-1
    colored_img = colored_img[0:n, 0:n]

    if k == "":
        m = int(n/2)
        key_orig = np.random.randint(0, mod, (m, m, 3))
        cv.imwrite(key_dir+s, key_orig)

    else:
        m = int(n/2)
        key_orig = read(key_dir+k)
        key_orig = cv.resize(key_orig, (m, m))

    key = [involutoryMatrixOf(i) for i in cv.split(key_orig)]
    [isInvolutory(i, mod) for i in key]

    e = [np.matmul(i, j) % mod for i, j in zip(cv.split(colored_img),key)]
    encrypted = cv.merge(e)

    cv.imwrite(enc_dir+s, encrypted)
    # return (cv.imencode('.png', encrypted), cv.imencode('.png', key_orig))

def hillImgDecrypt(s: str, k: str):
    mod = 256
    encrypted = read(enc_dir+s)

    n = encrypted.shape[0]
    if n % 2 != 0:
        n = n-1

    m = int(n/2)
    key_orig = read(key_dir+k)
    key_orig = cv.resize(key_orig, (m, m))

    isSquare(encrypted)
    isSquare(key_orig)

    key = [involutoryMatrixOf(i) for i in cv.split(key_orig)]
    [isInvolutory(i, mod) for i in key]

    d = [np.matmul(i, j) % mod for i, j in zip(cv.split(encrypted),key)]
    decrypted = cv.merge(d)

    cv.imwrite(dec_dir+s, decrypted)

def isInvolutory(a: np.ndarray, mod: int):
    isSquare(a)
    y = np.identity(a.shape[0])
    x = np.matmul(a % mod, a % mod) % mod
    if np.array_equal(x, y):
        return
    raise InputKeyError("Error de código")

def isSquare(a: np.ndarray):
    if a.shape[0] != a.shape[1]:
        raise InputKeyError("Encrypted image and key image must be squared")

def read(s: str):
    if s.split(".")[-1] != "png":
        raise InputKeyError(s+"image format must be png")

    coloredIm = cv.imread(s)

    if coloredIm is None:
        raise InputKeyError("There´s no image with the name "+s+" in " + os.getcwd())

    return coloredIm

b = os.getcwd()+'\\'
os.chdir(b+dir)

"""b = os.getcwd()+'\\'
os.chdir(b+dir)

print(os.listdir(b+dir+img_dir))
for filename in os.listdir(b+dir+img_dir):
    f = os.path.join(b+dir+img_dir, filename)
    print(filename)
    hillImgEncrypt(filename, 'mani.png')
    hillImgDecrypt(filename, 'mani.png')"""
