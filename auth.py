import hashlib
from datetime import datetime, timedelta
from db import conectar


def hash_senha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def criar_usuario(user, senha, admin=0):

    con = conectar()
    cur = con.cursor()

    try:
        cur.execute("""
        INSERT INTO users(username,password,admin)
        VALUES (?,?,?)
        """,(user,hash_senha(senha),admin))

        con.commit()
        return True
    except:
        return False
    finally:
        con.close()


def buscar(user):

    con=conectar()
    cur=con.cursor()

    cur.execute("SELECT * FROM users WHERE username=?",(user,))
    r=cur.fetchone()

    con.close()
    return r


def resetar(user):

    con=conectar()
    cur=con.cursor()

    cur.execute("""
    UPDATE users SET tentativas=0,bloqueado_ate=NULL WHERE username=?
    """,(user,))

    con.commit()
    con.close()


def erro(user):

    con=conectar()
    cur=con.cursor()

    cur.execute("""
    UPDATE users SET tentativas=tentativas+1 WHERE username=?
    """,(user,))

    cur.execute("""
    SELECT tentativas FROM users WHERE username=?
    """,(user,))

    t=cur.fetchone()[0]

    if t>=3:

        ate=(datetime.now()+timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("""
        UPDATE users SET bloqueado_ate=? WHERE username=?
        """,(ate,user))

    con.commit()
    con.close()


def validar(user,senha):

    d=buscar(user)

    if not d:
        return "NAO"

    _,_,hash_,tent,ate,admin=d

    if ate:
        fim=datetime.strptime(ate,"%Y-%m-%d %H:%M:%S")

        if datetime.now()<fim:
            return "BLOCK"

        resetar(user)

    if hash_==hash_senha(senha):

        resetar(user)
        return "OK"

    erro(user)
    return "ERRO"