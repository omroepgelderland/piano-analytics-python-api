"""
© 2024 Omroep Gelderland
SPDX-License-Identifier: MIT
"""

from datetime import date, datetime

import src.piano_analytics_api.period as period


def test_single_day_period():
    p = period.Day(date(1999, 12, 31))
    assert p.format() == [{"type": "D", "start": "1999-12-31", "end": "1999-12-31"}]


def test_day_period():
    p = period.Day(date(1999, 12, 31), date(2000, 1, 10))
    assert p.format() == [{"type": "D", "start": "1999-12-31", "end": "2000-01-10"}]


def test_time_period():
    p = period.Day(datetime(1999, 12, 31, 0, 0, 0), datetime(1999, 12, 31, 23, 40, 50))
    assert p.format() == [
        {
            "type": "D",
            "start": "1999-12-31T00:00:00",
            "end": "1999-12-31T23:40:50",
        }
    ]


def test_relative_day_period():
    p = period.RelativeDay(-2)
    assert p.format() == [{"type": "R", "granularity": "D", "offset": -2}]


def test_relative_week_period():
    p = period.RelativeWeek()
    assert p.format() == [{"type": "R", "granularity": "W", "offset": 0}]


def test_relative_month_period():
    p = period.RelativeMonth(2)
    assert p.format() == [{"type": "R", "granularity": "M", "offset": 2}]


def test_relative_quarter_period():
    p = period.RelativeQuarter(-2)
    assert p.format() == [{"type": "R", "granularity": "Q", "offset": -2}]


def test_relative_year_period():
    p = period.RelativeYear(-2)
    assert p.format() == [{"type": "R", "granularity": "Y", "offset": -2}]
