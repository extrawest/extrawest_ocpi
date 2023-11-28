Installation
============

Install library
~~~~~~~~~~~~~~~

Extrawest OCPI is available on PyPI - to install it run:

.. code-block:: sh

    python -m pip install extrawest-ocpi

Install supported ASGI-server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure to install any ASGI-server supported by fastapi. Let's install `uvicorn` as an example:

.. code-block:: sh

    python -m pip install uvicorn

Fill .env variables
~~~~~~~~~~~~~~~~~~~

The next step is to create `.env` file with otherwise the default values will be used.

.. list-table::
   :widths: 20 20 120
   :header-rows: 1

   * - Var name
     - Default value
     - Description
   * - ENVIRONMENT
     - production
     - The environment setting for the project (e.g., development, testing).
   * - PROJECT_NAME
     - OCPI
     - The name of the project.
   * - BACKEND_CORS_ORIGINS
     - []
     - A list of allowed CORS origins for the backend.
   * - OCPI_HOST
     - www.example.com
     - The host address for the OCPI service.
   * - OCPI_PREFIX
     - ocpi
     - The prefix for OCPI-related routes.
   * - PUSH_PREFIX
     - push
     - The prefix for push-related routes.
   * - COUNTRY_CODE
     - US
     - The country code associated with the project.
   * - PARTY_ID
     - NON
     - The party ID for the project.
   * - PROTOCOL
     - https
     - The protocol used for communication (e.g., http for developing purposes).
   * - COMMAND_AWAIT_TIME
     - 5
     - The time, in seconds, to await a response for a command.
   * - GET_ACTIVE_PROFILE_AWAIT_TIME
     - 5
     - The time, in seconds, to await a response for the charging profile module's commands.

Create crud
~~~~~~~~~~~

Implement and connect your business logic and db methods inside this Crud class.

crud.py

.. code-block:: python

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

Implement authenticator
~~~~~~~~~~~~~~~~~~~~~~~

Implement `get_valid_token_c` and `get_valid_token_a` method of
Authenticator class which would return list of valid tokens. Given
authorization token will be compared with this list.

.. note::
    OCPI versions 2.2 and higher sends encoded authorization tokens,
    so it will be decoded before compared.

auth.py

.. code-block:: python

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

Initialize fastapi application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

main.py

.. code-block:: python

    from py_ocpi import get_application
    from py_ocpi.core.enums import RoleEnum, ModuleID
    from py_ocpi.modules.versions.enums import VersionNumber

    from auth import ClientAuthenticator
    from crud import Crud


    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1, VersionNumber.v_2_2_1],
        roles=[RoleEnum.cpo, RoleEnum.emsp],
        modules=[
            ModuleID.credentials_and_registration,
            ModuleID.locations,
        ],
        authenticator=ClientAuthenticator,
        crud=Crud,
    )

Initialize fastapi application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

    uvicorn main:app --reload

Check the API docs
~~~~~~~~~~~~~~~~~~

As this project is based on fastapi, use `/docs` or `redoc/` to check
the documentation after the project is running.

Example: `http://127.0.0.1:8000/ocpi/docs/ <http://127.0.0.1:8000/ocpi/docs/>`_
