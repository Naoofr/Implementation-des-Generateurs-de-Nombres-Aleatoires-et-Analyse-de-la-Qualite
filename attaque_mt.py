from generators import MersenneTwister

def inverser_droite(y, shift):
    """
    Inverse une opération de décalage à droite avec XOR utilisée
    dans l'étape de tempering du Mersenne Twister.

    Paramètres
    ----------
    y : int
        Valeur temperée à corriger.
    shift : int
        Nombre de bits du décalage à droite.

    Retour
    ------
    int
        Valeur partiellement reconstruite avant l'opération
        de décalage à droite.
    """
    t = y
    for _ in range(32 // shift):
        t = y ^ (t >> shift)
    return t

def inverser_gauche(y, shift, mask):
    """
    Inverse une opération de décalage à gauche avec XOR et masque
    utilisée dans l'étape de tempering du Mersenne Twister.

    Paramètres
    ----------
    y : int
        Valeur temperée à corriger.
    shift : int
        Nombre de bits du décalage à gauche.
    mask : int
        Masque binaire appliqué lors de l'opération.

    Retour
    ------
    int
        Valeur partiellement reconstruite avant l'opération
        de décalage à gauche avec masque.
    """
    t = y
    for _ in range(32 // shift):
        t = y ^ ((t << shift) & mask)
    return t

def inverser_tempering(y):
    """
    Annule complètement l'étape de tempering du Mersenne Twister.

    Cette fonction applique successivement les inversions
    des transformations effectuées lors du tempering afin
    de retrouver l'état interne original à partir d'une
    sortie du générateur.

    Paramètres
    ----------
    y : int
        Valeur produite par le Mersenne Twister après tempering.

    Retour
    ------
    int
        Valeur correspondant à l'état interne non temperé.
    """
    y = inverser_droite(y, 18)
    y = inverser_gauche(y, 15, 0xEFC60000)
    y = inverser_gauche(y, 7, 0x9D2C5680)
    y = inverser_droite(y, 11)

    return y