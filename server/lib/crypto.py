from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

def encrypt_string_aes_256(plain_text, password):
    # Generate a random salt
    salt = os.urandom(16)

    # Derive a key from the password and salt using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    # Generate a random initialization vector (IV)
    iv = os.urandom(16)

    # Create an AES cipher object with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Apply padding to the plaintext
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()

    # Encrypt the padded data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Concatenate the salt and IV with the encrypted data
    encrypted_message = salt + iv + encrypted_data

    return encrypted_message

# Usage: encrypted = encrypt_string_aes_256("plain_text", "password")
#encrypted = encrypt_string_aes_256("Hello, world!", "my_password")
#print(encrypted)

def decrypt_aes_256_cbc(encrypted_message, password):
    # Extract the salt, IV, and encrypted data from the encrypted message
    salt = encrypted_message[:16]
    iv = encrypted_message[16:32]
    encrypted_data = encrypted_message[32:]

    # Derive the key from the password and salt using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    # Create an AES cipher object with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the encrypted data
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove the padding from the decrypted data
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data.decode()

# Usage: decrypted = decrypt_aes_256_cbc(encrypted_message, "password")
#encrypted_message = b'\x8a\x8a\xb9\x9a\xc8s \xfc\xe6\xca~\xea5\xed\x90\xee\xef\xcb7\x9f\x85\xac\xa9\xd5\xa8c&\xbf\x0b\x0eBt\x18Q\xe3\xd7\xd5e\x1f.\xa6X\x16\xe5\xaa\x04\xdd!\xda'
#password = "my_password"
#decrypted = decrypt_aes_256_cbc(encrypted_message, password)
#print(decrypted)