from typing import Any

from fastapi.testclient import TestClient

from py_ocpi.main import get_application
from py_ocpi.core import enums
from py_ocpi.core.crud import Crud
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.enums import ModuleID, RoleEnum, Action


def test_get_versions():
    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        modules=[],
    )

    client = TestClient(app)
    response = client.get("/ocpi/versions")

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_get_versions_v_2_1_1():
    token = None

    class MockCrud(Crud):
        @classmethod
        async def do(
            cls,
            module: ModuleID,
            role: RoleEnum,
            action: Action,
            auth_token,
            *args,
            data: dict = None,
            **kwargs,
        ) -> Any:
            nonlocal token
            token = auth_token
            return {}

    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.cpo],
        crud=MockCrud,
        modules=[],
    )

    client = TestClient(app)
    response = client.get(
        "/ocpi/2.1.1/details", headers={"authorization": "Token Zm9v"}
    )

    assert response.status_code == 200
    assert response.json()["data"]["version"] == "2.1.1"
    assert token == "Zm9v"


def test_get_versions_v_2_1_1_requires_auth():
    class MockCrud(Crud):
        @classmethod
        async def do(
            cls,
            module: ModuleID,
            role: RoleEnum,
            action: Action,
            auth_token,
            *args,
            data: dict = None,
            **kwargs,
        ) -> Any:
            return None

    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.cpo],
        crud=MockCrud,
        modules=[],
    )

    client = TestClient(app)
    response = client.get("/ocpi/2.1.1/details")

    assert response.status_code == 401
