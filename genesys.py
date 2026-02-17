import os

def generate_random_binary_number(taille_octets=4):
    """
    Génère un entier pseudo-aléatoire à l'aide de os.urandom.

    Paramètres
    ----------
    taille_octets : int
        Nombre d'octets à générer (4 octets = 32 bits par défaut).

    Retour  
    ------
    int
        Entier correspondant aux octets générés.
    """

    bytes_data = os.urandom(taille_octets)
    number = int.from_bytes(bytes_data, 'big')
    return number


def generer_octets(taille=1, nb=10000):
    """
    Génère une liste d'entiers aléatoires produits par os.urandom.

    Paramètres
    ----------
    taille : int
        Nombre d'octets utilisés pour chaque entier généré.
    nb : int
        Nombre total de valeurs à produire.

    Retour
    ------
    list
        Liste contenant les entiers aléatoires générés.
    """

    b=[]
    for i in range(nb) :
        b.append(generate_random_binary_number(taille))
    return b