import os, pytest
from ecies.ecies import keygen, encrypt, decrypt

def test_roundtrip():
    skB, pkB = keygen()
    msg = os.urandom(257)
    aad = b"testing"
    ctx = b"A->B"
    bundle = encrypt(pkB, msg, aad=aad, ctx_info=ctx)
    out = decrypt(skB, bundle, aad=aad, ctx_info=ctx)
    assert out == msg

def test_ctx_or_aad_mismatch_breaks():
    skB, pkB = keygen()
    msg = b"hi"
    a = encrypt(pkB, msg, aad=b"A", ctx_info=b"CTX1")
    import pytest
    with pytest.raises(Exception):
        _ = decrypt(skB, a, aad=b"A", ctx_info=b"CTX2")
    with pytest.raises(Exception):
        _ = decrypt(skB, a, aad=b"B", ctx_info=b"CTX1")
