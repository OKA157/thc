from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    return private_key, public_key

def encrypt(public_key, plaintext):
    ciphertext = pow(plaintext, public_key.public_numbers().e, public_key.public_numbers().n)
    return ciphertext

def decrypt(private_key, ciphertext):
    plaintext = pow(ciphertext, private_key.private_numbers().d, private_key.private_numbers().public_numbers.n)
    return plaintext

def test(iter):
    private_key, public_key = generate_key_pair()

    num1 = 7
    num2 = 11

    ciphertext_num1 = encrypt(public_key, num1)
    ciphertext_num2 = encrypt(public_key, num2)

    num_operations = iter
    for i in range(num_operations):
        result_ciphertext = (ciphertext_num1 * ciphertext_num2) % public_key.public_numbers().n

        decrypted_result = decrypt(private_key, result_ciphertext)
        op1 = decrypted_result = decrypt(private_key, ciphertext_num1)
        op2 = decrypted_result = decrypt(private_key, ciphertext_num2)
        print(f"Iteration {i+1}: \nOperation: {op1} X {op2} \nEncrypted Product: {result_ciphertext},\nDecrypted Product: {decrypted_result}\n")

        ciphertext_num1 = result_ciphertext

def multiplication():
    private_key, public_key = generate_key_pair()

    num1 = 7
    num2 = 11

    ciphertext_num1 = encrypt(public_key, num1)
    ciphertext_num2 = encrypt(public_key, num2)

    result_ciphertext = (ciphertext_num1 * ciphertext_num2) % public_key.public_numbers().n

    decrypted_result = decrypt(private_key, result_ciphertext)

    print(f"Original Numbers: {num1}, {num2}")
    print(f"\nEncrypted Numbers: {ciphertext_num1}, {ciphertext_num2}")
    print(f"\nEncrypted Product: {result_ciphertext}")
    print(f"\nDecrypted Product: {decrypted_result}")

def addition():
    private_key, public_key = generate_key_pair()

    num1 = 7
    num2 = 11

    ciphertext_num1 = encrypt(public_key, num1)
    ciphertext_num2 = encrypt(public_key, num2)

    result_ciphertext = (ciphertext_num1 * ciphertext_num2) % public_key.public_numbers().n

    decrypted_result = decrypt(private_key, result_ciphertext)

    print(f"Original Numbers: {num1}, {num2}")
    print(f"\nEncrypted Numbers: {ciphertext_num1}, {ciphertext_num2}")
    print(f"\nEncrypted Product: {result_ciphertext}")
    print(f"\nDecrypted Product: {decrypted_result}")

if __name__ == "__main__":
    test(7)
