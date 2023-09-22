from fastapi import APIRouter

from py_ocpi.modules.credentials.v_2_1_1.api import (
    cpo_router as credentials_cpo_2_1_1_router,
)
from py_ocpi.modules.locations.v_2_1_1.api import (
    cpo_router as locations_cpo_2_1_1_router,
)


router = APIRouter()

router.include_router(locations_cpo_2_1_1_router)
router.include_router(credentials_cpo_2_1_1_router)
