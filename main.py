# Importation des classes qu'on vient d'écrire
from generators import LCG, MersenneTwister
print(" Test du LCG")
mon_lcg = LCG(graine=1)
print(mon_lcg.suivant())
print(mon_lcg.suivant())
print(mon_lcg.suivant())
print("\n Test du Mersenne Twister")
mon_mt = MersenneTwister(graine=1)
print(mon_mt.suivant())
print(mon_mt.suivant())
print(mon_mt.suivant())
print("\n--- Vérification de la prédiction ---")
print(f"4ème nombre réel du LCG : {mon_lcg.suivant()}")