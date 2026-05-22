import sqlite3
from datetime import datetime
from typing import Literal

from ai.definitions import (
    CREATE_AI_PROCESSED_DATA_TABLE, CREATE_AI_PROCESSED_HASH_INDEX,
    DB_PATH, AIProcessedData, AI_MODEL
)

class AIRepository:
    def __init__(self):
        self.__conn = sqlite3.connect(DB_PATH)
        self.__conn.row_factory = sqlite3.Row

        self.initialize_processed_table()


    def close(self) -> None:
            self.__conn.close()


    def initialize_processed_table(self) -> None:
        cursor = self.__conn.cursor()

        cursor.execute(CREATE_AI_PROCESSED_DATA_TABLE)
        cursor.execute(CREATE_AI_PROCESSED_HASH_INDEX)
        
        self.__conn.commit()


    def fetch_one_column_from_processed_table(self, column_key: str) -> list:
        cursor = self.__conn.cursor()

        cursor.execute(f"SELECT {column_key} FROM ai_processed_data")

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


    def fetch_one_row_from_processed_table(self, article_id: str) -> dict:
        cursor = self.__conn.cursor()
        
        cursor.execute(
            """
            SELECT *
            FROM ai_processed_data
            WHERE article_id = ?
            """,
            (article_id,)
        )

        row = cursor.fetchone()

        # データが存在しない場合
        if row is None:
            raise ValueError(f"No data found for article_id={article_id}")

        return dict(row)

    def record_ai_processed_data(self, processed_data: AIProcessedData) -> None:
        cursor = self.__conn.cursor()

        cursor.execute("""
            INSERT INTO ai_processed_data (
                article_id,
                hash_value,
                summary,
                reader_level,
                model_name,
                processed_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(article_id) DO UPDATE SET
                hash_value = excluded.hash_value,
                summary = excluded.summary,
                reader_level = excluded.reader_level,
                model_name = excluded.model_name,
                processed_at = excluded.processed_at
        """, (
            processed_data.id,
            processed_data.hash_value,
            processed_data.ai_output.summary,
            processed_data.ai_output.reader_level,
            AI_MODEL.name,
            datetime.now().isoformat()
        ))
    
        self.__conn.commit()
