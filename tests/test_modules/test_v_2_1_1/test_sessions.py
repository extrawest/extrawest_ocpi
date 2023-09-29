from uuid import uuid4

from fastapi.testclient import TestClient

from py_ocpi.main import get_application
from py_ocpi.core import enums
from py_ocpi.core.config import settings
from py_ocpi.modules.cdrs.v_2_1_1.enums import AuthMethod, CdrDimensionType
from py_ocpi.modules.sessions.v_2_1_1.enums import SessionStatus
from py_ocpi.modules.versions.enums import VersionNumber

from tests.test_modules.test_v_2_1_1.test_locations import LOCATIONS

SESSIONS = [
    {
        "id": str(uuid4()),
        "start_datetime": "2022-01-02 00:00:00+00:00",
        "end_datetime": "2022-01-02 00:05:00+00:00",
        "kwh": 100,
        "auth_id": "100",
        "auth_method": AuthMethod.auth_request,
        "location": LOCATIONS[0],
        "currency": "MYR",
        "charging_periods": [
            {
                "start_date_time": "2022-01-02 00:00:00+00:00",
                "dimensions": [
                    {
                        "type": CdrDimensionType.time,
                        "volume": 10,
                    }
                ],
            }
        ],
        "status": SessionStatus.active,
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]


class Crud:
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        return SESSIONS[0]

    @classmethod
    async def update(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: dict,
        id,
        *args,
        **kwargs,
    ):
        return data

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

    @classmethod
    async def list(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        filters: dict,
        *args,
        **kwargs,
    ) -> list:
        return SESSIONS, 1, True


def test_cpo_get_sessions_v_2_1_1():
    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        modules=[enums.ModuleID.sessions],
    )

    client = TestClient(app)
    response = client.get("/ocpi/cpo/2.1.1/sessions")

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["id"] == SESSIONS[0]["id"]


def test_emsp_get_session_v_2_1_1():
    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.emsp],
        crud=Crud,
        modules=[enums.ModuleID.sessions],
    )

    client = TestClient(app)
    response = client.get(
        f"/ocpi/emsp/2.1.1/sessions/{settings.COUNTRY_CODE}/{settings.PARTY_ID}"
        f'/{SESSIONS[0]["id"]}'
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == SESSIONS[0]["id"]


def test_emsp_add_session_v_2_1_1():
    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.emsp],
        crud=Crud,
        modules=[enums.ModuleID.sessions],
    )

    client = TestClient(app)
    response = client.put(
        f"/ocpi/emsp/2.1.1/sessions/{settings.COUNTRY_CODE}/{settings.PARTY_ID}"
        f'/{SESSIONS[0]["id"]}',
        json=SESSIONS[0],
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == SESSIONS[0]["id"]


def test_emsp_patch_session_v_2_1_1():
    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.emsp],
        crud=Crud,
        modules=[enums.ModuleID.sessions],
    )

    patch_data = {"id": str(uuid4())}
    client = TestClient(app)
    response = client.patch(
        f"/ocpi/emsp/2.1.1/sessions/{settings.COUNTRY_CODE}/{settings.PARTY_ID}"
        f'/{SESSIONS[0]["id"]}',
        json=patch_data,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == patch_data["id"]
