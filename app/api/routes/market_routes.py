from datetime import date, timedelta

from fastapi import APIRouter, HTTPException

from app.services.market_service import market_service
from app.services.instrument_service import instrument_service
from app.schemas.market import MarketBreadth

router = APIRouter()


@router.get("/status", response_model=MarketBreadth)
async def market_status():
    # Must await — get_market_breadth is async now
    return await market_service.get_market_breadth()


@router.get("/quote/{instrument_key}")
async def get_quote(instrument_key: str):
    """
    Example: /api/market/quote/NSE_EQ|INE002A01018
    """
    try:
        return await market_service.get_market_quote(instrument_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{symbol}")
async def get_history(symbol: str):
    """
    Example: /api/market/history/NIFTY50
    """
    try:
        instrument = instrument_service.get_by_symbol(symbol)

        if instrument is None:
            raise HTTPException(
                status_code=404,
                detail=f"Instrument '{symbol}' not found",
            )

        to_date = date.today()
        from_date = to_date - timedelta(days=7)

        candles = await market_service.get_historical_candles(
            instrument_key=instrument["instrument_key"],
            unit="minutes",
            interval=3,
            to_date=to_date.isoformat(),
            from_date=from_date.isoformat(),
        )

        return {
            "symbol": symbol.upper(),
            "instrument_key": instrument["instrument_key"],
            "interval": "3minute",
            "from_date": from_date.isoformat(),
            "to_date": to_date.isoformat(),
            "candles": candles,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))