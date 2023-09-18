
# Extrawest OCPI


[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![commit-check](https://img.shields.io/badge/commit--check-enabled-brightgreen?logo=Git&logoColor=white)](https://github.com/commit-check/commit-check)

---

Python implementation of Open Charge Point Interface (OCPI) protocol based on fastapi.

---


## Requirements

---

Python >= 3.11.1


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

To use this project, you will need to add the following environment variables to your .env file

`API_KEY` 
`ANOTHER_API_KEY`
`PROJECT_NAME`
`BACKEND_CORS_ORIGINS`
`OCPI_HOST`
`OCPI_PREFIX`
`PUSH_PREFIX`
`COUNTRY_CODE`
`PARTY_ID`


## Usage/Examples

---

1) Implement and connect your db methods inside this Crud class. 

crud.py
```python curd.py
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

2) Implement all needed module adapters inside Adapter class.

adapter.py
```python
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.locations.v_2_2_1.schemas import Location


class Adapter:

    @classmethod
    def location_adapter(cls, data: dict, version: VersionNumber) -> Location:
        """Return location."""
        return Location(**data)

```

3) Initialize fastapi application

main.py
```python
from py_ocpi import get_application
from py_ocpi.core.enums import RoleEnum
from py_ocpi.modules.versions.enums import VersionNumber

from adapter import Adapter
from crud import Crud


app = get_application(
    version_numbers=[VersionNumber.v_2_2_1],
    roles=[RoleEnum.cpo],
    crud=Crud,
    adapter=Adapter,
)

```

4) Run

```bash
  uvicorn main:app --reload
```

## API Reference

---

As this project is based on fastapi, use `/docs` or `redoc/` to check the documentation after the project is running.

Example: `http://127.0.0.1:8000/ocpi/docs/`


## Roadmap

---

- [in progress] Add support for OCPI v2.1.1
  - What's done so far:
    - Add version, credentials and locations module;
    - Add support for initializing v2.1.1 (It's possible to initialize only one version for one project); 


## Related

---

The project was created through inspiration and adaptation of this project  [PY_OCPI](https://github.com/TECHS-Technological-Solutions/ocpi).


## License

---

This project is licensed under the terms of the [MIT](https://github.com/extrawest/extrawest_ocpi/blob/main/LICENSE) license.

