from fastapi import APIRouter

from .urls import router as urls_router


router = APIRouter()
router.include_router(urls_router, include_in_schema=False)