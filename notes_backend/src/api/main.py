from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

from .routers import notes
from .core.settings import get_app_settings
from .core.docs import oceanize_swagger_ui_html, oceanize_redoc_html, get_openapi_schema

# Initialize app with metadata matching style guide and production readiness
settings = get_app_settings()
app = FastAPI(
    title="Note Keeper API",
    description=(
        "A modern, clean RESTful API for managing notes. "
        "Create, read, update, and delete notes with a simple interface."
    ),
    version="1.0.0",
    contact={"name": "Note Keeper", "url": "https://example.com"},
    license_info={"name": "MIT"},
    openapi_tags=[
        {
            "name": "Health",
            "description": "Service health and readiness.",
        },
        {
            "name": "Notes",
            "description": "CRUD operations for notes and related actions.",
        },
        {
            "name": "Docs",
            "description": "Documentation and usage references.",
        },
    ],
)

# CORS (wide-open by default; adjust via env in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(notes.router, prefix="/api", tags=["Notes"])


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
    description="Returns service health and readiness status.",
    response_model=dict,
)
def health_check():
    """Health endpoint to verify service is operational."""
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.get(
    "/docs-theme",
    include_in_schema=False,
)
def themed_swagger_ui() -> HTMLResponse:
    """
    Returns a themed Swagger UI leveraging the 'Ocean Professional' palette.
    """
    return oceanize_swagger_ui_html(app=app)


# PUBLIC_INTERFACE
@app.get(
    "/redoc-theme",
    include_in_schema=False,
)
def themed_redoc() -> HTMLResponse:
    """
    Returns a themed ReDoc UI leveraging the 'Ocean Professional' palette.
    """
    return oceanize_redoc_html(app=app)


# Override default OpenAPI generation to add servers + descriptions consistently
app.openapi = lambda: get_openapi_schema(app)
