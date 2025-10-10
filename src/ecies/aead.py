from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

class AEAD:
    def __init__(self, key: bytes):
        if len(key) != 32:
            raise ValueError("ChaCha20-Poly1305 expects 32-byte key")
        self._aead = ChaCha20Poly1305(key)

    def encrypt(self, nonce: bytes, plaintext: bytes, aad: bytes) -> bytes:
        return self._aead.encrypt(nonce, plaintext, aad)

    def decrypt(self, nonce: bytes, ciphertext: bytes, aad: bytes) -> bytes:
        return self._aead.decrypt(nonce, ciphertext, aad)
