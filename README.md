# EFU CSV Utilities

Utilities for parsing and writing Everything EFU CSV files.

This package provides helper functions for losslessly converting between
Everything's EFU CSV format and Python objects. It preserves the original
newline style and quoting rules so that files can be parsed and written back
verbatim. A small CLI is included for round‐trip verification.

See [docs/README.md](docs/README.md) for the full design specification.
Additional documentation resides in the `docs` directory.
