from allsafe_auth.authentication.hotp import HOTP
from allsafe_auth.utils.qr_code_generator import QRCodeGenerator

if __name__ == "__main__":
    # Example secret key (in a real application, this would be unique per user)
    secret_key = "JBSWY3DPEHPK3PXP"
    account_name = "allsafe@example.com"
    issuer_name = "allsafe"
    qr_filename = "hotp_qr_code.png"  # Name of the PNG file to save

    # Generate HOTP (Counter starts at 1)
    hotp = HOTP(secret_key)
    current_hotp = hotp.generate(counter=1)  # Increment the counter as needed
    print(f"Current HOTP: {current_hotp}")

    # Generate the URI for HOTP QR Code
    uri = QRCodeGenerator.generate_uri(issuer_name, account_name, secret_key)

    # Save the QR code as a PNG file
    QRCodeGenerator.save_to_file(uri, qr_filename)
    print(f"QR code saved as {qr_filename}")
