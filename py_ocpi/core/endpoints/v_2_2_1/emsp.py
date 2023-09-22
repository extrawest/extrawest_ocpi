from py_ocpi.core.enums import ModuleID
from py_ocpi.core.data_types import URL
from py_ocpi.core.config import settings
from py_ocpi.modules.versions.v_2_2_1.schemas import (
    Endpoint,
    InterfaceRole,
    VersionNumber,
)


CREDENTIALS_AND_REGISTRATION = Endpoint(
    identifier=ModuleID.credentials_and_registration,
    role=InterfaceRole.receiver,
    url=URL(
        f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp"
        f"/{VersionNumber.v_2_2_1.value}/"
        f"{ModuleID.credentials_and_registration.value}"
    ),
)

LOCATIONS = Endpoint(
    identifier=ModuleID.locations,
    role=InterfaceRole.receiver,
    url=URL(
        f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp"
        f"/{VersionNumber.v_2_2_1.value}/{ModuleID.locations.value}"
    ),
)

SESSIONS = Endpoint(
    identifier=ModuleID.sessions,
    role=InterfaceRole.receiver,
    url=URL(
        f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp"
        f"/{VersionNumber.v_2_2_1.value}/{ModuleID.sessions.value}"
    ),
)

CDRS = Endpoint(
    identifier=ModuleID.cdrs,
    role=InterfaceRole.receiver,
    url=URL(
        f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp"
        f"/{VersionNumber.v_2_2_1.value}/{ModuleID.cdrs.value}"
    ),
)

TARIFFS = Endpoint(
    identifier=ModuleID.tariffs,
    role=InterfaceRole.receiver,
    url=URL(
        f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp"
        f"/{VersionNumber.v_2_2_1.value}/{ModuleID.tariffs.value}"
    ),
)

COMMANDS = Endpoint(
    identifier=ModuleID.commands,
    role=InterfaceRole.sender,
    url=URL(
        f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp"
        f"/{VersionNumber.v_2_2_1.value}/{ModuleID.commands.value}"
    ),
)

TOKENS = Endpoint(
    identifier=ModuleID.tokens,
    role=InterfaceRole.sender,
    url=URL(
        f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp"
        f"/{VersionNumber.v_2_2_1.value}/{ModuleID.tokens.value}"
    ),
)

ENDPOINTS_LIST = [
    CREDENTIALS_AND_REGISTRATION,
    LOCATIONS,
    SESSIONS,
    CDRS,
    TARIFFS,
    COMMANDS,
    TOKENS,
]
