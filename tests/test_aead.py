import os, pytest
from ecies.aead import AEAD

def test_aead_roundtrip():
    key = os.urandom(32)
    nonce = os.urandom(12)
    aead = AEAD(key)
    pt = b"hello aead"
    aad = b"meta"
    ct = aead.encrypt(nonce, pt, aad)
    assert aead.decrypt(nonce, ct, aad) == pt

def test_aead_aad_mismatch():
    key = os.urandom(32); nonce = os.urandom(12)
    aead = AEAD(key)
    ct = aead.encrypt(nonce, b"x", b"A")
    import pytest
    with pytest.raises(Exception):
        _ = aead.decrypt(nonce, ct, b"B")
