import sqlite3

from ai.definitions import (
    TABLE_COLUMN_ITEM, AIArticleData, AIExecutionData, CREATE_AI_PROCESSED_TABLE
)

def fetch_one_column(column_key: TABLE_COLUMN_ITEM, conn: sqlite3.Connection) -> list:
    cursor = conn.cursor()

    ALLOWED_CORSOR = TABLE_COLUMN_ITEM

    if column_key not in ALLOWED_CORSOR:
        raise ValueError(f"Invalid value for table cursor: {column_key}")

    cursor.execute(f"SELECT {column_key} FROM ai_processed")

    rows = cursor.fetchall()

    #以下の判別は変更に弱い。方法を変更すること。
    #なぜこうしているのか。cursor.fetchall()の性質上、それぞれの値が単一であったとしても、(value,)というタプルで返されるため、
    #これをvalueそのものに置き換えるためである。
    if not column_key == "title":
        rows = [row[0] for row in rows]
        return rows 
    elif column_key == "tags":
        return rows

    raise ValueError(f"Invalid value: {column_key} was selected as column_key of ai_processed TABLE.") 


#hash_valuesは、今までにAI処理をした記事の本文ハッシュ値リスト
def convert_article_to_execution(ai_data_list: list[AIArticleData], hash_values: list) -> list[AIExecutionData]:

    ai_execution_list: list[AIExecutionData] = [] 

    #ai_articleからai_executionに移す。
    for ai_data in ai_data_list:
        ai_execution_data: AIExecutionData = {
            "data_type": "execution",

            "id": ai_data["id"],
            "title": ai_data["title"],
            "body": ai_data["body"],
            "tags": ai_data["tags"],
            "hash_value": ai_data["hash_value"],

            "reuse": True if ai_data["hash_value"] in hash_values else False
        }

        ai_execution_list.append(ai_execution_data)

    return ai_execution_list


def execution_planner(ai_data_list: list[AIArticleData]) -> list[AIExecutionData]:

    ai_processed_conn = sqlite3.connect("ai_processed_data.db")
    ai_processed_conn.execute(CREATE_AI_PROCESSED_TABLE)

    try:
        hash_values: list = fetch_one_column("hash_value", ai_processed_conn)

        ai_execution_list = convert_article_to_execution(ai_data_list, hash_values)

        return ai_execution_list
    finally:
        ai_processed_conn.close()

