from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.customers import router as customers_router
from app.api.routes.documents import router as documents_router
from app.api.routes.health import router as health_router
from app.api.routes.proposals import router as proposals_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "AI-powered life insurance sampling "
        "and risk assessment system."
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    health_router,
    prefix="/api",
)

app.include_router(
    customers_router,
    prefix="/api",
)

app.include_router(
    proposals_router,
    prefix="/api",
)

app.include_router(
    documents_router,
    prefix="/api",
)


@app.get("/")
async def root():
    return {
        "message": "AI Insurance Sampler API is running",
        "version": settings.app_version,
    }