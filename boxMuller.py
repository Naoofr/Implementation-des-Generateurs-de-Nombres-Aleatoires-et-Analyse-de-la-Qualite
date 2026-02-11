from operator import xor
import struct
import sys
import math
import random

# usage: box_muller.py [n [m [s]]]
n = 1  # number of samples to output
mean = 0.0
stddev = 1.0

if len(sys.argv) >= 2:
    n = int(sys.argv[1])
if len(sys.argv) >= 3:
    mean = float(sys.argv[2])
if len(sys.argv) >= 4:
    stddev = float(sys.argv[3])

# function box_muller implements the polar form of the box muller method,
# and returns 2 pseudo random numbers from standard normal distribution
def box_muller():
    while True:
        u1 = 2.0 * random.random() - 1.0  # uniformly distributed random numbers
        u2 = 2.0 * random.random() - 1.0  # ditto
        s = u1 * u1 + u2 * u2  # variance
        if s != 0.0 and s < 1.0:
            break
    w = math.sqrt(-2.0 * math.log(s) / s)  # weight
    g1 = u1 * w  # normally distributed random number
    g2 = u2 * w  # ditto
    return g1, g2

def calculate_entropy(data_bytes):
    if not data_bytes:
        return 0.0
    
    # Compter l'occurrence de chaque octet (0-255)
    frequencies = {}
    for byte in data_bytes:
        frequencies[byte] = frequencies.get(byte, 0) + 1
    
    entropy = 0.0
    total_len = len(data_bytes)
    for count in frequencies.values():
        p = count / total_len
        entropy -= p * math.log2(p)
    return entropy

def run_simulation(iterations=100, samples_per_iter=1000):
    entropies = []
    
    for _ in range(iterations):
        buffer = bytearray()
        # Générer des nombres et les convertir en binaire (double précision / 8 octets)
        for _ in range(samples_per_iter // 2):
            g1, g2 = box_muller()
            # 'd' correspond au format double (8 bytes)
            buffer.extend(struct.pack('d', g1))
            buffer.extend(struct.pack('d', g2))
        
        entropies.append(calculate_entropy(buffer))
    
    avg_entropy = sum(entropies) / len(entropies)

    print(f"Moyenne de l'entropie pour {iterations} simulations : {avg_entropy:.6f} bits/octet")