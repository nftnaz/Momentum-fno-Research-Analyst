import json
from pathlib import Path


class InstrumentService:

    def __init__(self):

        file_path = (
            Path(__file__)
            .parent.parent
            / "data"
            / "instruments.json"
        )

        with open(file_path, "r") as f:
            self.instruments = json.load(f)

    def get_all(self):
        return self.instruments

    def get_by_symbol(self, symbol: str):

        symbol = symbol.upper()

        for instrument in self.instruments:

            if instrument["symbol"] == symbol:
                return instrument

        return None


instrument_service = InstrumentService()