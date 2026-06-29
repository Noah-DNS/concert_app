import sqlite3

DB = "tickets.db"


def init_db():
    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tickets(
        id TEXT PRIMARY KEY,
        nom TEXT,
        utilise INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def get_ticket(id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM tickets WHERE id=?",
        (id,)
    )

    ticket = cur.fetchone()

    conn.close()

    return ticket


def add_ticket(id, nom=""):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO tickets(id, nom) VALUES (?,?)",
        (id, nom)
    )

    conn.commit()
    conn.close()


def validate_ticket(id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "UPDATE tickets SET utilise=1 WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()