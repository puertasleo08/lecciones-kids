import os
from playwright.sync_api import sync_playwright

def render_access_card():
    base_dir = r"d:\dev\LECCIONES KIDS"
    import base64
    def to_b64(p):
        ext = os.path.splitext(p)[1].lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        with open(p, "rb") as f:
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"

    logo_path = os.path.join(base_dir, "imagens-pg-vendas", "logo-lk-horizontal.png")
    capa_path = os.path.join(base_dir, "imagens-pg-vendas", "capa-cronograma-30-clases.jpg")
    selos_path = os.path.join(base_dir, "imagens-pg-vendas", "selos-garantia.png")

    logo_b64 = to_b64(logo_path)
    capa_b64 = to_b64(capa_path)
    selos_b64 = to_b64(selos_path) if os.path.exists(selos_path) else ""

    drive_url = "https://drive.google.com/drive/folders/1mpgI1cNmZ6rXFff4ryLuCyiSPCsskUd6?usp=sharing"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Acceso al Cronograma Pedagógico (30 Clases) - Lecciones Kids</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    @page {{
      size: A4 portrait;
      margin: 0;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    body {{
      font-family: 'Nunito', sans-serif;
      background: #FFFFFF;
      color: #374151;
    }}
    .sheet {{
      width: 210mm;
      height: 297mm;
      padding: 11mm 15mm;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }}
    .logo-row {{
      text-align: center;
      margin-bottom: 2px;
    }}
    .logo-row img {{
      height: 48px;
      width: auto;
    }}
    .congrats-badge {{
      background: #FEF3C7;
      border: 1.5px solid #FCD34D;
      color: #92400E;
      font-weight: 800;
      font-size: 9.5pt;
      padding: 4px 14px;
      border-radius: 999px;
      display: inline-block;
      margin: 0 auto 5px auto;
      text-align: center;
      letter-spacing: 0.5px;
    }}
    .main-title {{
      font-family: 'Fredoka', sans-serif;
      font-size: 19pt;
      font-weight: 700;
      color: #3B2A1A;
      text-align: center;
      line-height: 1.2;
    }}
    .main-sub {{
      font-size: 9.5pt;
      color: #5C5148;
      text-align: center;
      margin: 3px 0 10px 0;
      line-height: 1.35;
      padding: 0 15px;
    }}

    .product-box {{
      background: #FFFDF7;
      border: 1.5px solid #FDE68A;
      border-radius: 12px;
      padding: 10px 14px;
      display: grid;
      grid-template-columns: 82px 1fr;
      gap: 14px;
      align-items: center;
      margin-bottom: 10px;
    }}
    .product-box img {{
      width: 82px;
      height: auto;
      border-radius: 8px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.12);
    }}
    .prod-info-title {{
      font-family: 'Fredoka', sans-serif;
      font-size: 12.5pt;
      font-weight: 700;
      color: #1F2937;
      margin-bottom: 3px;
    }}
    .prod-info-desc {{
      font-size: 8.5pt;
      color: #4B5563;
      line-height: 1.3;
      margin-bottom: 6px;
    }}
    .prod-bullets {{
      display: flex;
      flex-direction: column;
      gap: 2px;
      font-size: 8.5pt;
      font-weight: 800;
      color: #15803D;
    }}

    .cta-button-wrap {{
      text-align: center;
      margin-bottom: 8px;
    }}
    .cta-btn {{
      display: block;
      background: linear-gradient(180deg, #22C55E 0%, #16A34A 100%);
      color: #FFFFFF;
      text-decoration: none;
      font-family: 'Fredoka', sans-serif;
      font-size: 13pt;
      font-weight: 700;
      padding: 12px 20px;
      border-radius: 12px;
      box-shadow: 0 6px 16px rgba(22, 163, 74, 0.35);
      letter-spacing: 0.5px;
      border: 1.5px solid #15803D;
    }}
    .cta-btn span {{
      display: block;
      font-family: 'Nunito', sans-serif;
      font-size: 8.5pt;
      font-weight: 600;
      color: #DCFCE7;
      margin-top: 2px;
    }}

    .copy-box {{
      background: #F8FAFC;
      border: 1.5px dashed #94A3B8;
      border-radius: 10px;
      padding: 8px 12px;
      margin-bottom: 10px;
      text-align: center;
    }}
    .copy-box-title {{
      font-size: 9pt;
      font-weight: 800;
      color: #1E3A8A;
      margin-bottom: 3px;
    }}
    .copy-box-url {{
      font-size: 8pt;
      font-weight: 700;
      color: #1D4ED8;
      word-break: break-all;
      background: #FFFFFF;
      padding: 4px 8px;
      border-radius: 6px;
      border: 1px solid #CBD5E1;
      display: inline-block;
      text-decoration: none;
    }}
    .copy-box-tip {{
      font-size: 7.5pt;
      color: #64748B;
      font-style: italic;
      margin-top: 3px;
    }}

    .steps-row {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-bottom: 10px;
    }}
    .step-card {{
      background: #FFFBEB;
      border: 1px solid #FDE68A;
      border-radius: 10px;
      padding: 8px 10px;
      font-size: 8pt;
    }}
    .step-card strong {{
      font-size: 8.5pt;
      color: #92400E;
      display: block;
      margin-bottom: 2px;
    }}
    .step-card p {{
      color: #5C5148;
      line-height: 1.25;
    }}

    .seal-wrap {{
      text-align: center;
      margin: 4px 0;
    }}
    .seal-wrap img {{
      height: 38px;
      width: auto;
    }}

    .card-footer {{
      border-top: 1px solid #E5E7EB;
      padding-top: 6px;
      text-align: center;
      font-size: 8pt;
      color: #64748B;
      line-height: 1.35;
    }}
    .card-footer strong {{
      color: #374151;
    }}
  </style>
</head>
<body>
  <div class="sheet">
    <div style="text-align: center;">
      <div class="logo-row">
        <img src="{logo_b64}" alt="Lecciones Kids">
      </div>
      <div class="congrats-badge">¡FELICITACIONES POR TU COMPRA! • ACCESO INMEDIATO</div>
      <h1 class="main-title">¡Bienvenido/a a tu Cronograma Pedagógico!</h1>
      <p class="main-sub">
        Tu planificación de 30 clases y materiales educativos de 1º a 5º grado ya están listos en formato digital de alta resolución. Para acceder inmediatamente a todos los archivos y guías, usa cualquiera de las opciones a continuación:
      </p>
    </div>

    <div class="product-box">
      <img src="{capa_b64}" alt="Cronograma 30 Clases">
      <div>
        <div class="prod-info-title">Cronograma Pedagógico Detallado (30 Clases) — 1º al 5º Grado</div>
        <div class="prod-info-desc">
          Planificación completa con alineación curricular BNCC, estructurada en 6 fases pedagógicas: Alfabetización Numérica, Consolidación Decimal CDU, Multiplicación, División, Fracciones y Desafíos Integrados de las 4 Operaciones.
        </div>
        <div class="prod-bullets">
          <div>✓ Incluye Solucionario y Guías Imprimibles A4</div>
          <div>✓ Enlaces directos a los materiales de referencia en Google Drive</div>
          <div>✓ Acceso permanente, vitalicio e ilimitado las 24 horas</div>
        </div>
      </div>
    </div>

    <div>
      <div class="cta-button-wrap">
        <a href="{drive_url}" target="_blank" class="cta-btn">
          HAZ CLIC AQUÍ PARA ACCEDER AL MATERIAL ➜
          <span>Acceso directo y seguro a la carpeta oficial en Google Drive</span>
        </a>
      </div>

      <div class="copy-box">
        <div class="copy-box-title">¿El botón no responde? Abre el enlace directamente:</div>
        <a href="{drive_url}" target="_blank" class="copy-box-url">{drive_url}</a>
        <div class="copy-box-tip">Tip: Copia este enlace y pégalo en la barra de direcciones de tu navegador preferido.</div>
      </div>
    </div>

    <div class="steps-row">
      <div class="step-card">
        <strong>Paso 1: Abrir enlace</strong>
        <p>Haz clic en el botón verde superior o copia el enlace en Google Chrome o Safari.</p>
      </div>
      <div class="step-card">
        <strong>Paso 2: Descargar</strong>
        <p>Dentro de Google Drive verás todas las carpetas organizadas por fases y clases.</p>
      </div>
      <div class="step-card">
        <strong>Paso 3: Guardar copia</strong>
        <p>Descarga los archivos a tu computadora o celular para tener acceso permanente.</p>
      </div>
    </div>

    <div class="seal-wrap">
      {'<img src="' + selos_b64 + '" alt="Sellos">' if selos_b64 else ''}
    </div>

    <div class="card-footer">
      <div><strong>Acceso 100% Seguro e Ilimitado</strong> • Material disponible las 24 horas para descargar cuando lo necesites.</div>
      <div>¿Necesitas ayuda con tu descarga? Estamos para servirte en nuestros canales de atención al cliente.</div>
      <div><strong>Lecciones Kids</strong> • Materiales Educativos de Excelencia</div>
    </div>
  </div>
</body>
</html>
"""
    html_out = os.path.join(base_dir, "acceso_cronograma_card.html")
    pdf_out = os.path.join(base_dir, "Acceso_Cronograma_Pedagogico.pdf")
    with open(html_out, "w", encoding="utf-8") as f:
        f.write(html)
        
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 1600})
        page.goto(f"file:///{html_out.replace(os.sep, '/')}")
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        
        # Screenshot preview
        card_el = page.query_selector(".sheet")
        preview_out = os.path.join(base_dir, "preview_acceso_cronograma.png")
        card_el.screenshot(path=preview_out)
        print(f"Card preview saved: {preview_out}")
        
        page.pdf(
            path=pdf_out,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True
        )
        print(f"Card PDF generated: {pdf_out} ({os.path.getsize(pdf_out)/1024:.1f} KB)")
        browser.close()

if __name__ == "__main__":
    render_access_card()
