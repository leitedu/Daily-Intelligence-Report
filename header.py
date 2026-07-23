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

    #Title
    title_style = ParagraphStyle(
        name='CabecalhoTitulo',
        alignment=1,
        fontSize=20,
        spaceAfter=12,
    )

    title = Paragraph("Relatório diário de Inteligência", title_style)
    w, h = titulo.wrap(doc.width, doc.topMargin)
    title.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - 0.5*cm)

    #Date
    date_style = ParagraphStyle(
        name='CabecalhoData',
        alignment=1,
        fontSize=12,
        spaceAfter=24
    )

    current_date = date.today() + timedelta(0)
    format_date = current_date.strftime("%d/%m/%Y")
    data_paragraph = Paragraph(f"Data:<br/>{format_date}", date_style)
    w, h = data_paragraph.wrap(doc.width, doc.topMargin)
    page_width = doc.pagesize[0]
    x = page_width - doc.rightMargin/1.75 - w/1.75
    data_paragraph.drawOn(canvas, x, doc.height + doc.topMargin - 1*cm)



    canvas.restoreState()
