# `utcnow`
[![pypi](https://badge.fury.io/py/utcnow.svg)](https://pypi.python.org/pypi/utcnow/)
[![Made with Python](https://img.shields.io/pypi/pyversions/utcnow)](https://www.python.org/)
[![Type hinted - mypy validated](https://img.shields.io/badge/typehinted-yes-teal)](https://github.com/kalaspuff/utcnow)
[![MIT License](https://img.shields.io/github/license/kalaspuff/utcnow.svg)](https://github.com/kalaspuff/utcnow/blob/master/LICENSE)

*Timestamps as RFC 3339 (Date and Time on the Internet) formatted strings with conversion from other timestamps in similar formats or from datetime objects or other date libraries that uses values convertable to strings and are compatible with RFC 3339. There's no other external dependencies required.*

A convenient utility package for when you need to store RFC 3339 timestamps in a datastore as a string, adding it to a JSON response or using a shared and common standard in your log outputs. Example output in string format would be `"2021-02-18T08:24:48.382262Z"`.

This is not a fullblown date library at all – it's simple and basically it just output timestamps into the fixes length string format `YYYY-MM-DDTHH:mm:ss.uuuuuuZ` (or as `%Y-%m-%dT%H:%M:%SZ` as if used with `datetime.datetime.strftime`). Always uses UTC in output and always appends the UTC timezone as a `Z` to the string (instead of using `+00:00` or ` UTC`).

## Transformation examples
```python
# This represents 20 minutes and 50.52 seconds after the 23rd hour of April 12th, 1985 in UTC.
from = "1985-04-12T23:20:50.52Z"
to = "1985-04-12T23:20:50.520000Z"

# This represents 39 minutes and 57 seconds after the 16th hour of December 19th, 1996 with an offset of
# -08:00 from UTC (Pacific Standard Time).  Note that this is equivalent to 1996-12-20T00:39:57Z in UTC.
from = "1996-12-19T16:39:57-08:00"
to = "1996-12-20T00:39:57.000000Z"

# This represents the same instant of time as noon, January 1, 1937, Netherlands time. Standard time in the
# Netherlands was exactly 19 minutes and 32.13 seconds ahead of UTC by law from 1909-05-01 through 1937-06-30.
from = "1937-01-01T12:00:27.87+00:20"
to = "1937-01-01T11:40:27.870000Z"

# Examples of other formats of accepted inputs:
#    from: "2021-02-18"                          =>    to: "2021-02-18T00:00:00.000000Z"
#    from: "2021-02-18 01:00"                    =>    to: "2021-02-18T01:00:00.000000Z"
#    from: "2021-02-18 03:00+01:00"              =>    to: "2021-02-18T02:00:00.000000Z"
#    from: "2021-02-18-01:00"                    =>    to: "2021-02-18T01:00:00.000000Z"
#    from: "2021-02-18+01:00"                    =>    to: "2021-02-17T23:00:00.000000Z"
#    from: "2021-02-18T23:55"                    =>    to: "2021-02-18T23:55:00.000000Z"
#    from: "2021-02-18T23:55:10"                 =>    to: "2021-02-18T23:55:10.000000Z"
#    from: "2021-02-18T23:55:10.0"               =>    to: "2021-02-18T23:55:10.000000Z"
#    from: "2021-02-18T23:55:10.0+05:00"         =>    to: "2021-02-18T18:55:10.000000Z"
#    from: "2021-02-18T23:55:10.0-05:00"         =>    to: "2021-02-19T04:55:10.000000Z"
#    from: "2021-02-18T23:55:10.550-05:00"       =>    to: "2021-02-19T04:55:10.550000Z"
#    from: "2021-02-18 23:55:10.550+05:00"       =>    to: "2021-02-18T18:55:10.550000Z"
#    from: "2021-02-18 23:55:10.550-01:00"       =>    to: "2021-02-19T00:55:10.550000Z"
#    from: "2021-02-28 10:10:59.123987+00:00"    =>    to: "2021-02-28T10:10:59.123987Z"
#    from: "2021-02-28 10:10:59.123987Z"         =>    to: "2021-02-28T10:10:59.123987Z"
#    from: "2021-02-28 10:10:59.123987 UTC"      =>    to: "2021-02-28T10:10:59.123987Z"
```

## Installation with `pip`
Like you would install any other Python package, use `pip`, `poetry`, `pipenv` or your weapon of choice.
```
$ pip install utcnow
```


## Usage and examples

```python
# Transform timestamps of many different formats to the same fixed length standard

from utcnow import utcnow
result = utcnow.as_string("1984-08-01 13:38")
# '1984-08-01T13:38:00.000000Z'
```

```python
# RFC 3339 timestamps works as input – dates and datetimes – UTC will be assumed if timezone is left out

from utcnow import utcnow
result = utcnow.as_string("2077-10-27")
# '2077-10-27T00:00:00.000000Z'
```

```python
# It's also possible to transform datetime values into timestamp strings

import datetime
from utcnow import utcnow
dt = datetime.datetime.utcnow()
result = utcnow.as_string(dt)
# '2021-02-18T08:24:48.382262Z'
```

```python
# Or vice versa, transforming a timestamp string into a datetime object (with tzinfo set to UTC)

from utcnow import utcnow
result = utcnow.as_datetime("1984-08-01T13:38:00.123450Z")
# datetime.datetime(1984, 8, 1, 13, 38, 0, 123450, tzinfo=datetime.timezone.utc)
```

```python
# Getting the current server time in UTC as a timestamp string

from utcnow import utcnow
utcnow()
# '2021-02-18T08:24:48.382262Z'
```

```python
# Or getting the current time in UTC as a datetime object

from utcnow import utcnow
utcnow.as_datetime()
# datetime.datetime(2021, 2, 18, 8, 24, 48, 382262, tzinfo=datetime.timezone.utc)
```

```python
# Just another way of getting the current server timestamp as an RFC 3339 timestamp in UTC

import utcnow
result = str(utcnow)
# '2021-02-18T08:24:48.382262Z'
```

```python
# Easy way of adding the current timestamp to a JSON response

import json
import utcnow
result = json.dumps({"timestamp": str(utcnow), "status": 200})
# '{"timestamp": "2021-02-18T08:24:48.382262Z", "status": 200}'
```

```python
# Or just adding the current time in an f-string

import utcnow
result = f"Current server time is: {utcnow}"
# 'Current server time is: 2021-02-18T08:24:48.382262Z'
```
