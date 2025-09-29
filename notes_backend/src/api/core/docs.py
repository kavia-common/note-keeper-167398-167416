from typing import Any, Dict
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

OCEAN_THEME = {
    "primary": "#2563EB",
    "secondary": "#F59E0B",
    "success": "#F59E0B",
    "error": "#EF4444",
    "background": "#f9fafb",
    "surface": "#ffffff",
    "text": "#111827",
}


def _custom_css() -> str:
    # Minimal styling override for Swagger UI/ReDoc to reflect "Ocean Professional"
    return f"""
    :root {{
        --ocean-primary: {OCEAN_THEME['primary']};
        --ocean-secondary: {OCEAN_THEME['secondary']};
        --ocean-text: {OCEAN_THEME['text']};
        --ocean-surface: {OCEAN_THEME['surface']};
        --ocean-bg: {OCEAN_THEME['background']};
    }}

    body, .swagger-ui {{
        background: var(--ocean-bg) !important;
        color: var(--ocean-text);
    }}
    .topbar, .information-container, .opblock-tag-section h3, .scheme-container {{
        background: var(--ocean-surface) !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.1);
        border-radius: 8px;
    }}
    .topbar-wrapper .link span {{
        color: var(--ocean-primary) !important;
    }}
    .btn.execute.opblock-control__btn {{
        background-color: var(--ocean-primary) !important;
    }}
    .btn.clear.opblock-control__btn, .btn.try-out__btn {{
        color: var(--ocean-primary) !important;
        border-color: var(--ocean-primary) !important;
    }}
    .opblock.opblock-post .opblock-summary-method {{
        background: var(--ocean-secondary) !important;
    }}
    .opblock.opblock-get .opblock-summary-method {{
        background: var(--ocean-primary) !important;
    }}
    .opblock.opblock-put .opblock-summary-method {{
        background: #10B981 !important;
    }}
    .opblock.opblock-patch .opblock-summary-method {{
        background: #8B5CF6 !important;
    }}
    .opblock.opblock-delete .opblock-summary-method {{
        background: {OCEAN_THEME['error']} !important;
    }}
    .markdown p, .markdown pre, .info__tos, .info__contact, .info__license {{
        color: var(--ocean-text) !important;
    }}
    """


# PUBLIC_INTERFACE
def oceanize_swagger_ui_html(app: FastAPI) -> HTMLResponse:
    """Return Swagger UI HTML with Ocean Professional theme."""
    html = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Docs",
    ).body.decode("utf-8")

    html = html.replace("</head>", f"<style>{_custom_css()}</style></head>")
    return HTMLResponse(html)


# PUBLIC_INTERFACE
def oceanize_redoc_html(app: FastAPI) -> HTMLResponse:
    """Return ReDoc HTML with Ocean Professional theme."""
    html = get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
    ).body.decode("utf-8")
    html = html.replace("</head>", f"<style>{_custom_css()}</style></head>")
    return HTMLResponse(html)


# PUBLIC_INTERFACE
def get_openapi_schema(app: FastAPI) -> Dict[str, Any]:
    """
    Generate and cache an OpenAPI schema with servers and consistent metadata.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        summary="Note Keeper API",
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["servers"] = [{"url": "/"}]
    app.openapi_schema = openapi_schema
    return openapi_schema
