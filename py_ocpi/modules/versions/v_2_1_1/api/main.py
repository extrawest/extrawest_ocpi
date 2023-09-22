from fastapi import (
    APIRouter,
    Depends,
    Request,
    HTTPException,
    status as fastapistatus,
)

from py_ocpi.core.crud import Crud
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.dependencies import get_endpoints, get_crud
from py_ocpi.core.utils import get_auth_token_from_header
from py_ocpi.core.enums import Action, ModuleID

from py_ocpi.modules.versions.v_2_1_1.schemas import (
    VersionDetail,
    VersionNumber,
)

router = APIRouter()


@router.get("/2.1.1/details", response_model=OCPIResponse)
async def get_version_details(
    request: Request,
    endpoints=Depends(get_endpoints),
    crud: Crud = Depends(get_crud),
):
    auth_token = get_auth_token_from_header(request)

    server_cred = await crud.do(
        ModuleID.credentials_and_registration,
        None,
        Action.get_client_token,
        auth_token=auth_token,
    )
    if server_cred is None:
        raise HTTPException(fastapistatus.HTTP_401_UNAUTHORIZED, "Unauthorized")

    return OCPIResponse(
        data=VersionDetail(
            version=VersionNumber.v_2_1_1,
            endpoints=endpoints[VersionNumber.v_2_1_1],
        ).dict(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
