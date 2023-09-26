import logging

from fastapi import APIRouter, Depends, Request, Response

from py_ocpi.modules.cdrs.v_2_1_1.schemas import Cdr
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.utils import get_auth_token_from_header
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.crud import Crud
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.config import settings
from py_ocpi.core.dependencies import get_crud, get_adapter

router = APIRouter(
    prefix="/cdrs",
)


@router.get("/{cdr_id}", response_model=OCPIResponse)
async def get_cdr(
    request: Request,
    cdr_id: CiString(36),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token_from_header(request)
    logging.info(f"AUTH TOKEN - {auth_token}")

    data = await crud.get(
        ModuleID.cdrs,
        RoleEnum.emsp,
        cdr_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_1_1,
    )
    logging.info(f"DATA - {data}")

    logging.info(
        f"Adapter - {adapter.cdr_adapter(data, VersionNumber.v_2_1_1).dict()}"
    )
    return OCPIResponse(
        data=[adapter.cdr_adapter(data, VersionNumber.v_2_1_1).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.post("/", response_model=OCPIResponse)
async def add_cdr(
    request: Request,
    response: Response,
    cdr: Cdr,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token_from_header(request)
    logging.info(f"AUTH TOKEN - {auth_token}")

    data = await crud.create(
        ModuleID.cdrs,
        RoleEnum.emsp,
        cdr.dict(),
        auth_token=auth_token,
        version=VersionNumber.v_2_1_1,
    )
    logging.info(f"Data - {data}")

    cdr_data = adapter.cdr_adapter(data, VersionNumber.v_2_1_1)
    logging.info(f"CDR data - {cdr_data}")
    cdr_url = (
        f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp"
        f"/{VersionNumber.v_2_1_1}/{ModuleID.cdrs}/{cdr_data.id}"
    )
    logging.info(f"CDR url - {cdr_url}")
    response.headers.append("Location", cdr_url)

    logging.info(f"CDR dict - {cdr_data.dict()}")

    return OCPIResponse(
        data=[cdr_data.dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )