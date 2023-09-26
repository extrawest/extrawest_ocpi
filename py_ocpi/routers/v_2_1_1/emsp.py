from py_ocpi.core.enums import ModuleID

from py_ocpi.modules.credentials.v_2_1_1.api import (
    emsp_router as credentials_emsp_2_1_1_router,
)
from py_ocpi.modules.locations.v_2_1_1.api import (
    emsp_router as locations_emsp_2_1_1_router,
)


router = {
    ModuleID.locations: locations_emsp_2_1_1_router,
    ModuleID.credentials_and_registration: credentials_emsp_2_1_1_router,
}
