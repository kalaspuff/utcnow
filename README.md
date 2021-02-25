# `utcnow`
[![pypi](https://badge.fury.io/py/utcnow.svg)](https://pypi.python.org/pypi/utcnow/)
[![Made with Python](https://img.shields.io/pypi/pyversions/utcnow)](https://www.python.org/)
[![Type hinted - mypy validated](https://img.shields.io/badge/typehinted-yes-teal)](https://github.com/kalaspuff/utcnow)
[![MIT License](https://img.shields.io/github/license/kalaspuff/utcnow.svg)](https://github.com/kalaspuff/utcnow/blob/master/LICENSE)

*Timestamps as RFC 3339 (Date & Time on the Internet) formatted strings with conversion functinonality from other timestamp formats or for timestamps on other timezones. Additionally converts timestamps from datetime objets and other common date utilities. Follow modern practices when developing API interfaces.*

```python
from utcnow import utcnow

utcnow.get()
# "2077-03-01T09:33:07.139361Z" | The most common use case – get current server time.
#                               | Always uses UTC in the returned value.

utcnow.get("2020-02-26 09:10:10+00:00")
# "2020-02-26T09:10:10.000000Z" | Reformats any valid date-time input to a defined standard.
#                               | RFC 3339 compliant: YYYY-MM-DDTHH:mm:ss.ffffffZ

utcnow.get("1997-08-04T02:14:00.53-04:00")
# "1997-08-04T06:14:00.530000Z" | Timezones as UTC for aligned and clean interfaces.
#                               | Uses "Z", Zulu Time, to specify UTC timezone.

utcnow.get("1989-12-13 08:35 UTC")
# "1989-12-13T08:35:00.000000Z" | Converts from different input formats and patterns.
#                               | Any other RFC 3339 compliant input is valid + more.

# 👋 Look further down for additional code examples of other types of input values.
```

## The elevator pitch – purpose for developers – the why

##### NOTE – OPINIONATED SOFTWARE

**`utcnow` is opinionated about the format of string based timestamps. For example, that timestamps as strings should be stored using the same formatting and preferably using the same length, as well as adhering to the current best practices – which for computer-to-computer comms should be by following ["RFC 3339 (Date and Time on the Internet: Timestamps)"](https://tools.ietf.org/html/rfc3339).**

##### TIMESTAMPS WILL USE UTC

**String based timestamps that are meant for logs, API responses and database records shall always be stored with timezone UTC.**

----

> **Someone – somewhere:**
> "Why UTC? It's not even a timezone for our markets."

> **Devs (and wikipedia):**
> "_Coordinated Universal Time_ or _Universal Time Coordinated_, UTC for short, is still currently _the primary time standard_ and is not affected by daylight saving time, which is usually not something that servers or software developers would want to work around."
>
> "It's pretty simple – modern internet applications shouldn't use any other timezone in their databases, logs, API:s or other computer to computer interfaces."

----

Good timestamps and UTC – really no wild and crazy opinions. Generailly this lib is just about making it ~easier to follow common best practices~ harder to do something wrong – and that's also why `utcnow` doesn't have any configuration options. The library does what it should do – "shoganai".

##### RULES FOR RETURNED TIMESTAMPS

**The following ruleset are applied to timestamps returned by `utcnow` when requesting a string based format:**

* Timestamps follow RFC 3339 (Date and Time on the Internet: Timestamps): https://tools.ietf.org/html/rfc3339.
* Timestamps are converted to UTC timezone which we'll note in the timestamp with the "Z" syntax instead of the also accepted "+00:00". "Z" stands for UTC+0 or "Zulu time" and refers to the zone description of zero hours.
* Timestamps are expressed as a date-time, including the full date (the "T" between the date and the time is optional in RFC 3339 (but not in ISO 8601) and usually describes the beginning of the time part.
* Timestamps are 27 characters long in the format: "YYYY-MM-DDTHH:mm:ss.ffffffZ". 4 digit year, 2 digit month, 2 digit days. "T", 2 digit hours, 2 digit minutes, 2 digit seconds, 6 fractional second digits (microseconds -> nanoseconds), followed by the timezone identifier for UTC: "Z".

`utcnow` is defined to return timestamps with 6 fractional second digits, which means timestamps down to the microsecond level. Having a six-digit fraction of a second is currently the most common way that timestamps are shown at this date.

When using a fixed length return value for string based timestamps it'll even make the returned strings comparable to each other.


### Where to use this – for what kind of applications or interfaces

Some examples of timestamps where this formatting would be reasonable to use includes, but are not limited to any timestamp that is written to a database / datastore as a string, also when timestamps are used in log output or used within a JSON response for an API such as a REST or GraphQL based API, maybe even using custom DateTime scalars.

If any of this sounds like the use-cases within your domains, try `utcnow` out – might do the trick.

If your work require a complex mix and match back and forth using different timezones even within internal applications (which may be true for legacy systems or on purely domestic use-cases), then go for `arrow`. Also iterating: Modern internet applications shouldn't use any other timezone than UTC in app to app / computer to computer interfaces.

Note that this library is built with backend developers in mind and while there's a good need for human readability and timestamp conversion into local timezones within a service's user interface, frontend applications, etc. Interfaces where conversion into date and time formats meant for human eyes will obviously also reap the benefits from well defined backends that delivers timestamp values in one standardized format.


## Supported input values for timestamp conversion

This library aims at going for simplicity by being explicit about the choices allowed to make. `utcnow` however allows the conversion methods to be called with the following kind of argument values:
* RFC 3339 compliant strings, which at the very least must include the full date, but could omit the time part of a date-time, leaving only the date, or by not including the seconds, microseconds or even laving out the timezone information – `utcnow` supports all of the use-cases of RFC 3339 inputs and then converts the input into an even more complete RFC 3339 timestamp in UTC timezone.
* The most common format for handling dates and datetimes in Python, the builtin `datetime.datetime` object values (both timezone aware values, as well as values that aren't timezone aware, as for which we'll assume UTC).
* Also supporting object values from other commonly used libraries, such as `arrow`.
* As a bonus – Unix time, mainly for convinience (`time.time()`) (we have many names for the things we love: epoch time, posix time, seconds since epoch, 2038-bug on 32-bit unsigned ints to time-travel back to the first radio-transmission across the atlantic, there will be movies about this ).


## A neat side-effect of defaulted string output – comparison as strings

> If date and time components are ordered from least precise to most precise, then a useful property is achieved.  Assuming that the time zones of the dates and times are the same (e.g., all in UTC), expressed using the same string (e.g., all "Z" or all "+00:00"), and all times have the same number of fractional second digits, then the date and time strings may be sorted as strings and a time-ordered sequence will result. he presence of optional punctuation would violate this characteristic.

Here follows a few examples of the problems with having to work with mismatching timestamps, even though the four example statements all use RFC 3339 compliant values. For example an API is kind enough for users to submit timestamps as long as they're good enough and for where the backend application has to convert inputs to values good for the cause.

*Matching two dates of different formats using strings won't go well at all. All of the following four string comparisons would've given an opposite result if compared as actual timestamps instead of as strings, where comparison is just alphabetic.*
```python
"2022-08-01 23:51:30.000000Z"          >  "2022-08-01T13:51:30.000000Z"          # False 😵
"2022-08-01 14:00:10"                  >  "2022-08-01T13:51:30.000000Z"          # False 😵
"2022-08-01T14:00:10+01:00"            >  "2022-08-01T13:51:30.000000Z"          # True  😵
"2022-08-01T13:51Z"                    >  "2022-08-01T13:51:30.000000Z"          # True  😵
```

*Using `utcnow` on the same set of timestamps, which returns a string value for comparison.
```python
from utcnow import utcnow

utcnow("2022-08-01 23:51:30.000000Z")  >  utcnow("2022-08-01T13:51:30.000000Z")  # True  🎉
utcnow("2022-08-01 14:00:10")          >  utcnow("2022-08-01T13:51:30.000000Z")  # True  ✅
utcnow("2022-08-01T14:00:10+01:00")    >  utcnow("2022-08-01T13:51:30.000000Z")  # False 🥇
utcnow("2022-08-01T13:51Z")            >  utcnow("2022-08-01T13:51:30.000000Z")  # False 😻
```

*This shown the returned values from the `utcnow` calls, and for what the comparisons is actually evaluated on.
```python
"2022-08-01T23:51:30.000000Z"          >  "2022-08-01T13:51:30.000000Z"          # True  🎉
"2022-08-01T14:00:10.000000Z"          >  "2022-08-01T13:51:30.000000Z"          # True  ✅
"2022-08-01T13:00:10.000000Z"          >  "2022-08-01T13:51:30.000000Z"          # False 🥇
"2022-08-01T13:51:00.000000Z"          >  "2022-08-01T13:51:30.000000Z"          # False 😻
```


## Transformation examples

Some additional examples of timestamps and to what they whould be converted. Thre first three examples are from the RFC document.

```python
import utcnow

# This represents 20 minutes and 50.52 seconds after the 23rd hour of April 12th, 1985 in UTC.
utcnow.get("1985-04-12T23:20:50.52Z")           # "1985-04-12T23:20:50.520000Z"

# This represents 39 minutes and 57 seconds after the 16th hour of December 19th, 1996 with an
# offset of -08:00 from UTC (Pacific Standard Time).  Note that this is equivalent to
# 1996-12-20T00:39:57Z in UTC.
utcnow.get("1996-12-19T16:39:57-08:00")         # "1996-12-20T00:39:57.000000Z"

# This represents the same instant of time as noon, January 1, 1937, Netherlands time. Standard
# time in the Netherlands was exactly 19 minutes and 32.13 seconds ahead of UTC by law from
# 1909-05-01 through 1937-06-30.
utcnow.get("1937-01-01T12:00:27.87+00:20")      # "1937-01-01T11:40:27.870000Z"

# Examples of other formats of accepted inputs:
utcnow.get("2021-02-18")                        # "2021-02-18T00:00:00.000000Z"
utcnow.get("2021-02-18 01:00")                  # "2021-02-18T01:00:00.000000Z"
utcnow.get("2021-02-18 03:00+01:00")            # "2021-02-18T02:00:00.000000Z"
utcnow.get("2021-02-18-01:00")                  # "2021-02-18T01:00:00.000000Z"
utcnow.get("2021-02-18+01:00")                  # "2021-02-17T23:00:00.000000Z"
utcnow.get("2021-02-18T23:55")                  # "2021-02-18T23:55:00.000000Z"
utcnow.get("2021-02-18T23:55:10")               # "2021-02-18T23:55:10.000000Z"
utcnow.get("2021-02-18T23:55:10.0")             # "2021-02-18T23:55:10.000000Z"
utcnow.get("2021-02-18T23:55:10.0+05:00")       # "2021-02-18T18:55:10.000000Z"
utcnow.get("2021-02-18T23:55:10.0-05:00")       # "2021-02-19T04:55:10.000000Z"
utcnow.get("2021-02-18T23:55:10.550-05:00")     # "2021-02-19T04:55:10.550000Z"
utcnow.get("2021-02-18 23:55:10.550+05:00")     # "2021-02-18T18:55:10.550000Z"
utcnow.get("2021-02-18 23:55:10.550-01:00")     # "2021-02-19T00:55:10.550000Z"
utcnow.get("2021-02-28 10:10:59.123987+00:00")  # "2021-02-28T10:10:59.123987Z"
utcnow.get("2021-02-28 10:10:59.123987Z")       # "2021-02-28T10:10:59.123987Z"
utcnow.get("2021-02-28 10:10:59.123987 UTC")    # "2021-02-28T10:10:59.123987Z"
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
result = utcnow.get("1984-08-01 13:38")
# "1984-08-01T13:38:00.000000Z"
```

```python
# RFC 3339 timestamps as input – dates and datetimes – UTC will be assumed if tz is left out

from utcnow import utcnow
result = utcnow.get("2077-10-27")
# "2077-10-27T00:00:00.000000Z"
```

```python
# Simple exmple of converting a naive datetime value, assuming UTC

import datetime
from utcnow import utcnow
dt = datetime.datetime(1984, 8, 1, 13, 38, 0, 4711)
result = utcnow.get(dt)
# "1984-08-01T13:38:00.004711Z"

# for non-tz-aware datetimes, the same result would be returned by both:
# 1. utcnow.get(dt)
# 2. dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
```

```python
# It's also possible to transform datetime values with timezone offsets into timestamp strings

import datetime
from utcnow import utcnow
tz_EDT = datetime.timezone(offset=datetime.timedelta(hours=-4))
dt = datetime.datetime(1997, 8, 4, 2, 14, tzinfo=tz_EDT)
result = utcnow.get(dt)
# "1997-08-04T06:14:00.000000Z"

# for timezone-aware datetimes, the same result would be returned by both:
# 1. utcnow.get(dt)
# 2. dt.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
```

```python
# Or vice versa, transforming a timestamp string into a datetime object (with tzinfo set to UTC)

from utcnow import utcnow
result = utcnow.as_datetime("1984-08-01T13:38:00.123450Z")
# datetime.datetime(1984, 8, 1, 13, 38, 0, 123450, tzinfo=datetime.timezone.utc)
```

```python
# Example of using a value from "arrow" – a popular date-time Python lib with a large featureset

import arrow
from utcnow import utcnow
value = arrow.get("2021-04-30T07:58:30.047110+02:00")
# <Arrow [2021-04-30T07:58:30.047110+02:00]>

str(value)
# "2021-04-30T07:58:30.047110+02:00"

result = utcnow.get(value)
# "2021-04-30T05:58:30.047110Z"

# the same output as via utcnow can be returned in the following ways, including direct via arrow:
# 1. utcnow.get(value)
# 2. value.to("UTC").strftime("%Y-%m-%dT%H:%M:%S.%fZ")
```

```python
# Getting the current server time in UTC as a timestamp string

import utcnow
utcnow.utcnow()
# "2021-02-18T08:24:48.382262Z"

# same thing can be accomplished using datetime and all of these calls returns the same str value:
# 1. utcnow.utcnow()
# 2. str(utcnow)
# 3. str(utcnow.utcnow)
# 4. utcnow.get()
# 5. utcnow.utcnow.get()
# 6. datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
# 7. datetime.datetime.utcnow().isoformat() + "Z"
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
# "2021-02-18T08:24:48.382262Z"
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
result = f"Current server time is: '{utcnow}'"
# "Current server time is: '2021-02-18T08:24:48.382262Z'"
```


## Finally

This is not a fullblown date library at all – it's simple and basically it just output timestamps into the fixes length string format `YYYY-MM-DDTHH:mm:ss.uuuuuuZ` (or as `%Y-%m-%dT%H:%M:%SZ` as if used with `datetime.datetime.strftime`). Always uses UTC in output and always appends the UTC timezone as a `Z` to the string (instead of using `+00:00` or ` UTC`).

There's no other external dependencies required. A convenient utility package for when you need to store timestamps in a datastore as a string, adding it to a JSON response or using a shared and common standard in your log outputs.

Wether you choose to use this library or anything else, or just specify _this is how we do it_ in a documement, it'll be worth it. It's never too late to start aligning your formatting standards and interfaces.

