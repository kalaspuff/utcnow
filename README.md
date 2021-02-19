# `utcnow`
[![pypi](https://badge.fury.io/py/utcnow.svg)](https://pypi.python.org/pypi/utcnow/)
[![Made with Python](https://img.shields.io/pypi/pyversions/utcnow)](https://www.python.org/)
[![Type hinted - mypy validated](https://img.shields.io/badge/typehinted-yes-teal)](https://github.com/kalaspuff/utcnow)
[![MIT License](https://img.shields.io/github/license/kalaspuff/utcnow.svg)](https://github.com/kalaspuff/utcnow/blob/master/LICENSE)

*Timestamps as RFC 3339 (Date and Time on the Internet) formatted strings with conversion from other timestamps in similar formats or from datetime objects or other date libraries that uses values convertable to strings and are compatible with RFC 3339. There's no other external dependencies required.*


## The elevator pitch – purpose for devs and our sanity

**Note: `utcnow` is opinionated in the format of timestamps as strings. For example that timestamps as strings shall be stored using the same formatting and preferably using the same length, as well as adhering to best practices and following "RFC 3339 (Date and Time on the Internet: Timestamps)". Also: String based timestamps that may be meant for logs, API responses and database records shall always be stored with timezone UTC.**

Why UTC? UTC (Coordinated Universal Time) is currently the primary time standard and not affected by DST. Modern internet applications shouldn't use any other timezone in their databases, logs, API:s or other computer to computer interfaces.

**The following strict rules are applied to timestamps returned by `utcnow` when requesting a string based format:**
* Timestamps follow RFC 3339 (Date and Time on the Internet: Timestamps): https://tools.ietf.org/html/rfc3339.
* Timestamps are converted to UTC timezone which we'll note in the timestamp with the "Z" syntax instead of the also accepted "+00:00". "Z" stands for UTC+0 or "Zulu time" and refers to the zone description of zero hours.
* Timestamps are expressed as a date-time, including the full date (the "T" between the date and the time is optional in RFC 3339 (but not in ISO 8601=).
* Timestamps are 27 characters long in the format: "YYYY-MM-DDTHH:mm:ss.ffffffZ". 4 digit year, 2 digit month, 2 digit days. "T", 2 digit hours, 2 digit minutes, 2 digit seconds, 6 fractional digit microseconds followed by the timezone identifier for UTC: "Z".

When using a fixed length return value for string based timestamps it'll even make the returned strings comparable to each other.


### For what kind of applications or interfaces

Some examples of timestamps where this formatting would be reasonable to use includes, but are not limited to any timestamp that is written to a database / datastore as a string, also when timestamps are used in log output or used within a JSON response for an API such as a REST or GraphQL based API, maybe even using custom DateTime scalars.

If any of this sounds like the use-cases within your domains, try `utcnow` out – might do the trick.

If your work require a complex mix and match back and forth using different timezones even within internal applications (which may be true for legacy systems or on purely domestic use-cases), then go for `arrow`. Also iterating: Modern internet applications shouldn't use any other timezone than UTC in app-to-app / computer-to-computer interfaces.


### Summarizing

This is not a fullblown date library at all – it's simple and basically it just output timestamps into the fixes length string format `YYYY-MM-DDTHH:mm:ss.uuuuuuZ` (or as `%Y-%m-%dT%H:%M:%SZ` as if used with `datetime.datetime.strftime`). Always uses UTC in output and always appends the UTC timezone as a `Z` to the string (instead of using `+00:00` or ` UTC`).

A convenient utility package for when you need to store timestamps in a datastore as a string, adding it to a JSON response or using a shared and common standard in your log outputs. Example output in string format would be `"2021-02-18T08:24:48.382262Z"`.

It's never too late to start aligning your formatting standards and interfaces.


## Supported input values for timestamp conversion

This library aims at going for simplicity by being explicit about the choices allowed to make. `utcnow` however allows the conversion methods to be called with the following kind of argument values:
* RFC 3339 compliant strings, which at the very least must include the full date, but could omit the time part of a date-time, leaving only the date, or by not including the seconds, microseconds or even laving out the timezone information – `utcnow` supports all of the use-cases of RFC 3339 inputs and then converts the input into an even more complete RFC 3339 timestamp in UTC timezone.
* The most common format for handling dates and datetimes in Python, the builtin `datetime.datetime` object values (both timezone aware values, as well as values that aren't timezone aware, as for which we'll assume UTC).
* Also supporting object values from other commonly used libraries, such as `arrow`.
* As a bonus – Unix time, mainly for convinience (`time.time()`) (we have many names for the things we love: epoch time, posix time, seconds since epoch, 2038-bug on 32-bit unsigned ints to time-travel back to the first radio-transmission across the atlantic, there will be movies about this ).


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


## Installation
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
# Simple exmple of converting a naive datetime value, assuming UTC

import datetime
from utcnow import utcnow
dt = datetime.datetime(1984, 8, 1, 13, 38, 0, 4711)
result = utcnow.as_string(dt)
# '1984-08-01T13:38:00.004711Z'
# for non-tz-aware datetimes, the same result would be returned by both:
# 1. utcnow.as_string(dt)
# 2. dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
```

```python
# It's also possible to transform datetime values with timezone offsets into timestamp strings

import datetime
from utcnow import utcnow
tz_EDT = datetime.timezone(offset=datetime.timedelta(hours=-4))
dt = datetime.datetime(1997, 8, 4, 2, 14, tzinfo=tz_EDT)
result = utcnow.as_string(dt)
# '1997-08-04T06:14:00.000000Z'
# for timezone-aware datetimes, the same result would be returned by both:
# 1. utcnow.as_string(dt)
# 2. dt.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
```

```python
# Or vice versa, transforming a timestamp string into a datetime object (with tzinfo set to UTC)

from utcnow import utcnow
result = utcnow.as_datetime("1984-08-01T13:38:00.123450Z")
# datetime.datetime(1984, 8, 1, 13, 38, 0, 123450, tzinfo=datetime.timezone.utc)
```

```python
# Getting the current server time in UTC as a timestamp string

import utcnow
utcnow.utcnow()
# '2021-02-18T08:24:48.382262Z'
# same thing can be accomplished using datetime and all of these calls returns the same str value:
# 1. utcnow.utcnow()
# 2. str(utcnow)
# 3. str(utcnow.utcnow)
# 4. utcnow.as_string()
# 5. utcnow.utcnow.as_string()
# 6. datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
# 7. datetime.datetime.utcnow().isoformat() + "Z"
# 8. datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
```

```python
# Or getting the current time in UTC as a datetime object

from utcnow import utcnow
utcnow.as_datetime()
# datetime.datetime(2021, 2, 18, 8, 24, 48, 382262, tzinfo=datetime.timezone.utc)
# this is merely a convinience, as the same value would be returned by both:
# 1. utcnow.as_datetime()
# 2. datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
```

```python
# As described – current server timestamp as a RFC 3339 timestamp in UTC

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
