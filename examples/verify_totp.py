# examples/verify_totp_simple.py

from allsafe_auth.authentication.totp import TOTP
import time

if __name__ == "__main__":
    # The same secret key used to generate the QR code
    secret_key = "JBSWY3DPEHPK3PXP"

    # Initialize the TOTP verifier
    totp_verifier = TOTP(secret_key)

    # Generate the expected OTP for the current time
    expected_otp = totp_verifier.generate()
    #print(f"Expected OTP (current time): {expected_otp}")

    # Prompt the user to enter the OTP from their authenticator app
    user_otp = input("Enter the OTP from your authenticator app: ")

    # Verify if the user's OTP matches the expected OTP for the current time
    if user_otp == expected_otp:
        print("OTP verification successful!")
    else:
        print("OTP verification failed.")