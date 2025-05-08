# allsafe_auth/authentication/totp.py

import hmac
import hashlib
import time
import struct
import binascii  # Still needed for the binascii.Error

class TOTP:
    """Generates Time-based One-Time Passwords (TOTP) without importing base64."""

    _b32_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    _b32_map = {v: k for k, v in enumerate(_b32_alphabet)}

    def __init__(self, secret, step=30, digits=6, digest=hashlib.sha1):
        """
        Initializes the TOTP generator with the secret key and parameters.

        Args:
            secret (str): The shared secret key (Base32 encoded).
            step (int): The time step in seconds (default: 30).
            digits (int): The number of digits in the OTP (default: 6).
            digest: The hash function to use (default: hashlib.sha1).
        """
        try:
            self.key = self._base32_decode(secret.upper())
        except binascii.Error:
            raise ValueError("Invalid Base32 secret")
        self.step = step
        self.digits = digits
        self.digest = digest

    def _base32_decode(self, s):
        """Decodes a Base32 encoded string to bytes."""
        s = s.rstrip('=')
        padding = 8 - (len(s) % 8) if len(s) % 8 != 0 else 0
        s += '=' * padding
        result = bytearray()
        for i in range(0, len(s), 8):
            chunk = s[i:i + 8]
            if '=' in chunk:
                chunk = chunk[:chunk.index('=')]
            value = 0
            for char in chunk:
                value = (value << 5) | self._b32_map.get(char, 0)
            bit_count = len(chunk) * 5
            for j in range(bit_count // 8):
                result.append((value >> (bit_count - (j + 1) * 8)) & 0xFF)
        return bytes(result)

    def generate(self):
        """Generates the TOTP for the current time."""
        current_time = int(time.time())
        counter = struct.pack('>Q', current_time // self.step)

        hmac_digest = hmac.new(self.key, counter, self.digest).digest()
        offset = hmac_digest[-1] & 0x0F
        truncated_hash = hmac_digest[offset:offset + 4]

        value = struct.unpack('>I', truncated_hash)[0] & 0x7FFFFFFF
        otp = value % (10 ** self.digits)
        return str(otp).zfill(self.digits)