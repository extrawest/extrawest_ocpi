from fastapi import APIRouter, Depends, Request

from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.utils import get_auth_token
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.config import logger
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.dependencies import get_crud, get_adapter

from py_ocpi.modules.chargingprofiles.v_2_2_1.schemas import (
    ActiveChargingProfile,
)

router = APIRouter(
    prefix="/chargingprofiles",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_2_1))],
)


@router.post("/", response_model=OCPIResponse)
async def receive_chargingprofile_command(
    request: Request,
    data: dict,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    logger.info("Received charging profile result.")
    logger.debug("Chargingprofile result data - %s" % data)
    auth_token = get_auth_token(request)
    query_params = request.query_params
    logger.debug("Request query_params - %s" % query_params)

    await crud.create(
        ModuleID.charging_profile,
        RoleEnum.emsp,
        data,
        query_params=query_params,
        auth_token=auth_token,
        version=VersionNumber.v_2_2_1,
    )

    return OCPIResponse(
        data=[],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.put("/{session_id}", response_model=OCPIResponse)
async def add_or_update_chargingprofile(
    request: Request,
    session_id: str,
    active_charging_profile: ActiveChargingProfile,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    logger.info(
        "Received request to add or update charging profile "
        "with session_id - `%s`." % session_id
    )
    logger.debug(
        "Active chargingprofile result data - %s"
        % active_charging_profile.dict()
    )
    auth_token = get_auth_token(request)

    await crud.update(
        ModuleID.charging_profile,
        RoleEnum.emsp,
        active_charging_profile.dict(),
        0,
        session_id=session_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_2_1,
    )

    return OCPIResponse(
        data=[],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
