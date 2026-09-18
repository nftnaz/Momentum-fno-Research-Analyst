import httpx

from app.core.config import settings


class OptionQuoteService:

    def __init__(self):

        self.base_url = settings.UPSTOX_BASE_URL.rstrip("/")

        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.UPSTOX_ACCESS_TOKEN}",
        }

    async def get_quote(
        self,
        instrument_key: str,
    ):

        url = f"{self.base_url}/v2/market-quote/quotes"

        params = {
            "instrument_key": instrument_key
        }

        async with httpx.AsyncClient(timeout=20) as client:

            response = await client.get(
                url,
                headers=self.headers,
                params=params,
            )

        response.raise_for_status()

        data = response.json()

        if (
            data.get("status") != "success"
            or not data.get("data")
        ):
            return None

        quote = next(iter(data["data"].values()))

        return {

            "symbol": quote.get("symbol"),

            "last_price": quote.get("last_price"),

            "volume": quote.get("volume"),

            "oi": quote.get("oi"),

            "change": quote.get("net_change"),

            "change_percent": quote.get(
                "net_change_percentage"
            ),

            "timestamp": quote.get("timestamp"),

        }


option_quote_service = OptionQuoteService()