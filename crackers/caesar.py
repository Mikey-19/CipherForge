import string

ALPHABET = string.ascii_uppercase

def clean_text(text):
    return "".join(c for c in text.upper() if c in ALPHABET)

def encrypt(plaintext, shift):
    """
    Encrypt plaintext using Caesar cipher with given shift
    """
    result = []
    plaintext = plaintext.upper()
    for c in plaintext:
        if c.isalpha():
            idx = (ord(c) - ord('A') + shift) % 26
            result.append(chr(idx + ord('A')))
        else:
            result.append(c)
    return "".join(result)

def crack(ciphertext, top_n=5):
    """
    Crack Caesar cipher using frequency analysis
    Returns top_n candidates as (score, shift, plaintext)
    """
    ciphertext = clean_text(ciphertext)
    candidates = []
    for shift in range(26):
        plaintext = encrypt(ciphertext, 26 - shift)  # decrypt
        # simple scoring: count most common English letters
        score = sum(plaintext.count(c) for c in "ETAOIN SHRDLU")
        candidates.append((score, shift, plaintext))
    candidates.sort(reverse=True, key=lambda x: x[0])
    return candidates[:top_n]
