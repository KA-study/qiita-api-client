import re
import hashlib
import sqlite3

from storage.scheme import ArticleData
from ai.definitions import (
    AIArticleData,
    AIExecutionData,
    CREATE_AI_PROCESSED_TABLE,
    TABLE_COLUMN_ITEM,
)


def normalize_body(body: str) -> str:

    # image
    body = re.sub(r"!\[.*?\]\(.*?\)", "[IMAGE]", body)

    # html
    body = re.sub(r"<[^>]+>", "", body)

    # url
    body = re.sub(r"https?://\S+", "[URL]", body)

    # multiple blank lines
    body = re.sub(r"\n{3,}", "\n\n", body)

    return body.strip()


def hash_body(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def normalize_for_ai(data: ArticleData) -> AIArticleData:
    ai_data: AIArticleData = {
        "data_type": "article",
        "id": "",
        "title": "",
        "body": "",
        "tags": [],
        "hash_value": "",
    }

    ai_data["id"] = data["id"]
    ai_data["title"] = data["title"]
    ai_data["body"] = normalize_body(data["body"])
    ai_data["tags"] = data["tags"]
    ai_data["hash_value"] = hash_body(data["body"])

    return ai_data


def fetch_one_column(column_key: TABLE_COLUMN_ITEM, conn: sqlite3.Connection) -> list:
    cursor = conn.cursor()
    cursor.execute(f"SELECT {column_key} FROM ai_processed")

    rows = cursor.fetchall()

    # 以下の判別は変更に弱い。方法を変更すること。
    if not column_key == "title" and column_key in TABLE_COLUMN_ITEM:
        for row in rows:
            row = row[0]
        return rows
    elif column_key == "tags":
        return rows

    raise ValueError(
        f"Invalid value: {column_key} was selected as column_key of ai_processed TABLE."
    )


def DB_processor(ai_data_list: list[AIArticleData]) -> list[AIExecutionData]:

    ai_processed_conn = sqlite3.connect("ai_processed_data.db")
    ai_processed_conn.execute(CREATE_AI_PROCESSED_TABLE)

    try:
        hash_values: list = fetch_one_column("hash_value", ai_processed_conn)

    finally:
        ai_processed_conn.close()
