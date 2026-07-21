from reportlab.platypus import Spacer, KeepTogether, Paragraph, Image, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY


def secao_tabela(titulo, tabela, estilo):
    return KeepTogether([
        Paragraph(titulo, estilo['Heading2']),
        Spacer(1, 0.2*cm),
        tabela,
        Spacer(1, 0.5*cm)
    ])


def secao_duas_tabelas(titulo, tabela1, tabela2, estilo):
    side_by_side = Table([[tabela1, '' , tabela2]], colWidths=[8*cm, 1*cm, 8*cm])

    side_by_side.setStyle([('VALIGN', (0,0), (-1,-1), 'TOP'),
                           ('LEFTPADDING', (0,0), (-1,-1), 0),
                           ('RIGHTPADDING', (0,0), (-1,-1), 0)])

    return KeepTogether([
        Paragraph(titulo, estilo['Heading2']),
        Spacer(1, 0.2*cm),
        side_by_side,
        Spacer(1, 0.5*cm)
    ])


def secao_imagem(titulo, imagem, estilo, max_width=16*cm):
    story = []
    story.append(Paragraph(titulo, estilo['Heading2']))
    story.append(Spacer(1, 0.2*cm))

    if imagem.drawWidth > max_width:
        proporcao = max_width / imagem.drawWidth
        imagem.drawWidth = max_width
        imagem.drawHeight = imagem.drawHeight * proporcao

    imagem.hAlign = 'CENTER'
    story.append(imagem)
    story.append(Spacer(1, 0.5*cm))

    return story


def secao_texto(titulo, texto, estilo):
    estilo_corpo = estilo['BodyText']
    estilo_corpo.alignment = TA_JUSTIFY

    return [
        Paragraph(titulo, estilo['Heading2']),
        Spacer(1, 0.2*cm),
        Paragraph(texto, estilo_corpo),
        Spacer(1, 0.5*cm)
    ]