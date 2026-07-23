from reportlab.platypus import Spacer, KeepTogether, Paragraph, Image, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY


def table_section(title, table, style):
    return KeepTogether([
        Paragraph(title, style['Heading2']),
        Spacer(1, 0.2*cm),
        table,
        Spacer(1, 0.5*cm)
    ])


def double_table_section(title, table1, table2, style):
    side_by_side = Table([[table1, '' , table2]], colWidths=[8*cm, 1*cm, 8*cm])

    side_by_side.setStyle([('VALIGN', (0,0), (-1,-1), 'TOP'),
                           ('LEFTPADDING', (0,0), (-1,-1), 0),
                           ('RIGHTPADDING', (0,0), (-1,-1), 0)])

    return KeepTogether([
        Paragraph(title, style['Heading2']),
        Spacer(1, 0.2*cm),
        side_by_side,
        Spacer(1, 0.5*cm)
    ])


def image_section(title, image, style, max_width=16*cm):
    story = []
    story.append(Paragraph(title, style['Heading2']))
    story.append(Spacer(1, 0.2*cm))

    if image.drawWidth > max_width:
        proporcao = max_width / image.drawWidth
        image.drawWidth = max_width
        image.drawHeight = image.drawHeight * proporcao

    image.hAlign = 'CENTER'
    story.append(image)
    story.append(Spacer(1, 0.5*cm))

    return story


def text_section(title, text, style):
    body_style = style['BodyText']
    body_style.alignment = TA_JUSTIFY

    return [
        Paragraph(title, style['Heading2']),
        Spacer(1, 0.2*cm),
        Paragraph(text, body_style),
        Spacer(1, 0.5*cm)
    ]
