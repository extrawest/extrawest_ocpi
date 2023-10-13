from fastapi import APIRouter, Depends, Response, Request

from py_ocpi.modules.tokens.v_2_1_1.enums import TokenType
from py_ocpi.modules.tokens.v_2_1_1.schemas import LocationReference
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.utils import get_list, get_auth_token_from_header
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.crud import Crud
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.core.data_types import String
from py_ocpi.core.enums import ModuleID, RoleEnum, Action
from py_ocpi.core.dependencies import get_crud, get_adapter, pagination_filters

router = APIRouter(
    prefix="/tokens",
)


@router.get("/", response_model=OCPIResponse)
async def get_tokens(
    request: Request,
    response: Response,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
    filters: dict = Depends(pagination_filters),
):
    auth_token = get_auth_token_from_header(request)

    data_list = await get_list(
        response,
        filters,
        ModuleID.tokens,
        RoleEnum.emsp,
        VersionNumber.v_2_1_1,
        crud,
        auth_token=auth_token,
    )

    tokens = []
    for data in data_list:
        tokens.append(adapter.token_adapter(data, VersionNumber.v_2_1_1).dict())

    return OCPIResponse(
        data=tokens,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.post("/{token_uid}/authorize", response_model=OCPIResponse)
async def authorize_token(
    request: Request,
    token_uid: String(36),  # type: ignore
    token_type: TokenType = TokenType.rfid,
    location_reference: LocationReference = None,  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token_from_header(request)

    # check if token exists
    token = await crud.get(
        ModuleID.tokens,
        RoleEnum.emsp,
        token_uid,
        auth_token=auth_token,
        token_type=token_type,
        version=VersionNumber.v_2_1_1,
    )
    if token:
        location_reference = (
            location_reference.dict()
            if location_reference
            else None  # type: ignore
        )
        data = {
            "token_uid": token_uid,
            "token_type": token_type,
            "location_reference": location_reference,
        }
        authroization_result = await crud.do(
            ModuleID.tokens,
            RoleEnum.emsp,
            Action.authorize_token,
            data=data,
            auth_token=auth_token,
        )

        # when the token information is not enough
        if not authroization_result:
            return OCPIResponse(
                data=[],
                **status.OCPI_2002_NOT_ENOUGH_INFORMATION,
            )

        return OCPIResponse(
            data=[
                adapter.authorization_adapter(
                    authroization_result, VersionNumber.v_2_1_1
                ).dict()
            ],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )

    raise NotFoundOCPIError
