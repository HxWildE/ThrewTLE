from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# Ensure all SQLAlchemy models are registered in class registry
import app.db.base  # noqa: F401
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.errors import (
    ThrewTLEException,
    generic_exception_handler,
    threwtle_exception_handler,
)
from app.core.logging import logger
from app.db.session import AsyncSessionLocal
from app.repositories.problem_repo import ProblemRepository
from scripts.seed_initial_problems import seed_problems


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing ThrewTLE Backend Application...")
    # Verify and seed initial database catalogue if empty
    try:
        async with AsyncSessionLocal() as session:
            repo = ProblemRepository(session)
            _, total = await repo.search(limit=1)
            if total == 0:
                logger.info("Catalogue empty on startup; auto-seeding baseline problems...")
                await seed_problems()
            else:
                logger.info(f"Database catalogue active with {total} indexed problems.")
    except Exception as e:
        logger.warning(f"Startup database probe warning: {e}")

    yield
    logger.info("Shutting down ThrewTLE Backend...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Problem-Specific LeetCode Test-Case Generator and Algorithmic Edge-Case Suite",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
app.add_exception_handler(ThrewTLEException, threwtle_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include API Routers
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/docs")
