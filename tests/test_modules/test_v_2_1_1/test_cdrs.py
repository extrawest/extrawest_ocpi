from uuid import uuid4

from fastapi.testclient import TestClient

from py_ocpi import get_application
from py_ocpi.core import enums
from py_ocpi.modules.cdrs.v_2_1_1.enums import AuthMethod, CdrDimensionType
from py_ocpi.modules.versions.enums import VersionNumber

from tests.test_modules.test_v_2_1_1.test_locations import LOCATIONS

CDRS = [
    {
        "id": str(uuid4()),
        "start_date_time": "2022-01-02 00:00:00+00:00",
        "end_date_time": "2022-01-02 00:00:00+00:00",
        "auth_id": "DE8ACC12E46L89",
        "auth_method": AuthMethod.auth_request,
        "location": LOCATIONS[0],
        "currency": "EUR",
        "tariffs": [
            {
                "id": "12",
                "currency": "EUR",
                "elements": [
                    {
                        "price_components": [
                            {"type": "TIME", "price": "2.00", "step_size": 300}
                        ]
                    }
                ],
                "last_updated": "2022-01-02 00:00:00+00:00",
            }
        ],
        "charging_periods": [
            {
                "start_date_time": "2022-01-02 00:00:00+00:00",
                "dimensions": [
                    {"type": CdrDimensionType.time, "volume": 1.973}
                ],
            }
        ],
        "total_cost": 4.00,
        "total_energy": 15.342,
        "total_time": 1.973,
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]


class Crud:
    @classmethod
    async def list(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        filters: dict,
        *args,
        **kwargs,
    ) -> list:
        return CDRS, 1, True

    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        return CDRS[0]

    @classmethod
    async def create(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: dict,
        *args,
        **kwargs,
    ):
        return data


def test_cpo_get_cdrs_v_2_1_1():
    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        modules=[enums.ModuleID.cdrs],
    )

    client = TestClient(app)
    response = client.get("/ocpi/cpo/2.1.1/cdrs")

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["id"] == CDRS[0]["id"]


def test_emsp_get_cdr_v_2_1_1():
    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.emsp],
        crud=Crud,
        modules=[enums.ModuleID.cdrs],
    )

    client = TestClient(app)
    response = client.get(f'/ocpi/emsp/2.1.1/cdrs/{CDRS[0]["id"]}')

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == CDRS[0]["id"]


def test_emsp_add_cdr_v_2_1_1():
    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.emsp],
        crud=Crud,
        modules=[enums.ModuleID.cdrs],
    )

    data = CDRS[0]

    client = TestClient(app)
    response = client.post("/ocpi/emsp/2.1.1/cdrs/", json=data)

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == CDRS[0]["id"]
    assert response.headers["Location"] is not None
