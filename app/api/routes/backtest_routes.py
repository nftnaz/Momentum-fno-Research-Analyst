from fastapi import APIRouter

router = APIRouter()


@router.post("/run")
def run_backtest(config: dict):

    return {
        "status": "completed",
        "strategy": config.get("strategy"),
        "total_return": "18.5%",
        "win_rate": "62%",
        "max_drawdown": "-8%"
    }


@router.get("/history")
def backtest_history():

    return {
        "backtests": [
            {
                "strategy": "EMA + Supertrend",
                "return": "25%",
                "date": "2026-08-01"
            }
        ]
    }