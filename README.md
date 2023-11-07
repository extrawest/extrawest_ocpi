
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


## Usage/Examples

---

1) Implement and connect your business logic and db methods inside this Crud class. 

[NOTE]: Check `example` directory for a mongo implementation example.
[Click here](examples)

crud.py
```python
from typing import Any, Tuple

from py_ocpi.core.enums import ModuleID, RoleEnum, Action


class Crud:

    @classmethod
    async def get(cls, module: ModuleID, role: RoleEnum, id, *args, **kwargs) -> Any:
        ...

    @classmethod
    async def list(cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs) -> Tuple[list, int, bool]:
        ...

    @classmethod
    async def create(cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs) -> Any:
        ...

    @classmethod
    async def update(cls, module: ModuleID, role: RoleEnum, data: dict, id, *args, **kwargs) -> Any:
        ...

    @classmethod
    async def delete(cls, module: ModuleID, role: RoleEnum, id, *args, **kwargs):
        ...

    @classmethod
    async def do(cls, module: ModuleID, role: RoleEnum, action: Action, *args, data: dict = None, **kwargs) -> Any:
        ...
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

## API Reference

---

As this project is based on fastapi, use `/docs` or `redoc/` to check 
.the documentation after the project is running.

[API's will appear depending on given `version_numbers`, `roles` and `modules` given to initializer.]

Example: `http://127.0.0.1:8000/ocpi/docs/`


## Roadmap

---

- [in progress] Add v2.2.1 modules: `Charging Profiles`, `Hub Client Info`


## Related

---

The project was created through inspiration and adaptation of this project  [PY_OCPI](https://github.com/TECHS-Technological-Solutions/ocpi).


## License

---

This project is licensed under the terms of the [MIT](https://github.com/extrawest/extrawest_ocpi/blob/main/LICENSE) license.

