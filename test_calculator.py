
from app.dependencies import expand_percent
from app.schemas import ExpressionIn


def test_expand_percent():
    assert expand_percent(ExpressionIn(expr="5 + 10%"))[1] == "5 + ((10/100)*5)"

    assert expand_percent(ExpressionIn(expr="20 - 30%"))[1] == "20 - ((30/100)*20)"

    assert expand_percent(ExpressionIn(expr="15 * 25%"))[1] == "15 * (25/100)"

    assert expand_percent(ExpressionIn(expr="40 / 50%"))[1] == "40 / (50/100)"

    assert expand_percent(ExpressionIn(expr="3 * 4% + 2 / 1%"))[1] == "3 * (4/100) + 2 / (1/100)"

    assert expand_percent(ExpressionIn(expr="100%"))[1] == "(100/100)"

    assert expand_percent(ExpressionIn(expr="10% + 20%"))[1] == "(10/100) + (20/100)"


if __name__ == "__main__":
    test_expand_percent()
    print("All tests passed!")
