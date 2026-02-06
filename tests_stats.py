import math
from generators import LCG, MersenneTwister

def calcul_entropie(donnees):
    taille = len(donnees)
    comptage = {}
    for octet in donnees:
        if octet in comptage:
            comptage[octet] += 1
        else:
            comptage[octet] = 1
    entropie = 0
    for octet in comptage:
        p = comptage[octet] / taille
        entropie -= p * math.log2(p)
    return entropie

def test_chi_carre(donnees):
    taille = len(donnees)
    attendu = taille / 256
    comptage = [0] * 256
    for octet in donnees:
        comptage[octet] += 1
    chi2 = 0
    for observe in comptage:
        chi2 += ((observe - attendu) ** 2) / attendu
    return chi2

def generer_octets(generateur, quantite):
    octets = []
    for _ in range(quantite):
        val = generateur.suivant()
        octets.append(val & 0xFF)
        octets.append((val >> 8) & 0xFF)
        octets.append((val >> 16) & 0xFF)
        octets.append((val >> 24) & 0xFF)
    return octets

# Exécution des tests
print("Analyse statistiques sur 100 000 nombres ")

# 1. Test du LCG
lcg = LCG(graine=12345)
data_lcg = generer_octets(lcg, 25000)
ent_lcg = calcul_entropie(data_lcg)
chi_lcg = test_chi_carre(data_lcg)
print(f"\n[LCG]")
print(f"Entropie (Idéal = 8.0) : {ent_lcg:.5f}")
print(f"Chi-carré (Idéal ~ 255): {chi_lcg:.2f}")
# 2. Test du Mersenne Twister
mt = MersenneTwister(graine=12345)
data_mt = generer_octets(mt, 25000)
ent_mt = calcul_entropie(data_mt)
chi_mt = test_chi_carre(data_mt)
print(f"\n[Mersenne Twister]")
print(f"Entropie (Idéal = 8.0) : {ent_mt:.5f}")
print(f"Chi-carré (Idéal ~ 255): {chi_mt:.2f}")

# Interprétation simple
def verdict(chi_score):
    if 200 < chi_score < 320:
        return "Succès (Distribution uniforme)"
    else:
        return "Echec (Distribution biaisée)"

print("\n VERDICT")
print(f"LCG              : {verdict(chi_lcg)}")
print(f"Mersenne Twister : {verdict(chi_mt)}")