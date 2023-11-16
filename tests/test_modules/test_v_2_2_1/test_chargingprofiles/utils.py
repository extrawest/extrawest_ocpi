from py_ocpi.core import enums

from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN,
    ENCODED_RANDOM_AUTH_TOKEN,
)

CPO_BASE_URL = "/ocpi/cpo/2.2.1/chargingprofiles/"
EMSP_BASE_URL = "/ocpi/emsp/2.2.1/chargingprofiles/"
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN}"}

CHARGING_PROFILE = {
    "start_date_time": "2022-01-02 00:00:00+00:00",
    "charging_profile": {
        "charging_rate_unit": "W",
        "min_charge_rate": 1,
        "charging_profile_period": {
            "start_period": 1,
            "limit": 1,
        },
    },
}


class Crud:
    @classmethod
    async def do(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        action: enums.Action,
        *args,
        data: dict = None,
        **kwargs,
    ) -> dict:
        return

    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ) -> dict:
        return

    @classmethod
    async def update(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: dict,
        id,
        *args,
        **kwargs,
    ):
        return

    @classmethod
    async def create(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: dict,
        *args,
        **kwargs,
    ):
        return
