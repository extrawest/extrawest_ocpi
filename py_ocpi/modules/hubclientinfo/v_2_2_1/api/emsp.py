from fastapi import APIRouter, Depends, Request

from py_ocpi.core.utils import get_auth_token
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.hubclientinfo.v_2_2_1.schemas import ClientInfo

router = APIRouter(
    prefix="/clientinfo",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_2_1))],
)


@router.get("/{country_code}/{party_id}", response_model=OCPIResponse)
async def get_hubclientinfo(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.hub_client_info,
        RoleEnum.emsp,
        None,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if data:
        return OCPIResponse(
            data=[adapter.hubclientinfo_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    raise NotFoundOCPIError


@router.put("/{country_code}/{party_id}", response_model=OCPIResponse)
async def add_or_update_clienthubinfo(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    client_hub_info: ClientInfo,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.hub_client_info,
        RoleEnum.emsp,
        None,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if data:
        data = await crud.update(
            ModuleID.hub_client_info,
            RoleEnum.emsp,
            client_hub_info.dict(),
            None,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_2_1,
        )
    else:
        data = await crud.create(
            ModuleID.hub_client_info,
            RoleEnum.emsp,
            client_hub_info.dict(),
            None,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_2_1,
        )

    return OCPIResponse(
        data=[adapter.hubclientinfo_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
