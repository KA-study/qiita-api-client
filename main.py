# Build the program. This file is entry point.

import argparse

from fetcher import fetcher
from processor import normalize, sort_data

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
        choices=["created_at", "updated_at", "likes"],
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

    # クエリパラメーターはスペース区切りの文字列。
    return " ".join(parts)


def main():
    # CLI入力 → クエリ構築 → API取得 → 正規化 → 出力
    args = parse_arguments()

    puery = build_query(args)

    params = {"query": puery, "page": args.page, "per_page": args.per_page}

    json = fetcher(params)

    # normalizeは一つずつの記事を処理
    data = [normalize(item) for item in json]

    sorted_data = sort_data(data, args)
