#!/usr/bin/env python
import sys
from typing import List, Optional

from utcnow import as_unixtime, rfc3339_timestamp


def error_message(message: str, usage: Optional[str] = None) -> str:
    if not usage:
        return f"error:\n  {message}\n"

    return f"error:\n  {message}\n\nusage:\n  {usage}"


def get_error_options(argv: List[str]) -> str:
    return ", ".join(
        [
            v
            for v in (argv if "--" not in argv else argv[: argv.index("--")])
            if v.startswith("-") and not v[1:2].isdigit()
        ]
    )


def cli_entrypoint(argv: Optional[List[str]] = None) -> int:
    if argv is None:  # pragma: no cover
        argv = sys.argv[1:]
    if argv and ("-v" in argv or "--version" in argv or "version" in argv):
        # utcnow --version
        from utcnow import __version__  # isort:skip

        print(__version__)
    else:
        if argv and ("-h" in argv or "--help" in argv or "help" in argv):
            # utcnow --help
            from utcnow import __version__  # isort:skip

            print("usage:")
            print("  utcnow [values ...]              | default     output in rfc3339 format")
            print("  utcnow --unixtime [values ...]   | short: -u   output as unixtime")
            print("  utcnow --diff <from> <to>        | short: -d   diff in seconds: from -> to")
            print("")
            print("help:")
            print("  utcnow --help                    | short: -h   display this message")
            print(f"  utcnow --version                 | short: -v   installed version ({__version__})")
        elif argv and ("-d" in argv or "--diff" in argv):
            usage = "utcnow --diff <from> <to>"
            argv = [v for v in argv if v not in ("-d", "--diff")]

            error_options = get_error_options(argv)
            if "--" in argv:
                argv.pop(argv.index("--"))
            if error_options or len(argv) != 2:
                if error_options:
                    print(error_message(f"invalid option(s) for --diff: {error_options}.", usage), file=sys.stderr)
                elif len(argv) < 2:
                    print(error_message("missing arguments - 'from' and 'to' are required.", usage), file=sys.stderr)
                elif len(argv) > 2:
                    print(error_message("too many arguments - only specify 'from' and 'to'.", usage), file=sys.stderr)
                return 1

            from_value, to_value = argv

            try:
                unixtime_from = as_unixtime(from_value)
            except ValueError:
                print(
                    error_message(f"invalid input value for 'from' argument: \"{from_value}\".", usage), file=sys.stderr
                )
                return 1

            try:
                unixtime_to = as_unixtime(to_value)
            except ValueError:
                print(error_message(f"invalid input value for 'to' argument: \"{to_value}\".", usage), file=sys.stderr)
                return 1

            diff_value = unixtime_to - unixtime_from
            output = str(f"{diff_value:.6f}")
            if "." in output:
                diff_value = float(output[0 : output.index(".") + 7])
                output = str(f"{diff_value:.6f}").rstrip("0").rstrip(".")
            print(output)
        else:
            output_unixtime = False
            if argv and (
                "-u" in argv or "--unixtime" in argv or "--unixtimestamp" in argv or "--unix-timestamp" in argv
            ):
                usage = "utcnow --unixtime [values ...]"
                argv = [v for v in argv if v not in ("-u", "--unixtime", "--unixtimestamp", "--unix-timestamp")]

                error_options = get_error_options(argv)
                if error_options:
                    print(error_message(f"invalid option(s) for --unixtime: {error_options}.", usage), file=sys.stderr)
                    return 1

                output_unixtime = True
            else:
                usage = "utcnow [values ...]"
                error_options = get_error_options(argv)
                if error_options:
                    print(error_message(f"invalid option(s): {error_options}.", usage), file=sys.stderr)
                    return 1

            if "--" in argv:
                argv.pop(argv.index("--"))

            if not argv:
                print(rfc3339_timestamp() if output_unixtime is False else str(as_unixtime()))
            else:
                values = [
                    (
                        (int(v) if "." not in v else float(v))
                        if (
                            v not in (".", "-")
                            and len(v.lstrip("-")) + 1 >= len(v)
                            and v.lstrip("-").replace(".", "", 1).isdigit()
                        )
                        else v
                    )
                    for v in argv
                ]
                output = ""
                for value in values:
                    try:
                        output += rfc3339_timestamp(value) if output_unixtime is False else str(as_unixtime(value))
                        output += "\n"
                    except ValueError:
                        print(error_message(f'invalid input value: "{value}".'), file=sys.stderr)
                        return 1
                print(output.strip("\n"))

    return 0
