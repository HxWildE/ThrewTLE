from fastapi import APIRouter
from app.api.v1.endpoints import generate, health, problems

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(problems.router, tags=["Problems"])
api_router.include_router(generate.router, tags=["Generate"])
