from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
import os
from datetime import datetime


def gerar_relatorio():

    base = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base, "logs", "seguranca.log")

    pdf_path = os.path.join(base, "relatorio_rovia_ia.pdf")

    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elementos = []

    # Título
    titulo = Paragraph("<b>Rovie IA - Relatório de Segurança</b>", styles["Title"])
    elementos.append(titulo)
    elementos.append(Spacer(1, 20))

    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    elementos.append(Paragraph(f"Data: {data}", styles["Normal"]))
    elementos.append(Spacer(1, 20))

    # Contadores
    baixo = medio = alto = 0
    dados = [["Evento", "Risco"]]

    if os.path.exists(log_path):

        with open(log_path) as f:
            linhas = f.readlines()[-50:]

        for l in linhas:

            partes = l.strip().split("|")

            evento = partes[0]
            risco = partes[1] if len(partes) > 1 else ""

            try:
                valor = float(risco.replace("RISCO", "").strip())
            except:
                valor = 0

            if valor >= 4:
                alto += 1
            elif valor >= 2:
                medio += 1
            else:
                baixo += 1

            dados.append([evento, risco])

    # Resumo
    elementos.append(Paragraph("<b>Resumo:</b>", styles["Heading2"]))
    elementos.append(Spacer(1, 10))

    elementos.append(Paragraph(f"Baixo: {baixo}", styles["Normal"]))
    elementos.append(Paragraph(f"Médio: {medio}", styles["Normal"]))
    elementos.append(Paragraph(f"Alto: {alto}", styles["Normal"]))
    elementos.append(Spacer(1, 20))

    # Tabela
    tabela = Table(dados, colWidths=[350, 150])
    elementos.append(tabela)

    doc.build(elementos)

    return pdf_path


if __name__ == "__main__":
    gerar_relatorio()