from py_ocpi.core.enums import ModuleID
from py_ocpi.core.data_types import URL
from py_ocpi.core.config import settings
from py_ocpi.modules.versions.v_2_1_1.schemas import (
    Endpoint,
    VersionNumber,
)

URL_BASE = (
    f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/"
    f"cpo/{VersionNumber.v_2_1_1.value}/"
)


CREDENTIALS_AND_REGISTRATION = Endpoint(
    identifier=ModuleID.credentials_and_registration,
    url=URL(f"{URL_BASE}/{ModuleID.credentials_and_registration.value}"),
)

LOCATIONS = Endpoint(
    identifier=ModuleID.locations,
    url=URL(f"{URL_BASE}/{ModuleID.locations.value}"),
)

CDRS = Endpoint(
    identifier=ModuleID.cdrs,
    url=URL(f"{URL_BASE}/{ModuleID.cdrs.value}"),
)

ENDPOINTS_LIST = {
    ModuleID.credentials_and_registration: CREDENTIALS_AND_REGISTRATION,
    ModuleID.locations: LOCATIONS,
    ModuleID.cdrs: CDRS,
}
