class LCG:
    def __init__(self, graine):
        self.etat = graine
        # Constantes standard
        self.m = 2**31
        self.a = 1103515245
        self.c = 12345

    def suivant(self):
        self.etat = (self.a * self.etat + self.c) % self.m
        return self.etat

class MersenneTwister:
    def __init__(self, graine):
        self.N = 624
        self.M = 397
        self.A = 0x9908B0DF
        self.F = 1812433253
        self.mt = [0] * self.N
        self.index = self.N
        self.mt[0] = graine
        for i in range(1, self.N):
            valeur_prec = self.mt[i-1]
            x = (self.F * (valeur_prec ^ (valeur_prec >> 30)) + i)
            self.mt[i] = x & 0xFFFFFFFF

    def twist(self):
        for i in range(self.N):
            x = (self.mt[i] & 0x80000000) + (self.mt[(i+1) % self.N] & 0x7FFFFFFF)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ self.A
            self.mt[i] = self.mt[(i + self.M) % self.N] ^ xA
        self.index = 0

    def suivant(self):
        if self.index >= self.N:
            self.twist()
        y = self.mt[self.index]
        self.index += 1
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & 0x9D2C5680)
        y = y ^ ((y << 15) & 0xEFC60000)
        y = y ^ (y >> 18)
        return y & 0xFFFFFFFF