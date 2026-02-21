from flask import Flask, render_template_string
import subprocess

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>VigilIA Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body {
            background: #0f172a;
            color: white;
            font-family: Arial;
            padding: 20px;
        }
        h1 {
            color: #38bdf8;
        }
        .log {
            background: #020617;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
            font-size: 14px;
        }
    </style>
</head>
<body>

<h1>🔐 VigilIA Dashboard</h1>

{% for linha in logs %}
<div class="log">{{ linha }}</div>
{% endfor %}

</body>
</html>
"""

@app.route("/")
def home():

    try:
        with open("logs/seguranca.log") as f:
            linhas = f.readlines()[-20:]
    except:
        linhas = ["Nenhum log encontrado"]

    return render_template_string(HTML, logs=linhas[::-1])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)