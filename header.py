from reportlab.platypus import Paragraph
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from datetime import date, timedelta
from dotenv import load_dotenv
import os

#Load environment variables from .env file
load_dotenv()

def cabecalho(canvas, doc):

    canvas.saveState()

    #Logo
    logo_path = os.getenv('LOGO')
    canvas.drawImage(
        logo_path, 
        0.5*cm,
        doc.height + doc.topMargin - 1*cm,
        width=4*cm, height=1*cm,
        preserveAspectRatio=True,
        mask = 'auto'
    )

    #Título
    estilo_titulo = ParagraphStyle(
        name='CabecalhoTitulo',
        alignment=1,
        fontSize=20,
        spaceAfter=12,
    )

    titulo = Paragraph("Relatório diário de Inteligência", estilo_titulo)
    w, h = titulo.wrap(doc.width, doc.topMargin)
    titulo.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - 0.5*cm)

    #Data
    estilo_data = ParagraphStyle(
        name='CabecalhoData',
        alignment=1,
        fontSize=12,
        spaceAfter=24
    )

    data_atual = date.today() + timedelta(0)
    data_formatada = data_atual.strftime("%d/%m/%Y")
    data_paragraph = Paragraph(f"Data:<br/>{data_formatada}", estilo_data)
    w, h = data_paragraph.wrap(doc.width, doc.topMargin)
    page_width = doc.pagesize[0]
    x = page_width - doc.rightMargin/1.75 - w/1.75
    data_paragraph.drawOn(canvas, x, doc.height + doc.topMargin - 1*cm)



    canvas.restoreState()
