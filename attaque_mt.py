from generators import MersenneTwister

def inverser_droite(y, shift):
    t = y
    for _ in range(32 // shift):
        t = y ^ (t >> shift)
    return t

def inverser_gauche(y, shift, mask):
    t = y
    for _ in range(32 // shift):
        t = y ^ ((t << shift) & mask)
    return t

def inverser_tempering(y):
    y = inverser_droite(y, 18)
    y = inverser_gauche(y, 15, 0xEFC60000)
    y = inverser_gauche(y, 7, 0x9D2C5680)
    y = inverser_droite(y, 11)

    return y
print("1. Preparation de la victime ")
vrai_mt = MersenneTwister(graine=1234)
print("La victime génère des nombres...")
valeurs_observees = []
for i in range(624):
    valeurs_observees.append(vrai_mt.suivant())

print(f"J'ai capturé {len(valeurs_observees)} valeurs.")

print("\n2. Reconstruction de l'état")
etat_reconstruit = []
for val in valeurs_observees:
    etat_interne = inverser_tempering(val)
    etat_reconstruit.append(etat_interne)
clone_mt = MersenneTwister(graine=0)
clone_mt.mt = list(etat_reconstruit)
clone_mt.index = 624
print("Clonage terminé. Le clone est prêt.")
print("\n--- 3. Vérification (Prédiction du futur) ---")
prochain_vrai = vrai_mt.suivant()
print(f"La victime génère : {prochain_vrai}")
prochain_clone = clone_mt.suivant()
print(f"Le clone prédit   : {prochain_clone}")
if prochain_vrai == prochain_clone:
    print("\n[Succès] Le générateur est cloné.")
else:
    print("\n[Echec] Les valeurs sont différentes.")