# py-ecies-p256

Simple implementation of **ECIES** (Elliptic‑Curve Integrated Encryption Scheme) over **NIST P‑256**, using **HKDF‑SHA256** and **ChaCha20‑Poly1305** as the AEAD.

## ✨ What you’ll see
- **Finite fields** $\mathbb{F}_p$: modular add/sub/mul/inverse using Fermat’s little theorem.
- **Elliptic curves** over $\mathbb{F}_p$: P‑256 with affine group law (point add/double, infinity).
- **Scalar multiplication**: left‑to‑right double‑and‑add; why $nG=\mathcal{O}$ at the group order.
- **ECIES = KEM + DEM**: ephemeral ECDH → HKDF → AEAD (key + nonce) with **context binding** (AAD/`info`).


## 🧮 Short math overview

### P‑256 field and curve
- Prime
  $p=2^{256}-2^{224}+2^{192}+2^{96}-1.$
- Curve equation (short Weierstrass): $E: y^2 = x^3 - 3x + b \pmod p$,
  with the standard P‑256 constant $b$ (see `p256.py`). The group law uses:
  - For two distinct points $P=(x_1,y_1), Q=(x_2,y_2)$, slope
    $\lambda = (y_2-y_1)(x_2-x_1)^{-1}$.
  - For doubling $P=Q$, slope
    $\lambda = (3x_1^2 + a)(2y_1)^{-1}$ with $a=-3$.
  - Then
    $x_3 = \lambda^2 - x_1 - x_2$ and  $y_3 = \lambda(x_1-x_3) - y_1.$
  - The **point at infinity** $\mathcal{O}$ acts as the identity.

### Scalar multiplication
- For integer $k$, compute $kG$ via **double‑and‑add** scanning bits from MSB→LSB.
- P‑256 has **order** $n$ and cofactor 1, so **$nG=\mathcal{O}$**, and every valid public key is in the prime subgroup.

### ECIES (KEM→DEM)
1. **Ephemeral ECDH:** Sender picks $e$, computes shared secret $Z = x(e\cdot P_B)$ (using the **x‑coordinate** only).
2. **KDF:** Use **HKDF‑SHA256** to derive an **AEAD key** and **nonce** from $Z$ and a **context string** `info` (we bind identities/purpose here).
3. **DEM:** Encrypt with **ChaCha20‑Poly1305** using AAD.
4. Receiver recomputes $Z'=x(d_B\cdot E)$ and derives the same key/nonce to decrypt.

**Why bind context and AAD?** It defeats unknown‑key‑share (UKS) confusions and helps with KCI‑style pitfalls by tying the derived keys to specific identities/flows via HKDF `info` and to specific messages via AEAD AAD.



## 📦 Project layout
```
src/ecies/
  field.py       # Finite field F_p operations
  p256.py        # P-256 params, affine point ops, scalar multiplication
  hkdf.py        # HKDF-SHA256 (extract + expand)
  aead.py        # ChaCha20-Poly1305 wrapper
  ecies.py       # ECIES KEM→DEM: keygen, encrypt, decrypt
examples/demo.py # CLI demo
tests/           # pytest unit tests
```



## 🚀 Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .

# Run the demo
python -m examples.demo

# Run the tests
pytest -q
```

Demo output should look like:
```
Bob pubkey.x: 0x1ab0... 
Ciphertext len: 35
Decrypted: b'hello, ECIES world!'
```



## 🔍 Security notes (honest & practical)
- **Not constant‑time.** CPython can leak via timing/cache; this repo is for education.
- **On‑curve validation** is enforced; P‑256’s cofactor = 1 simplifies subgroup issues.
- **Context binding:** ECIES uses `info = b"ECIES-P256-HKDF-SHA256|" + ctx_info` and AAD in AEAD to reduce UKS/KCI surprises.
- **Randomness:** Ephemeral keys and symmetric keys rely on `os.urandom`.

**If you wanted production‑grade:** use vetted libraries (e.g., OpenSSL/boringssl/RustCrypto), constant‑time primitives, structured key handling, and side‑channel hardening.



## 🧪 Tests included
- Field math: add/sub/mul/inv, negatives, modp sanity.
- Curve ops: on‑curve checks, add/double identities, $nG=\mathcal{O}$.
- HKDF: determinism and length.
- AEAD: round‑trip and AAD mismatch failure.
- ECIES: round‑trip; context/AAD mismatch should fail.

Run all tests:
```bash
pytest -q
```



## 🗺️ Roadmap (stretch ideas)
- Compressed point parsing (requires Tonelli‑Shanks square root mod p).
- Regularized scalar multiplication (Montgomery ladder style) + timing harness.
- Pre‑computation/batching for performance demonstrations.
- Simple CLI (`ecies encrypt/decrypt`) with file I/O and hex keys.
- Formal write‑up (KEM‑DEM IND‑CCA sketch in the ROM).



## 📚 References
- NIST FIPS 186‑5 (Digital Signature Standard) for P‑256 parameters.
- RFC 5869 (HKDF).
- ChaCha20‑Poly1305 (RFC 8439).
- KEM–DEM composition folklore and modern proofs (e.g., Bellare, Boldyreva, Staddon).
