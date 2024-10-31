# Piano analytics (formerly ‘AT Internet’) Python client

This library enables you to get queries from the Piano Analytics Reporting API v3.
This is a third-party library.
A subscription to Piano Analytics is required.

## Requirements ##
* [Python 3.9](https://www.python.org/downloads/) or higher.

## Installation ##

You can use **Pip** or **Download the Release**

### Pip

The preferred method is via [the Python package index](https://pypi.org/).

```sh
pip3 install piano-analytics-api
```

## Usage example

1. Create an API key in your [Piano Analytics account](https://analytics.piano.io/profile/#/apikeys).
2. Get the access key and secret key from the API key.
3. Find the site ID’s in [Piano Analytics access management](https://analytics.piano.io/access-management/#/sites).
   Select a site on the page and copy the id from the address bar.

```python
import piano_analytics_api.period as period
import piano_analytics_api.pfilter as pfilter
from piano_analytics_api import Client, Request

site_id = 614694
access_key = ""
secret_key = ""

# Create API connection
client = Client(access_key, secret_key)

# Get page titles and number of visits for each page,
# where the page title is not empty and domain is example.com,
# ordered by the number of visits from high to low.
request = Request(
    client=client,
    sites=[site_id],
    columns=["page", "m_visits"],
    period=period.today(),
    sort=["-m_visits"],
    property_filter=pfilter.ListAnd(
        pfilter.IsEmpty("page", False),
        pfilter.Contains("domain", ["example.com", "www.example.com"])
    )
)

# All results
i = 0
for item in request.get_result_rows():
    print(item)
    i += 1

# Number of results
print(f"rowcount: {request.get_rowcount()}")

# Cumulative metrics for all resulting rows
print(f"total: {request.get_total()}")
```
