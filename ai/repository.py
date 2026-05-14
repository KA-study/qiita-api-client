import sqlite3

from ai.definitions import (
    TABLE_COLUMN_ITEM, AIArticleData, AIExecutionData, CREATE_AI_PROCESSED_TABLE
)

def fetch_one_column(column_key: TABLE_COLUMN_ITEM, conn: sqlite3.Connection) -> list:
    cursor = conn.cursor()
    cursor.execute(f"SELECT {column_key} FROM ai_processed")

    rows = cursor.fetchall()

    #以下の判別は変更に弱い。方法を変更すること。
    if not column_key == "title" and column_key in TABLE_COLUMN_ITEM:
        for row in rows:
            row = row[0]
        return rows
    elif column_key == "tags":
        return rows

    raise ValueError(f"Invalid value: {column_key} was selected as column_key of ai_processed TABLE.") 


#hash_valuesは、今までにAI処理をした記事の本文ハッシュ値リスト
def convert_article_to_execution(ai_data_list: list[AIArticleData], hash_values: list) -> list[AIExecutionData]:

    ai_execution_list: list[AIExecutionData] = [] 

    #ai_articleからai_executionに移す。
    for ai_data, ai_execution_data in zip(ai_data_list, ai_execution_list):

        if ai_data["hash_value"] in hash_values:
            ai_execution_data["reuse"] = True
        else:
            ai_execution_data["id"] = ai_data["id"]
            ai_execution_data["title"] = ai_data["title"]
            ai_execution_data["body"] = ai_data["body"]
            ai_execution_data["tags"] = ai_data["tags"]
            ai_execution_data["hash_value"] = ai_data["hash_value"]

            ai_execution_data["reuse"] = False

    return ai_execution_list


def DB_main_fetcher(ai_data_list: list[AIArticleData]) -> list[AIExecutionData]:

    ai_processed_conn = sqlite3.connect("ai_processed_data.db")
    ai_processed_conn.execute(CREATE_AI_PROCESSED_TABLE)

    try:
        hash_values: list = fetch_one_column("hash_value", ai_processed_conn)

        ai_execution_list = convert_article_to_execution(ai_data_list, hash_values)

        return ai_execution_list
    finally:
        ai_processed_conn.close()

