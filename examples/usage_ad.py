from allsafe_auth.authentication.active_directory import ActiveDirectoryAuthenticator

# Configuration
AD_SERVER_IP = "10.195.130.34"
AD_DOMAIN = "allsafe.com.et"
AD_SEARCH_BASE = "DC=allsafe,DC=com,DC=et"

ADMIN_USER = "Administrator"
ADMIN_PASS = "Wour152809@@"

# Initialize Authenticator
ad_auth = ActiveDirectoryAuthenticator(
    server_ip=AD_SERVER_IP,
    domain=AD_DOMAIN,
    search_base=AD_SEARCH_BASE,
    use_ssl=False  # Change to True if using LDAPS
)

# Test Authentication
username = input("Enter username: ")
password = input("Enter password: ")

user_data = ad_auth.authenticate(username, password)
if user_data:
    print("✅ Login successful!")
    print("User Info:", user_data)
else:
    print("❌ Authentication failed.")

# Test List Users (requires admin credentials)
users = ad_auth.list_users(ADMIN_USER, ADMIN_PASS)
print(f"\n📄 Found {len(users)} users:")
for user in users:
    print(f" - {user['sAMAccountName'][0]}")