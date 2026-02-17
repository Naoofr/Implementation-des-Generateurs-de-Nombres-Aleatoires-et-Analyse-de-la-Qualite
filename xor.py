import BBS 
import genesys
from operator import xor




def xor_generator(input1 = BBS.BBS_generator(TAILLE_NB_GENERE=128), input2 = genesys.generate_random_binary_number(taille_octets=16)):
    """
    Génère une valeur en appliquant une opération XOR entre
    deux nombres.

    Paramètres
    ----------
    input1 : int
        Premier entier binaire (par défaut issu de BBS).
    input2 : int
        Second entier binaire (par défaut issu d'un générateur système).

    Retour
    ------
    int
        Résultat de l'opération XOR entre les deux entrées.
    """
    
    a=xor(input1,input2)
    return a