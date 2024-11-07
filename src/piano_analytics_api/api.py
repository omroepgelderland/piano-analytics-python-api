"""
© 2024 Omroep Gelderland
SPDX-License-Identifier: MIT
"""

import http.client
import json
from typing import Any, Final, Literal, Optional, TypedDict, Union, cast

from . import period, pfilter
from .exceptions import APIException, PianoAnalyticsException


class _DataFeedColumnType(TypedDict):
    Category: Literal["Dimension", "Metric"]
    Name: str
    Type: str
    CustomerType: str
    Label: str
    Description: str
    Filterable: bool


class _DataFeedType(TypedDict):
    Columns: "list[_DataFeedColumnType]"
    Rows: "list[dict[str, Any]]"
    Context: "dict[str, Any]"


class _RowCountType(TypedDict):
    RowCount: int


class _APIResponseType(TypedDict, total=False):
    DataFeed: _DataFeedType
    RowCounts: list[_RowCountType]
    ErrorMessage: str
    ErrorType: str


class EvolutionDictType(TypedDict):
    pass


class _RequestSpaceType(TypedDict):
    s: list[int]


class _RequestPeriodsDictTypeNotRequired(TypedDict, total=False):
    p2: "period.PeriodDictType"


class _RequestPeriodsDictType(_RequestPeriodsDictTypeNotRequired):
    p1: period.PeriodDictType


class _RequestOptionsType(TypedDict):
    ignore_null_properties: bool


class _RequestFiltersType(TypedDict, total=False):
    metric: pfilter.DictType
    property: pfilter.DictType


_RequestDictTypeRequired = TypedDict(
    "_RequestDictTypeRequired",
    {
        "space": _RequestSpaceType,
        "columns": list[str],
        "period": _RequestPeriodsDictType,
        "max-results": int,
        "page-num": int,
        "options": _RequestOptionsType,
    },
)


class _RequestDictType(_RequestDictTypeRequired, total=False):
    filter: _RequestFiltersType
    evo: EvolutionDictType
    sort: list[str]


class _RequestTotalsTypeNotRequired(TypedDict, total=False):
    filter: _RequestFiltersType
    evo: EvolutionDictType


class _RequestTotalsType(_RequestTotalsTypeNotRequired):
    space: _RequestSpaceType
    columns: list[str]
    period: _RequestPeriodsDictType
    options: _RequestOptionsType


"""Maximum number of results in one page."""
MAX_PAGE_RESULTS: Final[Literal[10000]] = 10000
"""Maximum number of pages in a request."""
MAX_PAGES: Final[Literal[20]] = 20


class Evolution(object):
    """
    @todo implementeren
    """

    def format(self) -> EvolutionDictType:
        return {}


class Client(object):
    def __init__(self, access_key: str, secret_key: str):
        """
        Construct a new API connection.
        :param access_key: Access key provided by Piano analytics.
        :param secret_key: Secret key.
        """
        self._access_key = access_key
        self._secret_key = secret_key

    def request(
        self,
        method: str,
        request: Union["Request", _RequestDictType, _RequestTotalsType],
    ) -> _APIResponseType:
        """
        Execute an API request.
        :param method: API method.
        :param request: Request object or dict.
        :return: API response.
        :raises APIError
        """
        request_dict = request.format() if isinstance(request, Request) else request
        connection = http.client.HTTPSConnection("api.atinternet.io")
        connection.request(
            method="POST",
            url=f"/v3/data/{method}",
            body=json.dumps(request_dict),
            headers=self._get_headers(),
        )
        with connection.getresponse() as response:
            response_raw = response.read()
            data: Optional[_APIResponseType] = json.loads(response_raw)
            http_status = response.status

        if data is None:
            raise APIException(response_raw.decode(), http_status)

        error_message = None
        error_type = None
        if "ErrorMessage" in data:
            error_message = data["ErrorMessage"]
        if "ErrorType" in data:
            error_type = data["ErrorType"]

        if http_status >= 400 or error_message is not None or error_type is not None:
            error_message = (
                f"{error_type}: {error_message}"
                if error_type is not None
                else error_message
            )
            error = APIException(error_message, http_status, error_type)
            raise error

        return data

    def _get_headers(self) -> "dict[str, str]":
        """
        Returns the headers for API requests.
        """
        return {
            "x-api-key": "{}_{}".format(self._access_key, self._secret_key),
            "Content-type": "application/json",
        }


