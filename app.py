   import os
from flask import Flask, render_template_string, send_file, url_for
from report import gerar_relatorio

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "logs", "seguranca.log")

HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Rovie IA | Security</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

:root{
  --bg:#020617;
  --blue:#38bdf8;
  --green:#22c55e;
  --orange:#f59e0b;
  --red:#ef4444;
  --text:#e5e7eb;
}

body{
  margin:0;
  background:#020617;
  font-family:Arial,Helvetica,sans-serif;
  color:var(--text);
}

header{
  display:flex;
  flex-direction:column;
  align-items:center;
  padding:20px;
  text-align:center;
}

.hero{
  width:180px;
  border-radius:16px;
  box-shadow:0 0 25px rgba(56,189,248,.4);
  margin-bottom:15px;
}

.logo{
  font-size:26px;
  font-weight:bold;
  color:var(--blue);
}

.subtitle{
  font-size:13px;
  opacity:.7;
  margin-top:5px;
}

.btn{
  background:var(--blue);
  color:black;
  padding:10px 16px;
  border-radius:8px;
  text-decoration:none;
  font-weight:bold;
  margin:15px 0;
  display:inline-block;
}

.container{
  padding:16px;
  max-width:900px;
  margin:auto;
}

.cards{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(120px,1fr));
  gap:12px;
  margin-bottom:20px;
}

.card{
  background:#020617;
  border-radius:14px;
  padding:14px;
  text-align:center;
  box-shadow:0 0 15px rgba(56,189,248,.08);
}

.card h2{
  margin:4px 0;
  font-size:22px;
}

.card span{
  font-size:12px;
  opacity:.7;
}

.baixo{color:var(--green);}
.medio{color:var(--orange);}
.alto{color:var(--red);}

.logs{
  display:flex;
  flex-direction:column;
  gap:10px;
}

.log{
  background:#020617;
  border-radius:10px;
  padding:10px;
  font-size:13px;
  border-left:4px solid;
}

.log.baixo{border-color:var(--green);}
.log.medio{border-color:var(--orange);}
.log.alto{border-color:var(--red);}

footer{
  text-align:center;
  font-size:11px;
  opacity:.5;
  padding:12px;
}

</style>
</head>

<body>

<header>

  <img src="{{ url_for('static', filename='hero.png') }}" class="hero">

  <div class="logo">Rovie IA</div>

  <div class="subtitle">
    Monitoramento Inteligente • Proteção Digital • Antifraude
  </div>

  <a href="/relatorio" class="btn">📄 Baixar Relatório</a>

</header>


<div class="container">

  <div class="cards">

    <div class="card">
      <h2>{{ total }}</h2>
      <span>Eventos</span>
    </div>

    <div class="card">
      <h2 class="baixo">{{ baixo }}</h2>
      <span>Baixo</span>
    </div>

    <div class="card">
      <h2 class="medio">{{ medio }}</h2>
      <span>Médio</span>
    </div>

    <div class="card">
      <h2 class="alto">{{ alto }}</h2>
      <span>Alto</span>
    </div>

  </div>


  <h3>📡 Atividade Recente</h3>

  <div class="logs">

    {% for l in logs %}
    <div class="log {{ l.classe }}">
      {{ l.texto }}
    </div>
    {% endfor %}

  </div>

</div>

<footer>
Rovie IA • Segurança com Inteligência Artificial • {{ data }}
</footer>

</body>
</html>
"""

@app.route("/")
def home():

    logs=[]
    baixo=medio=alto=0

    if os.path.exists(LOG_PATH):

        with open(LOG_PATH) as f:
            linhas=f.readlines()[-60:]

        for l in linhas[::-1]:

            classe="baixo"

            if "ALTO" in l:
                classe="alto"
                alto+=1
            elif "MÉDIO" in l:
                classe="medio"
                medio+=1
            else:
                baixo+=1

            logs.append({
                "texto":l.strip(),
                "classe":classe
            })

    total=baixo+medio+alto

    from datetime import datetime
    data=datetime.now().strftime("%d/%m/%Y %H:%M")

    return render_template_string(
        HTML,
        logs=logs,
        baixo=baixo,
        medio=medio,
        alto=alto,
        total=total,
        data=data
    )


@app.route("/relatorio")
def relatorio():
    caminho=gerar_relatorio()
    return send_file(caminho,as_attachment=True)


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)