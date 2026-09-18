from fastapi import APIRouter

from app.services.option_scanner_service import (
    option_scanner_service,
)

router = APIRouter(
    prefix="/options",
    tags=["Options Scanner"],
)


@router.get("/scan")
async def scan_options():

    return await option_scanner_service.scan_options()