from allsafe_auth.authentication.hotp import HOTP
from allsafe_auth.utils.qr_code_generator import QRCodeGenerator

if __name__ == "__main__":
    # Example secret key (in a real application, this would be unique per user)
    secret_key = "JBSWY3DPEHPK3PXP"
    account_name = "allsafe@example.com"
    issuer_name = "allsafe"
    qr_filename = "hotp_qr_code.png"  # Name of the PNG file to save

    # Initialize the HOTP generator
    try:
        hotp_generator = HOTP(secret_key)
        current_hotp = hotp_generator.generate(counter=1)  # Counter starts from 1, can be incremented
        print(f"Current HOTP: {current_hotp}")
    except ValueError as e:
        print(f"Error initializing HOTP: {e}")
        exit()

    # Generate the URI for Google Authenticator using the secret key for HOTP
    try:
        uri = QRCodeGenerator.generate_uri(issuer_name, account_name, secret_key, type='hotp', counter=1)
        
        # Use QRCodeGenerator to save the QR code as a PNG file
        QRCodeGenerator.save_to_file(uri, qr_filename)
        print(f"QR code for HOTP saved as {qr_filename}")
    except Exception as e:
        print(f"Error generating or saving QR code: {e}")
