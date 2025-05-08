import unittest
from unittest.mock import MagicMock, patch
from allsafe_auth.authentication.active_directory import ActiveDirectoryAuthenticator


class TestActiveDirectoryAuthenticator(unittest.TestCase):

    @patch('ldap.initialize')
    def test_authenticate_successful(self, mock_ldap_initialize):
        # Mock the LDAP connection
        mock_conn = MagicMock()
        mock_ldap_initialize.return_value = mock_conn
        
        # Simulate a successful bind
        mock_conn.simple_bind_s.return_value = None
        
        # Set up the authenticator
        authenticator = ActiveDirectoryAuthenticator(
            server_uri="ldap://WB-MSDC-004.wegagenbanksc.local",
            base_dn="dc=wegagenbanksc,dc=local",
            domain_name="wegagenbanksc.local"
        )

        # Test successful authentication
        result = authenticator.authenticate("jdoe", "correct_password")
        self.assertTrue(result)
        mock_conn.simple_bind_s.assert_called_once_with('CN=Samrawit Getu Birbo,OU=Users,OU=Infrastructure Management Services,OU=VP IT,OU=Head Office,OU=City,OU=Wegagen Bank,DC=wegagenbanksc,DC=local', 'correct_password')

    @patch('ldap.initialize')
    def test_authenticate_invalid_credentials(self, mock_ldap_initialize):
        # Mock the LDAP connection
        mock_conn = MagicMock()
        mock_ldap_initialize.return_value = mock_conn
        
        # Simulate invalid credentials error
        mock_conn.simple_bind_s.side_effect = Exception('Invalid credentials')
        
        # Set up the authenticator
        authenticator = ActiveDirectoryAuthenticator(
            server_uri="ldap://example.com",
            base_dn="DC=example,DC=com",
            domain_name="EXAMPLE"
        )

        # Test invalid credentials
        result = authenticator.authenticate("jdoe", "wrong_password")
        self.assertFalse(result)
        mock_conn.simple_bind_s.assert_called_once_with('EXAMPLE\\jdoe', 'wrong_password')

    @patch('ldap.initialize')
    def test_authenticate_server_down(self, mock_ldap_initialize):
        # Mock the LDAP connection
        mock_conn = MagicMock()
        mock_ldap_initialize.return_value = mock_conn
        
        # Simulate server down error
        mock_conn.simple_bind_s.side_effect = Exception('LDAP server is down')
        
        # Set up the authenticator
        authenticator = ActiveDirectoryAuthenticator(
            server_uri="ldap://example.com",
            base_dn="DC=example,DC=com",
            domain_name="EXAMPLE"
        )

        # Test LDAP server down
        result = authenticator.authenticate("jdoe", "password")
        self.assertFalse(result)
        mock_conn.simple_bind_s.assert_called_once_with('EXAMPLE\\jdoe', 'password')

    @patch('ldap.initialize')
    def test_search_user_found(self, mock_ldap_initialize):
        # Mock the LDAP connection
        mock_conn = MagicMock()
        mock_ldap_initialize.return_value = mock_conn
        
        # Simulate a successful user search result
        mock_conn.search_s.return_value = [('dn', {'sAMAccountName': ['jdoe']})]
        
        # Set up the authenticator
        authenticator = ActiveDirectoryAuthenticator(
            server_uri="ldap://example.com",
            base_dn="DC=example,DC=com",
            domain_name="EXAMPLE"
        )

        # Test searching for a user
        result = authenticator.search_user("jdoe")
        self.assertIsNotNone(result)
        self.assertEqual(result, [('dn', {'sAMAccountName': ['jdoe']})])
        mock_conn.search_s.assert_called_once_with('DC=example,DC=com', 2, '(sAMAccountName=jdoe)')

    @patch('ldap.initialize')
    def test_search_user_not_found(self, mock_ldap_initialize):
        # Mock the LDAP connection
        mock_conn = MagicMock()
        mock_ldap_initialize.return_value = mock_conn
        
        # Simulate no results found
        mock_conn.search_s.return_value = []
        
        # Set up the authenticator
        authenticator = ActiveDirectoryAuthenticator(
            server_uri="ldap://example.com",
            base_dn="DC=example,DC=com",
            domain_name="EXAMPLE"
        )

        # Test searching for a non-existing user
        result = authenticator.search_user("nonexistent_user")
        self.assertIsNone(result)
        mock_conn.search_s.assert_called_once_with('DC=example,DC=com', 2, '(sAMAccountName=nonexistent_user)')

    @patch('ldap.initialize')
    def test_search_user_ldap_error(self, mock_ldap_initialize):
        # Mock the LDAP connection
        mock_conn = MagicMock()
        mock_ldap_initialize.return_value = mock_conn
        
        # Simulate an LDAP error during search
        mock_conn.search_s.side_effect = Exception('LDAP search error')
        
        # Set up the authenticator
        authenticator = ActiveDirectoryAuthenticator(
            server_uri="ldap://example.com",
            base_dn="DC=example,DC=com",
            domain_name="EXAMPLE"
        )

        # Test search with an error
        result = authenticator.search_user("jdoe")
        self.assertIsNone(result)
        mock_conn.search_s.assert_called_once_with('DC=example,DC=com', 2, '(sAMAccountName=jdoe)')

if __name__ == '__main__':
    unittest.main()
