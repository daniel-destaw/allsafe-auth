import unittest
from unittest.mock import patch
import time
import base64
import struct
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from allsafe_auth.authentication.totp import TOTP  # Import the TOTP class
from allsafe_auth.utils.qr_code_generator import generate_qr_code # Import the module

class TestTOTP(unittest.TestCase):
    """
    Unit tests for the TOTP class.
    """
    def setUp(self):
        """
        Set up the test environment.  This is run before each test method.
        """
        self.secret = "JBSWY3DPEHPK3PXP"  #  Fixed secret for testing
        self.account_name = "testuser@example.com"
        self.issuer = "TestApp"
        self.totp = TOTP(self.secret, self.account_name, self.issuer)
        # Patch time.time() to return a fixed value for predictable OTPs
        self.fixed_time = 1678886400  # Example fixed timestamp

    def test_generate_otp(self):
        """
        Test the generate_otp method.
        """
        with patch('time.time', return_value=self.fixed_time):
            otp = self.totp.generate_otp()
            self.assertEqual(otp, 123456)  # Expected OTP for the fixed time and secret.  You'll need to calculate this.

        with patch('time.time', return_value=self.fixed_time + 30):
            otp = self.totp.generate_otp()
            self.assertEqual(otp, 654321) # another expected OTP

    def test_generate_provisioning_uri(self):
        """
        Test the generate_provisioning_uri method.
        """
        uri = self.totp.generate_provisioning_uri()
        expected_uri = f"otpauth://totp/{self.issuer}:{self.account_name}?secret={self.secret}&issuer={self.issuer}"
        self.assertEqual(uri, expected_uri)

    @patch('allsafe_auth.utils.qr_code_generator.generate_qr_code')  # Corrected path
    def test_generate_qr_code(self, mock_generate_qr_code):
        """
        Test the generate_qr_code method.  We only need to check if it's called.
        """
        self.totp.generate_qr_code()
        mock_generate_qr_code.assert_called_once_with(self.totp.generate_provisioning_uri())

    def test_get_time_step(self):
        """
        Test the _get_time_step method
        """
        with patch('time.time', return_value=self.fixed_time):
            time_step = self.totp._get_time_step()
            self.assertEqual(time_step, int(self.fixed_time / 30))

    def test_hmac_generation(self):
        """
        Test the _generate_hmac method.
        """
        with patch('time.time', return_value=self.fixed_time):
            time_step = self.totp._get_time_step()
            msg = struct.pack(">Q", time_step)
            hmac_result = self.totp._generate_hmac(msg)
            self.assertEqual(len(hmac_result), 20)  # SHA1 HMAC result is 20 bytes

    def test_otp_extraction(self):
        """
        Test the _extract_otp_from_hmac method.
        """
        # Example HMAC result (replace with a *real* one for your test case)
        example_hmac_result = b'\x1f\x2e\x3d\x4c\x5b\x6a\x79\x88\x97\xa6\xb5\xc4\xd3\e2\xf1\x00\x11\x22\x33\x44'
        otp = self.totp._extract_otp_from_hmac(example_hmac_result)
        self.assertEqual(type(otp), int) # Check that the result is an integer.

if __name__ == '__main__':
    unittest.main()
