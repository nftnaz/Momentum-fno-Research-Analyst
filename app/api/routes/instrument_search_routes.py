from fastapi import APIRouter

from app.services.instrument_search_service import (
    instrument_search_service
)

router = APIRouter()


@router.get("/{symbol}")
async def search(symbol: str):

    return await instrument_search_service.get_option_contracts(
        symbol
    )