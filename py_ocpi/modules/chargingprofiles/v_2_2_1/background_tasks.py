import httpx

from asyncio import sleep

from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.utils import encode_string_base64
from py_ocpi.core.config import settings
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.crud import Crud
from py_ocpi.core.data_types import CiString, URL
from py_ocpi.core.enums import ModuleID, RoleEnum, Action

from py_ocpi.modules.chargingprofiles.v_2_2_1.schemas import (
    ChargingProfileResult,
    ChargingProfileResultType,
)


async def send_get_chargingprofile(
    session_id: CiString(36),  # type: ignore
    duration: int,
    response_url: URL,
    auth_token: str,
    crud: Crud,
    adapter: Adapter,
):
    client_auth_token = await crud.do(
        ModuleID.commands,
        RoleEnum.cpo,
        Action.get_client_token,
        auth_token=auth_token,
        version=VersionNumber.v_2_2_1,
    )

    active_charging_profile_result = None
    for _ in range(30 * settings.GET_ACTIVE_PROFILE_AWAIT_TIME):
        # since charging profile has no id, 0 is used for id parameter of crud.get
        active_charging_profile_result = await crud.get(
            ModuleID.hub_client_info,
            RoleEnum.cpo,
            0,
            session_id=session_id,
            duration=duration,
            response_url=response_url,
            auth_token=auth_token,
            version=VersionNumber.v_2_2_1,
        )
        if active_charging_profile_result:
            break
        await sleep(2)

    if not active_charging_profile_result:
        active_charging_profile_result = ChargingProfileResult(
            result=ChargingProfileResultType.rejected
        )
    else:
        active_charging_profile_result = (
            adapter.active_charging_profile_result_adapter(
                active_charging_profile_result, VersionNumber.v_2_2_1
            )
        )

    async with httpx.AsyncClient() as client:
        authorization_token = f"Token {encode_string_base64(client_auth_token)}"
        await client.post(
            response_url,
            json=active_charging_profile_result.dict(),
            headers={"authorization": authorization_token},
        )
