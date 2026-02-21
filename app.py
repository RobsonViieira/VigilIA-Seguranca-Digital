import os
from flask import Flask, render_template_string, send_file
from report import gerar_relatorio

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "logs", "seguranca.log")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Rovie IA Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { background:#020617; color:white; font-family:Arial; padding:20px; }
        h1 { color:#38bdf8; }

        .status { display:flex; gap:15px; margin-bottom:20px; }

        .card { flex:1; padding:15px; border-radius:10px; text-align:center; }

        .baixo { background:#064e3b; }
        .medio { background:#78350f; }
        .alto  { background:#7f1d1d; }

        .log { padding:10px; border-radius:8px; margin:6px 0; }
        .btn {
            display:inline-block;
            background:#38bdf8;
            color:black;
            padding:10px 15px;
            border-radius:8px;
            text-decoration:none;
            font-weight:bold;
            margin-bottom:15px;
        }
    </style>
</head>
<body>

<h1>🔐 Rovie IA Security Dashboard</h1>

<a href="/relatorio" class="btn">📄 Baixar Relatório</a>

<div class="status">
    <div class="card baixo">🟢 Baixo: {{ baixo }}</div>
    <div class="card medio">🟠 Médio: {{ medio }}</div>
    <div class="card alto">🔴 Alto: {{ alto }}</div>
</div>

{% for linha in logs %}
<div class="log {{ linha.classe }}">{{ linha.texto }}</div>
{% endfor %}

</body>
</html>
"""

@app.route("/")
def home():

    logs = []
    baixo = medio = alto = 0

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            linhas = f.readlines()[-50:]

        for l in linhas[::-1]:

            classe = "baixo"

            if "BAIXO" in l:
                classe = "baixo"
                baixo += 1
            elif "MÉDIO" in l:
                classe = "medio"
                medio += 1
            elif "ALTO" in l:
                classe = "alto"
                alto += 1

            logs.append({
                "texto": l.strip(),
                "classe": classe
            })

    return render_template_string(
        HTML,
        logs=logs,
        baixo=baixo,
        medio=medio,
        alto=alto
    )


@app.route("/relatorio")
def relatorio():
    caminho = gerar_relatorio()
    return send_file(caminho, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)   