import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, Flowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pypdfium2 as pdfium

# Register Windows Segoe UI fonts
font_dir = "C:/Windows/Fonts"
if os.path.exists(os.path.join(font_dir, "segoeui.ttf")):
    pdfmetrics.registerFont(TTFont("SegoeUI", os.path.join(font_dir, "segoeui.ttf")))
    pdfmetrics.registerFont(TTFont("SegoeUI-Bold", os.path.join(font_dir, "segoeuib.ttf")))
    pdfmetrics.registerFont(TTFont("SegoeUI-Italic", os.path.join(font_dir, "segoeuii.ttf")))
    pdfmetrics.registerFont(TTFont("SegoeUI-SemiBold", os.path.join(font_dir, "seguisb.ttf")))
    FONT_FAMILY = "SegoeUI"
    FONT_BOLD = "SegoeUI-Bold"
    FONT_ITALIC = "SegoeUI-Italic"
    FONT_SEMIBOLD = "SegoeUI-SemiBold"
else:
    FONT_FAMILY = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"
    FONT_ITALIC = "Helvetica-Oblique"
    FONT_SEMIBOLD = "Helvetica-Bold"

class ClickableButton(Flowable):
    """A button flowable with rounded corners and a full-area clickable link."""
    def __init__(self, text, subtext, url, width, height, bg_color, border_color=None, corner_radius=10):
        super().__init__()
        self.text = text
        self.subtext = subtext
        self.url = url
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.border_color = border_color
        self.corner_radius = corner_radius

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(self.bg_color)
        if self.border_color:
            c.setStrokeColor(self.border_color)
            c.setLineWidth(1.5)
            c.roundRect(0, 0, self.width, self.height, self.corner_radius, fill=1, stroke=1)
        else:
            c.roundRect(0, 0, self.width, self.height, self.corner_radius, fill=1, stroke=0)

        # Draw main text
        c.setFillColor(colors.white)
        c.setFont(FONT_BOLD, 12.5)
        c.drawCentredString(self.width / 2.0, self.height / 2.0 + 3.5, self.text)

        # Draw subtext
        if self.subtext:
            c.setFillColor(colors.HexColor("#E2E8F0"))
            c.setFont(FONT_FAMILY, 8.5)
            c.drawCentredString(self.width / 2.0, self.height / 2.0 - 11.5, self.subtext)

        # Add clickable URI annotation across the ENTIRE button rectangle
        c.linkURL(self.url, (0, 0, self.width, self.height), relative=1)
        c.restoreState()

