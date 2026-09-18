from fastapi import APIRouter

from app.services.fno_universe_service import (
    fno_universe_service
)

router = APIRouter()


@router.get("/universe")
async def get_fno_universe():

    return await fno_universe_service.get_fno_universe()