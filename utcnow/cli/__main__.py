#!/usr/bin/env python
import sys

from utcnow.cli import entrypoint

if __name__ == "__main__":  # pragma: no cover
    argv = sys.argv[1:] if sys.argv else []
    sys.exit(entrypoint(argv))
