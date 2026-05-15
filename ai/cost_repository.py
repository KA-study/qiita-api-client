import sqlite3
from pathlib import Path
from datetime import datetime

from ai.definitions import (
    CREATE_COST_LOG_TABLE, CREATE_AI_PROCESSED_TABLE, COST_STATE, DB_PATH
    )


def initialize_db(conn: sqlite3.Connection) -> None:
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(CREATE_COST_LOG_TABLE)
    cursor.execute(CREATE_AI_PROCESSED_TABLE)

    conn.commit()


def initialize_state(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()

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

    conn.commit()


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)

    # dictっぽく扱えるようにする
    conn.row_factory = sqlite3.Row

    initialize_db(conn)
    initialize_db(conn)

    return conn


def get_current_state() -> COST_STATE:
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM cost_state
    WHERE scope = ?
    """, ("global",))

    row = cursor.fetchone()

    conn.close()

    cost_state = COST_STATE(
        scope=dict(row)["scope"],

        available_cost=dict(row)["available_cost"],
        reserved_cost=dict(row)["reserved_cost"],
        committed_cost=dict(row)["committed_cost"],

        updated_at=dict(row)["updated_at"],
    )

    return cost_state