from typing import Any, List

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from py_ocpi.core.endpoints import ENDPOINTS

from py_ocpi.modules.versions import router as versions_router
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.versions.schemas import Version
from py_ocpi.core.dependencies import (
    get_crud,
    get_adapter,
    get_versions,
    get_endpoints,
    get_modules,
)
from py_ocpi.core import status
from py_ocpi.core.adapter import BaseAdapter
from py_ocpi.core.enums import RoleEnum, ModuleID
from py_ocpi.core.config import settings
from py_ocpi.core.data_types import URL
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.exceptions import AuthorizationOCPIError, NotFoundOCPIError
from py_ocpi.core.push import (
    http_router as http_push_router,
    websocket_router as websocket_push_router,
)
from py_ocpi.core.routers import ROUTERS


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        try:
            response = await call_next(request)
        except AuthorizationOCPIError as e:
            raise HTTPException(403, str(e)) from e
        except NotFoundOCPIError as e:
            raise HTTPException(404, str(e)) from e
        except ValidationError:
            response = JSONResponse(
                OCPIResponse(
                    data=[],
                    **status.OCPI_3000_GENERIC_SERVER_ERROR,
                ).dict()
            )
        return response


def get_application(
    version_numbers: List[VersionNumber],
    roles: List[RoleEnum],
    crud: Any,
    modules: List[ModuleID],
    adapter: Any = BaseAdapter,
    http_push: bool = False,
    websocket_push: bool = False,
) -> FastAPI:
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url=f"/{settings.OCPI_PREFIX}/docs",
        openapi_url=f"/{settings.OCPI_PREFIX}/openapi.json",
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.add_middleware(ExceptionHandlerMiddleware)

    _app.include_router(
        versions_router,
        prefix=f"/{settings.OCPI_PREFIX}",
    )

    if http_push:
        _app.include_router(
            http_push_router,
            prefix=f"/{settings.PUSH_PREFIX}",
        )

    if websocket_push:
        _app.include_router(
            websocket_push_router,
            prefix=f"/{settings.PUSH_PREFIX}",
        )

    versions = []
    version_endpoints: dict[str, list] = {}

    for version in version_numbers:
        mapped_version = ROUTERS.get(version)
        if not mapped_version:
            raise ValueError("Version isn't supported yet.")

        _app.include_router(
            mapped_version["version_router"],
            prefix=f"/{settings.OCPI_PREFIX}",
        )

        versions.append(
            Version(
                version=version,
                url=URL(
                    f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/"
                    f"{version.value}/details"
                ),
            ).dict(),
        )

        version_endpoints[version] = []

        if RoleEnum.cpo in roles:
            for module in modules:
                cpo_router = mapped_version["cpo_router"].get(module)
                if cpo_router:
                    _app.include_router(
                        cpo_router,
                        prefix=f"/{settings.OCPI_PREFIX}/cpo/{version.value}",
                        tags=[f"CPO {version}"],
                    )
                    version_endpoints[version] += ENDPOINTS[version][
                        RoleEnum.cpo
                    ]

        if RoleEnum.emsp in roles:
            for module in modules:
                emsp_router = mapped_version["emsp_router"].get(module)
                if emsp_router:
                    _app.include_router(
                        emsp_router,
                        prefix=f"/{settings.OCPI_PREFIX}/emsp/{version.value}",
                        tags=[f"EMSP {version}"],
                    )
                    version_endpoints[version] += ENDPOINTS[version][
                        RoleEnum.emsp
                    ]

    def override_get_crud():
        return crud

    _app.dependency_overrides[get_crud] = override_get_crud

    def override_get_adapter():
        return adapter

    _app.dependency_overrides[get_adapter] = override_get_adapter

    def override_get_versions():
        return versions

    _app.dependency_overrides[get_versions] = override_get_versions

    def override_get_endpoints():
        return version_endpoints

    _app.dependency_overrides[get_endpoints] = override_get_endpoints

    def override_get_modules():
        return modules

    _app.dependency_overrides[get_modules] = override_get_modules()

    return _app
