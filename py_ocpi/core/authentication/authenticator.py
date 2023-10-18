from abc import ABC, abstractmethod

from typing import List

from py_ocpi.core.exceptions import AuthorizationOCPIError


class Authenticator(ABC):
    """Base class responsible for verifying authorization tokens."""

    @classmethod
    async def authenticate(cls, auth_token: str) -> None:
        """Authenticate given auth token.

        :raises AuthorizationOCPIError: If auth_token is not in a given
          list of verified tokens C.
        """
        list_token_c = await cls.get_valid_token_c()
        if auth_token not in list_token_c:
            raise AuthorizationOCPIError

    @classmethod
    @abstractmethod
    async def get_valid_token_c(cls) -> List[str]:
        """Return valid token c list."""
        pass
