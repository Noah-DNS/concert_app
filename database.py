import sqlite3
from datetime import datetime

DB = "tickets.db"


def get_connection():
    return sqlite3.connect(DB)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    DROP TABLE IF EXISTS tickets
    """)

    cur.execute("""
    CREATE TABLE tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT UNIQUE,
        nom TEXT,
        utilise INTEGER DEFAULT 0,
        heure TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_ticket(numero, nom):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO tickets(numero, nom, utilise, heure)
        VALUES (?, ?, 0, NULL)
        """,
        (numero, nom)
    )

    conn.commit()
    conn.close()


def get_ticket(numero):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM tickets WHERE numero=?",
        (numero,)
    )

    ticket = cur.fetchone()

    conn.close()

    return ticket


def validate_ticket(numero):
    conn = get_connection()
    cur = conn.cursor()

    heure = datetime.now().strftime("%H:%M:%S")

    cur.execute(
        """
        UPDATE tickets
        SET utilise=1, heure=?
        WHERE numero=?
        """,
        (heure, numero)
    )

    conn.commit()
    conn.close()


def get_all_tickets():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM tickets ORDER BY id"
    )

    tickets = cur.fetchall()

    conn.close()

    return tickets