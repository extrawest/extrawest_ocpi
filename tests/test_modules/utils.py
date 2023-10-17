from uuid import uuid4

from py_ocpi.core.authentication.authenticator import Authenticator

AUTH_TOKEN = str(uuid4())
RANDOM_AUTH_TOKEN = str(uuid4())


class ClientAuthenticator(Authenticator):
    @classmethod
    async def get_valid_token_c(cls):
        """Return a list of valid tokens."""
        return [AUTH_TOKEN]
