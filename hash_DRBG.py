import hashlib
import math
import os

# --- paramètres ---
HASH = hashlib.sha256
OUTLEN = 256
SEEDLEN = 440


def int_to_bytes(i, length):
    """
    Convertit un entier en représentation binaire
    sur un nombre fixe d'octets.

    Paramètres
    ----------
    i : int
        Entier à convertir.
    length : int
        Nombre d'octets de sortie.

    Retour
    ------
    bytes
        Représentation binaire de l'entier sur 'length' octets.
    """
    return i.to_bytes(length, "big")


def hash_df(input_data: bytes, no_of_bits: int):
    """
    Fonction de dérivation basée sur une fonction de hachage (Hash_df)
    conforme au standard NIST SP 800-90A.

    Elle permet de dériver une quantité arbitraire de bits
    à partir d'un matériel d'entrée via itérations du hash.

    Paramètres
    ----------
    input_data : bytes
        Données d'entrée (entropy, nonce, etc.).
    no_of_bits : int
        Nombre de bits à produire.

    Retour
    ------
    bytes
        Chaîne d'octets de longueur suffisante pour couvrir
        le nombre de bits demandé.
    """
    counter = 1
    output = b""
    no_of_bytes = math.ceil(no_of_bits / 8)

    while len(output) < no_of_bytes:
        h = HASH()
        h.update(int_to_bytes(counter, 1))
        h.update(int_to_bytes(no_of_bits, 4))
        h.update(input_data)
        output += h.digest()
        counter += 1

    return output[:no_of_bytes]


class HashDRBG:
    """
    Implémentation simplifiée d'un générateur déterministe
    basé sur une fonction de hachage (Hash_DRBG),
    conforme au standard NIST SP 800-90A.

    Le générateur maintient un état interne (V, C)
    et un compteur de reseed pour produire des
    bits pseudo-aléatoires de manière sécurisée.
    """

    def __init__(self, entropy_input: bytes, nonce: bytes, personalization: bytes = b""):
        """
        Initialise le générateur Hash_DRBG.

        Paramètres
        ----------
        entropy_input : bytes
            Source d'entropie initiale.
        nonce : bytes
            Valeur unique supplémentaire.
        personalization : bytes, optionnel
            Chaîne optionnelle pour personnaliser l'instance.
        """

        seed_material = entropy_input + nonce + personalization

        self.V = hash_df(seed_material, SEEDLEN)
        self.C = hash_df(b"\x00" + self.V, SEEDLEN)
        self.reseed_counter = 1

    def generate(self, n_bits: int, additional_input: bytes = b"") -> bytes:
        """
        Génère une séquence de bits pseudo-aléatoires.

        Paramètres
        ----------
        n_bits : int
            Nombre de bits à produire.
        additional_input : bytes, optionnel
            Données supplémentaires intégrées dans la mise à jour
            de l'état avant génération.

        Retour
        ------
        bytes
            Séquence pseudo-aléatoire de longueur suffisante
            pour couvrir 'n_bits'.
        """

        # 1. additional_input
        if additional_input:
            h = HASH(b"\x02" + self.V + additional_input).digest()
            self.V = self._add_mod(self.V, h)

        # 2. génération
        returned_bits = self._hashgen(n_bits)

        # 3. mise à jour de l'état
        H = HASH(b"\x03" + self.V).digest()
        self.V = self._add_mod(self.V, H, self.C, int_to_bytes(self.reseed_counter, len(self.V)))
        self.reseed_counter += 1

        return returned_bits

    def _hashgen(self, n_bits: int) -> bytes:
        """
        Fonction interne de génération basée sur des itérations
        successives de la fonction de hachage.

        Paramètres
        ----------
        n_bits : int
            Nombre de bits à produire.

        Retour
        ------
        bytes
            Données pseudo-aléatoires générées.
        """

        data = b""
        V = self.V
        n_bytes = math.ceil(n_bits / 8)

        while len(data) < n_bytes:
            V = self._add_mod(V, b"\x01")
            data += HASH(V).digest()

        return data[:n_bytes]

    def _add_mod(self, *args) -> bytes:
        """
        Additionne plusieurs valeurs binaires interprétées comme
        entiers, puis applique une réduction modulo 2^SEEDLEN.

        Paramètres
        ----------
        *args : bytes
            Valeurs binaires à additionner.

        Retour
        ------
        bytes
            Résultat de l'addition modulaire, sur SEEDLEN bits.
        """

        total = 0
        for a in args:
            total += int.from_bytes(a, "big")
        return int_to_bytes(total % (1 << SEEDLEN), SEEDLEN // 8)