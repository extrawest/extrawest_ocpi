Quickstart
==========

Creating a project
~~~~~~~~~~~~~~~~~~

If you don't already have a project directory, you will need to create one.

From the command line, create and move into a directory of your project,
then run the following command:

.. code-block:: sh

    $ mkdir my-ocpi-project
    $ cd my-ocpi-project/

Create and activate virtual env and fill project dir with following contents:

.. code-block:: sh

    $ virualenv venv

.. warning::

    Make sure that you've used `python version 3.10` and higher.


.. code-block:: text

    my-ocpi-project/
        venv/
        main.py
        db.py
        crud.py
        auth.py
        .env

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
   * - NO_AUTH
     - False
     - When set to `True`, enables a mode where authentication is skipped.
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
   * - TRAILING_SLASH
     - True
     - If set `True` urls in `{version}/details` will be returned with `/` in the end

.. warning::

   It's strongly recommend to secure your endpoints with authentication. (`NO_AUTH = False`)

.. note::

   As credentials module is built on top of credentials exchange,
   `NO_AUTH` flag doesn't influence credentials module.

Add business logic and db operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's assume you're going to store `locations` as a `CPO` role.
And you're gonna use `MONGO` to store locations.

.. code-block:: sh

    $ pip install motor

Open `db.py` and create `DbInterface` class containing your db logic.

.. note::
    Make sure you replaced `mongo-username`, `mongo-password` and `mongo-host`
    with your own credentials.

db.py

.. code-block:: python

    from motor import motor_asyncio

    from py_ocpi.core.config import logger
    from py_ocpi.core.enums import ModuleID

    db_url = f"mongodb+srv://mongo-username:mongo-password@mongo-host"
    client = motor_asyncio.AsyncIOMotorClient(db_url)
    db = client.ocpi_database


    class DbInterface:
        """Mongo db operations interface class."""

        MODULE_MAP = {
            ModuleID.locations: "locations_table",
        }

        @classmethod
        async def get(cls, module, id, *args, **kwargs) -> dict | None:
            """Return single object from collection."""
            logger.info("GET obj from `%s` module with id - `%s`" % (module, id))
            collection = cls.MODULE_MAP[module]
            match module:
                case ModuleID.locations:
                    query = {"id": id}
                case _:
                    raise NotImplementedError
            return await db[collection].find_one(query)

        @classmethod
        async def get_all(cls, module, filters, *args, **kwargs) -> tuple[list[dict], int, bool]:
            """GET paginated list of objects result from collection."""
            data_list = await cls.list(module, filters, *args, **kwargs)
            total = await cls.count(module, filters, *args, **kwargs)
            is_last_page = await cls.is_last_page(
                module, filters, total, *args, **kwargs
            )
            return data_list, total, is_last_page

        @classmethod
        async def list(cls, module, filters, *args, **kwargs) -> list[dict]:
            """GET paginated list of objects result from collection."""
            collection = cls.MODULE_MAP[module]

            offset = await cls._get_offset_filter(filters)
            limit = await cls._get_limit_filter(filters)

            query = await cls._get_date_from_query(filters)
            query |= await cls._get_date_to_query(filters)

            return await db[collection].find(query).sort("_id").skip(offset).limit(limit).to_list(None)

        @classmethod
        async def count(cls, module, filters, *args, **kwargs) -> int:
            """Return amount of objects in collection using corresponding filters."""
            collection = cls.MODULE_MAP[module]

            query = await cls._get_date_from_query(filters)
            query |= await cls._get_date_to_query(filters)

            total = db[collection].count_documents(query)
            return total

        @classmethod
        async def is_last_page(
            cls, module, filters, total, *args, **kwargs
        ) -> bool:
            """Return whether paginated result is the last page or not."""
            offset = await cls._get_offset_filter(filters)
            limit = await cls._get_limit_filter(filters)
            return offset + limit >= total if limit else True

        @classmethod
        async def _get_offset_filter(cls, filters: dict) -> int:
            """Return offset value from filters."""
            return filters.get("offset", 0)

        @classmethod
        async def _get_limit_filter(cls, filters: dict) -> int:
            """Return limit value from filters."""
            return filters.get("limit", 0)

        @classmethod
        async def _get_date_from_query(cls, filters: dict) -> int:
            """Return date from value from filters."""
            query = {}
            date_to = filters.get("date_to")
            if date_to:
                query.setdefault("last_updated", {}).update(
                    {"$lte": date_to.isoformat()}
                )
            return query

        @classmethod
        async def _get_date_to_query(cls, filters: dict) -> int:
            """Return date to value from filters."""
            query = {}
            date_from = filters.get("date_from")
            if date_from:
                query.setdefault("last_updated", {}).update(
                    {"$gte": date_from.isoformat()}
                )
            return query

