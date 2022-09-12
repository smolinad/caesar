# Encryption systems

In the first instance we assume we are working in English language, so the dictionary has 26 letters and they are numbered as follows:

| A | B | C | D | E | F | G | H | I | J | K  | L  | M  | N  | O  | P  | Q  | R  | S  | T  | U  | V  | W  | X  | Y  | Z  |
|---|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |

For all methods where text is encrypted, the letters are converted to their numerical value, for example: 

    HELLO = 7 4 11 11 14

## Caesar
**Key:** Integer number between $0$ and $25$.

**Method:** Add to every letter the value of the given key. 

**Example:** 

    Key = 2

    HELLO = 7 4 11 11 14

    7+2 4+2 11+2 11+2 14+2 = 9 6 13 13 16 = K H N N R


## Affine

**Key:** Two integers $a$ and $b$ between $0$ and $25$ separated by a space, where $a$ is relative prime with $26$. Therefore, $a$ is one of these values:

    3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25

**Method:** Multiply $a$ to every letter value in the input text and then sum $b$, module $26$.

**Example:** 

    Key = 2 3

    HELLO = 7 4 11 11 14

    (2*7)+3 (4*2)+3 (11*2)+3 (11*2)+3 (14*2)+3  = 17 11 25 25 5 = S L Z Z F

## Vigenere
**Key:** A word with 4 to 7 characters.

**Method:** The input text is separated by chunks of the length of the key, and to each letter of each chunk is added the value of the letter of the key.

**Example:** 

    Key = LOVE = 11 14 21 4

    HELLO = 7 4 11 11 14

    7+11 4+14 11+21 11+4 14+11  = 18 18 7 15 25 = S S H P Z


## Permutation
**Key:** A permutation of numbers between $1$ and $n$, where $n$ divides length of the text.

**Method:** The word is separated by chunks of the length of the key, and each letter of each chunk is sent to the value through the permutation on the key.

**Example:** 

    Key = 3 1 4 2 

    HELLOMIA = 7 4 11 11 14 12 8 0

    7 4 11 11 -> 4 11 7 11 = E L H L
    14 12 8 0 -> 12 0 14 8 =  M A O I


## Substitution

**Key:** A permutaton of the 26-letter alphabet.

**Method:** Replace each letter in the input text with the letter which is in the same position at the key.

**Example:** 

    Key = BACDEFGHIJKLMNOPQRSTUVWXYZ 

    HELLOMIA = 7 4 11 11 14 12 8 0

    7 4 11 11 14 12 8 1 = HELLOMIB

In the previous example, we are just replacing `A` for `B`.



## Hill

**Key:** An invertible matrix over module $26$, of size $m \times m$.

**Method:** Multiply every chunk of length $n$ in the input text (or image) by the matrix.

**Example:** 

Key = $\left[\begin{matrix}
    7 & 18 \\
    23 & 11\end{matrix}\right]$

    HELLO = 7 4 11 11 14 

$$\left(\begin{matrix}7 & 4\end{matrix}\right) \left[\begin{matrix} 7 & 18 \\ 23 & 11\end{matrix}\right] =  ( 7 \cdot 7 + 4 \cdot 23, 7 \cdot 18 + 4 \cdot 11) = ( 11, 14 )$$

$$\left(\begin{matrix}11 & 11\end{matrix}\right) \left[\begin{matrix} 7 & 18 \\ 23 & 11\end{matrix}\right] =  ( 11 \cdot 7 + 11 \cdot 23, 11 \cdot 18 + 11 \cdot 11) = ( 18, 7 ) $$
    
$$\left(\begin{matrix}14 & 0\end{matrix}\right) \left[\begin{matrix} 7 & 18 \\ 23 & 11\end{matrix}\right] =  ( 14 \cdot 7 + 0 \cdot 23, 14 \cdot 18 + 0 \cdot 11) = ( 20, 18 ) $$

    11 14 18 7 20 18 = LOSHUS

