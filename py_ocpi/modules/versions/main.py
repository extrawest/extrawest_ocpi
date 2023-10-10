from fastapi import (
    APIRouter,
    Depends,
    Request,
    HTTPException,
    status as fastapistatus,
)

from py_ocpi.core import status
from py_ocpi.core.crud import Crud
from py_ocpi.core.dependencies import (
    get_versions as get_versions_,
    get_crud,
)
from py_ocpi.core.enums import Action, ModuleID, RoleEnum
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.utils import get_auth_token_from_header


router = APIRouter()


@router.get("/versions", response_model=OCPIResponse)
async def get_versions(
    request: Request,
    versions=Depends(get_versions_),
    crud: Crud = Depends(get_crud),
):
    auth_token = get_auth_token_from_header(request)

    server_cred = await crud.do(
        ModuleID.credentials_and_registration,
        RoleEnum.cpo,
        Action.get_client_token,
        auth_token=auth_token,
    )
    if server_cred is None:
        raise HTTPException(
            fastapistatus.HTTP_401_UNAUTHORIZED,
            "Unauthorized",
        )
    return OCPIResponse(
        data=versions,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
