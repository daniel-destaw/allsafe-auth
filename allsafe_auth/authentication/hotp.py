import hmac
import hashlib
import struct

class HOTP:
    def __init__(self, secret: str):
        """
        Initializes the HOTP generator with a secret key.
        
        Args:
            secret (str): The shared secret key.
        """
        self.secret = secret.encode('utf-8')
    
    def generate(self, counter: int) -> str:
        """
        Generate a HOTP token using HMAC-SHA1.
        
        Args:
            counter (int): The counter value, which should be incremented with each request.
        
        Returns:
            str: A 6-digit OTP.
        """
        # Convert the counter to a byte representation
        counter_bytes = struct.pack(">Q", counter)
        
        # Generate HMAC-SHA1 hash
        hmac_hash = hmac.new(self.secret, counter_bytes, hashlib.sha1).digest()
        
        # Dynamic Truncation
        offset = hmac_hash[-1] & 0x0F
        otp = struct.unpack(">I", hmac_hash[offset:offset + 4])[0] & 0x7FFFFFFF  # Remove sign
        
        # Get a 6-digit OTP
        otp %= 1000000
        
        return str(otp).zfill(6)
