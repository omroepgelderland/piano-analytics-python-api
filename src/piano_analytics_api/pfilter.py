from abc import ABC, abstractmethod
from typing import Any, Union, Final
import datetime

EndpointDictType = dict[str, dict[str, Any]]

ListDictType = dict[str, list['DictType']]

DictType = Union[EndpointDictType, ListDictType]

class Filter(ABC):
    """
    Abstract class

    A filter can be a statement (FilterEndpoint) or a list of (nested) endpoints.
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/filter
    """

    @abstractmethod
    def format(self) -> DictType:
        pass


class List(Filter):
    """
    Abstract class

    Represents a combination of filters.
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/filter
    """

    def __init__(self, *args: Filter):
        """
        List of filters. Arguments can be endpoints or other filter lists.
        """
        self._filters = args

    @abstractmethod
    def _get_operator(self) -> str:
        pass

    def format(self) -> ListDictType:
        return {self._get_operator(): self._get_formatted_filters()}

    def _get_formatted_filters(self):
        lijst: "list[dict[str, Any]]" = []
        for filter in self._filters:
            lijst.append(filter.format())
        return lijst


class ListAnd(List):
    """
    List of filters combined by AND.
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/filter
    """

    def _get_operator(self):
        return "$AND"


class ListOr(List):
    """
    List of filters combined by OR.
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/filter
    """

    def _get_operator(self):
        return "$OR"


class Endpoint(Filter):
    """
    Represents a filter statement.

    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/filter
    """

    def __init__(
        self, field: str, operator: str, expression: Any
    ):
        """
        :param field: Property or metric to compare.
        :param operator: Comparison operator.
        :param expression: Comparison expression (integer, string, date, datetime or list)
        """
        self._field = field
        self._operator = operator
        self._expression = expression

    def format(self) -> EndpointDictType:
        if isinstance(self._expression, datetime.datetime):
            expression = self._expression.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(self._expression, datetime.date):
            expression = self._expression.strftime("%Y-%m-%d")
        else:
            expression = self._expression
        return {self._field: {self._operator: expression}}


"""Filter for integers, strings, dates and booleans"""
EQUALS: Final[str] = '$eq'
"""Filter for integers, string and booleans"""
NOT_EQUALS: Final[str] = '$neq'
"""Filter for integers and strings"""
IN_ARRAY: Final[str] = '$in'
"""Filter for integers and dates"""
GREATER: Final[str] = '$gt'
"""Filter for integers and dates"""
GREATER_OR_EQUAL: Final[str] = '$gte'
"""Filter for integers and dates"""
LOWER: Final[str] = '$lt'
"""Filter for integers and dates"""
LOWER_OR_EQUAL: Final[str] = '$lte'
"""Filter for integers, strings and booleans"""
IS_NULL: Final[str] = '$na'
"""Filter for integers, strings and booleans"""
IS_UNDEFINED: Final[str] = '$undefined'
"""combination of IS_NULL and IS_UNDEFINED. Filter for integers, strings and booleans"""
IS_EMPTY: Final[str] = '$empty'
"""Filter for strings"""
CONTAINS: Final[str] = '$lk'
"""Filter for strings"""
NOT_CONTAINS: Final[str] = '$nlk'
"""Filter for strings"""
STARTS_WITH: Final[str] = '$start'
"""Filter for strings"""
NOT_STARTS_WITH: Final[str] = '$nstart'
"""Filter for strings"""
ENDS_WITH: Final[str] = '$end'
"""Filter for strings"""
NOT_ENDS_WITH: Final[str] = '$nend'
"""
Compare a datetime field to the period of the analysis.
Possible expressions:
start: Is equal to the start of the time period
end: Is equal to the end of the period.
all: Is equal to the time period.
"""
PERIOD: Final[str] = '$period'
