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
print("-------Test statistiques sur nos générateurs-------")

# Estimation d’entropie (Shannon) par octet
print("\n-------Test d'entropie de Shannon par octet sur Box-Muller-------")
tes1 = boxMuller.run_simulation()
print("\n-------Test d'entropie de Shannon par octet sur Box-Muller-------")
lcg = LCG(graine=12345)
data_lcg = tests_stats.generer_octets(lcg, 1000)
test_LCG = tests_stats.calcul_entropie(data_lcg)
print("Entropie sur LCG : ", test_LCG)


# Test du χ2 (chi-carré) pour l’uniformité des octets.



print("\n--- Vérification de la prédiction ---")
print(f"4ème nombre réel du LCG : {mon_lcg.suivant()}")