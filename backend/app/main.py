from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import get_settings
from app.core.database import engine, Base
from app.core.rate_limit import limiter
from app.core.error_handlers import rate_limit_handler, general_exception_handler
from app.api.routes import campaign, image, seasonal


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Debug mode: {settings.debug}")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created")

    yield

    await engine.dispose()
    print("Shutting down application")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API for generating UK-focused social media marketing content using AI",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.app_version,
    }


app.include_router(campaign.router, prefix="/api/v1")
app.include_router(image.router, prefix="/api/v1")
app.include_router(seasonal.router, prefix="/api/v1")
