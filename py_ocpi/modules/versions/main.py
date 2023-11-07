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
from py_ocpi.core import status
from py_ocpi.core.crud import Crud
from py_ocpi.core.dependencies import (
    get_versions as get_versions_,
    get_crud,
)
from py_ocpi.core.schemas import OCPIResponse


router = APIRouter()
cred_dependency = CredentialsAuthorizationVerifier(None)


@router.get("/versions", response_model=OCPIResponse)
async def get_versions(
    request: Request,
    versions=Depends(get_versions_),
    crud: Crud = Depends(get_crud),
    server_cred: str | dict | None = Depends(cred_dependency),
):
    if server_cred is None:
        raise HTTPException(
            fastapistatus.HTTP_401_UNAUTHORIZED,
            "Unauthorized",
        )
    return OCPIResponse(
        data=versions,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
