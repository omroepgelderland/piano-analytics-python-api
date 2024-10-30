from datetime import date, datetime

import src.piano_analytics_api.period as period


def test_single_day_period():
    p = period.DayPeriod(date(1999, 12, 31))
    assert p.format() == [{"type": "D", "start": "1999-12-31", "end": "1999-12-31"}]


def test_day_period():
    p = period.DayPeriod(date(1999, 12, 31), date(2000, 1, 10))
    assert p.format() == [{"type": "D", "start": "1999-12-31", "end": "2000-01-10"}]


def test_time_period():
    p = period.DayPeriod(
        datetime(1999, 12, 31, 0, 0, 0), datetime(1999, 12, 31, 23, 40, 50)
    )
    assert p.format() == [
        {
            "type": "D",
            "start": "1999-12-31 00:00:00",
            "end": "1999-12-31 23:40:50",
        }
    ]


def test_month_period():
    p = period.RelativePeriod(period.MONTH, -1)
    assert p.format() == [{"type": "R", "granularity": "M", "offset": -1}]
