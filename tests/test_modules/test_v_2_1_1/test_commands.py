import datetime
from uuid import uuid4

from fastapi.testclient import TestClient

from py_ocpi import get_application
from py_ocpi.core import enums
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.modules.tokens.v_2_1_1.enums import TokenType, WhitelistType
from py_ocpi.modules.commands.v_2_1_1.enums import (
    CommandType,
    CommandResponseType,
)
from py_ocpi.modules.versions.enums import VersionNumber

from tests.test_modules.test_v_2_1_1.test_tokens import TOKENS

COMMAND_RESPONSE = {"result": CommandResponseType.accepted}


class Crud:
    @classmethod
    async def do(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        action: enums.Action,
        *args,
        data: dict = None,
        **kwargs,
    ) -> dict:
        if action == enums.Action.get_client_token:
            return "foo"

        return COMMAND_RESPONSE

    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ) -> dict:
        return COMMAND_RESPONSE

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
        ...


def test_cpo_receive_command_start_session_v_2_1_1():
    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        modules=[enums.ModuleID.commands, enums.ModuleID.sessions],
    )

    data = {
        "response_url": "https://dummy.restapiexample.com/api/v1/create",
        "token": TOKENS[0],
        "location_id": str(uuid4()),
    }

    client = TestClient(app)
    response = client.post(
        f"/ocpi/cpo/2.1.1/commands/{CommandType.start_session.value}", json=data
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["result"] == COMMAND_RESPONSE["result"]


def test_cpo_receive_command_stop_session_v_2_1_1():
    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        modules=[enums.ModuleID.commands, enums.ModuleID.sessions],
    )

    data = {
        "response_url": "https://dummy.restapiexample.com/api/v1/create",
        "session_id": str(uuid4()),
    }

    client = TestClient(app)
    response = client.post(
        f"/ocpi/cpo/2.1.1/commands/{CommandType.stop_session.value}", json=data
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["result"] == COMMAND_RESPONSE["result"]


def test_cpo_receive_command_reserve_now_v_2_1_1():
    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        modules=[enums.ModuleID.commands],
    )

    data = {
        "response_url": "https://dummy.restapiexample.com/api/v1/create",
        "token": TOKENS[0],
        "expiry_date": str(
            datetime.datetime.now() + datetime.timedelta(days=1)
        ),
        "reservation_id": 0,
        "location_id": str(uuid4()),
    }

    client = TestClient(app)
    response = client.post(
        f"/ocpi/cpo/2.1.1/commands/{CommandType.reserve_now.value}", json=data
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["result"] == COMMAND_RESPONSE["result"]


def test_cpo_receive_command_reserve_now_unknown_location_v_2_1_1():
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ) -> dict:
        if module == enums.ModuleID.commands:
            return COMMAND_RESPONSE
        if module == enums.ModuleID.locations:
            raise NotFoundOCPIError()

    _get = Crud.get
    Crud.get = get

    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        modules=[enums.ModuleID.commands],
    )

    data = {
        "response_url": "https://dummy.restapiexample.com/api/v1/create",
        "token": TOKENS[0],
        "expiry_date": str(
            datetime.datetime.now() + datetime.timedelta(days=1)
        ),
        "reservation_id": 0,
        "location_id": str(uuid4()),
    }

    client = TestClient(app)
    response = client.post(
        f"/ocpi/cpo/2.1.1/commands/{CommandType.reserve_now.value}", json=data
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["result"] == CommandResponseType.rejected

    # revert Crud changes
    Crud.get = _get


def test_emsp_receive_command_result_v_2_1_1():
    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.emsp],
        crud=Crud,
        modules=[enums.ModuleID.commands],
    )

    client = TestClient(app)
    response = client.post(
        "/ocpi/emsp/2.1.1/commands/1234", json=COMMAND_RESPONSE
    )

    assert response.status_code == 200