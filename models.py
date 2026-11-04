from datetime import datetime

from pydantic import BaseModel

from calculator import expand_percent as expand_percent_function


class Expression(BaseModel):
    expr: str

    def expand_percent(self) -> str:
        return expand_percent_function(self.expr)


class CalculatorLog(BaseModel):
    timestamp: datetime
    expr: str
    result: float | int | str