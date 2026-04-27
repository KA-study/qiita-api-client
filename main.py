# Build the program. This file is entry point.

import argparse

from config import URL, TAG_DEFAULT, SORT_DEFAULT, KEYWORD_DEFAULT, LIMIT_DEFAULT


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tag",
        default=TAG_DEFAULT,
        help="set a tag relate to what you are interested in.",
    )
    parser.add_argument(
        "--sort",
        default=SORT_DEFAULT,
        choices=["created", "reactions", "stock"],
        help="set a sorting criteria.",
    )
    parser.add_argument(
        "--keyword",
        default=KEYWORD_DEFAULT,
        help="set a keyword relate to what you are interested in.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=LIMIT_DEFAULT,
        help="set the number of articles you want to get.",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
