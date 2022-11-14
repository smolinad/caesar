def legendre(a, p):
    return pow(a, (p - 1) // 2, p)

def tonelli(n, p):
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

def ec_gen_points_set(a, b, p):
    ec_points_on_curve = []
    for x in range(p):
        y2 = x ** 3 + a * x + b
        lengdre_val = legendre(y2, p)
        if lengdre_val != 0:
            if lengdre_val != 1:  # (y2 | p) must be ≡ 1 to have a square if not continue to next num
                continue
        elif lengdre_val == 0:
            y_root1 = 0
            gen1 = (x, y_root1)
            ec_points_on_curve.append(gen1)
            continue
        y_root1 = tonelli(y2, p)  # one possible root
        y_root2 = p - y_root1

        if y_root2 < y_root1:
            gen1 = (x, y_root2)
            gen2 = (x, y_root1)
        else:
            gen1 = (x, y_root1)
            gen2 = (x, y_root2)

        ec_points_on_curve.append(gen1)
        ec_points_on_curve.append(gen2)
    return ec_points_on_curve

def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)


# calculate `modular inverse`
def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g == 1:
        return x % m
    else:
        return None

#OPERACIONES ECC
# double function
def ecc_double(x1, y1, p, a):
    if modinv(2 * y1, p) is None: return None

    s = ((3 * (x1 ** 2) + a) * modinv(2 * y1, p)) % p
    x3 = (s ** 2 - x1 - x1) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)


# add function
def ecc_add(x1, y1, x2, y2, p, a):
    s = 0
    if (x1 == x2):
        if modinv(2 * y1, p) is None : return None
        s = ((3 * (x1 ** 2) + a) * modinv(2 * y1, p)) % p
    else:
        if modinv(x2 - x1, p) is None: return None
        s = ((y2 - y1) * modinv(x2 - x1, p)) % p
    x3 = (s ** 2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)


def double_and_add(multi, generator, p, a):
    (x3, y3) = (0, 0)
    (x1, y1) = generator
    (x_tmp, y_tmp) = generator
    init = 0
    for i in str(bin(multi)[2:]):
        if (i == '1') and (init == 0):
            init = 1
        elif (i == '1') and (init == 1):
            if ecc_double(x_tmp, y_tmp, p, a) is None: return None
            if ecc_add(x1, y1, x3, y3, p, a) is None: return None
            (x3, y3) = ecc_double(x_tmp, y_tmp, p, a)
            (x3, y3) = ecc_add(x1, y1, x3, y3, p, a)
            (x_tmp, y_tmp) = (x3, y3)
        else:
            if ecc_double(x_tmp, y_tmp, p, a) is None: return None
            (x3, y3) = ecc_double(x_tmp, y_tmp, p, a)
            (x_tmp, y_tmp) = (x3, y3)
    return (x3, y3)


def scale_point_set(a, b, p, generator):
    ec_curve_points = ec_gen_points_set(a, b, p)
    scaled_points_set = {}
    i = 1
    scaled_points_set[str(i) + "P"] = generator

    while True:
        i += 1
        scaled_point = double_and_add(i, generator, p, a)

        if scaled_point is None or scaled_point not in ec_curve_points:
            scaled_points_set[str(i) + "P"] = "O"
            break

        elif scaled_point in ec_curve_points:
            scaled_points_set[str(i) + "P"] = scaled_point
            if str(i) + "P" != "2P" and scaled_points_set["2P"] == scaled_points_set[str(i) + "P"]:  # the current index is not 2P and no other duplicate point exists
                scaled_points_set[str(i) + "P"] = "O"
                break    #if duplicate P exists then stop

    return scaled_points_set

def KeyGen(key, pointSet):
    order = len(pointSet)
    if key > order:
        key = key % order

        if key == 0: return pointSet[str(order) + "P"]  # if the modulo is zero return the last element in list

        key = pointSet[str(key) + "P"]  # User Public Key
    else:
        key = pointSet[str(key) + "P"]  # User Public Key

    return key

# agoritmo extendido de euclides que toma 2 primos relativos y les encuentra inverso modular
def Inverse_Mod(e, m):
    m0 = m
    y = 0
    x = 1
    if (m == 1):
        return 0
    while (e > 1):
        q = int(e / m)  # q is quotient
        temp = m
        m = e % m
        e = temp
        temp = y
        # Update x and y
        y = x - q * y
        x = temp
    # Make x positive
    if (x < 0): x = x + m0
    return x
def primitivo(a,b,p):
	for x in range(1,p):
		val=((x*x*x)+a*x+b) % p
		res = math.sqrt(val)
		if (abs(res-int(res))<0.0001):
			return(x,int(res))


import random
from sympy import N, randprime
import random
import math


def elgammalEcEncrypt(text,p = ""):
    a,b,p,gx, gy, Nb, Ka = generateMvData(p)
    cifrado=[]
    generator=(gx,gy)
    y0 = KeyGen(Ka, scale_point_set(a, b, p, generator))
    publicKeyB = KeyGen(Nb, scale_point_set(a, b, p, generator))
    mask = KeyGen(Ka, scale_point_set(a, b, p, publicKeyB))
    for i in range(len(text)):
        m=str(ord(text[i]))
        if((len(m)%2)!=0):
            m1 = int(m[:(len(m)//2)+1])
            m2 = int(m[len(m)//2+1:])
        else:
            m1 = int(m[:(len(m)//2)])
            m2 = int(m[len(m)//2:])
        y1 = (mask[0]*m1)%p
        y2 = (mask[1]*m2)%p
        cifrado.append((y0,y1,y2))
    #print("(C1,C2)):", mask)
    return(cifrado,[p,0,(a,b),Nb])
  
def elgammalEcDecrypt(tcifrado,p,a,b,Nb):

    text = tcifrado
    text = [eval(binario) for binario in text[1:-1].replace(" ","").split(', ((')]
    tcifrado = [text[0][i] for i in range(len(text[0]))]
    print(tcifrado)
    TextoDecifrado=""
    for i in range(len(tcifrado)):
        Nb_hint= KeyGen(Nb, scale_point_set(a, b, p, tcifrado[i][0]))
        inv_c1 = Inverse_Mod(Nb_hint[0],p)
        decrypt_m1 = (inv_c1*tcifrado[i][1])%p
        inv_c2 = Inverse_Mod(Nb_hint[1],p)
        decrypt_m2 = (inv_c2*tcifrado[i][2])%p
        TextoDecifrado = TextoDecifrado + chr(int(str(decrypt_m1) + str(decrypt_m2)))
    return (TextoDecifrado,[p,0,(a,b),Nb])

def generateMvData(p):
    if p=="":
        p=randprime(100,1000)
    else:
        p=int(p)
    a=random.randint(0,100)
    b=random.randint(0,100)
    gx,gy=primitivo(a,b,p)
    ca=random.randint(10**2,10**3)
    while(ca>p):
        ca=random.randint(10**2,10**3)
    cb=random.randint(10**2,10**3)
    while(cb>p):
        cb=random.randint(10**2,10**3)
    return a,b,p,gx, gy, cb, ca

#cifrado,p,a,b,Nb = elgammalEcEncrypt("hola","")
#d ..
# print(elgammalEcDecrypt("[((367, 614), 412, 103), ((367, 614), 412, 932), ((367, 614), 412, 309), ((367, 614), 487, 726)]",937,66, 97,213))