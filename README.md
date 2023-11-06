
# Extrawest OCPI


[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![commit-check](https://img.shields.io/badge/commit--check-enabled-brightgreen?logo=Git&logoColor=white)](https://github.com/commit-check/commit-check)

---

Python implementation of Open Charge Point Interface (OCPI) protocol based on fastapi.

Supported OCPI versions: 2.2.1, 2.1.1

OCPI Documentation: [2.2.1](https://github.com/ocpi/ocpi/tree/release-2.2.1-bugfixes), [2.1.1](https://github.com/ocpi/ocpi/tree/release-2.1.1-bugfixes)

---


## Requirements

---

Python >= 3.10


## Installation

---

```bash
  pip install extrawest-ocpi
```

Make sure to install any ASGI-server supported by fastapi:
```bash
  pip install uvicorn
```


## Environment Variables

---

To use this project, you will need to add the following environment variables 
to your .env file, overwise default values would be taken

`PROJECT_NAME`
`BACKEND_CORS_ORIGINS`
`OCPI_HOST`
`OCPI_PREFIX`
`PUSH_PREFIX`
`COUNTRY_CODE`
`PARTY_ID`
`COMMAND_AWAIT_TIME`


## API Reference

---

As this project is based on fastapi, use `/docs` or `redoc/` to check 
.the documentation after the project is running.

[API's will appear depending on given `version_numbers`, `roles` and `modules` given to initializer.]

Example: `http://127.0.0.1:8000/ocpi/docs/`


## Roadmap

---

- [in progress] Add v2.2.1 modules: `Charging Profiles`, `Hub Client Info`


## Usage/Examples

---

0) Create DbInterface class for db operations (Mongo example).

```python db_interface.py
from motor import motor_asyncio  # TODO: pip install motor

from py_ocpi.core.enums import ModuleID

client = motor_asyncio.AsyncIOMotorClient("db_url")
db = client.ocpi_database


class DbInterface:
    MODULE_MAP = {
        ModuleID.credentials_and_registration: "credentials_table",
        ModuleID.locations: "locations_table",
        ModuleID.cdrs: "cdrs_table",
        ModuleID.tokens: "tokens_table",
        ModuleID.tariffs: "tariffs_table",
        ModuleID.sessions: "sessions_table",
        ModuleID.commands: "commands_table",
        "integration": "integration_table",
    }

    @classmethod
    async def get(cls, module, id, *args, **kwargs) -> dict | None:
        collection = cls.MODULE_MAP[module]

        match module:
            case ModuleID.commands:
                # TODO: implement query using your identification for commands
                command_data = kwargs["comand_data"]
                query = {}
            case ModuleID.tokens:
                query = {"uid": id}
            case "integration":
                query = {"credentials_id": id}
            case _:
                query = {"id": id}
        return await db[collection].find_one(query)

    @classmethod
    async def get_all(cls, module, filters, *args, **kwargs) -> list[dict]:
        collection = cls.MODULE_MAP[module]

        offset = await cls.get_offset_filter(filters)
        limit = await cls.get_limit_filter(filters)

        query = await cls.get_date_from_query(filters)
        query |= await cls.get_date_to_query(filters)

        return await db[collection].find(
            query,
        ).sort("_id").skip(offset).limit(limit).to_list(None)

    @classmethod
    async def create(cls, module, data, *args, **kwargs) -> dict:
        collection = cls.MODULE_MAP[module]

        return await db[collection].insert_one(data)

    @classmethod
    async def update(cls, module, data, id, *args, **kwargs) -> dict:
        collection = cls.MODULE_MAP[module]

        match module:
            case ModuleID.tokens:
                token_type = kwargs.get("token_type")
                query = {"uid": id}
                if token_type:
                    query |= {"token_type": token_type}
            case "integration":
                query = {"credentials_id": id}
            case ModuleID.credentials_and_registration:
                query = {"token": id}
            case _:
                query = {"id": id}

        return await db[collection].update_one(query, {"$set": data})

    @classmethod
    async def delete(cls, module, id, *args, **kwargs) -> None:
        collection = cls.MODULE_MAP[module]
        if module == ModuleID.credentials_and_registration:
            query = {"token": id}
        else:
            query = {"id": id}
        await db[collection].delete_one(query)

    @classmethod
    async def count(cls, module, filters, *args, **kwargs) -> int:
        collection = cls.MODULE_MAP[module]

        query = await cls.get_date_from_query(filters)
        query |= await cls.get_date_to_query(filters)

        total = db[collection].count_documents(query)
        return total

    @classmethod
    async def is_last_page(cls, module, filters, total, *args, **kwargs) -> bool:
        offset = await cls.get_offset_filter(filters)
        limit = await cls.get_limit_filter(filters)
        return offset + limit >= total if limit else True

    @classmethod
    async def get_offset_filter(cls, filters: dict) -> int:
        return filters.get("offset", 0)

    @classmethod
    async def get_limit_filter(cls, filters: dict) -> int:
        return filters.get("limit", 0)

    @classmethod
    async def get_date_from_query(cls, filters: dict) -> int:
        query = {}
        date_to = filters.get("date_to")
        if date_to:
            query.setdefault("last_updated", {}).update({'$lte': date_to.isoformat()})
        return query

    @classmethod
    async def get_date_to_query(cls, filters: dict) -> int:
        query = {}
        date_from = filters.get("date_from")
        if date_from:
            query.setdefault("last_updated", {}).update({'$gte': date_from.isoformat()})
        return query
```

1) Implement and connect your business logic and db methods inside this Crud class. 

crud.py
```python crud.py
import copy
from typing import Any, Tuple
from uuid import uuid4

from py_ocpi.core.crud import Crud
from py_ocpi.core.enums import ModuleID, RoleEnum, Action

from .crud_interface import DbInterface


class CrudExample(Crud):

    @classmethod
    async def get(cls, module: ModuleID, role: RoleEnum, id, *args, **kwargs) -> Any:
        version = kwargs["version"]
        party_id = kwargs.get("party_id")
        country_code = kwargs.get("country_code")
        command_data = kwargs.get("command_data")
        return await DbInterface.get(module, id, *args, **kwargs)

    @classmethod
    async def list(cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs) -> Tuple[list, int, bool]:
        version = kwargs["version"]
        party_id = kwargs.get("party_id")
        country_code = kwargs.get("country_code")
        data_list = await DbInterface.get_all(module, filters, *args, **kwargs)
        total = await DbInterface.count(module, filters, *args, **kwargs)
        is_last_page = await DbInterface.is_last_page(module, filters, total, *args, **kwargs)
        return data_list, total, is_last_page

    @classmethod
    async def create(cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs) -> Any:
        version = kwargs["version"]
        auth_token = kwargs["auth_token"]
        command = kwargs.get("command")
        party_id = kwargs.get("party_id")
        country_code = kwargs.get("country_code")
        token_type = kwargs.get("token_type")
        if module == ModuleID.credentials_and_registration:
            # It's advised to save somewhere in separate table token B sent by client:
            integration_data = copy.deepcopy(data["credentials"])
            integration_data["endpoints"] = data.pop("endpoints")
            integration_data["credentials_id"] = auth_token
            await DbInterface.create("integration", integration_data, *args, **kwargs)

            # It's advised to re-create token A after it was used for register purpose
            token_a = uuid4()  # TODO: Don't forget to save it!

        return await DbInterface.create(module, data, *args, **kwargs)

    @classmethod
    async def update(cls, module: ModuleID, role: RoleEnum, data: dict, id, *args, **kwargs) -> Any:
        version = kwargs["version"]
        party_id = kwargs["party_id"]
        country_code = kwargs.get("country_code")
        token_type = kwargs.get("token_type")
        match module:
            case ModuleID.credentials_and_registration:
                # re-create client credentials
                await DbInterface.update("integration", data, id, *args, **kwargs)

                # Generate new token_c instead the one client used
                new_token_с = uuid4()
                data = {"token": new_token_с}

        return await DbInterface.update(module, data, id, *args, **kwargs)

    @classmethod
    async def delete(cls, module: ModuleID, role: RoleEnum, id, *args, **kwargs):
        version = kwargs["version"]
        if module.credentials_and_registration:
            # Make sure to delete corresponding token_b given you by client
            await DbInterface.delete("integration", id, *args, **kwargs)
        await DbInterface.delete(module, id, *args, **kwargs)

    @classmethod
    async def do(cls, module: ModuleID, role: RoleEnum, action: Action, *args, data: dict = None, **kwargs) -> Any:
        """CRUD DO."""
        auth_token = kwargs["auth_token"]

        match action:
            case Action.get_client_token:
                token_b = await DbInterface.get("integration", auth_token, *args, **kwargs)
                return token_b["token"]
            case Action.authorize_token:
                # TODO: implement token authorization and return result
                #  of AuthorizationInfo type
                return {}
            case Action.send_command:
                # TODO: implement logic of send command action,
                #  check validity of the token data, check token, send command
                #  to chargepoint, save token in db
                #  return result of CommandResponse type
                return None
```

2) Implement `get_valid_token_c` and `get_valid_token_a` method of 
Authenticator class which would return list of valid tokens. Given 
authorization token will be compared with this list.

[Reminder]: OCPI versions 2.2 and higher sends encoded authorization tokens, 
so it will be decoded before compared.

auth.py
```python
from typing import List

from py_ocpi.core.authentication.authenticator import Authenticator


class ClientAuthenticator(Authenticator):
    @classmethod
    async def get_valid_token_c(cls) -> List[str]:
        """Return a list of valid tokens c."""
        ...
        return ["..."]

    @classmethod
    async def get_valid_token_a(cls) -> List[str]:
        """Return a list of valid tokens a."""
        ...
        return ["..."]
```

3) Initialize fastapi application

If you need to have support for pushing the updates you could set 
`http_push=True` to use push endpoint or `websocket_push=True` to 
use websocket connection.

main.py
```python
from py_ocpi import get_application
from py_ocpi.core.enums import RoleEnum, ModuleID
from py_ocpi.modules.versions.enums import VersionNumber

from auth import ClientAuthenticator
from crud import Crud


app = get_application(
    version_numbers=[VersionNumber.v_2_1_1, VersionNumber.v_2_2_1],
    roles=[RoleEnum.cpo],
    modules=[
        ModuleID.credentials_and_registration,
        ModuleID.locations,
        ModuleID.cdrs,
        ModuleID.tokens,
        ModuleID.tariffs,
        ModuleID.sessions,
        ModuleID.commands,
    ],
    authenticator=ClientAuthenticator,
    crud=Crud,
    http_push=False,
    websocket_push=False,
)
```

4) Run

```bash
  uvicorn main:app --reload
```


## Related

---

The project was created through inspiration and adaptation of this project  [PY_OCPI](https://github.com/TECHS-Technological-Solutions/ocpi).


## License

---

This project is licensed under the terms of the [MIT](https://github.com/extrawest/extrawest_ocpi/blob/main/LICENSE) license.

