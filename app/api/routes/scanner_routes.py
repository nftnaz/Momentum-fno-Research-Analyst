from fastapi import APIRouter, HTTPException, Query
from app.services.scanner_service import scanner_service
from app.services.option_chain_service import option_chain_service

scanner_router = APIRouter()


@scanner_router.get("/run")
async def run_scanner(
    category: str = Query(default="FNO"),
    enrich_options: bool = Query(default=True),
):
    try:
        result = await scanner_service.run_scan(category=category)
        stocks = result["stocks"]

        if enrich_options:
            stocks = await option_chain_service.enrich_scan_rows(
                stocks,
                high_score=60,
                low_score=40,
                max_enrich=25,
            )

        return {
            "status": "success",
            "count": len(stocks),
            "stats": result["stats"],
            "errors": result["errors"],
            "data": stocks,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))