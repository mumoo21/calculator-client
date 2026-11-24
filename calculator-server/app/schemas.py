
from datetime import datetime

from pydantic import BaseModel


class BaseExpression(BaseModel):
    expr: str


class ExpressionIn(BaseExpression):
    pass


class ExpressionOut(ExpressionIn):
    timestamp: datetime
    result: float | int | str


# Compatibility aliases
Expression = ExpressionIn
CalculatorLog = ExpressionOut
