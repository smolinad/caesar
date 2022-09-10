import imageio.v2 as imageio
import numpy as np

"""
hillEncrypt y hillDecrypt reciben nombre de imagen
y guardan la nueva información respectivamente en 
Encrypted.png y Key.png
Decrypted.png
"""

def hillEncrypt(s: str):
    mod = 256
    img = imageio.imread(s)
    image = valuesOfImage(img)
    key = randomKey(mod, img.shape)

    Enc1 = (np.matmul(key % mod, image[:, :, 0] % mod)) % mod
    Enc2 = (np.matmul(key % mod, image[:, :, 1] % mod)) % mod
    Enc3 = (np.matmul(key % mod, image[:, :, 2] % mod)) % mod

    Enc1 = np.resize(Enc1, (Enc1.shape[0], Enc1.shape[1], 1))
    Enc2 = np.resize(Enc2, (Enc2.shape[0], Enc2.shape[1], 1))
    Enc3 = np.resize(Enc3, (Enc3.shape[0], Enc3.shape[1], 1))

    # Enc = key * image
    Enc = np.concatenate((Enc1, Enc2, Enc3), axis=2)

    imageio.imwrite('Encrypted.png', Enc.astype(np.uint8))

def hillDecrypt(s: str):
    mod = 256
    Enc = imageio.imread(s)    #Reading Encrypted Image to Decrypt

    # Loading the key
    key = imageio.imread('Key.png')
    l = key[-1][0] * mod + key[-1][1] # The length of the original image
    w = key[-1][2] * mod + key[-1][3] # The width of the original image
    key = key[0:-1]

    Dec1 = (np.matmul(key % mod, Enc[:, :, 0] % mod)) % mod
    Dec2 = (np.matmul(key % mod, Enc[:, :, 1] % mod)) % mod
    Dec3 = (np.matmul(key % mod, Enc[:, :, 2] % mod)) % mod

    Dec1 = np.resize(Dec1, (Dec1.shape[0], Dec1.shape[1], 1))
    Dec2 = np.resize(Dec2, (Dec2.shape[0], Dec2.shape[1], 1))
    Dec3 = np.resize(Dec3, (Dec3.shape[0], Dec3.shape[1], 1))
    Dec = np.concatenate((Dec1, Dec2, Dec3), axis=2)
    #Dec = key * Enc

    Final = Dec[:l,:w,:]
    #Returning Dimensions to the real image

    imageio.imwrite('Decrypted.png', Final.astype(np.uint8))


def valuesOfImage(img):
    l = img.shape[0]
    w = img.shape[1]
    n = max(l, w)
    if n % 2:
        n = n + 1
    # Making the picture to have square dimensions
    image = np.zeros((n, n, 3))
    image[:l, :w, :] += img
    return image


def randomKey(mod: int, imgShape: list):

    l = imgShape[0]
    w = imgShape[1]
    n = max(l,w)
    if n % 2:
        n = n + 1
    k = 23  # Key for Encryption

    # Arbitrary Matrix
    d = np.random.randint(256, size=(int(n / 2), int(n / 2)))
    a = np.mod(-d, mod)
    I = np.identity(int(n / 2))


    b = np.mod((k * np.mod(I - a, mod)), mod)
    k = np.mod(np.power(k, 127), mod)
    c = np.mod((I + a), mod)
    c = np.mod(c * k, mod)

    A1 = np.concatenate((a, b), axis=1)
    A2 = np.concatenate((c, d), axis=1)
    key = np.concatenate((A1, A2), axis=0)

    # making sure that key is an involutory matrix, key*key = I
    Test = np.mod(np.matmul(np.mod(key, mod), np.mod(key, mod)), mod)
    saveKeyAsImage(key, mod, l, w)
    return key

    # Saving key as an image
def saveKeyAsImage(key, mod: int, l: int, w: int):
    n = max(l, w)
    if n % 2:
        n = n + 1
    k = np.zeros((n + 1, n))
    k[:n, :n] += key
    # Adding the dimension of the original image within the key
    # Elements of the matrix should be below 256
    k[-1][0] = int(l / mod)
    k[-1][1] = l % mod
    k[-1][2] = int(w / mod)
    k[-1][3] = w % mod
    # Get the information of the incoming image type
    k = k.astype(np.uint8)
    imageio.imwrite("Key.png",k)

hillEncrypt('imageio:wikkie.png')
hillDecrypt('Encrypted.png')
