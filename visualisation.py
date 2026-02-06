import matplotlib.pyplot as plt
from generators import LCG, MersenneTwister

def generer_points(generateur, n_points):
    x = []
    y = []
    for _ in range(n_points):
        val_x = generateur.suivant() / (2**31 if isinstance(generateur, LCG) else 2**32)
        val_y = generateur.suivant() / (2**31 if isinstance(generateur, LCG) else 2**32)
        x.append(val_x)
        y.append(val_y)
    return x, y

print("Génération des graphiques en cours...")
lcg = LCG(graine=123)
lcg.m = 2048
lcg.a = 1229
lcg.c = 1
x_lcg, y_lcg = generer_points(lcg, 1000)
mt = MersenneTwister(graine=123)
x_mt, y_mt = generer_points(mt, 1000)
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.scatter(x_lcg, y_lcg, s=2, c='red')
plt.title("Défaut du LCG (Alignement)")
plt.xlabel("Valeur X")
plt.ylabel("Valeur Y (suivante)")
plt.subplot(1, 2, 2)
plt.scatter(x_mt, y_mt, s=2, c='blue')
plt.title("Qualité du Mersenne Twister")
plt.xlabel("Valeur X")
plt.ylabel("Valeur Y (suivante)")
plt.savefig("comparaison_visuelle.png")
print("Fait ! Regarde l'image 'comparaison_visuelle.png'.")
plt.show()