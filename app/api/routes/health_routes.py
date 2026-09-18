from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():

    return {

        "status": "healthy",

        "service": "NSE AI Research Analyst",

        "version": "1.0.0"

    }