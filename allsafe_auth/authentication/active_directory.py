import ldap

class ActiveDirectoryAuthenticator:
    def __init__(self, server_uri, base_dn, domain_name):
        self.server_uri = server_uri
        self.base_dn = base_dn
        self.domain_name = domain_name

    def authenticate(self, username, password):
        conn = None
        try:
            # Connect to the LDAP server
            conn = ldap.initialize(self.server_uri)
            conn.set_option(ldap.OPT_REFERRALS, 0)

            # Bind using the provided credentials
            user_dn = f'{self.domain_name}\\{username}'  # Domain\Username format
            conn.simple_bind_s(user_dn, password)

            # Successful authentication
            print("Authentication successful.")
            return True

        except ldap.INVALID_CREDENTIALS:
            print("Authentication failed: Invalid credentials.")
            return False

        except ldap.SERVER_DOWN:
            print("Authentication failed: LDAP server is down or unreachable.")
            return False

        except ldap.LDAPError as e:
            print(f"LDAP error: {e}")
            return False

        except Exception as e:
            print(f"Unexpected error during authentication: {e}")
            return False

        finally:
            if conn:
                conn.unbind_s()

    def search_user(self, username):
        conn = None
        try:
            # Connect to the LDAP server
            conn = ldap.initialize(self.server_uri)
            conn.set_option(ldap.OPT_REFERRALS, 0)
            conn.simple_bind_s()

            # Search for the user in the base DN
            search_filter = f"(sAMAccountName={username})"
            result = conn.search_s(self.base_dn, ldap.SCOPE_SUBTREE, search_filter)

            if not result:
                print(f"User {username} not found.")
                return None

            return result

        except ldap.NO_SUCH_OBJECT:
            print(f"Search failed: Base DN not found ({self.base_dn}).")
            return None

        except ldap.LDAPError as e:
            print(f"LDAP search error: {e}")
            return None

        except Exception as e:
            print(f"Unexpected error during search: {e}")
            return None

        finally:
            if conn:
                conn.unbind_s()
