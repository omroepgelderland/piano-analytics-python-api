"""
© 2024 Omroep Gelderland
SPDX-License-Identifier: MIT
"""

from datetime import date

import pytest

import src.piano_analytics_api.pfilter as pfilter
from src.piano_analytics_api.exceptions import PianoAnalyticsException


def test_number_equals():
    f = pfilter.Equals("m_visits", 19)
    assert f.format() == {"m_visits": {"$eq": 19}}


def test_number_not_equals():
    f = pfilter.NotEquals("m_visits", 19)
    assert f.format() == {"m_visits": {"$neq": 19}}


def test_number_in():
    f = pfilter.In("article_id", [2, 3, 4])
    assert f.format() == {"article_id": {"$in": [2, 3, 4]}}


def test_number_not_in():
    f = pfilter.NotIn("article_id", [2, 3, 4])
    assert f.format() == {"article_id": {"$nin": [2, 3, 4]}}


def test_number_greater():
    f = pfilter.Greater("m_visits", 19)
    assert f.format() == {"m_visits": {"$gt": 19}}


def test_number_greater_or_equal():
    f = pfilter.GreaterOrEqual("m_visits", 19)
    assert f.format() == {"m_visits": {"$gte": 19}}


def test_number_less():
    f = pfilter.Less("m_visits", 19)
    assert f.format() == {"m_visits": {"$lt": 19}}


def test_number_less_or_equal():
    f = pfilter.LessOrEqual("m_visits", 19)
    assert f.format() == {"m_visits": {"$lte": 19}}


def test_str_equals():
    f = pfilter.Equals("page", "index")
    assert f.format() == {"page": {"$eq": "index"}}


def test_str_not_equals():
    f = pfilter.NotEquals("page", "index")
    assert f.format() == {"page": {"$neq": "index"}}


def test_str_in():
    f = pfilter.In("article_id", ["a", "b", "3"])
    assert f.format() == {"article_id": {"$in": ["a", "b", "3"]}}


def test_str_not_in():
    f = pfilter.NotIn("article_id", ["a", "b", "3"])
    assert f.format() == {"article_id": {"$nin": ["a", "b", "3"]}}


def test_str_contains():
    f = pfilter.Contains("domain", "example.org")
    assert f.format() == {"domain": {"$lk": "example.org"}}


def test_str_contains_list():
    f = pfilter.Contains("domain", ["example.org", "www.example.org"])
    assert f.format() == {"domain": {"$lk": ["example.org", "www.example.org"]}}


def test_str_not_contains():
    f = pfilter.NotContains("domain", "example.org")
    assert f.format() == {"domain": {"$nlk": "example.org"}}


def test_str_not_contains_list():
    f = pfilter.NotContains("domain", ["example.org", "www.example.org"])
    assert f.format() == {"domain": {"$nlk": ["example.org", "www.example.org"]}}


def test_str_starts_with():
    f = pfilter.StartsWith("page", "ind")
    assert f.format() == {"page": {"$start": "ind"}}


def test_str_starts_with_list():
    f = pfilter.StartsWith("page", ["ind", "ho"])
    assert f.format() == {"page": {"$start": ["ind", "ho"]}}


def test_str_not_starts_with():
    f = pfilter.NotStartsWith("page", "ind")
    assert f.format() == {"page": {"$nstart": "ind"}}


def test_str_not_starts_with_list():
    f = pfilter.NotStartsWith("page", ["ind", "ho"])
    assert f.format() == {"page": {"$nstart": ["ind", "ho"]}}


def test_str_ends_with():
    f = pfilter.EndsWith("page", "ex")
    assert f.format() == {"page": {"$end": "ex"}}


def test_str_ends_with_list():
    f = pfilter.EndsWith("page", ["ex", "me"])
    assert f.format() == {"page": {"$end": ["ex", "me"]}}


def test_str_not_ends_with():
    f = pfilter.NotEndsWith("page", "ex")
    assert f.format() == {"page": {"$nend": "ex"}}


def test_str_not_ends_with_list():
    f = pfilter.NotEndsWith("page", ["ex", "me"])
    assert f.format() == {"page": {"$nend": ["ex", "me"]}}


def test_date_equals():
    f = pfilter.Equals("date", date(1999, 12, 31))
    assert f.format() == {"date": {"$eq": "1999-12-31"}}


def test_date_not_equals():
    f = pfilter.NotEquals("date", date(1999, 12, 31))
    assert f.format() == {"date": {"$neq": "1999-12-31"}}


def test_date_in():
    f = pfilter.In("date", [date(1999, 12, 31), date(2000, 1, 1)])
    assert f.format() == {"date": {"$in": ["1999-12-31", "2000-01-01"]}}


def test_date_not_in():
    f = pfilter.NotIn("date", [date(1999, 12, 31), date(2000, 1, 1)])
    assert f.format() == {"date": {"$nin": ["1999-12-31", "2000-01-01"]}}


def test_date_greater():
    f = pfilter.Greater("date", date(1999, 12, 31))
    assert f.format() == {"date": {"$gt": "1999-12-31"}}


def test_date_greater_or_equal():
    f = pfilter.GreaterOrEqual("date", date(1999, 12, 31))
    assert f.format() == {"date": {"$gte": "1999-12-31"}}


def test_date_less():
    f = pfilter.Less("date", date(1999, 12, 31))
    assert f.format() == {"date": {"$lt": "1999-12-31"}}


def test_date_less_or_equal():
    f = pfilter.LessOrEqual("date", date(1999, 12, 31))
    assert f.format() == {"date": {"$lte": "1999-12-31"}}


def test_is_null():
    f = pfilter.IsNull("article_id", True)
    assert f.format() == {"article_id": {"$na": True}}


def test_is_undefined():
    f = pfilter.IsUndefined("article_id", False)
    assert f.format() == {"article_id": {"$undefined": False}}


def test_is_empty():
    f = pfilter.IsEmpty("article_id", True)
    assert f.format() == {"article_id": {"$empty": True}}


def test_period():
    f = pfilter.Period("publication_date", "all")
    assert f.format() == {"publication_date": {"$period": "all"}}


def test_and_list():
    f = pfilter.ListAnd(
        pfilter.Equals("page", "index"), pfilter.NotContains("article_id", "wf")
    )
    assert f.format() == {
        "$AND": [{"page": {"$eq": "index"}}, {"article_id": {"$nlk": "wf"}}]
    }


def test_or_list():
    f = pfilter.ListOr(
        pfilter.Equals("page", "index"), pfilter.NotContains("article_id", "wf")
    )
    assert f.format() == {
        "$OR": [{"page": {"$eq": "index"}}, {"article_id": {"$nlk": "wf"}}]
    }


def test_and_list_single():
    f = pfilter.ListAnd(pfilter.Equals("page", "index"))
    assert f.format() == {"page": {"$eq": "index"}}


def test_or_list_single():
    f = pfilter.ListOr(pfilter.Equals("page", "index"))
    assert f.format() == {"page": {"$eq": "index"}}


def test_empty_and_list():
    f = pfilter.ListAnd()
    with pytest.raises(PianoAnalyticsException):
        f.format()


def test_empty_or_list():
    f = pfilter.ListOr()
    with pytest.raises(PianoAnalyticsException):
        f.format()

def test_add_list():
    f = pfilter.ListAnd()
    f.add(pfilter.Equals("page", "index"))
    f.add(pfilter.NotContains("article_id", "wf"))
    assert f.format() == {
        "$AND": [{"page": {"$eq": "index"}}, {"article_id": {"$nlk": "wf"}}]
    }
