# hill image

import cv2 as cv
import numpy
import numpy as np
from goodies import InputKeyError

"""
hillEncrypt recibe (s: str, k="") donde s es el nombre de la imagen a encriptar  y k es el nombre de la imagen clave
no devuelve nada, en lugar de ello guarda las imagenes encrypted y key en la carpeta test-img

hillDecrypt recibe (s: str, k: str) donde s y k son los descritos arriba.
no devuelve nada, en lugar de ello guarda las imagenes decrypted y key en la carpeta test-img
"""

def hillEncrypt(s: str, k=""):
    mod = 256
    plain_rectangle = readGray(s)

    n = min(plain_rectangle.shape)
    if n % 2 != 0:
        n = n-1
    plain = plain_rectangle[0:n, 0:n]

    if k == "":
        m = int(n/2)
        key_orig = numpy.random.randint(0, mod, (m, m))
    else:
        m = int(n/2)
        key_orig = readGray(k)
        key_orig = cv.resize(key_orig, (m, m))

    key = involutoryMatrixOf(key_orig)
    isInvolutory(key, mod)
    encrypted = np.matmul(plain, key) % mod

    cv.imwrite('test-img/encrypted.png', encrypted)
    cv.imwrite('test-img/key.png', key_orig)

def hillDecrypt(s: str, k: str):
    mod = 256
    encrypted = readGray(s)
    key_orig = readGray(k)

    isSquare(encrypted)
    isSquare(key_orig)

    key = involutoryMatrixOf(key_orig)
    isInvolutory(key, mod)

    if key.shape[0] != encrypted.shape[0]:
        raise InputKeyError

    decrypted = np.matmul(encrypted, key) % mod

    cv.imwrite('test-img/decrypted.png', decrypted)
    cv.imwrite('test-img/key.png', key_orig)

def isInvolutory(a: numpy.ndarray, mod: int):
    isSquare(a)
    y = numpy.identity(a.shape[0])
    x = numpy.matmul(a % mod, a % mod) % mod
    if numpy.array_equal(x, y):
        return
    raise InputKeyError("Error de código")

def involutoryMatrixOf(a11: numpy.ndarray):
    a22 = -a11
    y = numpy.identity(a11.shape[0])
    a12 = y - a11
    a21 = y + a11
    a1 = numpy.concatenate((a11, a21))
    a2 = numpy.concatenate((a12, a22))
    a = numpy.concatenate((a1, a2), axis=1)
    return a

def isSquare(a: numpy.ndarray):
    if a.shape[0] != a.shape[1]:
        raise InputKeyError("Encrypted image and key image must be squared")

def readGray(s: str):
    coloredIm = cv.imread(s)

    if coloredIm is None:
        raise InputKeyError("There´s no image with the name "+s)

    return cv.cvtColor(coloredIm, cv.COLOR_BGR2GRAY)

hillEncrypt('test-img/mani.png')
hillDecrypt('test-img/encrypted.png', 'test-img/key.png')
