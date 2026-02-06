import scipy.stats
from collections import Counter
import os

def chi_squared_test(nombre_octets=10000):
    data = os.urandom(nombre_octets)
    counts = Counter(data)
    observed = [counts.get(i, 0) for i in range(256)]
    expected = [nombre_octets / 256] * 256
    chi2, p = scipy.stats.chisquare(observed, expected)
    return chi2, p

# Exécution du test
chi2, p = chi_squared_test()
print(f"Statistique du chi-carré : {chi2}")
print(f"Valeur p : {p}")
if p > 0.05:
    print("Le test suggère que les octets sont uniformément distribués (on ne rejette pas l'hypothèse nulle).")
else:
    print("Le test suggère que les octets ne sont pas uniformément distribués (on rejette l'hypothèse nulle).")