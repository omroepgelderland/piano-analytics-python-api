"""
© 2024 Omroep Gelderland
SPDX-License-Identifier: MIT
"""

import datetime
from abc import ABC, abstractmethod
from typing import Final, Literal, Optional, TypedDict, Union


class _SingleDayDictType(TypedDict):
    type: Literal["D"]
    start: str
    end: str


RelativeGranularity = Literal["Y", "Q", "M", "W", "D"]


class _SingleRelativeDictType(TypedDict):
    type: Literal["R"]
    granularity: RelativeGranularity
    offset: int


DayDictType = list[_SingleDayDictType]

RelativeDictType = list[_SingleRelativeDictType]

PeriodDictType = Union[DayDictType, RelativeDictType]


class Period(ABC):
    """
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/period
    """

    @abstractmethod
    def format(self) -> PeriodDictType:
        pass


class _Absolute(Period):
    """
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/period#absolute-periods
    """

    pass


class Day(_Absolute):
    """
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/period#absolute-periods
    """

    def __init__(
        self,
        start: Union[datetime.date, datetime.datetime],
        end: Optional[Union[datetime.date, datetime.datetime]] = None,
    ):
        """
        Provide start and end as datetime.date objects to include data for the entire days.
        Provide start and end as datetime.datetime objects to include the time of day in the request.

        :param start: start of period.
        :param end: end of period. If not specified the end date will be the same date as the start.
        """
        self._start = start
        self._end = end if end is not None else start

    def format(self) -> DayDictType:
        start_str = (
            self._start.strftime("%Y-%m-%dT%H:%M:%S")
            if isinstance(self._start, datetime.datetime)
            else self._start.strftime("%Y-%m-%d")
        )
        end_str = (
            self._end.strftime("%Y-%m-%dT%H:%M:%S")
            if isinstance(self._end, datetime.datetime)
            else self._end.strftime("%Y-%m-%d")
        )
        return [
            {
                "type": "D",
                "start": start_str,
                "end": end_str,
            }
        ]


class _Relative(Period):
    """
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/period#relative-periods
    """

    @abstractmethod
    def __init__(self, granularity: RelativeGranularity, offset: int):
        """
        :param granularity: Time period.
        :param offset: Offset relative to the current data. Can be negative.
        """
        self._granularity: RelativeGranularity = granularity
        self._offset = offset

    def format(self) -> RelativeDictType:
        return [{"type": "R", "granularity": self._granularity, "offset": self._offset}]


class RelativeDay(_Relative):
    def __init__(self, offset: int = 0):
        """
        Construct a period of one day.
        :param offset: Offset relative to the current date. 0 is the current day, -1 is yesterday, etc.
        """
        super().__init__("D", offset)


class RelativeWeek(_Relative):
    def __init__(self, offset: int = 0):
        """
        Construct a period of one week.
        :param offset: Offset relative to the current date. 0 is the current week, -1 is last week, etc.
        """
        super().__init__("W", offset)


class RelativeMonth(_Relative):
    def __init__(self, offset: int = 0):
        """
        Construct a period of one month.
        :param offset: Offset relative to the current date. 0 is the current month, -1 is the previous month, etc.
        """
        super().__init__("M", offset)


class RelativeQuarter(_Relative):
    def __init__(self, offset: int = 0):
        """
        Construct a period of one quarter.
        Offset relative to the current date. 0 is the current quarter, -1 is the previous quarter, etc.
        :param offset:
        """
        super().__init__("Q", offset)


class RelativeYear(_Relative):
    def __init__(self, offset: int = 0):
        """
        Construct a period of one year.
        :param offset: Offset relative to the current date. 0 is the current year, -1 is last year, etc.
        """
        super().__init__("Y", offset)


def today():
    """
    Creates an absolute period for only the current day.
    """
    return Day(datetime.date.today(), datetime.date.today())
