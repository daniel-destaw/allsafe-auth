

from typing import List, Dict, Optional
from allsafe_auth.user_management.resolvers.ldap_resolver import LDAPResolver
class ActiveDirectoryAuthenticator:
    def __init__(
        self,
        server_ip: str,
        domain: str,
        search_base: str,
        use_ssl: bool = False,
        port: int = None
    ):
        self.ldap_resolver = LDAPResolver(
            server_ip=server_ip,
            domain=domain,
            search_base=search_base,
            use_ssl=use_ssl,
            port=port
        )

    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """
        Authenticate a user against Active Directory.
        Returns user info dict if successful, None otherwise.
        """
        user_info = self.ldap_resolver.get_user(username, password)
        if user_info:
            return user_info
        return None

    def list_users(self, admin_username: str, admin_password: str) -> List[Dict]:
        """
        List all users in AD using admin credentials.
        """
        return self.ldap_resolver.list_users(admin_username, admin_password)