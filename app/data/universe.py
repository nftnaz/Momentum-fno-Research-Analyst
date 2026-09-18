import json
from pathlib import Path


STOCK_FILE = Path(__file__).parent / "stocks.json"


def load_all_stocks():
    with open(STOCK_FILE, "r") as file:
        return json.load(file)


def load_fno_universe():
    """
    Liquid NSE F&O equity universe used by the momentum scanner.
    Symbols must exist in stocks.json (instrument_key required).
    """

    stocks = load_all_stocks()

    # Broad liquid F&O-style universe (equity underlyings)
    preferred_symbols = {
        # Banks / Financials
        "HDFCBANK", "ICICIBANK", "SBIN", "AXISBANK", "KOTAKBANK",
        "INDUSINDBK", "BANDHANBNK", "FEDERALBNK", "IDFCFIRSTB",
        "PNB", "BANKBARODA", "AUBANK", "CHOLAFIN", "BAJFINANCE",
        "BAJAJFINSV", "HDFCLIFE", "SBILIFE", "ICICIPRULI", "PFC", "RECLTD",
        # IT
        "TCS", "INFY", "WIPRO", "HCLTECH", "TECHM", "LTIM", "PERSISTENT",
        "COFORGE", "MPHASIS", "LTTS",
        # Energy / Oil
        "RELIANCE", "ONGC", "BPCL", "IOC", "GAIL", "NTPC", "POWERGRID",
        "TATAPOWER", "ADANIGREEN", "ADANIENSOL",
        # Auto
        "MARUTI", "TATAMOTORS", "M&M", "BAJAJ-AUTO", "HEROMOTOCO",
        "EICHERMOT", "TVSMOTOR", "ASHOKLEY", "BOSCHLTD",
        # Metals / Mining
        "TATASTEEL", "JSWSTEEL", "HINDALCO", "VEDL", "COALINDIA",
        "NMDC", "SAIL", "JINDALSTEL", "NATIONALUM",
        # Pharma / Healthcare
        "SUNPHARMA", "DRREDDY", "CIPLA", "DIVISLAB", "APOLLOHOSP",
        "AUROPHARMA", "LUPIN", "BIOCON", "TORNTPHARM",
        # FMCG / Consumer
        "HINDUNILVR", "ITC", "NESTLEIND", "BRITANNIA", "DABUR",
        "MARICO", "GODREJCP", "TATACONSUM", "COLPAL", "UBL",
        # Infra / Capital goods
        "LT", "SIEMENS", "ABB", "BHEL", "HAL", "BEL", "IRCTC",
        "CONCOR", "ADANIPORTS", "GRASIM",
        # Telecom / Media
        "BHARTIARTL", "IDEA", "INDUSTOWER",
        # Others / Conglomerates
        "ADANIENT", "ADANIPOWER", "TITAN", "ASIANPAINT", "ULTRACEMCO",
        "SHREECEM", "AMBUJACEM", "DLF", "GODREJPROP", "PIDILITIND",
        "HAVELLS", "VOLTAS", "DIXON", "POLYCAB", "SRF", "PIIND",
        "NAUKRI", "ZOMATO", "PAYTM", "NYKAA", "POLICYBZR",
    }

    by_symbol = {s["symbol"].upper(): s for s in stocks}

    filtered = []
    for sym in preferred_symbols:
        if sym in by_symbol:
            filtered.append(by_symbol[sym])

    return filtered