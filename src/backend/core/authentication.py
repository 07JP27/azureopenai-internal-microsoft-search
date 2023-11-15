# Refactored from https://github.com/Azure-Samples/ms-identity-python-on-behalf-of

import logging
import os
from tempfile import TemporaryDirectory
from typing import Any, Optional

from msal import ConfidentialClientApplication
from msal_extensions import (
    FilePersistence,
    PersistedTokenCache,
    build_encrypted_persistence,
)


# AuthError is raised when the authentication token sent by the client UI cannot be parsed or there is an authentication error accessing the graph API
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


class AuthenticationHelper:
    scope: str = "https://graph.microsoft.com/.default"

    def __init__(
        self,
        use_authentication: bool,
        server_app_id: Optional[str],
        server_app_secret: Optional[str],
        client_app_id: Optional[str],
        tenant_id: Optional[str],
        token_cache_path: Optional[str] = None,
    ):
        self.use_authentication = use_authentication
        self.server_app_id = server_app_id
        self.server_app_secret = server_app_secret
        self.client_app_id = client_app_id
        self.tenant_id = tenant_id
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"

        if self.use_authentication:
            self.token_cache_path = token_cache_path
            if not self.token_cache_path:
                self.temporary_directory = TemporaryDirectory()
                self.token_cache_path = os.path.join(self.temporary_directory.name, "token_cache.bin")
            try:
                persistence = build_encrypted_persistence(location=self.token_cache_path)
            except Exception:
                logging.exception("Encryption unavailable. Opting in to plain text.")
                persistence = FilePersistence(location=self.token_cache_path)
            self.confidential_client = ConfidentialClientApplication(
                server_app_id,
                authority=self.authority,
                client_credential=server_app_secret,
                token_cache=PersistedTokenCache(persistence),
            )

    def get_auth_setup_for_client(self) -> dict[str, Any]:
        # returns MSAL.js settings used by the client app
        return {
            "useLogin": self.use_authentication,  # Whether or not login elements are enabled on the UI
            "msalConfig": {
                "auth": {
                    "clientId": self.client_app_id,  # Client app id used for login
                    "authority": self.authority,  # Directory to use for login https://learn.microsoft.com/azure/active-directory/develop/msal-client-application-configuration#authority
                    "redirectUri": "/redirect",  # Points to window.location.origin. You must register this URI on Azure Portal/App Registration.
                    "postLogoutRedirectUri": "/",  # Indicates the page to navigate after logout.
                    "navigateToLoginRequestUrl": False,  # If "true", will navigate back to the original request location before processing the auth code response.
                },
                "cache": {
                    "cacheLocation": "sessionStorage",
                    "storeAuthStateInCookie": False,
                },  # Configures cache location. "sessionStorage" is more secure, but "localStorage" gives you SSO between tabs.  # Set this to "true" if you are having issues on IE11 or Edge
            },
            "loginRequest": {
                # Scopes you add here will be prompted for user consent during sign-in.
                # By default, MSAL.js will add OIDC scopes (openid, profile, email) to any login request.
                # For more information about OIDC scopes, visit:
                # https://docs.microsoft.com/azure/active-directory/develop/v2-permissions-and-consent#openid-connect-scopes
                "scopes": [".default"],
                # Uncomment the following line to cause a consent dialog to appear on every login
                # For more information, please visit https://learn.microsoft.com/azure/active-directory/develop/v2-oauth2-auth-code-flow#request-an-authorization-code
                # "prompt": "consent"
            },
            "tokenRequest": {
                "scopes": [f"api://{self.server_app_id}/access_as_user"],
            },
        }

    @staticmethod
    def get_token_auth_header(headers: dict) -> str:
        # Obtains the Access Token from the Authorization Header
        auth = headers.get("Authorization", None)
        if not auth:
            raise AuthError(
                {"code": "authorization_header_missing", "description": "Authorization header is expected"}, 401
            )

        parts = auth.split()

        if parts[0].lower() != "bearer":
            raise AuthError(
                {"code": "invalid_header", "description": "Authorization header must start with Bearer"}, 401
            )
        elif len(parts) == 1:
            raise AuthError({"code": "invalid_header", "description": "Token not found"}, 401)
        elif len(parts) > 2:
            raise AuthError({"code": "invalid_header", "description": "Authorization header must be Bearer token"}, 401)

        token = parts[1]
        return token