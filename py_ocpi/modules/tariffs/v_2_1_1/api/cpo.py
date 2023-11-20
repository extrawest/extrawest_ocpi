from fastapi import APIRouter, Depends, Response, Request

from py_ocpi.core.utils import get_list, get_auth_token
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.config import logger
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.dependencies import get_crud, get_adapter, pagination_filters
from py_ocpi.modules.versions.enums import VersionNumber

router = APIRouter(
    prefix="/tariffs",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_1_1))],
)


@router.get("/", response_model=OCPIResponse)
async def get_tariffs(
    request: Request,
    response: Response,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
    filters: dict = Depends(pagination_filters),
):
    logger.info("Received request to get tariffs")
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data_list = await get_list(
        response,
        filters,
        ModuleID.tariffs,
        RoleEnum.cpo,
        VersionNumber.v_2_1_1,
        crud,
        auth_token=auth_token,
    )

    tariffs = []
    for data in data_list:
        tariffs.append(
            adapter.tariff_adapter(data, VersionNumber.v_2_1_1).dict()
        )
    return OCPIResponse(
        data=tariffs,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
