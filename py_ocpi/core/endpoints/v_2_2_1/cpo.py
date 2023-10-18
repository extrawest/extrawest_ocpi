from py_ocpi.core.enums import ModuleID
from py_ocpi.core.data_types import URL
from py_ocpi.core.config import settings
from py_ocpi.modules.versions.v_2_2_1.schemas import (
    Endpoint,
    InterfaceRole,
    VersionNumber,
)

URL_BASE = (
    f"{settings.PROTOCOL}://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/"
    f"cpo/{VersionNumber.v_2_2_1.value}"
)

CREDENTIALS_AND_REGISTRATION = Endpoint(
    identifier=ModuleID.credentials_and_registration,
    role=InterfaceRole.receiver,
    url=URL(f"{URL_BASE}/{ModuleID.credentials_and_registration.value}/"),
)

LOCATIONS = Endpoint(
    identifier=ModuleID.locations,
    role=InterfaceRole.sender,
    url=URL(f"{URL_BASE}/{ModuleID.locations.value}/"),
)

SESSIONS = Endpoint(
    identifier=ModuleID.sessions,
    role=InterfaceRole.sender,
    url=URL(f"{URL_BASE}/{ModuleID.sessions.value}/"),
)

CDRS = Endpoint(
    identifier=ModuleID.cdrs,
    role=InterfaceRole.sender,
    url=URL(f"{URL_BASE}/{ModuleID.cdrs.value}/"),
)

TARIFFS = Endpoint(
    identifier=ModuleID.tariffs,
    role=InterfaceRole.sender,
    url=URL(f"{URL_BASE}/{ModuleID.tariffs.value}/"),
)

TOKENS = Endpoint(
    identifier=ModuleID.tokens,
    role=InterfaceRole.receiver,
    url=URL(f"{URL_BASE}/{ModuleID.tokens.value}/"),
)

ENDPOINTS_LIST = {
    ModuleID.credentials_and_registration: CREDENTIALS_AND_REGISTRATION,
    ModuleID.locations: LOCATIONS,
    ModuleID.sessions: SESSIONS,
    ModuleID.cdrs: CDRS,
    ModuleID.tariffs: TARIFFS,
    ModuleID.tokens: TOKENS,
}
