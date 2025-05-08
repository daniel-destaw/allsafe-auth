from allsafe_auth.user_management.resolvers.ldap_resolver import LDAPResolver

def list_users():
    # Configuration for the LDAP server
    ldap_server = "ldap://WB-MSDC-004.wegagenbanksc.local"
    base_dn = "dc=wegagenbanksc,dc=local"
    user_dn = "CN=Samrawit Getu Birbo,OU=Users,OU=Infrastructure Management Services,OU=VP IT,OU=Head Office,OU=City,OU=Wegagen Bank,DC=wegagenbanksc,DC=local"
    password = "your_admin_password"

    # Initialize the LDAPResolver
    resolver = LDAPResolver(ldap_server, base_dn, user_dn, password)

    try:
        # Connect to the LDAP server
        resolver.connect()
        print("Connected to LDAP server successfully.")

        # Search for all users
        search_filter = "(objectClass=person)"  # Adjust the filter as needed
        users = resolver.search(base_dn, search_filter)

        # Print the list of users
        if users:
            print("Users found:")
            for dn, attributes in users:
                print(f"DN: {dn}, Attributes: {attributes}")
        else:
            print("No users found.")

    except ConnectionError as ce:
        print(f"Connection error: {ce}")
    except RuntimeError as re:
        print(f"Runtime error: {re}")
    finally:
        # Disconnect from the LDAP server
        resolver.disconnect()
        print("Disconnected from LDAP server.")

if __name__ == "__main__":
    list_users()