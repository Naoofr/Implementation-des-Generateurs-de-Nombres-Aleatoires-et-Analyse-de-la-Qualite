def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Pas d\'inverse modulaire')
    else:
        return x % m

def attaque_lcg(x1, x2, x3, m):
    diff_output = (x3 - x2) % m
    diff_input = (x2 - x1) % m
    try:
        inverse = modinv(diff_input, m)
        a_trouve = (diff_output * inverse) % m
    except:
        return "Échec : Impossible d'inverser (les nombres ne conviennent pas)"
    c_trouve = (x2 - a_trouve * x1) % m

    return a_trouve, c_trouve

# Test avec mes valeurs générées précédemment
valeur1 = 1103527590
valeur2 = 377401575
valeur3 = 662824084
MODULO_CONNU = 2**31
print(f"Attaque sur les valeurs : {valeur1}, {valeur2}, {valeur3}")
print("Recherche des constantes secrètes a et c...")
a_hack, c_hack = attaque_lcg(valeur1, valeur2, valeur3, MODULO_CONNU)
print(f"\nRésultat du Hack :")
print(f"Multiplicateur (a) trouvé : {a_hack}")
print(f"Incrément (c) trouvé      : {c_hack}")
# Vérification
prochain_calcul = (a_hack * valeur3 + c_hack) % MODULO_CONNU
print(f"\nPrédiction du 4ème nombre : {prochain_calcul}")