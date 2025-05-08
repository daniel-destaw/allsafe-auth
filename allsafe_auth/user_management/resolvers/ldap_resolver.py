import ldap
from ldap.filter import escape_filter_chars

class LDAPResolver:
    def __init__(self, ldap_server, base_dn, user_dn, password):
        self.ldap_server = ldap_server
        self.base_dn = base_dn
        self.user_dn = user_dn
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = ldap.initialize(self.ldap_server)
            self.connection.simple_bind_s(self.user_dn, self.password)
        except ldap.LDAPError as e:
            raise ConnectionError(f"Failed to connect to LDAP server: {e}")

    def search_user(self, username):
        if not self.connection:
            raise ConnectionError("Not connected to LDAP server.")

        search_filter = f"(uid={escape_filter_chars(username)})"
        try:
            result = self.connection.search_s(self.base_dn, ldap.SCOPE_SUBTREE, search_filter)
            return result if result else None
        except ldap.LDAPError as e:
            raise RuntimeError(f"Failed to search user: {e}")

    def authenticate_user(self, username, password):
        user_data = self.search_user(username)
        if not user_data:
            return False

        user_dn = user_data[0][0]
        try:
            temp_connection = ldap.initialize(self.ldap_server)
            temp_connection.simple_bind_s(user_dn, password)
            return True
        except ldap.INVALID_CREDENTIALS:
            return False
        except ldap.LDAPError as e:
            raise RuntimeError(f"Failed to authenticate user: {e}")
        finally:
            temp_connection.unbind_s()

    def disconnect(self):
        if self.connection:
            self.connection.unbind_s()
            self.connection = None