#!/usr/bin/env python
if __name__ == "__main__":  # pragma: no cover
    import sys  # isort:skip
    from utcnow.interface import cli_entrypoint  # isort:skip

    argv = sys.argv[1:] if sys.argv else []
    exit_code: int = cli_entrypoint(argv)
    if exit_code:
        sys.exit(exit_code)
