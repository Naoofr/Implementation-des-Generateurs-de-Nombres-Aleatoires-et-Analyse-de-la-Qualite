import os

def generate_random_binary_number(taille_octets=4):
    """
    Génère un nombre aléatoire en utilisant os.urandom et le retourne en binaire.

    :param taille_octets: Nombre d'octets à générer (par défaut 4 pour un nombre 32 bits).
    :return: Chaîne binaire du nombre (ex: '0b101010...').
    """
    bytes_data = os.urandom(taille_octets)
    number = int.from_bytes(bytes_data, 'big')
    return bin(number)

print(generate_random_binary_number(128))