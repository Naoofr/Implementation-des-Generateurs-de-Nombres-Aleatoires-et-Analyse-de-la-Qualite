def egcd(a, b):
    """
    Algorithme d'Euclide étendu.

    Paramètres
    ----------
    a : int
        Premier entier.
    b : int
        Second entier.

    Retour
    ------
    tuple (g, x, y)
        g : PGCD de a et b
        x, y : coefficients de Bézout tels que ax + by = g
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    """
    Calcule l'inverse modulaire de a modulo m.

    Paramètres
    ----------
    a : int
        Entier dont on cherche l'inverse.
    m : int
        Module.

    Retour
    ------
    int
        Inverse modulaire de a modulo m.
    """
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Pas d\'inverse modulaire')
    else:
        return x % m

def attaque_lcg(x1, x2, x3, m):
    """
    Retrouve les paramètres d'un générateur congruentiel linéaire (LCG)
    à partir de trois sorties consécutives.

    Paramètres
    ----------
    x1 : int
        Première valeur générée.
    x2 : int
        Deuxième valeur générée.
    x3 : int
        Troisième valeur générée.
    m : int
        Module du générateur.

    Retour
    ------
    tuple (a, c)
        a : multiplicateur du LCG
        c : incrément du LCG
    """
    diff_output = (x3 - x2) % m
    diff_input = (x2 - x1) % m
    try:
        inverse = modinv(diff_input, m)
        a_trouve = (diff_output * inverse) % m
    except:
        return "Échec : Impossible d'inverser (les nombres ne conviennent pas)"
    c_trouve = (x2 - a_trouve * x1) % m

    return a_trouve, c_trouve