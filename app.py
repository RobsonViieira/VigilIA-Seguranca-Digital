import os
from datetime import datetime
from flask import Flask, request, redirect, session, render_template_string

from db import criar_tabelas
from auth import criar_usuario, validar_login, buscar_usuario

app = Flask(__name__)
app.secret_key = "rovie-secure-2026"

criar_tabelas()

LOG = "logs/seguranca.log"


# ================= HTML =================

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Rovie IA</title>
<style>

body{
background:#020617;
color:white;
font-family:Arial;
text-align:center;
}

.box{
background:#081a33;
width:330px;
margin:80px auto;
padding:30px;
border-radius:14px;
box-shadow:0 0 25px #38bdf8;
}

input{
width:90%;
padding:12px;
border-radius:8px;
border:none;
margin:8px;
}

button{
background:#38bdf8;
border:none;
padding:12px;
width:95%;
border-radius:8px;
font-size:16px;
}

a{color:#38bdf8;text-decoration:none;}

</style>
</head>

<body>

<div class="box">

<h2>🔐 Rovie IA</h2>

<form method="post">

<input name="user" placeholder="Usuário">
<input name="senha" type="password" placeholder="Senha">

<button>Entrar</button>

</form>

<a href="/register">Criar conta</a>

<p style="color:red">{{erro}}</p>

</div>
</body>
</html>
"""


DASH_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Rovie IA</title>
<style>

body{background:#020617;color:white;font-family:Arial;}

header{
background:#020f2f;
padding:20px;
text-align:center;
}

.card{
background:#081a33;
margin:10px;
padding:12px;
border-radius:10px;
}

.alto{border-left:6px solid red;}
.medio{border-left:6px solid orange;}
.baixo{border-left:6px solid green;}

</style>
</head>

<body>

<header>
<h2>🛡️ Rovie IA</h2>
<p>Usuário: {{user}}</p>
<p>IP: {{ip}}</p>
<a href="/logout">Sair</a>
</header>

{% for l in logs %}

<div class="card
{% if "ALTO" in l %}alto
{% elif "MÉDIO" in l %}medio
{% else %}baixo{% endif %}">

{{l}}

</div>

{% endfor %}

</body>
</html>
"""

# ================= ROTAS =================


@app.route("/", methods=["GET","POST"])
def login():

    erro=""

    if request.method=="POST":

        u = request.form["user"]
        s = request.form["senha"]

        ip = request.remote_addr
        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        status = validar_login(u,s)

        if status=="OK":

            session["user"]=u
            session["ip"]=ip

            log = f"[{hora}] Login autorizado | User:{u} | IP:{ip} | BAIXO"

        elif status=="BLOQUEADO":

            erro="Conta bloqueada por tentativas"

            log = f"[{hora}] Login bloqueado | User:{u} | IP:{ip} | ALTO"

        else:

            erro="Senha inválida"

            log = f"[{hora}] Login inválido | User:{u} | IP:{ip} | ALTO"


        if not os.path.exists("logs"):
            os.mkdir("logs")

        with open(LOG,"a") as f:
            f.write(log+"\n")

        if status=="OK":
            return redirect("/dashboard")


    return render_template_string(LOGIN_HTML,erro=erro)


@app.route("/register",methods=["GET","POST"])
def register():

    erro=""

    if request.method=="POST":

        u=request.form["user"]
        s=request.form["senha"]

        if criar_usuario(u,s):
            return redirect("/")

        else:
            erro="Usuário já existe"

    return render_template_string(
        LOGIN_HTML.replace("Entrar","Cadastrar"),
        erro=erro
    )


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    logs=[]

    if os.path.exists(LOG):

        with open(LOG) as f:
            logs=f.readlines()[-50:]

    return render_template_string(
        DASH_HTML,
        logs=logs[::-1],
        user=session["user"],
        ip=session["ip"]
    )


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


# ================= START =================

if __name__=="__main__":

    app.run(host="0.0.0.0",port=5000)