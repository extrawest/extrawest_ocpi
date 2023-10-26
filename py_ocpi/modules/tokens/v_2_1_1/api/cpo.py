from copy import deepcopy

from fastapi import APIRouter, Request, Depends

from py_ocpi.core import status
from py_ocpi.core.data_types import String
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.utils import (
    get_auth_token,
    partially_update_attributes,
)
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.tokens.v_2_1_1.schemas import Token, TokenPartialUpdate

router = APIRouter(
    prefix="/tokens",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_1_1))],
)


@router.get(
    "/{country_code}/{party_id}/{token_uid}", response_model=OCPIResponse
)
async def get_token(
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    token_uid: String(36),  # type: ignore
    request: Request,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data = await crud.get(
        ModuleID.tokens,
        RoleEnum.cpo,
        token_uid,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if data:
        return OCPIResponse(
            data=[adapter.token_adapter(data, VersionNumber.v_2_1_1).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    raise NotFoundOCPIError


@router.put(
    "/{country_code}/{party_id}/{token_uid}", response_model=OCPIResponse
)
async def add_or_update_token(
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    token_uid: String(36),  # type: ignore
    token: Token,
    request: Request,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data = await crud.get(
        ModuleID.tokens,
        RoleEnum.cpo,
        token_uid,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if data:
        data = await crud.update(
            ModuleID.tokens,
            RoleEnum.cpo,
            token.dict(),
            token_uid,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_1_1,
        )
    else:
        data = await crud.create(
            ModuleID.tokens,
            RoleEnum.cpo,
            token.dict(),
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_1_1,
        )
    return OCPIResponse(
        data=[adapter.token_adapter(data, VersionNumber.v_2_1_1).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.patch(
    "/{country_code}/{party_id}/{token_uid}", response_model=OCPIResponse
)
async def partial_update_token(
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    token_uid: String(36),  # type: ignore
    token: TokenPartialUpdate,
    request: Request,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    old_data = await crud.get(
        ModuleID.tokens,
        RoleEnum.cpo,
        token_uid,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if not old_data:
        raise NotFoundOCPIError
    old_token = adapter.token_adapter(old_data, VersionNumber.v_2_1_1)

    new_token = deepcopy(old_token)
    partially_update_attributes(
        new_token, token.dict(exclude_defaults=True, exclude_unset=True)
    )

    data = await crud.update(
        ModuleID.tokens,
        RoleEnum.cpo,
        new_token.dict(),
        token_uid,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    return OCPIResponse(
        data=[adapter.token_adapter(data, VersionNumber.v_2_1_1).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
