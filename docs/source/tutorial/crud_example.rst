Full CRUD example
=================

Check in the :doc:`crud` to get understanding what parameters could be received
as `*args` and `**kwargs`.

.. note::
   This example is for representational purposes only. Actual implementation details
   and functionality may vary. It serves as a template and may not accurately
   reflect the current state of the code or your implementation.

.. code-block:: python

    import copy

    from typing import Any, Tuple
    from uuid import uuid4

    from py_ocpi.core.crud import Crud
    from py_ocpi.core.enums import ModuleID, RoleEnum, Action

    from .db_interface import DbInterface

    class CrudExample(Crud):

        @classmethod
        async def get(
            cls, module: ModuleID, role: RoleEnum, id, *args, **kwargs
        ) -> Any:
            return await DbInterface.get(module, id, *args, **kwargs)

        @classmethod
        async def list(
            cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs
        ) -> Tuple[list, int, bool]:
            data_list, total, is_last_page = await DbInterface.get_all(
                module, filters, *args, **kwargs
            )
            return data_list, total, is_last_page

        @classmethod
        async def create(
            cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs
        ) -> Any:
            if module == ModuleID.credentials_and_registration:
                # It's advised to save somewhere in separate table token B sent by client:
                integration_data = copy.deepcopy(data["credentials"])
                integration_data["endpoints"] = data.pop("endpoints")
                integration_data["credentials_id"] = auth_token
                await DbInterface.create(
                    "integration", integration_data, *args, **kwargs
                )

                # It's advised to re-create token A after it was used for register purpose
                # Implement your own logic here
                token_a = uuid4()

            return await DbInterface.create(module, data, *args, **kwargs)

        @classmethod
        async def update(
            cls, module: ModuleID, role: RoleEnum, data: dict, id, *args, **kwargs
        ) -> Any:
            match module:
                case ModuleID.credentials_and_registration:
                    # re-create client credentials
                    await DbInterface.update(
                        "integration", data, id, *args, **kwargs
                    )

                    # Generate new token_c instead the one client used
                    new_token_с = uuid4()
                    data = {"token": new_token_с}

            return await DbInterface.update(module, data, id, *args, **kwargs)

        @classmethod
        async def delete(
            cls, module: ModuleID, role: RoleEnum, id, *args, **kwargs
        ):
            if module.credentials_and_registration:
                # Make sure to delete corresponding token_b given you by client
                await DbInterface.delete("integration", id, *args, **kwargs)
            await DbInterface.delete(module, id, *args, **kwargs)

        @classmethod
        async def do(
            cls,
            module: ModuleID,
            role: RoleEnum,
            action: Action,
            *args,
            data: dict = None,
            **kwargs,
        ) -> Any:
            """CRUD DO."""
            auth_token = kwargs["auth_token"]

            match action:
                case Action.get_client_token:
                    token_b = await DbInterface.get(
                        "integration", auth_token, *args, **kwargs
                    )
                    return token_b["token"]
                case Action.authorize_token:
                    # TODO: implement your token auth business logic here
                    return {}
                case Action.send_command:
                    # TODO: implement your send command to Charge Point business logic here
                    pass
                case Action.send_get_chargingprofile:
                    # TODO: implement your set charging profile business logic here
                    pass
                case Action.send_delete_chargingprofile:
                    # TODO: implement your delete charging profile business logic here
                    pass
                case Action.send_update_charging_profile:
                    # TODO: implement your update charging profile business logic here
                    pass
