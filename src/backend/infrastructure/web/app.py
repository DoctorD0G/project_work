import traceback
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from starlette.responses import RedirectResponse

from infrastructure.config import app_settings
from infrastructure.container import init_container
from infrastructure.web.api.api_v1.api import api_router
from infrastructure.web.api.exceptions import FormFieldValidationException
from infrastructure.web.config import web_settings


container = init_container()
app_manager_service = container.app_manager_service()
fastapi_user_container = container.fastapi_user_container()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # подключаем роуты fastapi_user
    fastapi_user_container.manager_router.enable_async_mode()
    fastapi_user_container.role_router.enable_async_mode()
    fastapi_user_container.auth_router.enable_async_mode()

    app.include_router(
        await fastapi_user_container.manager_router(),
        prefix="/api/v1/user-manager",
        tags=["user-manager"],
    )
    app.include_router(
        await fastapi_user_container.auth_router(),
        prefix="/api/v1/user-auth",
        tags=["user-auth"],
    )
    app.include_router(
        await fastapi_user_container.role_router(),
        prefix="/api/v1/user-role",
        tags=["user-role"],
    )

    yield


app = FastAPI(
    title=app_settings.PROJECT_NAME,
    openapi_url=f"{web_settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)
app.include_router(api_router, prefix=web_settings.API_V1_STR)


app.add_middleware(
    CORSMiddleware,
    allow_origins=web_settings.APP_CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(FormFieldValidationException)
async def validation_exception_handler(_: Request, exc: FormFieldValidationException):
    return JSONResponse(status_code=exc.status_code, content=exc.fields)


@app.exception_handler(HTTPException)
async def http_validation_exception_handler(_: Request, exc: HTTPException):
    content = {"detail": exc.detail}

    if await app_manager_service.is_app_on_debug():
        traceback_data = traceback.format_exception(
            exc, value=exc, tb=exc.__traceback__
        )
        content["traceback"] = traceback_data

    return JSONResponse(status_code=exc.status_code, content=content)


sentry_sdk.init(
    dsn=web_settings.SENTRY_DSN,
    environment=web_settings.SENTRY_ENVIRONMENT,
    traces_sample_rate=web_settings.SENTRY_TRACES_SAMPLE_RATE,
    send_default_pii=True,
    integrations=[
        StarletteIntegration(
            transaction_style="endpoint",
        ),
        FastApiIntegration(
            transaction_style="endpoint",
        ),
    ],
)
sentry_sdk.utils.MAX_STRING_LENGTH = 2048


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return RedirectResponse(url="/docs")


container.wire(packages=["infrastructure.web.api", "common", __name__])