Open `crud.py` and create `Crud` class containing your business logic.

crud.py

.. code-block:: python

    from typing import Any, Tuple

    from py_ocpi.core.config import logger
    from py_ocpi.core.crud import Crud
    from py_ocpi.core.enums import ModuleID, RoleEnum, Action

    from .db import DbInterface


    class AppCrud(Crud):
        """Class contains crud business logic."""

        @classmethod
        async def get(
            cls, module: ModuleID, role: RoleEnum, id, *args, **kwargs
        ) -> dict | None:
            """Return single obj from db."""
            logger.info(
                'Get single obj -> module - `%s`, role - `%s`, version - `%s`'
                % (module, role, kwargs.get("version", ""))
            )
            return await DbInterface.get(module, id, *args, **kwargs)

        @classmethod
        async def list(
            cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs
        ) -> tuple[list[dict], int, bool]:
            """Return list of obj from db."""
            logger.info(
                'Get list of objs -> module - `%s`, role - `%s`, version - `%s`'
                % (module, role, kwargs.get("version", ""))
            )
            data_list, total, is_last_page = await DbInterface.get_all(
                module, filters, *args, **kwargs
            )
            return data_list, total, is_last_page

Add authentication logic
~~~~~~~~~~~~~~~~~~~~~~~~

Implement `get_valid_token_c` and `get_valid_token_a` method of
Authenticator class which would return list of valid tokens. Given
authorization token will be compared with this list.

.. note::
    OCPI versions 2.2 and higher sends encoded authorization tokens,
    so it will be decoded before compared.

.. note::
    Make sure to retrieve valid tokens from the source you need.

auth.py

.. code-block:: python

    from typing import List

    from py_ocpi.core.authentication.authenticator import Authenticator


    class ClientAuthenticator(Authenticator):

        @classmethod
        async def get_valid_token_c(cls) -> List[str]:
            """Return a list of valid tokens c."""
            return ["my_valid_token_c"]

        @classmethod
        async def get_valid_token_a(cls) -> List[str]:
            """Return a list of valid tokens a."""
            return ["my_valid_token_a"]

Initialize fastapi application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

main.py

.. code-block:: python

    from py_ocpi import get_application
    from py_ocpi.core.enums import RoleEnum, ModuleID
    from py_ocpi.modules.versions.enums import VersionNumber

    from .auth import ClientAuthenticator
    from .crud import AppCrud


    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[RoleEnum.cpo],
        modules=[ModuleID.locations],
        authenticator=ClientAuthenticator,
        crud=AppCrud,
    )

Initialize fastapi application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

    $ uvicorn main:app --reload

Request the list of locations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
    Make sure you replaced `my_valid_token` with the right value.

.. code-block:: sh

    $ curl --request GET 'http://127.0.0.1:8000/ocpi/cpo/2.1.1/locations/' --header 'Authorization: Token my_valid_token'

Check the API docs
~~~~~~~~~~~~~~~~~~

As this project is based on fastapi, use `/docs` or `redoc/` to check
the documentation after the project is running.

Example: `http://127.0.0.1:8000/ocpi/docs/ <http://127.0.0.1:8000/ocpi/docs/>`_
