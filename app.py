import os
import requests
from datetime import datetime
from flask import Flask,request,redirect,session,render_template_string

from db import criar_tabelas
from auth import criar_usuario,validar,buscar
from api import api


app=Flask(__name__)
app.secret_key="rovie-enterprise"

app.register_blueprint(api)

criar_tabelas()

LOG="logs/seguranca.log"


# ================= HTML =================

LOGIN="""
<h2>🔐 Rovie IA</h2>

<form method=post>

<input name=user placeholder=Usuário><br>
<input name=senha type=password placeholder=Senha><br>

<button>Entrar</button>

</form>

<a href=/register>Cadastrar</a>

<p style=color:red>{{e}}</p>
"""


ADMIN="""
<h2>👑 Painel Admin</h2>

<p>Usuário: {{u}}</p>

<a href=/dashboard>Dashboard</a> |
<a href=/logout>Sair</a>

<hr>

<h3>📊 Ranking de Ataques</h3>

{% for ip,c in rank %}
<p>{{ip}} → {{c}} ataques</p>
{% endfor %}

<hr>

<h3>🌍 Mapa IP (Geo)</h3>

{% for ip,pais in geo %}
<p>{{ip}} → {{pais}}</p>
{% endfor %}
"""


DASH="""
<h2>🛡️ Dashboard</h2>

<p>User: {{u}}</p>
<p>IP: {{ip}}</p>

<a href=/admin>Admin</a> |
<a href=/logout>Sair</a>

<hr>

{% for l in logs %}
<p>{{l}}</p>
{% endfor %}
"""


# ================= FUNÇÕES =================

def logar(txt):

    if not os.path.exists("logs"):
        os.mkdir("logs")

    with open(LOG,"a") as f:
        f.write(txt+"\n")


def ranking():

    ips={}

    if os.path.exists(LOG):

        with open(LOG) as f:

            for l in f:

                if "IP:" in l:

                    ip=l.split("IP:")[1].split()[0]

                    ips[ip]=ips.get(ip,0)+1

    return sorted(ips.items(),key=lambda x:x[1],reverse=True)


def geo_ip(ip):

    try:
        r=requests.get(f"http://ip-api.com/json/{ip}").json()
        return r.get("country","?")
    except:
        return "?"


# ================= ROTAS =================


@app.route("/",methods=["GET","POST"])
def login():

    e=""

    if request.method=="POST":

        u=request.form["user"]
        s=request.form["senha"]

        ip=request.remote_addr
        h=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        r=validar(u,s)

        if r=="OK":

            session["u"]=u
            session["ip"]=ip

            logar(f"[{h}] Login OK | {u} | IP:{ip} | BAIXO")

            return redirect("/dashboard")

        if r=="BLOCK":

            e="Bloqueado"

            logar(f"[{h}] Bloqueado | {u} | IP:{ip} | ALTO")

        else:

            e="Erro"

            logar(f"[{h}] Erro login | {u} | IP:{ip} | ALTO")


    return render_template_string(LOGIN,e=e)


@app.route("/register",methods=["GET","POST"])
def reg():

    e=""

    if request.method=="POST":

        u=request.form["user"]
        s=request.form["senha"]

        if criar_usuario(u,s):
            return redirect("/")

        e="Existe"

    return render_template_string(LOGIN.replace("Entrar","Cadastrar"),e=e)


@app.route("/dashboard")
def dash():

    if "u" not in session:
        return redirect("/")

    logs=[]

    if os.path.exists(LOG):

        with open(LOG) as f:
            logs=f.readlines()[-40:]

    return render_template_string(
        DASH,
        u=session["u"],
        ip=session["ip"],
        logs=logs[::-1]
    )


@app.route("/admin")
def admin():

    if "u" not in session:
        return redirect("/")

    user=buscar(session["u"])

    if not user or user[5]!=1:
        return "Acesso negado"

    rank=ranking()[:10]

    geo=[]

    for ip,_ in rank:
        geo.append((ip,geo_ip(ip)))

    return render_template_string(
        ADMIN,
        u=session["u"],
        rank=rank,
        geo=geo
    )


@app.route("/logout")
def out():

    session.clear()
    return redirect("/")


# ================= START =================

if __name__=="__main__":

    app.run(host="0.0.0.0",port=5000)