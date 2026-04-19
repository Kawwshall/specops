from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

REQUIRED_ENV = [
    "APPSCRIPT_URL", "APPSCRIPT_SECRET",
    "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REDIRECT_URI",
    "JWT_SECRET", "ENCRYPTION_KEY", "FRONTEND_URL",
]
_missing = [k for k in REQUIRED_ENV if not os.environ.get(k)]
if _missing:
    raise SystemExit(f"FATAL: missing required env vars: {', '.join(_missing)}")

from routers import submissions, auth

app = FastAPI(title="SpecOps Onboarding")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(submissions.router, prefix="/submit", tags=["submit"])

@app.get("/health")
async def health():
    return {"status": "ok"}
