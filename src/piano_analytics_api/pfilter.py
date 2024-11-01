"""
© 2024 Omroep Gelderland
SPDX-License-Identifier: MIT
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Literal, TypeVar, Union, cast

from .exceptions import PianoAnalyticsException

_ExpressionType = Union[int, str, bool, date, list[int], list[str], list[date]]

_ExpressionFormattedType = Union[int, str, bool, list[int], list[str]]

_EndpointDictType = dict[str, dict[str, _ExpressionFormattedType]]

_ListDictType = dict[str, list["DictType"]]

DictType = Union[_EndpointDictType, _ListDictType]


class Filter(ABC):
    """
    Abstract class

    A filter can be a statement (FilterEndpoint) or a list of (nested) endpoints.
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/filter
    """

    @abstractmethod
    def format(self) -> DictType:
        pass


class _List(Filter):
    """
    Abstract class

    Represents a combination of filters.
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/filter
    """

    def __init__(self, *args: Filter):
        """
        List of filters. Arguments can be endpoints or other filter lists.
        The list must contain at least one filter.
        """
        self.filters: list[Filter] = list(args)

    @abstractmethod
    def _get_operator(self) -> str:
        pass

    def format(self) -> Union[_ListDictType, DictType]:
        """
        Formats the filterlist in JSON format.
        Raises an error if the list does not contain any filters.
        If the list has only one filter then only that filter is returned.

        :raises PianoAnalyticsException If the list is empty.
        """
        if len(self.filters) == 0:
            raise PianoAnalyticsException("Filterlist cannot be empty")
        elif len(self.filters) == 1:
            return self.filters[0].format()
        else:
            return {self._get_operator(): self._get_formatted_filters()}

    def _get_formatted_filters(self):
        lijst: "list[dict[str, Any]]" = []
        for filter in self.filters:
            lijst.append(filter.format())
        return lijst
    
    def add(self, fil: Filter):
        """
        Add a filter or filterlist to this list
        """
        self.filters.append(fil)


class ListAnd(_List):
    """
    List of filters combined by AND.
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/filter
    """

    def _get_operator(self):
        return "$AND"


class ListOr(_List):
    """
    List of filters combined by OR.
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/filter
    """

    def _get_operator(self):
        return "$OR"


class _Endpoint(Filter):
    """
    Represents a filter statement.

    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/filter
    """

    @abstractmethod
    def __init__(self, field: str, operator: str, expression: _ExpressionType):
        """
        :param field: Property or metric to compare.
        :param operator: Comparison operator.
        :param expression: Comparison expression (integer, string, date, datetime or list)
        """
        self._field = field
        self._operator = operator
        self._expression = expression

    def format(self) -> _EndpointDictType:
        if type(self._expression) is list:
            expression = cast(
                Union[list[int], list[str]], list(map(_cast_date, self._expression))
            )
        else:
            c_expression = cast(Union[int, str, bool, date], self._expression)
            expression = _cast_date(c_expression)
        return {self._field: {self._operator: expression}}


class Equals(_Endpoint):
    def __init__(self, field: str, expression: Union[int, str, date]):
        super().__init__(field, "$eq", expression)


class NotEquals(_Endpoint):
    def __init__(self, field: str, expression: Union[int, str, date]):
        super().__init__(field, "$neq", expression)


class In(_Endpoint):
    def __init__(self, field: str, expression: Union[list[int], list[str], list[date]]):
        super().__init__(field, "$in", expression)


class NotIn(_Endpoint):
    def __init__(self, field: str, expression: Union[list[int], list[str], list[date]]):
        super().__init__(field, "$nin", expression)


class Greater(_Endpoint):
    def __init__(self, field: str, expression: Union[int, date]):
        super().__init__(field, "$gt", expression)


class GreaterOrEqual(_Endpoint):
    def __init__(self, field: str, expression: Union[int, date]):
        super().__init__(field, "$gte", expression)


class Less(_Endpoint):
    def __init__(self, field: str, expression: Union[int, date]):
        super().__init__(field, "$lt", expression)


class LessOrEqual(_Endpoint):
    def __init__(self, field: str, expression: Union[int, date]):
        super().__init__(field, "$lte", expression)


class Contains(_Endpoint):
    def __init__(self, field: str, expression: Union[str, list[str]]):
        super().__init__(field, "$lk", expression)


class NotContains(_Endpoint):
    def __init__(self, field: str, expression: Union[str, list[str]]):
        super().__init__(field, "$nlk", expression)


class StartsWith(_Endpoint):
    def __init__(self, field: str, expression: Union[str, list[str]]):
        super().__init__(field, "$start", expression)


class NotStartsWith(_Endpoint):
    def __init__(self, field: str, expression: Union[str, list[str]]):
        super().__init__(field, "$nstart", expression)


class EndsWith(_Endpoint):
    def __init__(self, field: str, expression: Union[str, list[str]]):
        super().__init__(field, "$end", expression)


class NotEndsWith(_Endpoint):
    def __init__(self, field: str, expression: Union[str, list[str]]):
        super().__init__(field, "$nend", expression)


class IsNull(_Endpoint):
    def __init__(self, field: str, expression: bool):
        super().__init__(field, "$na", expression)


class IsUndefined(_Endpoint):
    def __init__(self, field: str, expression: bool):
        super().__init__(field, "$undefined", expression)


class IsEmpty(_Endpoint):
    def __init__(self, field: str, expression: bool):
        super().__init__(field, "$empty", expression)


class Period(_Endpoint):
    def __init__(self, field: str, expression: Literal["start", "end", "all"]):
        super().__init__(field, "$period", expression)


T = TypeVar("T")


def _cast_date(arg: Union[T, date]) -> Union[T, str]:
    return arg.strftime("%Y-%m-%d") if isinstance(arg, date) else arg
