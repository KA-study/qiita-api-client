# Build the program. This file is entry point.

import argparse

from fetcher import fetcher

from config import (
    TAG_DEFAULT,
    KEYWORD_DEFAULT,
    QUERY_DEFAULT,
    SORT_DEFAULT,
    PER_PAGE_DEFAULT,
    PAGE_DEFAULT,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--keyword",
        default=KEYWORD_DEFAULT,
        help="set a keyword relate to what you are interested in.",
    )
    parser.add_argument(
        "--tag",
        default=TAG_DEFAULT,
        help="set a tag relate to what you are interested in.",
    )
    parser.add_argument(
        "--query",
        default=QUERY_DEFAULT,
        help="""set strings in query format.
        The choices are user/stocks/created/title....
        """,
    )
    parser.add_argument(
        "--sort",
        default=SORT_DEFAULT,
        choices=["created", "reactions", "stock"],
        help="set a sorting criteria.",
    )
    parser.add_argument(
        "--page", default=PAGE_DEFAULT, help="set a page number you need"
    )
    parser.add_argument(
        "--per_page",
        type=int,
        default=PER_PAGE_DEFAULT,
        help="set the number of articles you want to get from a page.",
    )

    return parser.parse_args()


def build_query(args: argparse.Namespace) -> str:
    parts = []

    parts.append(args.keyword)
    parts.append(f"tag:{args.tag}")
    parts.append(args.query)

    return " ".join(parts)


def main():
    args = parse_arguments()

    puery = build_query(args)

    params = {"query": puery, "page": args.page, "per_page": args.per_page}

    json = fetcher(params)
