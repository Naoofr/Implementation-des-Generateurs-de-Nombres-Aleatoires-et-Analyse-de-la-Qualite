# Importation des générateurs
from generators import LCG, MersenneTwister
import BBS
import genesys
from hash_DRBG import HashDRBG
import xor
import boxMuller

# Importations des tests
import tests_stats


# Autres importations
import os
import numpy as np
import matplotlib.pyplot as plt



#---------Exemple de génération de nombres aléatoires---------
print("-------Exemple de génération de nombres aléatoires-------")

# Linear Congruential Generator (LCG) 
print("\nExemple du LCG")
mon_lcg = LCG(graine=1)
print("Valeur 1 : ", mon_lcg.suivant())
print("Valeur 2 : ", mon_lcg.suivant())
print("Valeur 3 : ", mon_lcg.suivant())

# Mersenne Twister (MT19937)
print("\nExemple du Mersenne Twister")
mon_mt = MersenneTwister(graine=1)
print("Valeur 1 : ", mon_mt.suivant())
print("Valeur 2 : ", mon_mt.suivant())
print("Valeur 3 : ", mon_mt.suivant())

# Transformée de Box–Muller
print("\nExemple de la transformée de Box-Muller")
res_BM = boxMuller.box_muller()
print("valeur 1 générée par Box-Muller : ", res_BM[0])
print("valeur 2 générée par Box-Muller : ", res_BM[1])


# NIST SP 800-90A DRBG (Deterministic Random Bit Generators) Hash_DRBG
print("\nExemple du hash_DRBG")
drbg=HashDRBG(entropy_input = os.urandom(32), nonce = os.urandom(16))
res_drbg=drbg.generate(256)
print("Valeur générée par le Hash DRBG : ", res_drbg.hex())



# Blum–Blum–Shub (BBS) 
print("\nExemple de blum_blum_shum")
blumblumshum = BBS.BBS_generator(TAILLE_NB_GENERE = 128)
print("Valeur générée par BBS : ", blumblumshum)



# Générateur système (os.urandom) 
print("\nExemple de os.urandom")
rdm = genesys.generate_random_binary_number(4)
print("Valeur générée par os.urandom : ", rdm)

# Construction XOR NRBG (Non-Random Bit Generator)
print("\nExemple de xor en utilisant les résultats de BBS et os.urandom")
res_xor = xor.xor_generator()
print("Valeur générée à la suite du xor : ", res_xor)


#---------Tests statistiques---------
print("\n\n-------Test statistiques sur nos générateurs-------")


# Estimation d’entropie (Shannon) par octet
print("\n-------Test d'entropie de Shannon par octet sur Box-Muller-------")
test1 = boxMuller.run_simulation()
print(test1)
print("\n-------Test d'entropie de Shannon par octet sur l'algorithme LCG-------")
lcg = LCG(graine=12345)
data_lcg = tests_stats.generer_octets(lcg, 1000)
test_LCG = tests_stats.calcul_entropie(data_lcg)
print("Entropie sur LCG : ", test_LCG)


# Test du χ2 (chi-carré) pour l’uniformité des octets.
print("\n-------Test du χ2 sur l'algorithme LCG-------")
chi_lcg = tests_stats.test_chi_carre(data_lcg)
print("Résultat du chi-carré sur LCG : ", chi_lcg)

print("\n-------Test du χ2 sur os.urandom-------")
data_os = genesys.generer_octets()
chi_os = tests_stats.test_chi_carre(data_os)
print("Résultat de chi-carré sur os.urandom : ", chi_os)


# Autocorrélation (lags 1, 8, . . . )
print("\n-------Test d'autocorrélation de l'agorithme BBS-------")
bits = BBS.generate_bits(5000)
ac = BBS.autocorrelation(bits, max_lag=40)
print("Résultat : cf graph")

plt.stem(range(1, 41), ac)
plt.axhline(0, linestyle='--')
plt.title("Autocorrélation des bits BBS")
plt.xlabel("Lag (retard)")
plt.ylabel("Corrélation")
plt.show()


print("\n-------Test d'autocorrélation de l'agorithme du xor-------")
bits = bin(xor.xor_generator(5000))[2:]
res = np.array([int(b) for b in bits])
ac = BBS.autocorrelation(res, max_lag=40)
print("Résultat : cf graph")

plt.stem(range(1, 41), ac)
plt.axhline(0, linestyle='--')
plt.title("Autocorrélation des bits du xor")
plt.xlabel("Lag (retard)")
plt.ylabel("Corrélation")
plt.show()


# Test de Kolmogorov–Smirnov (KS)




#---------Tests statistiques---------
print("\n--- Vérification de la prédiction ---")
print(f"4ème nombre réel du LCG : {mon_lcg.suivant()}")