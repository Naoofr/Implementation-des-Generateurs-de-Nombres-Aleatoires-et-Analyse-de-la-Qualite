import hashlib
import math
import os

# --- paramètres ---
HASH = hashlib.sha256
OUTLEN = 256
SEEDLEN = 440


def int_to_bytes(i, length):
    return i.to_bytes(length, "big")


def hash_df(input_data: bytes, no_of_bits: int) :
    """
    Hash derivation function (Hash_df) - SP 800-90A
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
    def __init__(self, entropy_input: bytes, nonce: bytes, personalization: bytes = b""):
        seed_material = entropy_input + nonce + personalization

        self.V = hash_df(seed_material, SEEDLEN)
        self.C = hash_df(b"\x00" + self.V, SEEDLEN)
        self.reseed_counter = 1

    def generate(self, n_bits: int, additional_input: bytes = b"") -> bytes:
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
        data = b""
        V = self.V
        n_bytes = math.ceil(n_bits / 8)

        while len(data) < n_bytes:
            V = self._add_mod(V, b"\x01")
            data += HASH(V).digest()

        return data[:n_bytes]

    def _add_mod(self, *args) -> bytes:
        total = 0
        for a in args:
            total += int.from_bytes(a, "big")
        return int_to_bytes(total % (1 << SEEDLEN), SEEDLEN // 8)