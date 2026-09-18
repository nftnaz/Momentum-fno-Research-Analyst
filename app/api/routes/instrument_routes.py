from fastapi import APIRouter, HTTPException

from app.services.instrument_service import instrument_service

router = APIRouter()


@router.get("/")
async def get_all_instruments():

    return instrument_service.get_all()


@router.get("/{symbol}")
async def get_instrument(symbol: str):

    instrument = instrument_service.get_by_symbol(symbol)

    if instrument is None:

        raise HTTPException(
            status_code=404,
            detail="Instrument not found"
        )

    return instrument