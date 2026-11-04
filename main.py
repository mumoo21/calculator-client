
# main.py
import math

from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter

from models import Expression, CalculatorLog

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})

history: list[CalculatorLog] = []


@app.post("/calculate")
def calculate(expression: Expression):
    expr = expression.expr

    try:
        code = expression.expand_percent()
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
            CalculatorLog(
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


@app.get("/history", response_model=list[CalculatorLog])
def get_history() -> list[CalculatorLog]:
    return history
