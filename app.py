import os
from flask import Flask, request, redirect, session, render_template_string
from db import criar_tabelas
from auth import criar_usuario, validar_login

app = Flask(__name__)
app.secret_key = "rovie-ia-2026"

criar_tabelas()

LOG_PATH = "logs/seguranca.log"

# ---------------- LOGIN ----------------

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Rovie IA</title>
<style>
body{
background: radial-gradient(circle,#020b1f,#000814);
font-family: Arial;
color:white;
text-align:center;
}
.box{
background:#081a33;
width:320px;
margin:80px auto;
padding:30px;
border-radius:15px;
box-shadow:0 0 25px #00b4ff;
}
input{
width:90%;
padding:12px;
border:none;
border-radius:8px;
margin:10px;
}
button{
background:#00b4ff;
border:none;
padding:12px;
width:95%;
border-radius:8px;
font-size:16px;
}
button:hover{background:#0095d9;}
a{color:#00b4ff;text-decoration:none;}
</style>
</head>
<body>
<div class="box">
<h2>🔐 Rovie IA</h2>
<form method="post">
<input name="user" placeholder="Usuário"><br>
<input name="senha" type="password" placeholder="Senha"><br>
<button>Entrar</button>
</form>
<br>
<a href="/register">Criar conta</a>
<p style="color:red">{{erro}}</p>
</div>
</body>
</html>
"""

# ---------------- DASHBOARD ----------------

DASH_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Rovie IA</title>
<style>
body{background:#000814;font-family:Arial;color:white;}
header{background:#020f2f;padding:20px;text-align:center;}
.logs{width:95%;margin:auto;}
.card{background:#081a33;margin:10px;padding:12px;border-radius:10px;}
.alto{border-left:6px solid red;}
.medio{border-left:6px solid orange;}
.baixo{border-left:6px solid green;}
a{color:#00b4ff;}
</style>
</head>
<body>
<header>
<h2>🛡️ Rovie IA</h2>
<p>Usuário: {{user}}</p>
<a href="/logout">Sair</a>
</header>
<div class="logs">
{% for l in logs %}
<div class="card 
{% if "ALTO" in l %}alto
{% elif "MÉDIO" in l %}medio
{% else %}baixo{% endif %}">
{{l}}
</div>
{% endfor %}
</div>
</body>
</html>
"""

# ---------------- ROTAS ----------------

@app.route("/", methods=["GET","POST"])
def login():
    erro=""
    if request.method=="POST":
        u=request.form["user"]
        s=request.form["senha"]
        if validar_login(u,s):
            session["user"]=u
            return redirect("/dashboard")
        else:
            erro="Login inválido"
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
    return render_template_string(LOGIN_HTML.replace("Entrar","Cadastrar"),erro=erro)

@app.route("/dashboard")
def dash():
    if "user" not in session:
        return redirect("/")
    logs=[]
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            logs=f.readlines()[-30:]
    return render_template_string(
        DASH_HTML,
        logs=logs[::-1],
        user=session["user"]
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)