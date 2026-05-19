import sqlite3
from pathlib import Path
from datetime import datetime

from ai.definitions import (
    CREATE_COST_LOG_TABLE, CREATE_AI_PROCESSED_TABLE, COST_STATE, DB_PATH
    )


def reserve_cost(
    execution_id: str,
    cost: int
) -> bool:

    conn = get_connection()

    try:
        cursor = conn.cursor()

        # lock
        cursor.execute("BEGIN IMMEDIATE")

        # 現在状態取得
        cursor.execute("""
        SELECT *
        FROM cost_state
        WHERE scope = ?
        """, ("global",))

        state = cursor.fetchone()

        if state is None:
            raise RuntimeError("state missing")

        available_cost = state["available_cost"]

        # 足りない
        if available_cost < cost:
            conn.rollback()
            return False

        now = datetime.now().isoformat()

        # event追加
        cursor.execute("""
        INSERT INTO cost_events (
            created_at,
            execution_id,
            event_type,
            delta_cost,
            note
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            now,
            execution_id,
            "reserve",
            -cost,
            ""
        ))

        # state更新
        cursor.execute("""
        UPDATE cost_state
        SET
            available_cost = available_cost - ?,
            reserved_cost = reserved_cost + ?,
            updated_at = ?
        WHERE scope = ?
        """, (
            cost,
            cost,
            now,
            "global"
        ))

        conn.commit()

        return True

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


class CostRepository:

    def __init__(self):
        self.__conn = sqlite3.connect(DB_PATH) 
        self.__conn.row_factory = sqlite3.Row

        self.initialize_db()
        self.initialize_state()


    @property
    def conn(self) -> sqlite3.Connection:
        return self.__conn

   
    def initialize_db(self) -> None:
        cursor = self.conn.cursor()

        cursor.execute(CREATE_COST_LOG_TABLE)
        cursor.execute(CREATE_AI_PROCESSED_TABLE)

        self.conn.commit()


    def initialize_state(self) -> None:
        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT OR IGNORE INTO cost_state (
            scope,
            available_cost,
            reserved_cost,
            committed_cost,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            "global",
            10000,
            0,
            0,
            datetime.now().isoformat()
        ))

        self.conn.commit()


    def close(self) -> None:
        self.conn.close()


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

                available_cost=0,
                reserved_cost=0,
                committed_cost=0,

                updated_at=""
            )

            return cost_state

        cost_state = COST_STATE(
            scope=(row)["scope"],

            available_cost=(row)["available_cost"],
            reserved_cost=(row)["reserved_cost"],
            committed_cost=(row)["committed_cost"],

            updated_at=(row)["updated_at"],
        )

        return cost_state