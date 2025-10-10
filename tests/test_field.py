from ecies.field import P, add, sub, mul, inv, neg, modp

def test_field_basic():
    a = 123456789123456789
    b = 987654321987654321
    assert add(a, b) == (a + b) % P
    assert sub(a, b) == (a - b) % P
    assert mul(a, b) == (a * b) % P
    x = 42
    assert (mul(x, inv(x)) % P) == 1
    assert modp(-1) == P - 1
    assert neg(5) == (P - 5) % P
