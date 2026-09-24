import os
import base64
from playwright.sync_api import sync_playwright

def to_b64(p):
    if not os.path.exists(p):
        return ""
    ext = os.path.splitext(p)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    with open(p, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"

def render_restricted_pdf():
    base_dir = r"d:\dev\LECCIONES KIDS"
    logo_path = os.path.join(base_dir, "imagens-pg-vendas", "logo-lk-horizontal.png")
    capa_path = os.path.join(base_dir, "imagens-pg-vendas", "capa-cronograma-30-clases.jpg")
    selos_path = os.path.join(base_dir, "imagens-pg-vendas", "selos-garantia.png")

    logo_b64 = to_b64(logo_path)
    capa_b64 = to_b64(capa_path)
    selos_b64 = to_b64(selos_path)

    upsell_url = "https://www.leccioneskids.shop/upsell"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Acceso Restringido - Cronograma Pedagógico 30 Clases | Lecciones Kids</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
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
      font-family: 'Nunito', system-ui, -apple-system, sans-serif;
      background: #FFFFFF;
      color: #374151;
    }}
    .sheet {{
      width: 210mm;
      height: 297mm;
      padding: 10mm 15mm 9mm 15mm;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
      background: linear-gradient(180deg, #FFFDF8 0%, #FFFFFF 100%);
    }}

    .logo-row {{
      text-align: center;
      margin-bottom: 2px;
    }}
    .logo-row img {{
      height: 46px;
      width: auto;
    }}

    .lock-badge {{
      background: #FEF2F2;
      border: 1.5px solid #FCA5A5;
      color: #DC2626;
      font-weight: 800;
      font-size: 9.5pt;
      padding: 3.5px 14px;
      border-radius: 999px;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      margin: 0 auto 5px auto;
      letter-spacing: 0.5px;
      box-shadow: 0 2px 4px rgba(220, 38, 38, 0.08);
    }}

    .main-title {{
      font-size: 19.5pt;
      font-weight: 900;
      color: #1F2937;
      text-align: center;
      line-height: 1.2;
    }}
    .main-title span {{
      color: #DC2626;
    }}

    .main-sub {{
      font-size: 9.2pt;
      color: #4B5563;
      text-align: center;
      margin: 3px 0 8px 0;
      line-height: 1.35;
      padding: 0 10px;
    }}

    /* PRODUCT CARD WITH LOCK OVERLAY */
    .product-box {{
      background: #FFFFFF;
      border: 1.5px solid #E2E8F0;
      border-radius: 14px;
      padding: 10px 14px;
      display: grid;
      grid-template-columns: 88px 1fr;
      gap: 14px;
      align-items: center;
      box-shadow: 0 4px 12px rgba(0,0,0,0.04);
      position: relative;
      overflow: hidden;
    }}
    .product-box::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 5px;
      height: 100%;
      background: #EF4444;
    }}

    .mockup-wrap {{
      position: relative;
      width: 88px;
    }}
    .mockup-wrap img {{
      width: 88px;
      height: auto;
      border-radius: 8px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.12);
      filter: brightness(0.92);
    }}
    .mockup-lock-badge {{
      position: absolute;
      bottom: -6px;
      right: -6px;
      background: #EF4444;
      color: #FFFFFF;
      border-radius: 50%;
      width: 26px;
      height: 26px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12pt;
      box-shadow: 0 2px 6px rgba(0,0,0,0.25);
      border: 2px solid #FFFFFF;
    }}

    .prod-info-title {{
      font-size: 12.5pt;
      font-weight: 800;
      color: #1F2937;
      margin-bottom: 2px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .status-pill {{
      background: #FEE2E2;
      color: #991B1B;
      font-size: 7.5pt;
      font-weight: 800;
      padding: 1.5px 6px;
      border-radius: 6px;
      display: inline-block;
    }}
    .prod-info-desc {{
      font-size: 8.5pt;
      color: #4B5563;
      line-height: 1.3;
      margin-bottom: 5px;
    }}
    .prod-bullets {{
      display: flex;
      flex-direction: column;
      gap: 2px;
      font-size: 8.3pt;
      font-weight: 700;
      color: #374151;
    }}
    .prod-bullets span.icon-lock {{
      color: #EF4444;
    }}
    .prod-bullets span.icon-check {{
      color: #10B981;
    }}

    /* UNLOCK DISCOUNT BANNER */
    .discount-banner {{
      background: #FEF3C7;
      border: 1.5px dashed #F59E0B;
      border-radius: 10px;
      padding: 6px 12px;
      text-align: center;
      margin: 8px 0;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .discount-banner-text {{
      font-size: 8.5pt;
      font-weight: 800;
      color: #92400E;
    }}
    .discount-price-pill {{
      background: #D97706;
      color: #FFFFFF;
      font-weight: 900;
      font-size: 9.5pt;
      padding: 3px 10px;
      border-radius: 8px;
    }}

    /* CTA BUTTON */
    .cta-button-wrap {{
      text-align: center;
      margin-bottom: 7px;
    }}
    .cta-btn {{
      display: block;
      background: linear-gradient(180deg, #10B981 0%, #059669 100%);
      color: #FFFFFF;
      text-decoration: none;
      font-size: 13.5pt;
      font-weight: 900;
      padding: 12px 20px;
      border-radius: 12px;
      box-shadow: 0 6px 16px rgba(16, 185, 129, 0.35);
      letter-spacing: 0.3px;
      border: 1.5px solid #047857;
    }}
    .cta-btn span {{
      display: block;
      font-size: 8.5pt;
      font-weight: 700;
      color: #D1FAE5;
      margin-top: 2px;
    }}

    /* COPY LINK BOX */
    .copy-box {{
      background: #F8FAFC;
      border: 1.5px dashed #CBD5E1;
      border-radius: 10px;
      padding: 7px 12px;
      margin-bottom: 8px;
      text-align: center;
    }}
    .copy-box-title {{
      font-size: 8.5pt;
      font-weight: 800;
      color: #1E40AF;
      margin-bottom: 2px;
    }}
    .copy-box-url {{
      font-size: 8.5pt;
      font-weight: 800;
      color: #2563EB;
      word-break: break-all;
      background: #FFFFFF;
      padding: 3px 10px;
      border-radius: 6px;
      border: 1px solid #BFDBFE;
      display: inline-block;
      text-decoration: underline;
    }}
    .copy-box-tip {{
      font-size: 7.5pt;
      color: #64748B;
      font-style: italic;
      margin-top: 2px;
    }}

    /* STEPS ROW */
    .steps-row {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 9px;
      margin-bottom: 8px;
    }}
    .step-card {{
      background: #FFFBEB;
      border: 1px solid #FDE68A;
      border-radius: 10px;
      padding: 7px 9px;
      font-size: 8pt;
    }}
    .step-card strong {{
      font-size: 8.3pt;
      color: #92400E;
      display: block;
      margin-bottom: 1.5px;
    }}
    .step-card p {{
      color: #5C5148;
      line-height: 1.25;
    }}

    .seal-wrap {{
      text-align: center;
      margin: 2px 0;
    }}
    .seal-wrap img {{
      height: 36px;
      width: auto;
    }}

    .card-footer {{
      border-top: 1px solid #E5E7EB;
      padding-top: 5px;
      text-align: center;
      font-size: 7.8pt;
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
      <div class="lock-badge">
        <span>🔒</span> MÓDULO BLOQUEADO • ACCESO RESTRINGIDO
      </div>
      <h1 class="main-title">Este Material <span>No Está Incluido</span> en tu Plan Actual</h1>
      <p class="main-sub">
        Para acceder al <strong>Cronograma Pedagógico Detallado (30 Clases Paso a Paso)</strong> con solucionario maestro y biblioteca de referencia en Google Drive, desbloquea tu acceso exclusivo con descuento especial a continuación:
      </p>
    </div>

    <!-- PRODUCT DETAIL BOX WITH LOCK -->
    <div class="product-box">
      <div class="mockup-wrap">
        <img src="{capa_b64}" alt="Cronograma 30 Clases">
        <div class="mockup-lock-badge">🔒</div>
      </div>
      <div>
        <div class="prod-info-title">
          <span>Cronograma Pedagógico (30 Clases)</span>
          <span class="status-pill">🔒 NO DESBLOQUEADO</span>
        </div>
        <div class="prod-info-desc">
          Planificación curricular completa alineada a la BNCC para 1º a 5º grado, estructurada en 6 fases estratégicas: Conteo, Suma/Resta CDU con reagrupación, Multiplicación, División, Fracciones y Desafíos Integrados.
        </div>
        <div class="prod-bullets">
          <div><span class="icon-check">✓</span> 30 Clases con objetivos y dinámicas paso a paso</div>
          <div><span class="icon-check">✓</span> Solucionario completo y Fichas Didácticas A4 listas para imprimir</div>
          <div><span class="icon-lock">🔒</span> Acceso digital directo a las carpetas en Google Drive</div>
        </div>
      </div>
    </div>

    <!-- SPECIAL UNLOCK PROMO BANNER -->
    <div class="discount-banner">
      <div class="discount-banner-text">
        ⚡ Oportunidad Única para Alumnos: Descuento Especial del 74%
      </div>
      <div class="discount-price-pill">
        Por solo $6.99 USD
      </div>
    </div>

    <!-- PRIMARY UNLOCK CTA -->
    <div>
      <div class="cta-button-wrap">
        <a href="{upsell_url}" target="_blank" class="cta-btn">
          🔓 HAZ CLIC AQUÍ PARA DESBLOQUEAR EL CRONOGRAMA ➜
          <span>Haz clic para abrir la página especial y activar tu acceso inmediato por solo $6.99 USD</span>
        </a>
      </div>

      <div class="copy-box">
        <div class="copy-box-title">¿El botón no responde? Abre el enlace directamente en tu navegador:</div>
        <a href="{upsell_url}" target="_blank" class="copy-box-url">{upsell_url}</a>
        <div class="copy-box-tip">Tip: Copia y pega esta dirección web en Google Chrome o Safari para acceder a tu oferta exclusiva.</div>
      </div>
    </div>

    <!-- 3 EASY UNLOCK STEPS -->
    <div class="steps-row">
      <div class="step-card">
        <strong>Paso 1: Abrir el Enlace</strong>
        <p>Haz clic en el botón verde superior para acceder a la página oficial de desbloqueo.</p>
      </div>
      <div class="step-card">
        <strong>Paso 2: Confirmar la Oferta</strong>
        <p>Aprovecha el descuento único de $6.99 USD (precio normal $27.00 USD).</p>
      </div>
      <div class="step-card">
        <strong>Paso 3: Acceso Inmediato</strong>
        <p>El candado se retira al instante y recibes la carpeta completa en Google Drive y correo.</p>
      </div>
    </div>

    <!-- TRUST SEALS -->
    <div class="seal-wrap">
      {'<img src="' + selos_b64 + '" alt="Sellos">' if selos_b64 else ''}
    </div>

    <!-- FOOTER -->
    <div class="card-footer">
      <div><strong>Compra 100% Segura</strong> • Garantía Incondicional de 7 Días • Soporte al Cliente las 24 horas.</div>
      <div>¿Tienes dudas con tu activación? Contáctanos a través de nuestros canales oficiales de atención.</div>
      <div><strong>Lecciones Kids</strong> • Materiales Educativos de Excelencia</div>
    </div>
  </div>
</body>
</html>
"""
    html_out = os.path.join(base_dir, "acceso_restringido_cronograma.html")
    pdf_out1 = os.path.join(base_dir, "Acceso_Restringido_Cronograma.pdf")
    pdf_out2 = os.path.join(base_dir, "Acceso_Cronograma_Pedagogico.pdf")
    
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
        preview_out = os.path.join(base_dir, "preview_acceso_restringido.png")
        card_el.screenshot(path=preview_out)
        print(f"Locked card preview saved: {preview_out}")
        
        # Save both PDF filenames
        page.pdf(
            path=pdf_out1,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True
        )
        page.pdf(
            path=pdf_out2,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True
        )
        print(f"Generated PDFs: {pdf_out1} & {pdf_out2}")
        browser.close()

if __name__ == "__main__":
    render_restricted_pdf()
