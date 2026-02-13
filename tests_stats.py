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

import math

def test_chi_carre(donnees):
    taille = len(donnees)
    attendu = taille / 256.0                     
    comptage = [0] * 256
    
    for octet in donnees:
        comptage[octet] += 1
    
    chi2 = 0.0
    for observe in comptage:
        chi2 += ((observe - attendu) ** 2) / attendu
    
    # === Calcul de la p-value via approximation de Fisher ===
    df = 255
    if chi2 <= 0:
        p_value = 1.0
    else:
        z = math.sqrt(2 * chi2) - math.sqrt(2 * df - 1.0)
        p_value = 0.5 * math.erfc(z / math.sqrt(2.0))
    return chi2, p_value

def generer_octets(generateur, quantite):
    octets = []
    for _ in range(quantite):
        val = generateur.suivant()
        octets.append(val & 0xFF)
        octets.append((val >> 8) & 0xFF)
        octets.append((val >> 16) & 0xFF)
        octets.append((val >> 24) & 0xFF)
    return octets

def ks_test_uniform(binary_data):
    """
    Effectue un test de Kolmogorov-Smirnov sur des données binaires.
    1. Transforme le binaire en valeurs normalisées (0-255 -> 0.0-1.0)
    2. Calcule la statistique D_n (distance maximale)
    """
    n = len(binary_data)
    if n == 0:
        return None

    # 1. Conversion des octets en float normalisés [0, 1]
    # On crée la Fonction de Répartition Empirique (ECDF)
    data_sorted = sorted([b / 256.0 for b in binary_data])

    d_max = 0.0

    # 2. Calcul de la distance maximale Dn
    # On compare chaque point i à la droite théorique y = x
    for i in range(n):
        x = data_sorted[i]
        
        # Distance au point i (échelon supérieur de l'escalier)
        d_plus = (i + 1) / n - x
        
        # Distance au point i (échelon inférieur de l'escalier)
        d_moins = x - i / n
        
        d_max = max(d_max, d_plus, d_moins)

    # 3. Calcul approximatif de la p-value (Formule de Kolmogorov)
    # Pour n > 35, on peut utiliser une approximation
    p_value = calculate_ks_p_value(d_max, n)

    return d_max, p_value

def calculate_ks_p_value(d_max, n):
    """
    Approximation de la p-value pour la statistique de Kolmogorov.
    Une p-value proche de 0 indique que les données ne sont PAS uniformes.
    """
    # Statistique normalisée
    sqrt_n = math.sqrt(n)
    z = (sqrt_n + 0.12 + 0.11 / sqrt_n) * d_max
    
    # Formule de la distribution de Kolmogorov (Série de Taylor)
    if z < 0.27:
        return 1.0
    if z > 4.0:
        return 0.0
        
    # Approximation simplifiée de la série
    sum_k = 0
    for k in range(1, 101):
        sign = -1 if k % 2 != 0 else 1
        sum_k += 2 * sign * math.exp(-2 * (k * z)**2)
    

    return min(max(sum_k, 0.0), 1.0)
