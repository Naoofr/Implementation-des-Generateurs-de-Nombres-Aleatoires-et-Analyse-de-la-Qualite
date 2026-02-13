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

def ks_test_uniform_from_bits(bit_array):
    """
    Adapte les bits reçus du BBS pour le test de Kolmogorov-Smirnov.
    1. Regroupe les bits par 8 pour former des octets (0-255).
    2. Applique le test KS sur ces octets.
    """
    n_bits = len(bit_array)
    if n_bits < 40: # Il faut assez de bits pour faire quelques octets
        return None

    # --- ÉTAPE 1 : Conversion des bits en octets (0-255) ---
    binary_data = []
    for i in range(0, n_bits - 7, 8):
        byte = 0
        for bit in bit_array[i:i+8]:
            byte = (byte << 1) | int(bit)
        binary_data.append(byte)
    
    n = len(binary_data)
    
    # --- ÉTAPE 2 : Calcul du KS classique ---
    # Normalisation : on transforme [0-255] en [0.0-1.0]
    data_sorted = sorted([b / 256.0 for b in binary_data])
    
    d_max = 0.0
    for i in range(n):
        x = data_sorted[i]
        # On compare l'escalier empirique à la droite théorique y = x
        d_plus = (i + 1) / n - x
        d_moins = x - i / n
        d_max = max(d_max, d_plus, d_moins)

    # --- ÉTAPE 3 : Calcul de la p-value ---
    p_value = calculate_ks_p_value(d_max, n)
    return d_max, p_value

def calculate_ks_p_value(d_max, n):
    """Approximation de la série de Kolmogorov (version corrigée)"""
    sqrt_n = math.sqrt(n)
    # Ajustement de Stephens pour la précision
    z = (sqrt_n + 0.12 + 0.11 / sqrt_n) * d_max
    
    if z < 0.27: return 1.0
    if z > 4.0: return 0.0
    
    p_value = 0
    for k in range(1, 101):
        sign = 1 if k % 2 != 0 else -1
        term = 2 * sign * math.exp(-2 * (k * z)**2)
        p_value += term
        if abs(term) < 1e-10: break
        
    return min(max(p_value, 0.0), 1.0)


