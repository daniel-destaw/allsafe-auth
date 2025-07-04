from allsafe_auth.authentication.totp import TOTP
from allsafe_auth.utils.qr_code_generator import QRCodeGenerator

if __name__ == "__main__":
    secret_key = "JBSWY3DPEHPK3PXP"
    account_name = "allsafe@example.com"
    issuer_name = "allsafe"
    qr_filename = "totp_qr_code.png"

    totp = TOTP(secret_key)
    print(f"Current TOTP: {totp.generate()}")

    uri = QRCodeGenerator.generate_uri(issuer_name, account_name, secret_key)
    QRCodeGenerator.save_to_file(uri, qr_filename)

    