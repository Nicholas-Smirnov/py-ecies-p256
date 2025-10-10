from ecies.hkdf import hkdf

def test_hkdf_len_and_repeatability():
    ikm = b"\x01\x02\x03"
    salt = b"salt"
    info = b"ctx"
    a = hkdf(ikm, salt, info, 64)
    b = hkdf(ikm, salt, info, 64)
    assert len(a) == 64
    assert a == b
