#Encryptation sistems

In the first instance we assume  we are working in English language, so the dictionary has 26 letters and they are numbered as follows:

    A : 0  B : 1  C : 2  D : 3 E : 4 
    F : 5  G : 6  H : 7  I : 8 J : 9 
    K : 10 L : 11 M : 12 N : 13 O : 14 
    P : 15 Q : 16 R : 17 S : 18 T : 19 
    U : 20 V : 21 W : 22 X : 23 Y : 24  
    Z : 25 

for all methods where text is encrypted, the letters pass to their numerical value.

Example: 

    HELLO = 7 4 11 11 14



## Caesar
key : Integer number between 0 and 25

Method : Add for all value letter the key 

Example: 

    key = 2

    HELLO = 7 4 11 11 14

    7+2 4+2 11+2 11+2 14+2  = 9 6 13 13 16 = K H N N R


## Affine

key : Two integers 'a' and 'b' between 0 and 25 separated by a space where a is relative prime with 26. it means a is one of these values:

        3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25


Method : Multiply a for all value letter and sum b in module 26

Example: 

    key = 2 3

    HELLO = 7 4 11 11 14

    (2*7)+3 (4*2)+3 (11*2)+3 (11*2)+3 (14*2)+3  = 17 11 25 25 5 = S L Z Z F

## Vigenere
key : Word with 4 to 7 characters

Method : the word is separated by chunks with length of the key and each letter of each chunks is added to the value of the letter of the key

Example: 

    key = LOVE = 11 14 21 4

    HELLO = 7 4 11 11 14

    7+11 4+14 11+21 11+4 14+11  = 18 18 7 15 25 = S S H P Z


## Permutation
key : A permutation of number between 1 and n where n divides lenght of the text

Method : the word is separated by chunks with length of the key and each letter of each chunks is send to the value of permutation of the key

Example: 

    key = 3 1 4 2 

    HELLOMIA = 7 4 11 11 14 12 8 0

    7 4 11 11 -> 4 11 7 11 = E L H L
    14 12 8 0 -> 12 0 14 8 =  M A O I


## Sustitution

key : An alphabet permutation 

Method : Replace each original text letter with the letter which is in the same position at the key

Example: 

    key = BACDEFGHIJKLMNOPQRSTUVWXYZ 

    HELLOMIA = 7 4 11 11 14 12 8 0

    7 4 11 11 14 12 8 1 = HELLOMIB

    just replace A for B at this example



## Hill

key : An invertible matrix over module 26, side m x m

Method : we make a product with the text and the key 


Example: 

    key = |7  18|
          |23 11|

    HELLO = 7 4 11 11 14 

    (7 4) | 7  18 | =  ( 7*7 + 4*23, 7*18 + 4*11) = ( 11, 14 ) 
          |23  11 | 

    (11 11) |7  18 | =  ( 11*7 + 11*23, 11*18 + 11*11) = ( 18, 7 ) 
            |23 11 |
    
    (14 0) |7  18|  =  ( 14*7 + 0*23, 14*18 + 0*11) = ( 20, 18 ) 
           |23 11| 

    11 14 18 7 20 18 = LOSHUS

