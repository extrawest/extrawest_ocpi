from fastapi import Header, Depends, Query, Path, WebSocketException, status

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
                try:
                    token = decode_string_base64(token)
                except UnicodeDecodeError:
                    raise AuthorizationOCPIError
            await authenticator.authenticate(token)
        except IndexError:
            raise AuthorizationOCPIError


class CredentialsAuthorizationVerifier:
    """
    A class responsible for verifying authorization tokens
    based on the specified version number.

    :param version (VersionNumber): OCPI version used.
    """

    def __init__(self, version: VersionNumber | None) -> None:
        self.version = version

    async def __call__(
        self,
        authorization: str = Header(...),
        authenticator: Authenticator = Depends(get_authenticator),
    ) -> str | dict | None:
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
        except IndexError:
            raise AuthorizationOCPIError

        if self.version:
            if self.version.startswith("2.2"):
                try:
                    token = decode_string_base64(token)
                except UnicodeDecodeError:
                    raise AuthorizationOCPIError
        else:
            try:
                token = decode_string_base64(token)
            except UnicodeDecodeError:
                pass
        return await authenticator.authenticate_credentials(token)


class HttpPushVerifier:
    """
    A class responsible for verifying authorization tokens if using push.
    """

    async def __call__(
        self,
        authorization: str = Header(...),
        version: VersionNumber = Path(...),
        authenticator: Authenticator = Depends(get_authenticator),
    ):
        """
        Verifies the authorization token using the specified version
        and an Authenticator.

        :param authorization (str): The authorization header containing
          the token.
        :param version (VersionNumber): The authorization header containing
          the token.
        :param authenticator (Authenticator): An Authenticator instance used
          for authentication.

        :raises AuthorizationOCPIError: If there is an issue with
          the authorization token.
        """
        try:
            token = authorization.split()[1]
            if version.value.startswith("2.2"):
                try:
                    token = decode_string_base64(token)
                except UnicodeDecodeError:
                    raise AuthorizationOCPIError
            await authenticator.authenticate(token)
        except IndexError:
            raise AuthorizationOCPIError


class WSPushVerifier:
    """
    A class responsible for verifying authorization tokens if using ws push.
    """

    async def __call__(
        self,
        token: str = Query(...),
        version: VersionNumber = Path(...),
        authenticator: Authenticator = Depends(get_authenticator),
    ):
        """
        Verifies the authorization token using the specified version
        and an Authenticator.

        :param token (str): Token parameter in ws.
        :param version (str): The authorization header containing
          the token.
        :param authenticator (Authenticator): An Authenticator instance used
          for authentication.

        :raises AuthorizationOCPIError: If there is an issue with
          the authorization token.
        """
        try:
            if not token:
                raise AuthorizationOCPIError

            if version.value.startswith("2.2"):
                try:
                    token = decode_string_base64(token)
                except UnicodeDecodeError:
                    raise AuthorizationOCPIError
            await authenticator.authenticate(token)
        except AuthorizationOCPIError:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
