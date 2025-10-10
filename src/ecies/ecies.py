# ECIES KEM→DEM over P-256 with HKDF-SHA256 and ChaCha20-Poly1305
from .p256 import N, pubkey_from_priv, scalar_mult, is_on_curve_point
from .hkdf import hkdf
from .aead import AEAD

def keygen():
    import os
    sk = (int.from_bytes(os.urandom(32), "big") % N) or 1
    pk = pubkey_from_priv(sk)
    return sk, pk

def _dh(sk: int, pk_peer: tuple[int,int]) -> bytes:
    if not is_on_curve_point(pk_peer):
        raise ValueError("peer public key not on curve")
    S = scalar_mult(sk, pk_peer)
    if S is None:
        raise ValueError("invalid shared secret (infinity)")
    x_shared, _ = S
    return x_shared.to_bytes(32, "big")

def kem_encap(pk_recipient, info: bytes, salt: bytes=b"") -> tuple[bytes, tuple[int,int]]:
    import os
    esk = (int.from_bytes(os.urandom(32), "big") % N) or 1
    eph_pub = pubkey_from_priv(esk)
    z = _dh(esk, pk_recipient)
    okm = hkdf(z, salt, info, 44)
    return okm, eph_pub

def kem_decap(sk_recipient: int, eph_pub, info: bytes, salt: bytes=b"") -> bytes:
    z = _dh(sk_recipient, eph_pub)
    okm = hkdf(z, salt, info, 44)
    return okm

def encrypt(pk_recipient, plaintext: bytes, aad: bytes=b"", ctx_info: bytes=b"") -> dict:
    kem_info = b"ECIES-P256-HKDF-SHA256|" + ctx_info
    okm, eph_pub = kem_encap(pk_recipient, kem_info, salt=b"")
    key, nonce = okm[:32], okm[32:]
    aead = AEAD(key)
    ct = aead.encrypt(nonce, plaintext, aad)
    return {"eph_pub": eph_pub, "nonce": nonce, "ciphertext": ct}

def decrypt(sk_recipient: int, bundle: dict, aad: bytes=b"", ctx_info: bytes=b"") -> bytes:
    kem_info = b"ECIES-P256-HKDF-SHA256|" + ctx_info
    eph_pub = tuple(bundle["eph_pub"])
    okm = kem_decap(sk_recipient, eph_pub, kem_info, salt=b"")
    key, nonce = okm[:32], okm[32:]
    aead = AEAD(key)
    return aead.decrypt(nonce, bundle["ciphertext"], aad)
