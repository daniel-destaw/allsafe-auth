# examples/verify_totp_and_ad.py

from allsafe_auth.authentication.active_directory import ActiveDirectoryAuthenticator
from allsafe_auth.authentication.totp import TOTP

# --- Configuration ---
AD_SERVER_IP = "10.195.130.34"
AD_DOMAIN = "allsafe.com.et"
AD_SEARCH_BASE = "DC=allsafe,DC=com,DC=et"

# This should be the same secret used in the TOTP QR code or mobile app
TOTP_SECRET_KEY = "JBSWY3DPEHPK3PXP"


def main():
    # Initialize AD Authenticator
    ad_auth = ActiveDirectoryAuthenticator(
        server_ip=AD_SERVER_IP,
        domain=AD_DOMAIN,
        search_base=AD_SEARCH_BASE
    )

    # Prompt for credentials
    username = input("Enter username: ")
    password = input("Enter password: ")
    totp_code = input("Enter TOTP from your authenticator app: ")

    print("\n[Step 1] Authenticating with Active Directory...")
    user_info = ad_auth.authenticate(username, password)

    if not user_info:
        print("❌ Authentication failed: Invalid username or password.")
        return

    print(f"✅ Successfully authenticated as '{username}' via Active Directory.")

    print("\n[Step 2] Verifying TOTP...")
    totp_verifier = TOTP(TOTP_SECRET_KEY)
    expected_otp = totp_verifier.generate()

    if totp_code == expected_otp:
        print("✅ TOTP verification successful!")
        print("🔓 Full access granted.")
    else:
        print("❌ TOTP verification failed.")
        print("🔐 Access denied.")


if __name__ == "__main__":
    main()