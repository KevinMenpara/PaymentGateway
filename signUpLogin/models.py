from django.db import models
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from django.conf import settings
import base64
import os

class User(models.Model):
    # transaction_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.TextField()  # Store encrypted password
    dob = models.DateField()
    expiry = models.DateField()
    ammount = models.PositiveIntegerField()  # Ensure it's a positive integer
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True ,auto_now=True)

    key = base64.b64decode(settings.ENCRYPTION_KEY)  # Ensure this key is 32 bytes long

    def set_password(self, raw_password):
        cipher = Cipher(algorithms.AES(self.key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        # Ensure password length is a multiple of 16 bytes (block size)
        padded_password = self._pad(raw_password.encode())
        encrypted_password = encryptor.update(padded_password) + encryptor.finalize()
        self.password = base64.b64encode(encrypted_password).decode()

    def check_password(self, raw_password):
        cipher = Cipher(algorithms.AES(self.key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        encrypted_password = base64.b64decode(self.password)
        padded_password = decryptor.update(encrypted_password) + decryptor.finalize()
        return self._unpad(padded_password).decode() == raw_password

    def _pad(self, data):
        """Pad the data to be a multiple of 16 bytes."""
        padding_length = 16 - (len(data) % 16)
        return data + bytes([padding_length] * padding_length)

    def _unpad(self, data):
        """Remove padding from the data."""
        padding_length = data[-1]
        return data[:-padding_length]
