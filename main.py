# Build the program. This file is entry point.

import argparse

from fetcher import fetch_pagenator
from processor import normalize, sort_data
from output import output

from config import (
    URL,
    TAG_DEFAULT,
    STOCKS_DEFAULT,
    KEYWORD_DEFAULT,
    QUERY_DEFAULT,
    NUMBER_OF_ARTICLES_DEFAULT,
)
from processor import SORT_MAP
from storage import update_data


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
        "--stocks",
        default=STOCKS_DEFAULT,
        help="set a smallest number of stocks you want to get articles.",
    )
    parser.add_argument(
        "--query",
        default=QUERY_DEFAULT,
        help="""set strings in query format.
        The choices are user/stocks/created/title....\n
        Do not include --sort parameter as an puery.
        """,
    )
    parser.add_argument(
        # choicesを決めておくことで、誤った入力があった時に正常終了し、ただし選択肢をユーザーに伝える。
        "--sort",
        default="created_at",
        choices=[s for s in SORT_MAP],  # keyのみ反復
        help="set a sorting criteria.\n " "This is local sort.",
    )
    parser.add_argument(
        "--number_of_articles",
        type=int,
        default=NUMBER_OF_ARTICLES_DEFAULT,
        help="set the number of articles you want to get from a page.",
    )

    args = parser.parse_args()

    # sort_keyを文字列からSortOption型オブジェクトに変換
    args.sort = SORT_MAP[args.sort]

    # 並び替えのパラメータはすべてSortOptionに束ね、クエリには含めない。
    if "sort:" in args.query:
        raise ValueError("sortは--sortで指定してください。")

    return args


def build_query(args: argparse.Namespace) -> str:
    parts = []

    parts.append(args.keyword)
    # sortの設計に問題があったため、API動作確認のため、一時的にstock:>20を追加。
    parts.append(f"tag:{args.tag}")
    parts.append(f"stocks:>{args.stocks}")
    parts.append(args.query)

    # クエリパラメーターはスペース区切りの文字列。
    return " ".join(parts)


def main():
    # CLI入力 → クエリ構築 → API取得 → 正規化 → 出力
    args = parse_arguments()  # parse_argsではない。ユーザー定義関数。

    query = build_query(args)

    params = {
        "query": query,
        "page": ...,
        "per_page": args.number_of_articles,
    }

    articles = fetch_pagenator(params, url=URL)

    # normalizeは一つずつの記事を処理
    data = [normalize(item) for item in articles]

    # json logファイル操作
    logs = update_data(
        # args.sortはSortOption型、args.sort.sort_keyはstr型
        tag=args.tag,
        keyword=args.keyword,
        sort=args.sort.sort_key,  # args.sortはSortOption型
    )

    sorted_data = sort_data(logs, data, args.sort)

    output(sorted_data)


main()
