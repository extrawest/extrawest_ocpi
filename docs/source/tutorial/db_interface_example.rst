Db interface example
====================

Check in the :doc:`crud` and :doc:`crud_example` to get understanding
what parameters could be received as `*args` and `**kwargs`.

.. note::
   This example is for representational purposes only. Actual implementation details
   and functionality may vary. It serves as a template and may not accurately
   reflect the current state of the code or your implementation.

.. code-block:: python

    from motor import motor_asyncio

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
            ModuleID.hub_client_info: "hubclientinfo_table",
            ModuleID.charging_profile: "chargingprofile_table",
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
        async def get_all(cls, module, filters, *args, **kwargs) -> tuple[list[dict], int, bool]:
            data_list = await cls.list(module, filters, *args, **kwargs)
            total = await cls.count(module, filters, *args, **kwargs)
            is_last_page = await cls.is_last_page(
                module, filters, total, *args, **kwargs
            )
            return data_list, total, is_last_page

        @classmethod
        async def list(cls, module, filters, *args, **kwargs) -> list[dict]:
            collection = cls.MODULE_MAP[module]

            offset = await cls._get_offset_filter(filters)
            limit = await cls._get_limit_filter(filters)

            query = await cls._get_date_from_query(filters)
            query |= await cls._get_date_to_query(filters)

            return (
                await db[collection]
                .find(
                    query,
                )
                .sort("_id")
                .skip(offset)
                .limit(limit)
                .to_list(None)
            )

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

            query = await cls._get_date_from_query(filters)
            query |= await cls._get_date_to_query(filters)

            total = db[collection].count_documents(query)
            return total

        @classmethod
        async def is_last_page(
            cls, module, filters, total, *args, **kwargs
        ) -> bool:
            offset = await cls._get_offset_filter(filters)
            limit = await cls._get_limit_filter(filters)
            return offset + limit >= total if limit else True

        @classmethod
        async def _get_offset_filter(cls, filters: dict) -> int:
            return filters.get("offset", 0)

        @classmethod
        async def _get_limit_filter(cls, filters: dict) -> int:
            return filters.get("limit", 0)

        @classmethod
        async def _get_date_from_query(cls, filters: dict) -> int:
            query = {}
            date_to = filters.get("date_to")
            if date_to:
                query.setdefault("last_updated", {}).update(
                    {"$lte": date_to.isoformat()}
                )
            return query

        @classmethod
        async def _get_date_to_query(cls, filters: dict) -> int:
            query = {}
            date_from = filters.get("date_from")
            if date_from:
                query.setdefault("last_updated", {}).update(
                    {"$gte": date_from.isoformat()}
                )
            return query

