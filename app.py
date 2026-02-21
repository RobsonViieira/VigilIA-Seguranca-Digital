import os
from flask import Flask, request, redirect, session, url_for, render_template_string
from db import criar_tabelas
from auth import criar_usuario, validar_login

app = Flask(__name__)
app.secret_key = "rovie-secret-123"

criar_tabelas()

LOG = "logs/seguranca.log"


LOGIN_HTML = """
<h2>🔐 Rovie IA Login</h2>

<form method="post">

<input name="user" placeholder="Usuário"><br><br>
<input name="senha" type="password" placeholder="Senha"><br><br>

<button>Entrar</button>

</form>

<a href="/register">Criar conta</a>

<p style="color:red">{{erro}}</p>
"""


REGISTER_HTML = """
<h2>📝 Cadastro</h2>

<form method="post">

<input name="user" placeholder="Usuário"><br><br>
<input name="senha" type="password" placeholder="Senha"><br><br>

<button>Cadastrar</button>

</form>

<a href="/">Voltar</a>

<p style="color:red">{{erro}}</p>
"""


DASH_HTML = """
<h2>📊 Rovie IA Dashboard</h2>

<p>Usuário: {{user}}</p>

<a href="/logout">Sair</a>

<hr>

{% for l in logs %}
<p>{{l}}</p>
{% endfor %}
"""


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

    return render_template_string(REGISTER_HTML,erro=erro)


@app.route("/dashboard")
def dash():

    if "user" not in session:
        return redirect("/")

    logs=[]

    if os.path.exists(LOG):

        with open(LOG) as f:
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