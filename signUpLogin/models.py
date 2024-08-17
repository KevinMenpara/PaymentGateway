from django.db import models
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from django.conf import settings
import base64

class User(models.Model):
    # Your existing fields...
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.TextField()  # Store encrypted password
    dob = models.DateField()
    expiry = models.DateField()
    ammount = models.PositiveIntegerField()  # Ensure it's a positive integer
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True, auto_now=True)

    key = base64.b64decode(settings.ENCRYPTION_KEY)  # Ensure this key is 32 bytes long

    def _get_cipher(self):
        return Cipher(algorithms.AES(self.key), modes.ECB(), backend=default_backend())

    def _pad(self, data):
        """Pad the data to be a multiple of 16 bytes."""
        padding_length = 16 - (len(data) % 16)
        return data + bytes([padding_length] * padding_length)

    def _unpad(self, data):
        """Remove padding from the data."""
        padding_length = data[-1]
        return data[:-padding_length]

    def encrypt(self, plaintext):
        cipher = self._get_cipher()
        encryptor = cipher.encryptor()
        padded_plaintext = self._pad(plaintext.encode())
        encrypted = encryptor.update(padded_plaintext) + encryptor.finalize()
        return base64.b64encode(encrypted).decode()

    def decrypt(self, ciphertext):
        cipher = self._get_cipher()
        decryptor = cipher.decryptor()
        encrypted = base64.b64decode(ciphertext)
        decrypted = decryptor.update(encrypted) + decryptor.finalize()
        return self._unpad(decrypted).decode()

    def set_password(self, raw_password):
        """Encrypt and set the user's password."""
        self.password = self.encrypt(raw_password)

    def check_password(self, raw_password):
        """Check the user's password."""
        return self.decrypt(self.password) == raw_password
