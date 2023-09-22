from py_ocpi.core.enums import ModuleID

from py_ocpi.modules.credentials.v_2_1_1.api import (
    cpo_router as credentials_cpo_2_1_1_router,
)
from py_ocpi.modules.locations.v_2_1_1.api import (
    cpo_router as locations_cpo_2_1_1_router,
)


router = {
    ModuleID.locations: locations_cpo_2_1_1_router,
    ModuleID.credentials_and_registration: credentials_cpo_2_1_1_router,
}
