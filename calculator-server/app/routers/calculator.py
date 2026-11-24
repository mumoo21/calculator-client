
import math
from datetime import datetime

from asteval import Interpreter
from fastapi import APIRouter, Depends

from app.dependencies import expand_percent, get_history
from app.schemas import ExpressionOut

router = APIRouter()

aeval = Interpreter(
    minimal=True,
    usersyms={"pi": math.pi, "e": math.e}
)


@router.post("/calculate")
def calculate(
    expanded=Depends(expand_percent),
    history=Depends(get_history),
):
    expression, code = expanded
    expr = expression.expr

    try:
        result = aeval(code)

        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()

            return {
                "ok": False,
                "expr": expr,
                "result": "",
                "error": msg,
            }

        history.append(
            ExpressionOut(
                timestamp=datetime.now(),
                expr=expr,
                result=result,
            )
        )

        return {
            "ok": True,
            "expr": expr,
            "result": result,
            "error": "",
        }

    except Exception as e:
        return {
            "ok": False,
            "expr": expr,
            "result": "",
            "error": str(e),
        }
