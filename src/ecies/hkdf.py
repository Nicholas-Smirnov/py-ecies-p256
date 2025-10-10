import hmac, hashlib

def hkdf_extract(salt: bytes, ikm: bytes, hashmod=hashlib.sha256) -> bytes:
    if salt is None:
        salt = b"\x00" * hashmod().digest_size
    return hmac.new(salt, ikm, hashmod).digest()

def hkdf_expand(prk: bytes, info: bytes, length: int, hashmod=hashlib.sha256) -> bytes:
    n = (length + hashmod().digest_size - 1) // hashmod().digest_size
    okm = b""
    t = b""
    for i in range(1, n + 1):
        t = hmac.new(prk, t + info + bytes([i]), hashmod).digest()
        okm += t
    return okm[:length]

def hkdf(ikm: bytes, salt: bytes, info: bytes, length: int, hashmod=hashlib.sha256) -> bytes:
    prk = hkdf_extract(salt, ikm, hashmod)
    return hkdf_expand(prk, info, length, hashmod)
