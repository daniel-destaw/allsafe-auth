from ldap3 import Server, Connection, ALL, NTLM
from typing import Optional, List, Dict


class LDAPResolver:
    def __init__(self, server_ip: str, domain: str, search_base: str, use_ssl: bool = False, port: int = None):
        self.server_ip = server_ip
        self.domain = domain
        self.search_base = search_base
        self.use_ssl = use_ssl
        self.port = port or (636 if use_ssl else 389)

        self.server = Server(self.server_ip, port=self.port, use_ssl=self.use_ssl, get_info=ALL)

    def get_user(self, username: str, password: str) -> Optional[Dict]:
        """Try to bind as the given user and return their attributes."""
        user_dn = f"{self.domain}\\{username}"
        try:
            with Connection(self.server, user=user_dn, password=password, authentication=NTLM) as conn:
                if not conn.bind():
                    return None

                # Search for the user
                conn.search(
                    search_base=self.search_base,
                    search_filter=f'(sAMAccountName={username})',
                    attributes=['*']
                )
                if len(conn.entries) == 0:
                    return None

                return conn.entries[0].entry_attributes_as_dict
        except Exception as e:
            print(f"[LDAP Resolver] Error fetching user: {e}")
            return None

    def list_users(self, admin_username: str, admin_password: str) -> List[Dict]:
        """List all users in AD using an admin account."""
        admin_dn = f"{self.domain}\\{admin_username}"
        users = []

        try:
            with Connection(self.server, user=admin_dn, password=admin_password, authentication=NTLM) as conn:
                if not conn.bind():
                    raise PermissionError("Failed to bind as admin for listing users")

                conn.search(
                    search_base=self.search_base,
                    search_filter='(&(objectClass=user)(objectCategory=person))',
                    attributes=['sAMAccountName', 'displayName', 'mail', 'memberOf']
                )

                for entry in conn.entries:
                    users.append(entry.entry_attributes_as_dict)
        except Exception as e:
            print(f"[LDAP Resolver] Error listing users: {e}")

        return users