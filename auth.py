import hashlib
from datetime import datetime, timedelta
from db import conectar


def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def criar_usuario(user, senha):

    con = conectar()
    cur = con.cursor()

    try:
        cur.execute("""
        INSERT INTO users(username,password,tentativas,bloqueado_ate)
        VALUES (?,?,0,NULL)
        """, (user, hash_senha(senha)))

        con.commit()
        return True

    except:
        return False

    finally:
        con.close()


def buscar_usuario(user):

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT * FROM users WHERE username=?", (user,))
    res = cur.fetchone()

    con.close()
    return res


def resetar_tentativas(user):

    con = conectar()
    cur = con.cursor()

    cur.execute("""
    UPDATE users SET tentativas=0, bloqueado_ate=NULL WHERE username=?
    """, (user,))

    con.commit()
    con.close()


def registrar_erro(user):

    con = conectar()
    cur = con.cursor()

    cur.execute("""
    UPDATE users SET tentativas = tentativas + 1 WHERE username=?
    """, (user,))

    cur.execute("""
    SELECT tentativas FROM users WHERE username=?
    """, (user,))

    t = cur.fetchone()[0]

    # Bloqueia por 10 minutos após 3 erros
    if t >= 3:

        bloqueio = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("""
        UPDATE users SET bloqueado_ate=? WHERE username=?
        """, (bloqueio, user))

    con.commit()
    con.close()


def validar_login(user, senha):

    dados = buscar_usuario(user)

    if not dados:
        return "NAO_EXISTE"

    _, _, senha_hash, tentativas, bloqueado_ate = dados

    agora = datetime.now()

    # Verifica bloqueio
    if bloqueado_ate:

        ate = datetime.strptime(bloqueado_ate, "%Y-%m-%d %H:%M:%S")

        if agora < ate:
            return "BLOQUEADO"

        else:
            resetar_tentativas(user)

    # Verifica senha
    if senha_hash == hash_senha(senha):

        resetar_tentativas(user)
        return "OK"

    else:

        registrar_erro(user)
        return "ERRO"