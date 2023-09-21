from py_ocpi.core.enums import ModuleID
from py_ocpi.core.data_types import URL
from py_ocpi.core.config import settings
from py_ocpi.modules.versions.v_2_1_1.schemas import (
    Endpoint,
    VersionNumber,
)


CREDENTIALS_AND_REGISTRATION = Endpoint(
    identifier=ModuleID.credentials_and_registration,
    url=URL(
        f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp"
        f"/{VersionNumber.v_2_1_1.value}/"
        f"{ModuleID.credentials_and_registration.value}"
    ),
)

LOCATIONS = Endpoint(
    identifier=ModuleID.locations,
    url=URL(
        f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp"
        f"/{VersionNumber.v_2_1_1.value}/{ModuleID.locations.value}"
    ),
)

ENDPOINTS_LIST = [
    CREDENTIALS_AND_REGISTRATION,
    LOCATIONS,
]
