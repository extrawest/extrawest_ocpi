from copy import deepcopy

from fastapi import APIRouter, Depends, Request

from py_ocpi.core import status
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.data_types import String
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.utils import (
    get_auth_token,
    partially_update_attributes,
)
from py_ocpi.modules.sessions.v_2_1_1.schemas import (
    SessionPartialUpdate,
    Session,
)
from py_ocpi.modules.versions.enums import VersionNumber

router = APIRouter(
    prefix="/sessions",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_1_1))],
)


@router.get(
    "/{country_code}/{party_id}/{session_id}", response_model=OCPIResponse
)
async def get_session(
    request: Request,
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    session_id: String(36),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data = await crud.get(
        ModuleID.sessions,
        RoleEnum.emsp,
        session_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if data:
        return OCPIResponse(
            data=[adapter.session_adapter(data, VersionNumber.v_2_1_1).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    raise NotFoundOCPIError


@router.put(
    "/{country_code}/{party_id}/{session_id}", response_model=OCPIResponse
)
async def add_or_update_session(
    request: Request,
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    session_id: String(36),  # type: ignore
    session: Session,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data = await crud.get(
        ModuleID.sessions,
        RoleEnum.emsp,
        session_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if data:
        data = await crud.update(
            ModuleID.sessions,
            RoleEnum.emsp,
            session.dict(),
            session_id,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_1_1,
        )
    else:
        data = await crud.create(
            ModuleID.sessions,
            RoleEnum.emsp,
            session.dict(),
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_1_1,
        )

    return OCPIResponse(
        data=[adapter.session_adapter(data, VersionNumber.v_2_1_1).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.patch(
    "/{country_code}/{party_id}/{session_id}", response_model=OCPIResponse
)
async def partial_update_session(
    request: Request,
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    session_id: String(36),  # type: ignore
    session: SessionPartialUpdate,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    old_data = await crud.get(
        ModuleID.sessions,
        RoleEnum.emsp,
        session_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if old_data:
        old_session = adapter.session_adapter(old_data, VersionNumber.v_2_1_1)

        new_session = deepcopy(old_session)
        partially_update_attributes(
            new_session, session.dict(exclude_defaults=True, exclude_unset=True)
        )

        data = await crud.update(
            ModuleID.sessions,
            RoleEnum.emsp,
            new_session.dict(),
            session_id,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_1_1,
        )

        return OCPIResponse(
            data=[adapter.session_adapter(data, VersionNumber.v_2_1_1).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    raise NotFoundOCPIError
