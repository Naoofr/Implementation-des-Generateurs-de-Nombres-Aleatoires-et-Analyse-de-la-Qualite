import os
import collections
from scipy.stats import chi2

def random_int(max_value):
    byte_count = (max_value.bit_length() + 7) // 8
    collected_bytes = []
    while True:
        random_bytes = os.urandom(byte_count)
        collected_bytes.append(random_bytes)
        num = int.from_bytes(random_bytes, 'big')
        if num < max_value:
            return num, collected_bytes

# Paramètres
max_val = 100000  # Entre 0 et max_val-1
num_numbers = 1000  # Environ 1000

# Génération
all_numbers = []
all_collected_bytes = []

for _ in range(num_numbers):
    num, bytes_list = random_int(max_val)
    all_numbers.append(num)
    all_collected_bytes.extend(bytes_list)
import os
import collections
from scipy.stats import chi2

def random_int(max_value):
    byte_count = (max_value.bit_length() + 7) // 8
    collected_bytes = []
    while True:
        random_bytes = os.urandom(byte_count)
        collected_bytes.append(random_bytes)
        num = int.from_bytes(random_bytes, 'big')
        if num < max_value:
            return int(num,2), num.bit_length(), collected_bytes

def main():
    # Paramètres
    max_val = 100000  # Entre 0 et max_val-1
    num_numbers = 1000  # Environ 1000

    # Génération
    all_numbers = []
    all_bitsizes = []
    all_collected_bytes = []

    for _ in range(num_numbers):
        num, bitsize, bytes_list = random_int(max_val)
        all_numbers.append(num)
        all_bitsizes.append(bitsize)
        all_collected_bytes.extend(bytes_list)

    # Aplatir tous les octets
    total_bytes = b''.join(all_collected_bytes)

    # Calcul des fréquences
    counter = collections.Counter(total_bytes)
    total_count = len(total_bytes)

    # Calcul du chi-carré
    expected = total_count / 256.0
    chi2_stat = 0.0
    for i in range(256):
        observed = counter.get(i, 0)
        chi2_stat += (observed - expected) ** 2 / expected

    # Degrés de liberté
    df = 255

    # p-value
    p_value = 1 - chi2.cdf(chi2_stat, df)

    # Affichage
    print(f"Nombre de nombres générés : {len(all_numbers)}")
    print(f"Total d'octets utilisés : {total_count}")
    print(f"Statistique du chi-carré : {chi2_stat:.6f}")
    print(f"p-value : {p_value:.6f}")

if __name__ == "__main__":
    main()
# Aplatir tous les octets
total_bytes = b''.join(all_collected_bytes)

# Calcul des fréquences
counter = collections.Counter(total_bytes)
total_count = len(total_bytes)

# Calcul du chi-carré
expected = total_count / 256.0
chi2_stat = 0.0
for i in range(256):
    observed = counter.get(i, 0)
    chi2_stat += (observed - expected) ** 2 / expected

# Degrés de liberté
df = 255

# p-value
p_value = 1 - chi2.cdf(chi2_stat, df)

# Affichage
print(f"Nombre de nombres générés : {len(all_numbers)}")
print(f"Total d'octets utilisés : {total_count}")
print(f"Statistique du chi-carré : {chi2_stat:.6f}")
print(f"p-value : {p_value:.6f}")