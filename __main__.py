"""
CipherForge CLI entry point
"""

from cipherforge.crackers import caesar

def main():
    print("CipherForge CLI")
    print("Demo Caesar crack on ciphertext 'khoor':")
    caesar.main()

if __name__ == "__main__":
    main()
