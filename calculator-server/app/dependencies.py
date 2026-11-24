
from collections import deque

from app.calculator import expand_percent as expand_percent_function
from app.schemas import ExpressionIn


HISTORY_MAX = 100

history = deque(maxlen=HISTORY_MAX)


def get_history():
    return history


def expand_percent(expression: ExpressionIn):
    return (
        expression,
        expand_percent_function(expression.expr),
    )
