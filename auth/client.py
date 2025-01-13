from typing import Any
from auth0.management import Auth0
from auth0.authentication import GetToken
from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier


class AuthClient:
    def __init__(self):
        self.domain = None
        self.client_id = None
        self.client_secret = None
        self.jwks_url = None
        self.mgmt_api_url = None


    def connect(
            self,
            domain: str,
            client_id: str,
            client_secret: str,
            jwks_url : str = None,
            mgmt_api_url: str = None
    ) -> None:
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret

        # set jwks_url and mgmt_api_url if provided
        self.jwks_url = jwks_url or f"https://{self.domain}/.well-known/jwks.json"
        self.mgmt_api_url = mgmt_api_url or f"https://{self.domain}/api/v2/"

        # get mgmt token and login to auth0
        get_token = GetToken(
            domain=self.domain,
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        get_mgmt_api_token = get_token.client_credentials(
            self.mgmt_api_url
        )
        mgmt_api_token = get_mgmt_api_token.get("access_token")

        # init auth0 client and connect to Management API
        self.auth0 = Auth0(domain, mgmt_api_token)

        # init token verifier
        self.sv = AsymmetricSignatureVerifier(self.jwks_url)
        self.tv = TokenVerifier(
            signature_verifier=self.sv,
            issuer=f"https://{self.domain}/",
            audience=self.client_id
        )
        

    def verify_token(self, token: str) -> dict[str, Any]:
        """
        Attempts to verify provided ID token, using Auth0's TokenVerifier class

        Args:
            token (str): JWT ID token to verify

        Returns:
            decoded payload from the token
        
        Raises:
            TokenValidationError: when the token cannot be decoded, the token signing algorithm is not the expected one,
            the token signature is invalid or the token has a claim missing or with unexpected value.
        """
        return self.tv.verify(token)

    
    def get_idp_user(self, idp_id: str) -> dict[str, Any]:
        return self.auth0.users.get(idp_id)


auth_cl = AuthClient()
