from typing import Any

from utcnow import __version__ as utcnow_version
from utcnow.cli.__version__ import __version__ as cli_version
from utcnow.interface import cli_entrypoint, error_message, get_error_options


def test_version_cli_package() -> None:
    assert cli_version == "1.0.0"


def test_cli_version_option(capsys: Any) -> None:
    exit_code = cli_entrypoint(["--version"])
    out, err = capsys.readouterr()
    assert err == ""
    assert exit_code == 0
    assert out == f"{utcnow_version}\n"


def test_cli_help_option(capsys: Any) -> None:
    exit_code = cli_entrypoint(["--help"])
    out, err = capsys.readouterr()
    assert err == ""
    assert exit_code == 0
    assert len(out)


def test_cli_no_arguments(capsys: Any) -> None:
    exit_code = cli_entrypoint([])
    out, err = capsys.readouterr()
    assert err == ""
    assert exit_code == 0
    assert len(out) == 27 + 1
    assert len(out.rstrip("\n")) == 27


def test_cli_arguments(capsys: Any) -> None:
    exit_code = cli_entrypoint(["1984-08-01 23:59", "--", "1000", "-1000.553999"])
    out, err = capsys.readouterr()
    assert err == ""
    assert exit_code == 0
    assert out.split("\n")[0] == "1984-08-01T23:59:00.000000Z"
    assert out.split("\n")[1] == "1970-01-01T00:16:40.000000Z"
    assert out.split("\n")[2] == "1969-12-31T23:43:19.446001Z"


def test_cli_unixtime(capsys: Any) -> None:
    exit_code = cli_entrypoint(["-u"])
    out, err = capsys.readouterr()
    assert err == ""
    assert exit_code == 0
    assert float(out.rstrip("\n")) > 0


def test_cli_unixtime_negative(capsys: Any) -> None:
    exit_code = cli_entrypoint(["-u", "-1"])
    out, err = capsys.readouterr()
    assert err == ""
    assert exit_code == 0
    assert float(out.rstrip("\n")) < 0


def test_cli_unixtime_invalid_argument(capsys: Any) -> None:
    exit_code = cli_entrypoint(["-u", "--test"])
    out, err = capsys.readouterr()
    assert err != ""
    assert exit_code == 1
    assert out == ""



def test_cli_diff(capsys: Any) -> None:
    exit_code = cli_entrypoint(["-d", "2020-01-01T00:00:00Z", "2020-01-01T00:00:01Z"])
    out, err = capsys.readouterr()
    assert err == ""
    assert exit_code == 0
    assert out.rstrip("\n") == "1"


def test_cli_diff_fraction(capsys: Any) -> None:
    exit_code = cli_entrypoint(["-d", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00.000001Z"])
    out, err = capsys.readouterr()
    assert err == ""
    assert exit_code == 0
    assert out.rstrip("\n") == "0.000001"


def test_cli_invalid_value(capsys: Any) -> None:
    exit_code = cli_entrypoint(["test"])
    out, err = capsys.readouterr()
    assert err != ""
    assert exit_code == 1
    assert out == ""


def test_cli_invalid_argument(capsys: Any) -> None:
    exit_code = cli_entrypoint(["--test"])
    out, err = capsys.readouterr()
    assert err != ""
    assert exit_code == 1
    assert out == ""


def test_cli_invalid_diff_argument(capsys: Any) -> None:
    exit_code = cli_entrypoint(["--diff", "--test"])
    out, err = capsys.readouterr()
    assert err != ""
    assert exit_code == 1
    assert out == ""


def test_cli_invalid_diff_from(capsys: Any) -> None:
    exit_code = cli_entrypoint(["--diff", "test", "0"])
    out, err = capsys.readouterr()
    assert err != ""
    assert exit_code == 1
    assert out == ""


def test_cli_invalid_diff_to(capsys: Any) -> None:
    exit_code = cli_entrypoint(["--diff", "0", "test"])
    out, err = capsys.readouterr()
    assert err != ""
    assert exit_code == 1
    assert out == ""


def test_cli_missing_diff_argument(capsys: Any) -> None:
    exit_code = cli_entrypoint(["--diff", "1"])
    out, err = capsys.readouterr()
    assert err != ""
    assert exit_code == 1
    assert out == ""


def test_cli_too_many_diff_arguments(capsys: Any) -> None:
    exit_code = cli_entrypoint(["--diff", "1", "2", "--", "3"])
    out, err = capsys.readouterr()
    assert err != ""
    assert exit_code == 1
    assert out == ""
