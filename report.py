from reportlab.platypus import SimpleDocTemplate
from layout import *
from secoes import *
from dados import *
from load import *
from transform import *
from cabecalho import *
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import os

#Load environment variables from .env file
load_dotenv()
root = Path(os.getenv('FOLDER_OUTPUT'))

dia = date.today()
doc_name = root / f'Relatório de Inteligência {dia.strftime("%d-%m-%Y")}.pdf'


def relatorio():
    doc = SimpleDocTemplate(doc_name, topMargin=4*cm, bottomMargin=2*cm, leftMargin=2*cm, rightMargin=2*cm)
    story = []
    style = build_styles()
    

    conteudo = load_content()

    for bloco in conteudo:
        if bloco['type'] == 'table':
            tabela = fazer_tabela(bloco['data'])
            story.append(secao_tabela(bloco['title'], tabela, style))

        elif bloco['type'] == 'two_tables':
            tabela1 = fazer_tabela(bloco['data'][0])
            tabela2 = fazer_tabela(bloco['data'][1])
            story.append(secao_duas_tabelas(bloco['title'], tabela1, tabela2, style))

        if bloco['type'] == 'image':
            imagem = add_imagem(bloco['data'])
            story.extend(secao_imagem(bloco['title'], imagem, style))

        if bloco['type'] == 'text':
            texto = bloco['data']
            story.extend(secao_texto(bloco['title'], texto, style))
                            
    doc.build(story, onFirstPage=cabecalho)

