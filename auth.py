import hashlib
from db import conectar

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_usuario(user, senha):
    con = conectar()
    cur = con.cursor()

    try:
        cur.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (user, hash_senha(senha))
        )
        con.commit()
        return True
    except:
        return False
    finally:
        con.close()

def validar_login(user, senha):
    con = conectar()
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (user, hash_senha(senha))
    )

    res = cur.fetchone()
    con.close()

    return res is not None