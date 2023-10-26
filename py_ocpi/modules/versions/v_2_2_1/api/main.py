from fastapi import (
    APIRouter,
    Depends,
    Request,
    HTTPException,
    status as fastapistatus,
)

from py_ocpi.core.authentication.verifier import (
    CredentialsAuthorizationVerifier,
)
from py_ocpi.core.crud import Crud
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.dependencies import get_endpoints, get_crud

from py_ocpi.modules.versions.v_2_2_1.schemas import (
    VersionDetail,
    VersionNumber,
)

router = APIRouter()
cred_dependency = CredentialsAuthorizationVerifier(VersionNumber.v_2_2_1)


@router.get("/2.2.1/details", response_model=OCPIResponse)
async def get_version_details(
    request: Request,
    endpoints=Depends(get_endpoints),
    crud: Crud = Depends(get_crud),
    server_cred: str | dict | None = Depends(cred_dependency),
):
    if server_cred is None:
        raise HTTPException(fastapistatus.HTTP_401_UNAUTHORIZED, "Unauthorized")

    return OCPIResponse(
        data=VersionDetail(
            version=VersionNumber.v_2_2_1,
            endpoints=endpoints[VersionNumber.v_2_2_1],
        ).dict(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
