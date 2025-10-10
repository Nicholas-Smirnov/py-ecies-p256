# NIST P-256 curve: affine reference implementation (educational; not constant-time)
from .field import P, add, sub, mul, inv, modp

# Curve: y^2 = x^3 - 3x + b over F_p
A = P - 3  # -3 mod p
B = int("5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B", 16)
GX = int("6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", 16)
GY = int("4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5", 16)
N  = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551  # group order
H  = 1  # cofactor

INF = None  # point at infinity sentinel

def is_on_curve_affine(x: int, y: int) -> bool:
    if x is None or y is None:
        return False
    if x < 0 or x >= P or y < 0 or y >= P:
        return False
    left = mul(y, y)
    right = add(add(mul(mul(x, x), x), mul(A, x)), B)
    return modp(left - right) == 0

def is_on_curve_point(Pt) -> bool:
    if Pt is INF:
        return False
    x, y = Pt
    return is_on_curve_affine(x, y)

def point_add(Pt, Qt):
    if Pt is INF: return Qt
    if Qt is INF: return Pt
    x1, y1 = Pt; x2, y2 = Qt
    if x1 == x2 and (y1 + y2) % P == 0:
        return INF
    if x1 == x2 and y1 == y2:
        # tangent slope λ = (3x1^2 + A)/(2y1)
        lam = mul(add(mul(3, mul(x1, x1)), A), inv((2 * y1) % P))
    else:
        # chord slope λ = (y2 - y1)/(x2 - x1)
        lam = mul(sub(y2, y1), inv((sub(x2, x1)) % P))
    x3 = sub(sub(mul(lam, lam), x1), x2)
    y3 = sub(mul(lam, sub(x1, x3)), y1)
    return (modp(x3), modp(y3))

def scalar_mult(k: int, Pt):
    k = k % N
    if k == 0 or Pt is INF:
        return INF
    Q = INF
    for i in reversed(range(k.bit_length())):
        if Q is not INF:
            Q = point_add(Q, Q)
        if (k >> i) & 1:
            Q = Pt if Q is INF else point_add(Q, Pt)
    return Q

G = (GX, GY)

def privkey_from_bytes(b: bytes) -> int:
    k = int.from_bytes(b, "big") % N
    return k or 1

def pubkey_from_priv(k: int):
    return scalar_mult(k, G)
