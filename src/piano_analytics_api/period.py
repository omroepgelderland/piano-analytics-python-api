import datetime
from typing import TypedDict, Literal, Final, Union
from abc import ABC, abstractmethod

class SingleDayDictType(TypedDict):
    type: Literal["D"]
    start: str
    end: str

RelativeGranularity = Literal['Y', 'Q', 'M', 'W', 'D']

class SingleRelativeDictType(TypedDict):
    type: Literal["R"]
    granularity: RelativeGranularity
    offset: int

DayDictType = list[SingleDayDictType]

RelativeDictType = list[SingleRelativeDictType]

PeriodDictType = Union[DayDictType, RelativeDictType]


YEAR: Final[str] = "Y"
QUARTER: Final[str] = "Q"
MONTH: Final[str] = "M"
WEEK: Final[str] = "W"
DAY: Final[str] = "D"


class Period(ABC):
    """
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/period
    """

    @abstractmethod
    def format(self) -> PeriodDictType:
        pass


class AbsolutePeriod(Period):
    """
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/period#absolute-periods
    """
    pass


class DayPeriod(AbsolutePeriod):
    """
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/period#absolute-periods
    """
    def __init__(
        self,
        start: Union[datetime.date, datetime.datetime],
        end: Union[datetime.date, datetime.datetime],
    ):
        """
        Provide start and end as datetime.date objects to include data for the entire days.
        Provide start and end as datetime.datetime objects to include the time of day in the request.

        :param start: start of period.
        :param end: end of period
        """
        self._start = start
        self._end = end

    def format(self) -> DayDictType:
        start_str = (
            self._start.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(self._start, datetime.datetime)
            else self._start.strftime("%Y-%m-%d")
        )
        end_str = (
            self._end.strftime("%Y-%m-%d %H:%M:%S")
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
    

class RelativePeriod(Period):
    """
    https://developers.atinternet-solutions.com/piano-analytics/data-api/parameters/period#relative-periods
    """

    def __init__(self, granularity: RelativeGranularity, offset: int):
        """
        :param granularity: Time period.
        :param offset: Offset relative to the current data. Can be negative.
        """
        self._granularity: RelativeGranularity = granularity
        self._offset = offset

    def format(self) -> RelativeDictType:
        return [{"type": "R", "granularity": self._granularity, "offset": self._offset}]


def today():
    """
    Creates a period for only the current day.
    """
    return DayPeriod(datetime.date.today(), datetime.date.today())

