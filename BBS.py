from random import randint
from math import gcd
from itertools import product

# p et q deux nombres premiers
p = 1000003 
q =  2001911
M = p * q
seed = randint(2, 10)

# seed doit avoir un pgcd avec n différent de n
while gcd(seed, M) != 1: 
  seed = randint(2, 10)

#génération du nombre aléatoire
bits = str(seed % 2)
for _ in range(1,10):
  seed = (seed * seed) % M
  bit = seed % 2 
  bits += str(bit)


