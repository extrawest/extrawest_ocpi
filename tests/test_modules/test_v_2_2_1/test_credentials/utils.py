import functools
from uuid import uuid4

from py_ocpi.core import enums

CREDENTIALS_TOKEN_GET = {
    "url": "url",
    "roles": [
        {
            "role": enums.RoleEnum.emsp,
            "business_details": {
                "name": "name",
            },
            "party_id": "JOM",
            "country_code": "MY",
        }
    ],
}

CREDENTIALS_TOKEN_CREATE = {
    "token": str(uuid4()),
    "url": "/ocpi/versions",
    "roles": [
        {
            "role": enums.RoleEnum.emsp,
            "business_details": {
                "name": "name",
            },
            "party_id": "JOM",
            "country_code": "MY",
        }
    ],
}


def partial_class(cls, *args, **kwds):
    class NewCls(cls):
        __init__ = functools.partialmethod(cls.__init__, *args, **kwds)

    return NewCls


class Crud:
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        if id == CREDENTIALS_TOKEN_CREATE["token"]:
            return None
        return dict(CREDENTIALS_TOKEN_GET, **{"token": id})

    @classmethod
    async def create(
        cls, module: enums.ModuleID, data, operation, *args, **kwargs
    ):
        if operation == "credentials":
            return None
        return CREDENTIALS_TOKEN_CREATE

    @classmethod
    async def do(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        action: enums.Action,
        *args,
        data: dict = None,
        **kwargs,
    ):
        return None
