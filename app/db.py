from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "medifind.sqlite3"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS favorites (
                medicine_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicine_id TEXT NOT NULL,
                pharmacy_id TEXT,
                report_type TEXT NOT NULL,
                note TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def list_favorites() -> set[str]:
    with connect() as conn:
        rows = conn.execute("SELECT medicine_id FROM favorites ORDER BY created_at DESC").fetchall()
    return {row["medicine_id"] for row in rows}


def toggle_favorite(medicine_id: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    with connect() as conn:
        existing = conn.execute("SELECT medicine_id FROM favorites WHERE medicine_id = ?", (medicine_id,)).fetchone()
        if existing:
            conn.execute("DELETE FROM favorites WHERE medicine_id = ?", (medicine_id,))
            conn.commit()
            return {"favorited": False, "medicine_id": medicine_id}

        conn.execute(
            "INSERT INTO favorites (medicine_id, created_at) VALUES (?, ?)",
            (medicine_id, now),
        )
        conn.commit()
    return {"favorited": True, "medicine_id": medicine_id}


def add_report(medicine_id: str, pharmacy_id: str | None, report_type: str, note: str | None) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    with connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO reports (medicine_id, pharmacy_id, report_type, note, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (medicine_id, pharmacy_id, report_type, note, now),
        )
        conn.commit()
        report_id = cursor.lastrowid

    return {
        "id": report_id,
        "medicine_id": medicine_id,
        "pharmacy_id": pharmacy_id,
        "report_type": report_type,
        "note": note or "",
        "created_at": now,
    }


def report_count() -> int:
    with connect() as conn:
        row = conn.execute("SELECT COUNT(*) AS count FROM reports").fetchone()
    return int(row["count"] if row else 0)

