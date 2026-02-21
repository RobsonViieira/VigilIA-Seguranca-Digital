import sqlite3

DB = "users.db"


def conectar():
    return sqlite3.connect(DB)


def criar_tabelas():

    con = conectar()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    con.commit()
    con.close()