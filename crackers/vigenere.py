import string
from itertools import product

ALPHABET = string.ascii_uppercase

def clean_text(text):
    return "".join(c for c in text.upper() if c in ALPHABET)

def encrypt(plaintext, key):
    """
    Encrypt plaintext using Vigenère cipher
    """
    plaintext = clean_text(plaintext)
    key = clean_text(key)
    ciphertext = []
    key_len = len(key)
    for i, c in enumerate(plaintext):
        shift = ALPHABET.index(key[i % key_len])
        idx = (ALPHABET.index(c) + shift) % 26
        ciphertext.append(ALPHABET[idx])
    return "".join(ciphertext)

def vigenere_decrypt(ciphertext, key):
    ciphertext = clean_text(ciphertext)
    key = clean_text(key)
    plaintext = []
    key_len = len(key)
    for i, c in enumerate(ciphertext):
        shift = ALPHABET.index(key[i % key_len])
        idx = (ALPHABET.index(c) - shift) % 26
        plaintext.append(ALPHABET[idx])
    return "".join(plaintext)

def crack(ciphertext, max_key_length=3):
    """
    Basic Vigenère cracker for demonstration
    Tries all keys of length 1..max_key_length
    Returns list of (score, key, plaintext)
    """
    ciphertext = clean_text(ciphertext)
    candidates = []
    for key_len in range(1, max_key_length + 1):
        for key_tuple in product(ALPHABET, repeat=key_len):
            key = "".join(key_tuple)
            plaintext = vigenere_decrypt(ciphertext, key)
            score = sum(plaintext.count(c) for c in "ETAOIN SHRDLU")
            candidates.append((score, key, plaintext))
    candidates.sort(reverse=True, key=lambda x: x[0])
    return candidates[:5]
