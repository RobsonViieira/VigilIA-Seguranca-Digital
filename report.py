from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
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

    elementos.append(Paragraph("<b>Rovie IA - Relatório de Segurança</b>", styles["Title"]))
    elementos.append(Spacer(1, 20))

    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    elementos.append(Paragraph(f"Gerado em: {data}", styles["Normal"]))
    elementos.append(Spacer(1, 20))

    baixo = medio = alto = 0

    if os.path.exists(log_path):
        with open(log_path) as f:
            linhas = f.readlines()[-50:]

        for l in linhas:
            if "BAIXO" in l:
                baixo += 1
            elif "MÉDIO" in l:
                medio += 1
            elif "ALTO" in l:
                alto += 1

    elementos.append(Paragraph("<b>Resumo Executivo:</b>", styles["Heading2"]))
    elementos.append(Spacer(1, 10))
    elementos.append(Paragraph(f"Eventos Baixo Risco: {baixo}", styles["Normal"]))
    elementos.append(Paragraph(f"Eventos Médio Risco: {medio}", styles["Normal"]))
    elementos.append(Paragraph(f"Eventos Alto Risco: {alto}", styles["Normal"]))
    elementos.append(Spacer(1, 20))

    doc.build(elementos)

    return pdf_path


if __name__ == "__main__":
    gerar_relatorio()