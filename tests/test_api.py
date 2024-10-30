import datetime
from src.piano_analytics_api import Request, Client, Evolution
import src.piano_analytics_api.period as period
import src.piano_analytics_api.pfilter as pfilter


def get_max_request():
    return Request(
        client=Client("a", "b"),
        sites=[0],
        columns=["page"],
        period=period.DayPeriod(
            datetime.date(1999, 12, 1), datetime.date(1999, 12, 31)
        ),
        cmp_period=period.DayPeriod(
            datetime.date(2000, 12, 1), datetime.date(2000, 12, 31)
        ),
        property_filter=pfilter.ListOr(
            pfilter.ListAnd(
                pfilter.Endpoint("page", pfilter.CONTAINS, "a"),
                pfilter.Endpoint("article_id", pfilter.GREATER_OR_EQUAL, 5),
            ),
            pfilter.Endpoint("article_id", pfilter.IS_EMPTY, False),
            pfilter.Endpoint(
                "domain", pfilter.CONTAINS, ["example.org", "www.example.org"]
            ),
        ),
        metric_filter=pfilter.Endpoint("m_visits", pfilter.GREATER, 1),
        evolution=Evolution(),
        sort=["-m_visits", "page"],
        max_results=100,
        ignore_null_properties=True,
    )


def test_min_request():
    request = Request(
        client=Client("a", "b"),
        sites=[0],
        columns=["page"],
        period=period.DayPeriod(datetime.date(1999, 12, 31)),
    )
    assert request.format() == {
        "space": {"s": [0]},
        "columns": ["page"],
        "period": {"p1": [{"type": "D", "start": "1999-12-31", "end": "1999-12-31"}]},
        "max-results": 10000,
        "page-num": 1,
        "options": {"ignore_null_properties": False},
    }


def test_max_request():
    request = get_max_request()
    assert request.format() == {
        "space": {"s": [0]},
        "columns": ["page"],
        "period": {
            "p1": [{"type": "D", "start": "1999-12-01", "end": "1999-12-31"}],
            "p2": [{"type": "D", "start": "2000-12-01", "end": "2000-12-31"}],
        },
        "max-results": 100,
        "page-num": 1,
        "options": {"ignore_null_properties": True},
        "filter": {
            "metric": {"m_visits": {"$gt": 1}},
            "property": {
                "$OR": [
                    {"$AND": [{"page": {"$lk": "a"}}, {"article_id": {"$gte": 5}}]},
                    {"article_id": {"$empty": False}},
                    {"domain": {"$lk": ["example.org", "www.example.org"]}},
                ]
            },
        },
        "evo": {},
        "sort": ["-m_visits", "page"],
    }


def test_format_totals():
    request = get_max_request()
    assert request._format_totals() == { # type: ignore
        "space": {"s": [0]},
        "columns": ["page"],
        "period": {
            "p1": [{"type": "D", "start": "1999-12-01", "end": "1999-12-31"}],
            "p2": [{"type": "D", "start": "2000-12-01", "end": "2000-12-31"}],
        },
        "options": {"ignore_null_properties": True},
        "filter": {
            "metric": {"m_visits": {"$gt": 1}},
            "property": {
                "$OR": [
                    {"$AND": [{"page": {"$lk": "a"}}, {"article_id": {"$gte": 5}}]},
                    {"article_id": {"$empty": False}},
                    {"domain": {"$lk": ["example.org", "www.example.org"]}},
                ]
            },
        },
        "evo": {},
    }