def create_access_pdf(output_pdf_path):
    # A4 dimensions: 595.27 x 841.89 pt (210 x 297 mm)
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=11 * mm,
        bottomMargin=11 * mm
    )

    url = "https://drive.google.com/drive/folders/1mpgI1cNmZ6rXFff4ryLuCyiSPCsskUd6?usp=sharing"

    styles = getSampleStyleSheet()

    # Brand palette
    c_brown = colors.HexColor("#3B2A1A")
    c_brown_light = colors.HexColor("#5C5148")
    c_green = colors.HexColor("#16A34A")
    c_green_dark = colors.HexColor("#15803D")
    c_yellow_badge = colors.HexColor("#FEF3C7")
    c_yellow_border = colors.HexColor("#FCD34D")

    badge_style = ParagraphStyle(
        'BadgeStyle',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#92400E"),
        alignment=TA_CENTER
    )

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=18,
        leading=22,
        textColor=c_brown,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontName=FONT_FAMILY,
        fontSize=10,
        leading=14,
        textColor=c_brown_light,
        alignment=TA_CENTER
    )

    product_title_style = ParagraphStyle(
        'ProductTitle',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=11.5,
        leading=15,
        textColor=c_brown,
        alignment=TA_LEFT
    )

    product_desc_style = ParagraphStyle(
        'ProductDesc',
        parent=styles['Normal'],
        fontName=FONT_FAMILY,
        fontSize=8.5,
        leading=12,
        textColor=c_brown_light,
        alignment=TA_LEFT
    )

    product_item_style = ParagraphStyle(
        'ProductItem',
        parent=styles['Normal'],
        fontName=FONT_SEMIBOLD,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#15803D"),
        alignment=TA_LEFT
    )

    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=11,
        leading=14.5,
        textColor=c_brown,
        alignment=TA_LEFT
    )

    exact_text_style = ParagraphStyle(
        'ExactTextStyle',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=TA_LEFT
    )

    url_text_style = ParagraphStyle(
        'UrlTextStyle',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=7.3,
        leading=10,
        textColor=colors.HexColor("#1D4ED8"),
        alignment=TA_CENTER
    )

    url_tip_style = ParagraphStyle(
        'UrlTip',
        parent=styles['Normal'],
        fontName=FONT_ITALIC,
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#64748B"),
        alignment=TA_CENTER
    )

    step_title_style = ParagraphStyle(
        'StepTitle',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=9.5,
        leading=12,
        textColor=c_brown,
        alignment=TA_LEFT
    )

    step_body_style = ParagraphStyle(
        'StepBody',
        parent=styles['Normal'],
        fontName=FONT_FAMILY,
        fontSize=8.2,
        leading=11,
        textColor=c_brown_light,
        alignment=TA_LEFT
    )

    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontName=FONT_FAMILY,
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#64748B"),
        alignment=TA_CENTER
    )

    story = []

    # 1. Logo
    logo_path = r"d:\dev\LECCIONES KIDS\imagens-pg-vendas\logo-lecciones-kids.png"
    if os.path.exists(logo_path):
        logo_img = RLImage(logo_path, width=4.4*cm, height=2.2*cm)
        logo_table = Table([[logo_img]], colWidths=[18*cm], hAlign='CENTER')
        logo_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(logo_table)
        story.append(Spacer(1, 2*mm))

    # 2. Welcome Badge
    badge_p = Paragraph("¡FELICITACIONES POR TU COMPRA! &bull; ACCESO INMEDIATO", badge_style)
    badge_table = Table([[badge_p]], colWidths=[15*cm], hAlign='CENTER')
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_yellow_badge),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 1, c_yellow_border),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 3*mm))

    # 3. Title & Welcome Message
    story.append(Paragraph("¡Bienvenido/a a tu Material Educativo!", title_style))
    story.append(Spacer(1, 1.5*mm))
    story.append(Paragraph(
        "Tu videocurso práctico y material educativo ya están listos en formato digital de alta resolución. Para acceder a todos los archivos y videos inmediatamente, usa cualquiera de las opciones a continuación:",
        subtitle_style
    ))
    story.append(Spacer(1, 3.5*mm))

    # 4. Product Preview Card (Mockup + Description provided by dj + Features)
    capa_path = r"d:\dev\LECCIONES KIDS\imagens-pg-vendas\capa-desafios-calculo.png"
    if not os.path.exists(capa_path):
        capa_path = r"d:\dev\LECCIONES KIDS\imagens-pg-vendas\capa-calculo-mental-caderno.png"

    if os.path.exists(capa_path):
        capa_img = RLImage(capa_path, width=3.3*cm, height=3.3*cm)
        product_cells = [
            Paragraph("<b>Desafíos de Cálculo y Problemas Matemáticos Kids (1.º al 5.º Grado)</b>", product_title_style),
            Spacer(1, 1*mm),
            Paragraph("21 videos y 240 minutos de contenido práctico para que los niños resuelvan problemas matemáticos al instante con total agilidad. Trucos y retos divertidos que superan por completo a la escuela tradicional.", product_desc_style),
            Spacer(1, 1.5*mm),
            Paragraph("&bull; ¡+21 videos prácticos y 240 minutos de contenido dinámico!", product_item_style),
            Paragraph("&bull; Acceso permanente, vitalicio e ilimitado en Google Drive", product_item_style),
        ]
        prod_table = Table([[capa_img, product_cells]], colWidths=[3.6*cm, 13.0*cm], hAlign='CENTER')
        prod_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFDF7")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FDE68A")),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),
            ('ALIGN', (0,0), (0,0), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(prod_table)
        story.append(Spacer(1, 4.5*mm))

    # 5. Primary CTA Button (Clickable Button Flowable)
    btn_flowable = ClickableButton(
        text="HAZ CLIC AQUÍ PARA ACCEDER AL MATERIAL  →",
        subtext="Toca o haz clic sobre este botón para abrir la carpeta directamente en Google Drive",
        url=url,
        width=16.8*cm,
        height=46,
        bg_color=c_green,
        border_color=c_green_dark,
        corner_radius=10
    )
    story.append(Table([[btn_flowable]], colWidths=[18*cm], hAlign='CENTER', style=[
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(Spacer(1, 4.5*mm))

    # 6. Alternative Option Box (Direct Raw URL)
    exact_heading = Paragraph("<b>Opción alternativa: Copiar y pegar el enlace</b>", section_heading_style)
    exact_copy_text = Paragraph(
        "¡Aquí tienes el enlace para acceder al material! Copia y pega este enlace en tu navegador.",
        exact_text_style
    )
    url_clickable = Paragraph(
        f'<nobr><a href="{url}" color="#1D4ED8"><u><b>{url}</b></u></a></nobr>',
        url_text_style
    )
    url_tip = Paragraph(
        "(Si no puedes hacer clic en el botón superior, copia el enlace anterior en la barra de tu navegador o haz clic directamente sobre él)",
        url_tip_style
    )

    url_container = Table([
        [url_clickable],
        [Spacer(1, 1*mm)],
        [url_tip]
    ], colWidths=[15.8*cm], style=[
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ])

    copy_box_content = [
        [exact_heading],
        [Spacer(1, 1*mm)],
        [exact_copy_text],
        [Spacer(1, 1.5*mm)],
        [url_container]
    ]

    copy_box = Table(copy_box_content, colWidths=[16.8*cm], hAlign='CENTER')
    copy_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('ROUNDEDCORNERS', [10, 10, 10, 10]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(copy_box)
    story.append(Spacer(1, 4*mm))

    # 7. Quick 3-step Instructions
    steps_data = [
        [
            Paragraph("<b>Paso 1: Abrir enlace</b>", step_title_style),
            Paragraph("<b>Paso 2: Descargar</b>", step_title_style),
            Paragraph("<b>Paso 3: Guardar copia</b>", step_title_style),
        ],
        [
            Paragraph("Haz clic en el botón verde o copia el enlace y pégalo en Google Chrome, Safari o tu navegador.", step_body_style),
            Paragraph("Dentro de Google Drive verás todas las carpetas, videos y archivos. Puedes abrirlos o descargarlos.", step_body_style),
            Paragraph("Guarda este PDF o agrega la carpeta a tus favoritos de Google Drive para tener acceso permanente.", step_body_style),
        ]
    ]
    steps_table = Table(steps_data, colWidths=[5.4*cm, 5.4*cm, 5.4*cm], hAlign='CENTER')
    steps_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFBEB")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FDE68A")),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(steps_table)
    story.append(Spacer(1, 3.5*mm))

    # 8. Trust Seals & Footer
    selos_path = r"d:\dev\LECCIONES KIDS\imagens-pg-vendas\selos-garantia.png"
    if os.path.exists(selos_path):
        selos_img = RLImage(selos_path, width=8.5*cm, height=2.1*cm)
        selos_table = Table([[selos_img]], colWidths=[18*cm], hAlign='CENTER')
        selos_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(selos_table)
        story.append(Spacer(1, 1.8*mm))

    footer_p1 = Paragraph("<b>Acceso 100% Seguro e Ilimitado</b> &bull; Material disponible las 24 horas para descargar cuando lo necesites.", footer_style)
    footer_p2 = Paragraph("¿Necesitas ayuda con tu descarga? Estamos para servirte en nuestros canales de atención.", footer_style)
    footer_p3 = Paragraph("<b>Lecciones Kids</b> &bull; Materiales Educativos de Excelencia", ParagraphStyle('F3', parent=footer_style, fontName=FONT_BOLD, textColor=c_brown))

    footer_table = Table([[footer_p1], [footer_p2], [footer_p3]], colWidths=[16.8*cm], hAlign='CENTER')
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 0.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
    ]))
    story.append(footer_table)

    doc.build(story)
    print(f"PDF built successfully: {output_pdf_path}")

if __name__ == "__main__":
    out_pdf = r"d:\dev\LECCIONES KIDS\Acceso_Desafios_Calculo_Kids.pdf"
    create_access_pdf(out_pdf)

    # Render preview
    p_doc = pdfium.PdfDocument(out_pdf)
    total_pages = len(p_doc)
    print(f"Total pages: {total_pages}")
    page = p_doc[0]
    bitmap = page.render(scale=2)
    pil_image = bitmap.to_pil()
    preview_path = r"d:\dev\LECCIONES KIDS\preview_desafios_calculo.png"
    pil_image.save(preview_path)
    print(f"Preview saved: {preview_path}")
    p_doc.close()
