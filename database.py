import sqlite3


def get_connection():
    return sqlite3.connect("tickets.db")


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS tickets")

    cur.execute("""
    CREATE TABLE tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT UNIQUE,
        nom TEXT,
        statut TEXT DEFAULT 'non_venu'
    )
    """)

    conn.commit()
    conn.close()



def add_ticket(numero, nom):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR REPLACE INTO tickets(numero, nom) VALUES (?, ?)",
        (numero, nom)
    )

    conn.commit()
    conn.close()



def validate_ticket(numero):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT nom, statut FROM tickets WHERE numero=?",
        (numero,)
    )

    ticket = cur.fetchone()

    if ticket is None:
        conn.close()
        return {"status":"inconnu"}

    nom, statut = ticket


    if statut == "utilise":
        conn.close()
        return {
            "status":"deja_utilise",
            "nom":nom
        }


    cur.execute(
        "UPDATE tickets SET statut='utilise' WHERE numero=?",
        (numero,)
    )

    conn.commit()
    conn.close()


    return {
        "status":"valide",
        "nom":nom
    }