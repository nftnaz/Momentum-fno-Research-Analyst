from fastapi import APIRouter, HTTPException

from app.services.signal_service import signal_service

router = APIRouter()


@router.get("/")
async def get_signals():

    try:
        return await signal_service.get_all_signals()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/{symbol}")
async def get_signal(symbol: str):

    signal = await signal_service.get_signal(symbol)

    if signal is None:

        raise HTTPException(
            status_code=404,
            detail="Signal not found"
        )

    return signal


@router.post("/generate")
async def generate_signal(symbol: str):

    signal = await signal_service.generate_signal(symbol)

    if signal is None:

        raise HTTPException(
            status_code=404,
            detail="Signal not found"
        )

    return signal


@router.post("/{signal_id}/telegram")
async def send_telegram(signal_id: str):

    signal = signal_service.mark_telegram_sent(signal_id)

    if signal is None:

        raise HTTPException(
            status_code=404,
            detail="Signal not found"
        )

    return {
        "success": True,
        "message": f"Telegram alert sent for {signal.symbol}",
        "signal": signal,
    }