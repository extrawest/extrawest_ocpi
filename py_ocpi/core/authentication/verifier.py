from fastapi import Header, Depends

from py_ocpi.core.authentication.authenticator import Authenticator
from py_ocpi.core.dependencies import get_authenticator
from py_ocpi.core.exceptions import AuthorizationOCPIError
from py_ocpi.core.utils import decode_string_base64
from py_ocpi.modules.versions.enums import VersionNumber


class AuthorizationVerifier:
    """
    A class responsible for verifying authorization tokens
    based on the specified version number.

    :param version (VersionNumber): OCPI version used.
    """

    def __init__(self, version: VersionNumber) -> None:
        self.version = version

    async def __call__(
        self,
        authorization: str = Header(...),
        authenticator: Authenticator = Depends(get_authenticator),
    ):
        """
        Verifies the authorization token using the specified version
        and an Authenticator.

        :param authorization (str): The authorization header containing
          the token.
        :param authenticator (Authenticator): An Authenticator instance used
          for authentication.

        :raises AuthorizationOCPIError: If there is an issue with
          the authorization token.
        """
        try:
            token = authorization.split()[1]
            if self.version.startswith("2.2"):
                token = decode_string_base64(token)
            await authenticator.authenticate(token)
        except IndexError:
            raise AuthorizationOCPIError
