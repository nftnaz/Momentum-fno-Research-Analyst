from fastapi import APIRouter

router = APIRouter()


@router.post("/analyze")
def analyze_stock(request: dict):

    symbol = request.get("symbol")

    return {
        "symbol": symbol,
        "analysis": {
            "trend": "Bullish",
            "risk": "Medium",
            "summary": "Stock showing positive momentum"
        }
    }


@router.get("/health")
def ai_health():

    return {
        "status": "AI service ready"
    }