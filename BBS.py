from random import randint
from math import gcd
from itertools import product
import numpy as np
import matplotlib.pyplot as plt

p = 1000003
q =  2001911

def BBS_generator(p = 1000003, q =  2001911, M = p * q, seed = randint(2, 10), TAILLE_NB_GENERE = 128):
  # seed doit avoir un pgcd avec n différent de n
  while gcd(seed, M) != 1: 
    seed = randint(2, 10)

  #génération du nombre aléatoire
  bits = str(seed % 2)
  for _ in range(1,TAILLE_NB_GENERE):
    seed = (seed * seed) % M
    bit = seed % 2 
    bits += str(bit)

  return int(bits, 2)



# --- Génère une grande séquence de bits ---
def generate_bits(n_bits=5000):
    x = BBS_generator(TAILLE_NB_GENERE=n_bits)
    bits = bin(x)[2:].zfill(n_bits)
    return np.array([int(b) for b in bits])

# --- Autocorrélation ---
def autocorrelation(x, max_lag=50):
    n = len(x)
    x = x - np.mean(x)
    result = []
    for lag in range(1, max_lag+1):
        c = np.corrcoef(x[:-lag], x[lag:])[0,1]
        result.append(c)
    return result