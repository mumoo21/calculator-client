
from fastapi import APIRouter, Depends

from app.dependencies import get_history
from app.schemas import ExpressionOut

router = APIRouter()


@router.get("/history", response_model=list[ExpressionOut])
def read_history(history=Depends(get_history)):
    return list(history)


@router.delete("/history")
def clear_history(history=Depends(get_history)):
    history.clear()

    return {
        "ok": True,
        "message": "History cleared successfully",
    }
