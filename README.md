# EFU CSV Utilities

Utilities for parsing and writing Everything EFU CSV files.

This package provides helper functions for losslessly converting between Everything's EFU CSV format and Python objects. It preserves the original newline style and quoting rules so that files can be parsed and written back verbatim. A small CLI is included for round‐trip verification.

The repository also contains a standalone project under
[`runtimeinfo/`](runtimeinfo/). That package provides a CLI for displaying
runtime host information such as hostname and IP address.
Each project contains its own tests. Navigate into the desired subdirectory and run `pytest -q`.

## Documentation

- [Specification](docs/REFERENCE.md)
- [Time Columns](docs/filetime.md)
- [Attribute Flags](docs/attribute-flags.md)
- [JSON Example](docs/json.md)
- [Remote Import Guide](docs/REMOTE.md)

Additional documentation resides in the `docs` directory.
