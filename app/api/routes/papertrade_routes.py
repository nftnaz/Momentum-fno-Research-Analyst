from fastapi import APIRouter

router = APIRouter()


@router.get("/portfolio")
def portfolio():

    return {
        "capital": 100000,
        "available_cash": 85000,
        "positions": []
    }


@router.post("/order")
def create_order(order: dict):

    return {
        "message": "Paper order executed",
        "order": order
    }


@router.get("/trades")
def trades():

    return {
        "trades": []
    }