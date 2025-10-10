from ecies.p256 import G, N, is_on_curve_point, point_add, scalar_mult, pubkey_from_priv

def test_generator_is_on_curve():
    assert is_on_curve_point(G)

def test_scalar_mult_small():
    P = scalar_mult(1, G)
    Q = scalar_mult(2, G)
    R = point_add(G, G)
    assert P == G
    assert Q == R
    assert scalar_mult(0, G) is None
    assert scalar_mult(N, G) is None  # n*G = O

def test_pubkey_from_priv():
    k = 123456789
    P = pubkey_from_priv(k)
    assert is_on_curve_point(P)
    assert P == scalar_mult(k, G)
