# Build the program. This file is entry point.

import argparse

from fetcher import FetchClientAbstract, QiitaClient
from processor import normalize, sort_data
from output import output

from config import (
    URL,
    TAG_DEFAULT,
    KEYWORD_DEFAULT,
    QUERY_DEFAULT,
    PER_PAGE_DEFAULT,
    PAGE_DEFAULT,
    SortOption,
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
        The choices are user/stocks/created/title....\n
        Do not include --sort parameter as an puery.
        """,
    )
    parser.add_argument(
        # choicesを決めておくことで、誤った入力があった時に正常終了し、ただし選択肢をユーザーに伝える。
        "--sort",
        default=SortOption.CREATED_AT.name,
        choices=[s.name for s in SortOption],
        help="set a sorting criteria.\n "
        "Some functions can be used via API, while others can only be used locally.",
    )
    parser.add_argument(
        "--page", type=int, default=PAGE_DEFAULT, help="set a page number you need"
    )
    parser.add_argument(
        "--per_page",
        type=int,
        default=PER_PAGE_DEFAULT,
        help="set the number of articles you want to get from a page.",
    )

    # 文字列を.nameとして扱い、メンバを呼び出す。
    args = parser.parse_args()
    args.sort = SortOption[args.sort]

    # 並び替えのパラメータはすべてSortOptionに束ね、クエリには含めない。
    if "sort:" in args.query:
        raise ValueError("sortは--sortで指定してください。")

    return args


def build_query(args: argparse.Namespace) -> str:
    parts = []

    parts.append(args.keyword)
    # sortの設計に問題があったため、API動作確認のため、一時的にstock:>20を追加。
    parts.append(f"tag:{args.tag} stocks:>20")
    parts.append(args.query)

    # クエリパラメーターはスペース区切りの文字列。
    return " ".join(parts)


def main():
    # CLI入力 → クエリ構築 → API取得 → 正規化 → 出力
    args = parse_arguments()

    query = build_query(args)

    params = {
        "query": query,
        "page": args.page,
        "per_page": args.per_page,
    }
    if args.sort.value[1]:
        params["sort"] = args.sort.value[0]
        params["order"] = "desc"

    qitta_client = QiitaClient(url=URL)

    articles = qitta_client.fetch(params)

    # normalizeは一つずつの記事を処理
    data = [normalize(item) for item in articles]

    sorted_data = sort_data(data, args.sort)

    output(sorted_data)


main()
