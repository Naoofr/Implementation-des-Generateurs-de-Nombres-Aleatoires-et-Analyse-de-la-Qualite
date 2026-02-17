class LCG:
    """
    Implémentation d'un générateur congruentiel linéaire (Linear Congruential Generator).

    Le générateur suit la relation :
        X_{n+1} = (a * X_n + c) mod m

    Attributs
    ---------
    etat : int
        État interne courant du générateur.
    m : int
        Module.
    a : int
        Multiplicateur.
    c : int
        Incrément.
    """

    def __init__(self, graine):
        """
        Initialise le générateur avec une graine donnée.

        Paramètres
        ----------
        graine : int
            Valeur initiale de l'état interne.
        """

        self.etat = graine
        # Constantes standard
        self.m = 2**31
        self.a = 1103515245
        self.c = 12345

    def suivant(self):
        """
        Calcule et retourne la valeur suivante du générateur.

        Retour
        ------
        int
            Prochain entier pseudo-aléatoire généré.
        """

        self.etat = (self.a * self.etat + self.c) % self.m
        return self.etat

class MersenneTwister:
    """
    Implémentation simplifiée du générateur Mersenne Twister (MT19937).

    Ce générateur est basé sur une récurrence matricielle
    et possède une très longue période (2^19937 - 1).

    Attributs
    --------------------
    mt : list
        Tableau représentant l'état interne (624 entiers).
    index : int
        Position courante dans l'état interne.
    """

    def __init__(self, graine):
        """
        Initialise le générateur Mersenne Twister avec une graine donnée.

        Paramètres
        ----------
        graine : int
            Valeur initiale utilisée pour initialiser l'état interne.
        """

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
        """
        Met à jour l'état interne complet du générateur.

        Cette opération combine les valeurs de l’état courant
        pour produire un nouvel état selon l’algorithme MT19937.
        """

        for i in range(self.N):
            x = (self.mt[i] & 0x80000000) + (self.mt[(i+1) % self.N] & 0x7FFFFFFF)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ self.A
            self.mt[i] = self.mt[(i + self.M) % self.N] ^ xA
        self.index = 0

    def suivant(self):
        """
        Retourne la prochaine valeur pseudo-aléatoire générée.

        Si nécessaire, applique l'opération 'twist' avant
        d'extraire un nombre. Une étape de 'tempering'
        est ensuite appliquée pour améliorer la distribution.

        Retour
        ------
        int
            Entier pseudo-aléatoire sur 32 bits.
        """

        if self.index >= self.N:
            self.twist()
        y = self.mt[self.index]
        self.index += 1
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & 0x9D2C5680)
        y = y ^ ((y << 15) & 0xEFC60000)
        y = y ^ (y >> 18)
        return y & 0xFFFFFFFF