from reportlab.platypus import Image, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(name='TitleCenter', parent=styles['Title'], alignment=1, fontSize=18, spaceAfter=12))
    return styles

def fazer_tabela(dataframe):
    dados = [dataframe.columns.tolist()] + dataframe.values.tolist()
    tabela = Table(dados, hAlign='CENTER')
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f68b20")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    return tabela

def add_imagem(caminho):
    return Image(caminho)