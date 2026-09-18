import httpx

from fastapi import HTTPException

from app.core.config import settings


class InstrumentSearchService:

    def __init__(self):

        self.base_url = settings.UPSTOX_BASE_URL.rstrip("/")

        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.UPSTOX_ACCESS_TOKEN}"
        }

    # --------------------------------------------------
    # Search Instruments
    # --------------------------------------------------

    async def search(self, query: str):

        url = f"{self.base_url}/v2/instruments/search"

        params = {
            "query": query,
            "segments": "OPT",
            "expiry": "current_month",
            "atm_offset": 0,
            "page_number": 1,
            "records": 30
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
                detail=e.response.text
            )

        return response.json()

    # --------------------------------------------------
    # Search Option Contracts
    # --------------------------------------------------

    async def get_option_contracts(
        self,
        symbol: str
    ):

        result = await self.search(symbol)

        print("\n==============================")
        print("Instrument Search")
        print(result)
        print("==============================\n")

        return result


instrument_search_service = InstrumentSearchService()