from reportlab.platypus import SimpleDocTemplate
from layout import *
from sections import *
from data import *
from load import *
from transform import *
from header import *
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import os

#Load environment variables from .env file
load_dotenv()
root = Path(os.getenv('FOLDER_OUTPUT'))

dia = date.today()
doc_name = root / f'Intelligence Report {dia.strftime("%d-%m-%Y")}.pdf'


def report():
    doc = SimpleDocTemplate(doc_name, topMargin=4*cm, bottomMargin=2*cm, leftMargin=2*cm, rightMargin=2*cm)
    story = []
    style = build_styles()
    

    content = load_content()

    for block in content:
        if block['type'] == 'table':
            tabela = make_table(block['data'])
            story.append(table_section(block['title'], tabela, style))

        elif block['type'] == 'two_tables':
            tabela1 = make_table(block['data'][0])
            tabela2 = make_table(block['data'][1])
            story.append(double_table_section(block['title'], tabela1, tabela2, style))

        if block['type'] == 'image':
            image = add_image(block['data'])
            story.extend(image_section(block['title'], image, style))

        if block['type'] == 'text':
            texto = block['data']
            story.extend(text_session(block['title'], texto, style))
                            
    doc.build(story, onFirstPage=cabecalho)

