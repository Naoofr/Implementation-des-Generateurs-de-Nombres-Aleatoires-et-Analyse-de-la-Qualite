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

