from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from datetime import datetime


def gerar_relatorio():

    base=os.path.dirname(os.path.abspath(__file__))
    log_path=os.path.join(base,"logs","seguranca.log")
    pdf=os.path.join(base,"relatorio_rovia_ia.pdf")

    doc=SimpleDocTemplate(pdf,pagesize=A4)
    styles=getSampleStyleSheet()
    itens=[]

    itens.append(Paragraph("Rovie IA - Relatório de Segurança",styles["Title"]))
    itens.append(Spacer(1,20))

    data=datetime.now().strftime("%d/%m/%Y %H:%M")
    itens.append(Paragraph(f"Gerado em: {data}",styles["Normal"]))
    itens.append(Spacer(1,20))

    baixo=medio=alto=0

    if os.path.exists(log_path):

        with open(log_path) as f:
            linhas=f.readlines()

        for l in linhas:
            if "ALTO" in l: alto+=1
            elif "MÉDIO" in l: medio+=1
            else: baixo+=1

    itens.append(Paragraph("Resumo Executivo",styles["Heading2"]))
    itens.append(Spacer(1,10))

    itens.append(Paragraph(f"Baixo: {baixo}",styles["Normal"]))
    itens.append(Paragraph(f"Médio: {medio}",styles["Normal"]))
    itens.append(Paragraph(f"Alto: {alto}",styles["Normal"]))
    itens.append(Spacer(1,20))

    doc.build(itens)

    return pdf


if __name__=="__main__":
    gerar_relatorio()