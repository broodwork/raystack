from fastapi import APIRouter

from .urls import router as urls_router


router = APIRouter(include_in_schema=False)
router.include_router(urls_router)