import httpx

from fastapi import HTTPException

from app.core.config import settings


class FnOUniverseService:

    def __init__(self):

        self.base_url = settings.UPSTOX_BASE_URL.rstrip("/")

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.UPSTOX_ACCESS_TOKEN}"
        }

    # ---------------------------------------------------------
    # Get FnO Universe
    # ---------------------------------------------------------

    async def get_fno_universe(self):

        url = f"{self.base_url}/v2/market/smartlist/futures"

        params = {
            "asset_type": "STOCK",
            "category": "TOP_TRADED",
            "page_number": 1,
            "page_size": 500
        }

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.get(
                url,
                headers=self.headers,
                params=params
            )

        try:
            response.raise_for_status()

        except httpx.HTTPStatusError as e:

            raise HTTPException(
                status_code=502,
                detail=f"Upstox SmartList Error : {e.response.text}"
            )

        data = response.json()

        print("\n==============================")
        print("FnO Smartlist Response")
        print(data)
        print("==============================\n")

        if data.get("status") != "success":

            raise HTTPException(
                status_code=502,
                detail="Unable to fetch FnO universe."
            )

        instruments = []

        for item in data.get("data", []):

            instruments.append(
                {
                    "symbol": item.get("trading_symbol"),
                    "instrument_key": item.get("instrument_key"),
                    "exchange": item.get("exchange"),
                    "name": item.get("name"),
                    "lot_size": item.get("lot_size"),
                    "expiry": item.get("expiry"),
                }
            )

        return instruments


fno_universe_service = FnOUniverseService()