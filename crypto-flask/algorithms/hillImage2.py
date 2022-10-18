import numpy as np
import requests
import imageio as iio
from numpy.linalg import inv, det
from PIL import Image

dir_up = 'crypto-flask/web/static/uploads/uploaded/'
dir_encr = 'crypto-flask/web/static/uploads/encrypted/'
dir_des = 'crypto-flask/web/static/uploads/decrypted/'


def hillImagenCifrar(nombre):
    img, original_shape = loadImage2(0,nombre)
    slice=computer_slice(img)
    key = np.random.random_integers(0, 100, (slice, slice))
    while det(key) == 0:
        key = np.random.random_integers(0, 100, (slice, slice))
    reversedKey = np.matrix(key).I.A
    encoded_image_vector = encode(slice,img[0],key)
    with open('key.npy', 'wb') as f:
        np.save(f, reversedKey)
        np.save(f, np.array([slice]))
        np.save(f,encoded_image_vector)
    encoded_image = encoded_image_vector.reshape(original_shape)
    encoded_image = encoded_image.astype('uint8')
    im = Image.fromarray(encoded_image)
    im = im.convert('RGB')
    im.save(dir_encr + nombre)

def hillImagenDescifrar():
    img,original_shape = loadImage2(1)
    with open('key.npy', 'rb') as f:
        reversedKey = np.load(f)
        slice=np.load(f)
        vector=np.load(f)
    slice=slice[0]
    decoded_image_vector = decode(slice,vector,reversedKey)
    decoded_image = decoded_image_vector.reshape(original_shape)
    decoded_image = decoded_image.astype('uint8')
    im = Image.fromarray(decoded_image)
    im = im.convert('RGB')
    im.save("imagen.jpg")

def computer_slice(image):
    max_slice = 100
    data_shape = image.shape[1]

    for i in range(max_slice, 0, -1):
        if data_shape % i == 0:
            return i

def loadImage(url):
    f = open('imagen.jpg', 'wb')
    f.write(requests.get(url).content)
    f.close()
    image = iio.imread('imagen.jpg')
    im = Image.fromarray(image)
    im = im.convert('RGB')
    im.save("imagen.jpg")

def loadImage2(a,nombre):
    if(a==0):

        image = iio.imread( dir_up + nombre)
    elif(a==1):
        image = iio.imread(dir_encr + nombre)
    reshape = 1
    for i in image.shape:
        reshape *= i
    return image.reshape((1, reshape)), image.shape

def loadImage3(path):
    image = iio.imread(path)
    im = Image.fromarray(image)
    im = im.convert('RGB')
    im.save("imagen.jpg")

def encode(slice, data, key):
        crypted = []
        for i in range(0, len(data), slice):
            temp = list(np.dot(key, data[i:i + slice]))
            crypted.append(temp)

        crypted = (np.array(crypted)).reshape((1, len(data)))
        return crypted[0]

def decode(slice, data, reversed_key):
        uncrypted = []

        for i in range(0, len(data), slice):
            temp = list(np.dot(reversed_key, data[i:i + slice]))
            uncrypted.append(temp)

        uncrypted = (np.array(uncrypted)).reshape((1, len(data)))

        return uncrypted[0]


hillImagenCifrar('image.png')
