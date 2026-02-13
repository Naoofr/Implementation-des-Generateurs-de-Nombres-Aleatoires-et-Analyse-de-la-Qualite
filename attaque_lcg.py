def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Pas d\'inverse modulaire')
    else:
        return x % m

def attaque_lcg(x1, x2, x3, m):
    diff_output = (x3 - x2) % m
    diff_input = (x2 - x1) % m
    try:
        inverse = modinv(diff_input, m)
        a_trouve = (diff_output * inverse) % m
    except:
        return "Échec : Impossible d'inverser (les nombres ne conviennent pas)"
    c_trouve = (x2 - a_trouve * x1) % m

    return a_trouve, c_trouve