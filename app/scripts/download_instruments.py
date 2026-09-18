import json
import gzip
import httpx
from pathlib import Path


UPSTOX_INSTRUMENT_URL = (
    "https://assets.upstox.com/"
    "market-quote/instruments/exchange/NSE.json.gz"
)


OUTPUT_FILE = (
    Path(__file__)
    .parent
    .parent
    / "data"
    / "stocks.json"
)



def download_instruments():

    print("Downloading Upstox instruments...")


    response = httpx.get(
        UPSTOX_INSTRUMENT_URL,
        timeout=60
    )


    response.raise_for_status()


    data = gzip.decompress(
        response.content
    )


    instruments = json.loads(
        data
    )


    print(
        f"Total instruments: {len(instruments)}"
    )


    stocks = []


    for item in instruments:

        if (
            item.get("segment") == "NSE_EQ"
            and item.get("instrument_type") == "EQ"
        ):

            stocks.append(
                {
                    "symbol": item.get(
                        "trading_symbol"
                    ),
                    "instrument_key": item.get(
                        "instrument_key"
                    ),
                    "exchange": "NSE"
                }
            )


    OUTPUT_FILE.parent.mkdir(
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            stocks,
            f,
            indent=4
        )


    print(
        f"Saved {len(stocks)} stocks"
    )



if __name__ == "__main__":

    download_instruments()