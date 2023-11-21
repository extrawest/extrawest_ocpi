import copy

from fastapi import APIRouter, Depends, Request

from py_ocpi.core.utils import (
    get_auth_token,
    partially_update_attributes,
)
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.config import logger
from py_ocpi.core.data_types import String
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.locations.v_2_1_1.schemas import (
    Location,
    LocationPartialUpdate,
    EVSE,
    EVSEPartialUpdate,
    Connector,
    ConnectorPartialUpdate,
)

router = APIRouter(
    prefix="/locations",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_1_1))],
)


@router.get(
    "/{country_code}/{party_id}/{location_id}", response_model=OCPIResponse
)
async def get_location(
    request: Request,
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    location_id: String(39),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    logger.info(
        "Received request to get location with id - `%s`." % location_id
    )
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if data:
        return OCPIResponse(
            data=[adapter.location_adapter(data, VersionNumber.v_2_1_1).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError


@router.get(
    "/{country_code}/{party_id}/{location_id}/{evse_uid}",
    response_model=OCPIResponse,
)
async def get_evse(
    request: Request,
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    location_id: String(39),  # type: ignore
    evse_uid: String(39),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    logger.info(
        "Received request to get evse by id - `%s` (location id - `%s`)"
        % (location_id, evse_uid)
    )
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if data:
        location = adapter.location_adapter(data, VersionNumber.v_2_1_1)
        for evse in location.evses:
            if evse.uid == evse_uid:
                return OCPIResponse(
                    data=[evse.dict()],
                    **status.OCPI_1000_GENERIC_SUCESS_CODE,
                )
        logger.debug("Evse with id `%s` was not found." % evse_uid)
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError


@router.get(
    "/{country_code}/{party_id}/{location_id}/{evse_uid}/{connector_id}",
    response_model=OCPIResponse,
)
async def get_connector(
    request: Request,
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    location_id: String(39),  # type: ignore
    evse_uid: String(39),  # type: ignore
    connector_id: String(36),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    logger.info(
        "Received request to get connector by id - `%s` "
        "(location id - `%s`, evse id - `%s`)"
        % (connector_id, location_id, evse_uid)
    )
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if data:
        location = adapter.location_adapter(data, VersionNumber.v_2_1_1)
        for evse in location.evses:
            if evse.uid == evse_uid:
                for connector in evse.connectors:
                    if connector.id == connector_id:
                        return OCPIResponse(
                            data=[connector.dict()],
                            **status.OCPI_1000_GENERIC_SUCESS_CODE,
                        )
                logger.debug(
                    "Connector with id `%s` was not found." % connector_id
                )
        logger.debug("Evse with id `%s` was not found." % evse_uid)
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError


@router.put(
    "/{country_code}/{party_id}/{location_id}", response_model=OCPIResponse
)
async def add_or_update_location(
    request: Request,
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    location_id: String(39),  # type: ignore
    location: Location,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    logger.info(
        "Received request to add or update location with id - `%s`."
        % location_id
    )
    logger.debug("Location data to update - %s" % location.dict())
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if data:
        logger.debug("Update location with id - `%s`." % location_id)
        data = await crud.update(
            ModuleID.locations,
            RoleEnum.emsp,
            location.dict(),
            location_id,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_1_1,
        )
    else:
        logger.debug("Create location with id - `%s`." % location_id)
        data = await crud.create(
            ModuleID.locations,
            RoleEnum.emsp,
            location.dict(),
            auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_1_1,
        )

    return OCPIResponse(
        data=[adapter.location_adapter(data, VersionNumber.v_2_1_1).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.put(
    "/{country_code}/{party_id}/{location_id}/{evse_uid}",
    response_model=OCPIResponse,
)
async def add_or_update_evse(
    request: Request,
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    location_id: String(39),  # type: ignore
    evse_uid: String(39),  # type: ignore
    evse: EVSE,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    logger.info(
        "Received request to add or update evse by id - `%s` "
        "(location id - `%s`)" % (location_id, evse_uid)
    )
    logger.debug("Evse data to update - %s" % evse.dict())
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    old_data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if old_data:
        old_location = adapter.location_adapter(old_data, VersionNumber.v_2_1_1)
        new_location = copy.deepcopy(old_location)

        for old_evse in old_location.evses:
            if old_evse.uid == evse_uid:
                logger.debug("Update evse with id - %s" % evse_uid)
                new_location.evses.remove(old_evse)
                break

        new_location.evses.append(evse)

        await crud.update(
            ModuleID.locations,
            RoleEnum.emsp,
            new_location.dict(),
            location_id,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_1_1,
        )

        return OCPIResponse(
            data=[evse.dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError


@router.put(
    "/{country_code}/{party_id}/{location_id}/{evse_uid}/{connector_id}",
    response_model=OCPIResponse,
)
async def add_or_update_connector(
    request: Request,
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    location_id: String(39),  # type: ignore
    evse_uid: String(39),  # type: ignore
    connector_id: String(36),  # type: ignore
    connector: Connector,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    logger.info(
        "Received request to get connector by id - `%s` "
        "(location id - `%s`, evse id - `%s`)"
        % (connector_id, location_id, evse_uid)
    )
    logger.debug("Connector data to update - %s" % connector.dict())
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    old_data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if old_data:
        old_location = adapter.location_adapter(old_data, VersionNumber.v_2_1_1)
        new_location = copy.deepcopy(old_location)

        for old_evse in old_location.evses:
            if old_evse.uid == evse_uid:
                new_location.evses.remove(old_evse)
                new_evse = copy.deepcopy(old_evse)
                for old_connector in old_evse.connectors:
                    if old_connector.id == connector_id:
                        logger.debug(
                            "Update connector with id - %s" % connector_id
                        )
                        new_evse.connectors.remove(old_connector)
                        break
                new_evse.connectors.append(connector)
                new_location.evses.append(new_evse)

                await crud.update(
                    ModuleID.locations,
                    RoleEnum.emsp,
                    new_location.dict(),
                    location_id,
                    auth_token=auth_token,
                    country_code=country_code,
                    party_id=party_id,
                    version=VersionNumber.v_2_1_1,
                )

                return OCPIResponse(
                    data=[connector.dict()],
                    **status.OCPI_1000_GENERIC_SUCESS_CODE,
                )
        logger.debug("Evse with id `%s` was not found." % evse_uid)
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError


@router.patch(
    "/{country_code}/{party_id}/{location_id}", response_model=OCPIResponse
)
async def partial_update_location(
    request: Request,
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    location_id: String(39),  # type: ignore
    location: LocationPartialUpdate,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    logger.info(
        "Received request to partially update location with id - `%s`."
        % location_id
    )
    logger.debug("Location data to update - %s" % location.dict())
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    old_data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if old_data:
        old_location = adapter.location_adapter(old_data, VersionNumber.v_2_1_1)
        new_location = copy.deepcopy(old_location)

        partially_update_attributes(
            new_location,
            location.dict(exclude_defaults=True, exclude_unset=True),
        )

        data = await crud.update(
            ModuleID.locations,
            RoleEnum.emsp,
            new_location.dict(),
            location_id,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_1_1,
        )

        return OCPIResponse(
            data=[adapter.location_adapter(data, VersionNumber.v_2_1_1).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError


@router.patch(
    "/{country_code}/{party_id}/{location_id}/{evse_uid}",
    response_model=OCPIResponse,
)
async def partial_update_evse(
    request: Request,
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    location_id: String(39),  # type: ignore
    evse_uid: String(39),  # type: ignore
    evse: EVSEPartialUpdate,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    logger.info(
        "Received request to partially update evse by id - `%s` "
        "(location id - `%s`)" % (location_id, evse_uid)
    )
    logger.debug("Evse data to update - %s" % evse.dict())
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    old_data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if old_data:
        old_location = adapter.location_adapter(old_data, VersionNumber.v_2_1_1)
        new_location = copy.deepcopy(old_location)

        for old_evse in old_location.evses:
            if old_evse.uid == evse_uid:
                new_location.evses.remove(old_evse)
                new_evse = copy.deepcopy(old_evse)
                partially_update_attributes(
                    new_evse,
                    evse.dict(exclude_defaults=True, exclude_unset=True),
                )
                new_location.evses.append(new_evse)

                await crud.update(
                    ModuleID.locations,
                    RoleEnum.emsp,
                    new_location.dict(),
                    location_id,
                    auth_token=auth_token,
                    country_code=country_code,
                    party_id=party_id,
                    version=VersionNumber.v_2_1_1,
                )
                return OCPIResponse(
                    data=[new_evse.dict()],
                    **status.OCPI_1000_GENERIC_SUCESS_CODE,
                )
        logger.debug("Evse with id `%s` was not found." % evse_uid)
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError


@router.patch(
    "/{country_code}/{party_id}/{location_id}/{evse_uid}/{connector_id}",
    response_model=OCPIResponse,
)
async def partial_update_connector(
    request: Request,
    country_code: String(2),  # type: ignore
    party_id: String(3),  # type: ignore
    location_id: String(36),  # type: ignore
    evse_uid: String(39),  # type: ignore
    connector_id: String(36),  # type: ignore
    connector: ConnectorPartialUpdate,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    logger.info(
        "Received request to partially update connector by id - `%s` "
        "(location id - `%s`, evse id - `%s`)"
        % (connector_id, location_id, evse_uid)
    )
    logger.debug("Connector data to update - %s" % connector.dict())
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    old_data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_1_1,
    )
    if old_data:
        old_location = adapter.location_adapter(old_data, VersionNumber.v_2_1_1)

        for old_evse in old_location.evses:
            if old_evse.uid == evse_uid:
                for old_connector in old_evse.connectors:
                    if old_connector.id == connector_id:
                        new_connector = old_connector
                        partially_update_attributes(
                            new_connector,
                            connector.dict(
                                exclude_defaults=True, exclude_unset=True
                            ),
                        )
                        new_location = old_location

                        await crud.update(
                            ModuleID.locations,
                            RoleEnum.emsp,
                            new_location.dict(),
                            location_id,
                            auth_token=auth_token,
                            country_code=country_code,
                            party_id=party_id,
                            version=VersionNumber.v_2_1_1,
                        )

                        return OCPIResponse(
                            data=[new_connector.dict()],
                            **status.OCPI_1000_GENERIC_SUCESS_CODE,
                        )
                logger.debug(
                    "Connector with id `%s` was not found." % connector_id
                )
        logger.debug("Evse with id `%s` was not found." % evse_uid)
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError
