import qrcode
from io import BytesIO
import base64

class QRCodeGenerator:
    """Generates QR codes as data URLs or saves them as PNG files."""

    @staticmethod
    def generate_uri(issuer_name: str, account_name: str, secret_key: str, type='totp', counter=1) -> str:
        """
        Helper function to generate the Google Authenticator URI.

        Args:
            issuer_name (str): The issuer's name (e.g., 'allsafe').
            account_name (str): The account name (e.g., 'user@example.com').
            secret_key (str): The shared secret key (Base32 encoded).
            type (str): Type of OTP ('totp' or 'hotp'). Defaults to 'totp'.
            counter (int): The counter for HOTP. Defaults to 1.

        Returns:
            str: The generated URI for Google Authenticator.
        """
        if type == 'totp':
            return f"otpauth://totp/{issuer_name}:{account_name}?secret={secret_key}&issuer={issuer_name}"
        elif type == 'hotp':
            return f"otpauth://hotp/{issuer_name}:{account_name}?secret={secret_key}&counter={counter}&issuer={issuer_name}"
        else:
            raise ValueError("Invalid OTP type. Use 'totp' or 'hotp'.")

    @staticmethod
    def save_to_file(uri: str, filename: str, error_correction='L', box_size=10, border=4):
        """
        Saves the QR code as a PNG file.

        Args:
            uri (str): The data to encode in the QR code.
            filename (str): The filename to save the QR code as.
            error_correction (str): Error correction level ('L', 'M', 'Q', 'H').
            box_size (int): Size of each box (pixel) in the QR code.
            border (int): Width of the border around the QR code (boxes).
        """
        # Generate QR code from URI
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L if error_correction == 'L' else
                             qrcode.constants.ERROR_CORRECT_M if error_correction == 'M' else
                             qrcode.constants.ERROR_CORRECT_Q if error_correction == 'Q' else
                             qrcode.constants.ERROR_CORRECT_H,
            box_size=box_size,
            border=border,
        )
        qr.add_data(uri)
        qr.make(fit=True)

        # Create the image and save to the specified file
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        print(f"QR code saved as {filename}")
