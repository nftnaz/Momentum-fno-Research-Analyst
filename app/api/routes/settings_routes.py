from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_settings():
    return {
        "app_name": "AI Stock Research Platform",
        "market": "NSE",
        "default_exchange": "NSE",
        "default_timeframe": "1D",
        "scanner_enabled": True
    }


@router.put("/")
def update_settings(settings: dict):
    return {
        "message": "Settings updated successfully",
        "settings": settings
    }