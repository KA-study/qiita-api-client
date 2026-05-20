import sqlite3
from datetime import datetime

from ai.definitions import (
    CREATE_COST_LOG_TABLE, CREATE_AI_PROCESSED_DATA_TABLE, CREATE_AI_PROCESSED_HASH_INDEX, CREATE_COST_STATE_TABLE,
    COST_STATE, DB_PATH, AIMetaData, EVENT_TYPE
    )


class CostRepository:

    def __init__(self):
        self.__conn = sqlite3.connect(DB_PATH) 
        self.__conn.row_factory = sqlite3.Row

        self.initialize_log()
        self.initialize_state()
        self.initialize_processed_data_table()


    @property
    def conn(self) -> sqlite3.Connection:
        return self.__conn
   

    def initialize_log(self) -> None:
        cursor = self.conn.cursor()

        cursor.execute(CREATE_COST_LOG_TABLE)

        self.conn.commit()

    def initialize_state(self) -> None:
        cursor = self.conn.cursor()

        cursor.execute(CREATE_COST_STATE_TABLE)

        cursor.execute("""
        INSERT OR IGNORE INTO cost_state (
            scope,
            available_tokens,
            used_tokens,
            last_log_id,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            "global",
            10000,
            0,
            "",
            datetime.now().isoformat()
        ))

        self.conn.commit()

    def initialize_processed_data_table(self) -> None:
        cursor = self.conn.cursor()

        cursor.execute(CREATE_AI_PROCESSED_DATA_TABLE)
        cursor.execute(CREATE_AI_PROCESSED_HASH_INDEX)

        self.conn.commit()

    def close(self) -> None:
        self.conn.close()


    def __insert_log(self, article_id: str, metadata: AIMetaData):
        cursor = self.conn.cursor()

        note = ""
        event_type = EVENT_TYPE

        cursor.execute("""
        INSERT INTO cost_events (
            article_id,
            created_at,
            event_type,
            prompt_tokens,
            completion_tokens,
            total_tokens,
            note
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            article_id,
            datetime.now().isoformat(),
            event_type,
            metadata.used_prompt_tokens,
            metadata.used_completion_tokens,
            metadata.used_total_tokens,
            note
        ))

    def __update_cost_state(self):
        cursor = self.conn.cursor()

        # 1. 現在のstate取得
        cursor.execute("""
        SELECT *
        FROM cost_state
        WHERE scope = 'global'
        """)
        state = cursor.fetchone()

        last_log_id = state["last_log_id"]

        # 2. 未処理ログだけ取得
        cursor.execute("""
        SELECT id, prompt_tokens, completion_tokens, total_tokens
        FROM cost_events
        WHERE id > ?
        ORDER BY id ASC
        """, (last_log_id,))

        rows = cursor.fetchall()

        if not rows:
            return

        # 3. 差分集計
        delta_prompt = 0
        delta_completion = 0
        delta_total = 0
        max_id = last_log_id

        for r in rows:
            delta_prompt += r["prompt_tokens"]
            delta_completion += r["completion_tokens"]
            delta_total += r["total_tokens"]
            max_id = max(max_id, r["id"])

        # 4. state更新（加算型）
        cursor.execute("""
        UPDATE cost_state
        SET
            used_tokens = used_tokens + ?,
            available_tokens = available_tokens - ?,
            last_log_id = ?,
            updated_at = ?
        WHERE scope = 'global'
        """, (
            delta_total,
            delta_total,
            max_id,
            datetime.now().isoformat()
        ))       

    def record_ai_usage(self, article_id: str, metadata: AIMetaData) -> None:
        with self.conn:  # ← トランザクション開始
            self.__insert_log(article_id, metadata)
            self.__update_cost_state()       


    #cost_stateテーブルから情報を取得する関数。
    #logテーブルから情報をcost_stateテーブルに移す関数はまだ実装していない。
    def get_current_state(self) -> COST_STATE:
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT *
        FROM cost_state
        WHERE scope = ?
        """, ("global",))

        row = cursor.fetchone()

        if row is None:
            cost_state = COST_STATE(
                scope="",

                available_tokens=0,
                used_tokens=0,
                last_log_id="",

                updated_at=""
            )

            return cost_state

        cost_state = COST_STATE(
            scope=(row)["scope"],

            available_tokens=(row)["available_tokens"],
            used_tokens=(row)["used_tokens"],
            last_log_id=(row)["last_log_id"],

            updated_at=(row)["updated_at"],
        )

        return cost_state