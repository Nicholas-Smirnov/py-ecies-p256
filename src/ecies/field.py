# Finite field operations mod the P-256 prime
# p = 2^256 - 2^224 + 2^192 + 2^96 - 1
P = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff

def modp(x: int) -> int:
    return x % P

def add(a: int, b: int) -> int:
    return (a + b) % P

def sub(a: int, b: int) -> int:
    return (a - b) % P

def mul(a: int, b: int) -> int:
    return (a * b) % P

def inv(a: int) -> int:
    if a == 0:
        raise ZeroDivisionError("inverse of zero")
    # Fermat's little theorem: a^(p-2) mod p (p is prime)
    return pow(a, P - 2, P)

def neg(a: int) -> int:
    return (-a) % P
