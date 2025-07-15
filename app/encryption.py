from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

class EncryptionService:
    def __init__(self, password: str):
        backend = default_backend()
        salt = b"uber-pl-salt-2024"  # In prod, random per user
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=backend
        )
        self.key = kdf.derive(password.encode())

    def encrypt(self, plaintext: str) -> str:
        if not plaintext:
            return ""
        aesgcm = AESGCM(self.key)
        nonce = os.urandom(12)
        data = aesgcm.encrypt(nonce, plaintext.encode(), None)
        return urlsafe_b64encode(nonce + data).decode()

    def decrypt(self, ciphertext: str) -> str:
        if not ciphertext:
            return ""
        data = urlsafe_b64decode(ciphertext)
        aesgcm = AESGCM(self.key)
        nonce, ct = data[:12], data[12:]
        return aesgcm.decrypt(nonce, ct, None).decode()

    # Add encrypt/decrypt_float for decimals