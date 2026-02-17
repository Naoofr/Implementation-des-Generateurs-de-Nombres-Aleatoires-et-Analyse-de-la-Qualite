from random import randint
from math import gcd
from itertools import product
import numpy as np
import matplotlib.pyplot as plt

p = 1000003
q =  2001911

def BBS_generator(p = 1000003, q =  2001911, M = p * q, seed = randint(2, 10), TAILLE_NB_GENERE = 128):
  """
  Générateur pseudo-aléatoire basé sur l'algorithme Blum-Blum-Shub (BBS).

  Paramètres
  ----------
  p : int
      Nombre premier congru à 3 modulo 4.
  q : int
      Nombre premier congru à 3 modulo 4.
  M : int
      Module utilisé pour le calcul (p * q).
  seed : int
      Graine initiale du générateur (doit être premier avec M).
  TAILLE_NB_GENERE : int
      Nombre de bits à générer.

  Retour
  ------
  int
      Entier correspondant à la concaténation des bits générés.
  """
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
    """
    Génère une séquence de bits à l'aide du générateur BBS.

    Paramètres
    ----------
    n_bits : int
        Nombre de bits à produire.

    Retour
    ------
    numpy.ndarray
        Tableau numpy contenant les bits.
    """
    x = BBS_generator(TAILLE_NB_GENERE=n_bits)
    bits = bin(x)[2:].zfill(n_bits)
    return np.array([int(b) for b in bits])

# --- Autocorrélation ---
def autocorrelation(x, max_lag=50):
    """
    Calcule l'autocorrélation d'une séquence pour différents retards (lags).

    Paramètres
    ----------
    x : array-like
        Séquence de bits.
    max_lag : int
        Nombre maximal à évaluer.

    Retour
    ------
    list
        Liste des coefficients de corrélation pour chaque lag.
    """
    n = len(x)
    x = x - np.mean(x)
    result = []
    for lag in range(1, max_lag+1):
        c = np.corrcoef(x[:-lag], x[lag:])[0,1]
        result.append(c)
    return result