class Request(object):
    """
    The request object contains the parameters for a data query.
    """

    def __init__(
        self,
        client: Client,
        sites: "list[int]",
        columns: "list[str]",
        period: period.Period,
        cmp_period: Optional[period.Period] = None,
        metric_filter: Optional[pfilter.Filter] = None,
        property_filter: Optional[pfilter.Filter] = None,
        evolution: Optional[Evolution] = None,
        sort: "list[str]" = [],
        max_results: int = MAX_PAGES * MAX_PAGE_RESULTS,
        ignore_null_properties: bool = False,
    ):
        """
        :param sites: List of site ID's.
        :param columns: List of metrics and properties.
        :param period: Analysis period.
        :param cmp_period: Comparison period (optional)
        :param metric_filter: Filters on metrics (optional)
        :param property_filter: Filters on properties (optional)
        :param evolution: Not implemented yet (optional)
        :param sort: List of properties/metrics according to which the results will be sorted (optional).
        :param max_results: Maximum number of results (default and maximum: 200000 (200k))
        :param ignore_null_properties: When set to true, null values will not be included in the results (default false)
        """
        self._client = client
        self._page_num = 1

        self._sites = sites
        self._columns = columns
        self._period = period
        self._cmp_period = cmp_period
        self._metric_filter = metric_filter
        self._property_filter = property_filter
        self._evolution = evolution
        self._sort = sort
        self._max_results = max_results
        self._ignore_null_properties = ignore_null_properties

    def format(self) -> _RequestDictType:
        dict: _RequestDictType = {
            "space": {"s": self._sites},
            "columns": self._columns,
            "period": {"p1": self._period.format()},
            "max-results": self._get_max_page_results(),
            "page-num": self._page_num,
            "options": {"ignore_null_properties": self._ignore_null_properties},
        }
        if self._cmp_period is not None:
            dict["period"]["p2"] = self._cmp_period.format()
        filters_dict = self._format_filters()
        if len(filters_dict) > 0:
            dict["filter"] = filters_dict
        if self._evolution is not None:
            dict["evo"] = self._evolution.format()
        if len(self._sort) > 0:
            dict["sort"] = self._sort
        return dict

    def _format_totals(self) -> _RequestTotalsType:
        """
        Serialization without some properties for getRowCount and getTotal queries.
        """
        response = cast(_RequestTotalsType, self.format())
        if "sort" in response:
            del response["sort"]
        if "max-results" in response:
            del response["max-results"]
        if "page-num" in response:
            del response["page-num"]
        return response

    def _format_filters(self) -> _RequestFiltersType:
        """
        Format the filters for serialization.
        """
        response: _RequestFiltersType = {}
        if self._metric_filter is not None:
            response["metric"] = self._metric_filter.format()
        if self._property_filter is not None:
            response["property"] = self._property_filter.format()
        return response

    def get_result_pages(self) -> "ResultPageList":
        """
        Execute a query and return a result object with multiple pages of responses from the API.
        Use ATInternet::get_result_rows() to get results without having to deal with paging.
        https://developers.atinternet-solutions.com/piano-analytics/data-api/technical-information/methods#getdata
        """
        return ResultPageList(self)

    def get_result_page(self, page_num: int) -> _APIResponseType:
        """
        Execute a data query. Only one page of results is returned. This page may not include all data.
        Use ATInternet::get_result_pages() to get a more complete result.
        Use ATInternet::get_result_rows() to get results without having to deal with paging.
        https://developers.atinternet-solutions.com/piano-analytics/data-api/technical-information/methods#getdata
        :raises APIException
        """
        self._page_num = page_num
        return self._client.request("getData", self)

    def get_result_rows(self) -> "ResultRowList":
        """
        Execute the query and return a result object with all rows from the API.
        https://developers.atinternet-solutions.com/piano-analytics/data-api/technical-information/methods#getdata
        """
        return ResultRowList(self)

    def get_rowcount(self) -> int:
        """
        Returns the number of results for a query. max_results is ignored.
        https://developers.atinternet-solutions.com/piano-analytics/data-api/technical-information/methods#getrowcount
        :raises APIException
        """
        rowcount_raw = self._client.request("getRowCount", self._format_totals())
        if "RowCounts" not in rowcount_raw:
            raise PianoAnalyticsException("Key RowCounts missing in response")
        return rowcount_raw["RowCounts"][0]["RowCount"]

    def get_total(self) -> dict[str, Any]:
        """
        Get the totals for each metric in a request.
        https://developers.atinternet-solutions.com/piano-analytics/data-api/technical-information/methods#gettotal
        :raises APIException
        """
        total_raw = self._client.request("getTotal", self._format_totals())
        if "DataFeed" not in total_raw:
            raise PianoAnalyticsException("Key DataFeed missing in response")
        data = total_raw["DataFeed"]["Rows"][0]
        return {k: v for k, v in data.items() if v != "-"}

    def _get_max_page_results(self) -> int:
        """
        Get the maximum number of results for the current page.
        """
        return max(
            0,
            min(
                MAX_PAGE_RESULTS,
                self._max_results - MAX_PAGE_RESULTS * (self._page_num - 1),
            ),
        )

    def is_after_last_page(self, page_num: int) -> bool:
        """
        Returns true if the current page is the page after the last page that contains results.
        :param page_num: The current page.
        """
        self._page_num = page_num
        return self._get_max_page_results() == 0


class ResultPageList(object):
    """
    Iterable set of pages with data results.
    """

    def __init__(self, request: Request):
        """
        :param request: Data request
        """
        self._request = request
        self._page_index = 1

    def __iter__(self) -> "ResultPageList":
        self._page_index = 1
        return self

    def __next__(self) -> _APIResponseType:
        data = self._request.get_result_page(self._page_index)
        self._page_index += 1
        if "DataFeed" not in data or len(data["DataFeed"]["Rows"]) == 0:
            raise StopIteration
        return data


class ResultRowList:
    """
    Iterator for all result rows across multiple pages.
    """

    def __init__(self, request: Request) -> None:
        """
        :param request: Data request
        """
        self._result_pages = ResultPageList(request)
        self._rows: Optional[list[dict[str, Any]]] = None
        self._row_index: int = 0
        self._total_index: int = 0

    def __iter__(self) -> "ResultRowList":
        self._result_pages.__iter__()
        self._rows = None
        self._row_index = 0
        self._total_index = 0
        return self

    def __next__(self) -> dict[str, Any]:
        data = self._get_rows()[self._row_index]
        self._row_index += 1
        self._total_index += 1
        if self._row_index >= self._get_row_count():
            self._rows = None
            self._row_index = 0
        return data

    def _get_rows(self):
        if self._rows is None:
            page = self._result_pages.__next__()
            if "DataFeed" not in page:
                raise PianoAnalyticsException("Key DataFeed missing in response")
            self._rows = page["DataFeed"]["Rows"]
        return self._rows

    def _get_row_count(self) -> int:
        return len(self._get_rows())
