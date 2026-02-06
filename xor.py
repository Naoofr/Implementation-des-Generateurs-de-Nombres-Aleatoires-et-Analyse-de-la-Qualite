import BBS 
import genesys
from operator import xor




def xor_generator(input1 = BBS.BBS_generator(TAILLE_NB_GENERE=128), input2 = genesys.generate_random_binary_number(taille_octets=16)):
    print("Nombre généré par l'algorithme BBS : ", input1)
    print("Nombre généré par os.urandom : ", input2)
    
    a=xor(input1,input2)
    return a


print("Résultat du xor : ", xor_generator())