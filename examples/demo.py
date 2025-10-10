from ecies.ecies import keygen, encrypt, decrypt

def main():
    alice_sk, alice_pk = keygen()
    bob_sk, bob_pk = keygen()
    print("Bob pubkey.x:", hex(bob_pk[0])[:20], "...")
    msg = b"hello, ECIES world!"
    aad = b"demo-aad"
    bundle = encrypt(bob_pk, msg, aad=aad, ctx_info=b"Alice->Bob demo")
    print("Ciphertext len:", len(bundle["ciphertext"]))
    pt = decrypt(bob_sk, bundle, aad=aad, ctx_info=b"Alice->Bob demo")
    print("Decrypted:", pt)

if __name__ == "__main__":
    main()
