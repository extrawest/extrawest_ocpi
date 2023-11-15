from fastapi import APIRouter, BackgroundTasks, Depends, Request

from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.utils import get_auth_token
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.data_types import CiString, URL
from py_ocpi.core.enums import ModuleID, RoleEnum, Action
from py_ocpi.core.dependencies import get_crud, get_adapter

from py_ocpi.modules.chargingprofiles.v_2_2_1.background_tasks import (
    send_get_chargingprofile,
)
from py_ocpi.modules.chargingprofiles.v_2_2_1.schemas import (
    ChargingProfileResponse,
    ChargingProfileResponseType,
)

router = APIRouter(
    prefix="/chargingprofiles",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_2_1))],
)


@router.get("/{session_id}", response_model=OCPIResponse)
async def get_chargingprofiles(
    request: Request,
    session_id: CiString(36),  # type: ignore
    duration: int,
    response_url: URL,
    background_tasks: BackgroundTasks,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token(request)

    session = await crud.get(
        ModuleID.sessions,
        RoleEnum.cpo,
        session_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_2_1,
    )

    if session:
        charging_profile_response = await crud.do(
            ModuleID.charging_profile,
            RoleEnum.cpo,
            Action.send_get_chargingprofile,
            session=session,
            duration=duration,
            response_url=response_url,
            auth_token=auth_token,
            version=VersionNumber.v_2_2_1,
        )

        if charging_profile_response:
            if (
                charging_profile_response["result"]
                == ChargingProfileResponseType.accepted
            ):
                background_tasks.add_task(
                    send_get_chargingprofile,
                    session_id=session_id,
                    duration=duration,
                    response_url=response_url,
                    auth_token=auth_token,
                    crud=crud,
                    adapter=adapter,
                )
            return OCPIResponse(
                data=[
                    adapter.charging_profile_response_adapter(
                        charging_profile_response
                    ).dict()
                ],
                **status.OCPI_1000_GENERIC_SUCESS_CODE,
            )

        charging_profile_response = ChargingProfileResponse(
            result=ChargingProfileResponseType.rejected, timeout=0
        )
        return OCPIResponse(
            data=[charging_profile_response.dict()],
            **status.OCPI_3000_GENERIC_SERVER_ERROR,
        )

    charging_profile_response = ChargingProfileResponse(
        result=ChargingProfileResponseType.rejected, timeout=0
    )
    return OCPIResponse(
        data=[charging_profile_response.dict()],
        **status.OCPI_2000_GENERIC_CLIENT_ERROR,
    )
