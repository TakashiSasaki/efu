from typing import Optional, List

from .root import Root


def main(argv: Optional[List[str]] = None) -> None:
    """Command line interface for displaying Root information."""
    import argparse

    parser = argparse.ArgumentParser(description="Show Root information")
    parser.add_argument("path", nargs="?", help="Optional path", default=None)
    parser.add_argument(
        "--json", action="store_true", help="Output canonical JSON"
    )
    args = parser.parse_args(argv)

    root = Root(args.path)
    if args.json:
        print(root.to_json())
    else:
        print(str(root))
