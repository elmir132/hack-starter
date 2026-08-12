"""FastAPI entry point for Hack Starter."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from app.core import build_brief


ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"

app = FastAPI(
    title="Hack Starter",
    description="A tiny, inspectable starting point for a hackathon demo.",
    version="0.1.0",
)


class BriefRequest(BaseModel):
    project_name: str = Field(min_length=2, max_length=60)
    audience: str = Field(min_length=2, max_length=120)
    problem: str = Field(min_length=3, max_length=240)
    approach: str = Field(min_length=3, max_length=240)

    @field_validator("project_name", "audience", "problem", "approach")
    @classmethod
    def strip_and_require_text(cls, value):
        clean = value.strip()
        if not clean:
            raise ValueError("This field cannot be blank.")
        return clean


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    if request.url.path not in {"/docs", "/redoc", "/docs/oauth2-redirect"}:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
            "connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"
        )
    return response


@app.get("/api/health")
def health():
    return {"ok": True, "mode": "deterministic-template", "model_configured": False}


@app.post("/api/brief")
def create_brief(payload: BriefRequest):
    return build_brief(**payload.model_dump())


# Keep the static mount last so it cannot shadow API endpoints.
app.mount("/", StaticFiles(directory=WEB, html=True), name="web")
