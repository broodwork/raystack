from fastapi import APIRouter, Request
from apps.admin.urls import router as admin_urls

router = APIRouter()
router.include_router(admin_urls, include_in_schema=False)
