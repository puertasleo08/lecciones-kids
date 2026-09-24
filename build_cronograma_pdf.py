import os
import base64
import subprocess
try:
    import pypdfium2 as pdfium
except ImportError:
    pdfium = None

def to_base64(path):
    if not os.path.exists(path):
        return ""
    ext = os.path.splitext(path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"

def generate_html():
    base_dir = r"d:\dev\LECCIONES KIDS"
    logo_horiz = to_base64(os.path.join(base_dir, "imagens-pg-vendas", "logo-lk-horizontal.png"))
    logo_square = to_base64(os.path.join(base_dir, "imagens-pg-vendas", "logo-lk-square.png"))
    capa_img = to_base64(os.path.join(base_dir, "imagens-pg-vendas", "capa-cronograma-30-clases.jpg"))
    selos_img = to_base64(os.path.join(base_dir, "imagens-pg-vendas", "selos-beneficios.png"))
    garantia_img = to_base64(os.path.join(base_dir, "imagens-pg-vendas", "selos-garantia.png"))

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Cronograma Pedagógico Detallado (30 Clases) - Lecciones Kids</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
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
      color: #1F2937;
      background: #F3F4F6;
      -webkit-font-smoothing: antialiased;
    }}

    .page {{
      width: 210mm;
      min-height: 297mm;
      height: 297mm;
      padding: 14mm 16mm;
      background: #FFFFFF;
      margin: 0 auto 10mm auto;
      page-break-after: always;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
    }}

    @media print {{
      body {{
        background: transparent;
      }}
      .page {{
        margin: 0;
        page-break-after: always;
        height: 297mm;
      }}
    }}

    /* HEADER & FOOTER */
    .doc-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #E5E7EB;
      padding-bottom: 8px;
      margin-bottom: 12px;
    }}
    .doc-header-logo img {{
      height: 38px;
      width: auto;
      object-fit: contain;
    }}
    .doc-header-info {{
      text-align: right;
    }}
    .doc-header-title {{
      font-family: 'Fredoka', sans-serif;
      font-weight: 700;
      font-size: 13pt;
      color: #1E40AF;
    }}
    .doc-header-badge {{
      font-size: 8.5pt;
      font-weight: 800;
      color: #047857;
      background: #D1FAE5;
      padding: 2px 8px;
      border-radius: 999px;
      display: inline-block;
      margin-top: 2px;
    }}

    .doc-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1.5px solid #E5E7EB;
      padding-top: 6px;
      margin-top: 8px;
      font-size: 8.5pt;
      color: #6B7280;
    }}
    .doc-footer strong {{
      color: #374151;
    }}

    /* =========================================
       PAGE 1: COVER
       ========================================= */
    .cover-page {{
      background: linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 50%, #ECFDF5 100%);
      align-items: center;
      text-align: center;
      justify-content: space-between;
      padding: 16mm 18mm 12mm 18mm;
    }}
    .cover-top-logo img {{
      height: 65px;
      width: auto;
      filter: drop-shadow(0 4px 6px rgba(0,0,0,0.06));
    }}
    .cover-badge-top {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #FEF3C7;
      border: 1.5px solid #FCD34D;
      color: #92400E;
      font-weight: 800;
      font-size: 10pt;
      padding: 6px 18px;
      border-radius: 999px;
      letter-spacing: 0.5px;
      margin-top: 10px;
    }}
    .cover-main-title {{
      font-family: 'Fredoka', sans-serif;
      font-size: 28pt;
      font-weight: 700;
      line-height: 1.15;
      color: #1E3A8A;
      margin-top: 10px;
    }}
    .cover-main-title span {{
      color: #059669;
    }}
    .cover-sub {{
      font-size: 12pt;
      font-weight: 700;
      color: #4B5563;
      margin-top: 6px;
    }}
    .cover-mockup-wrap {{
      margin: 10px 0;
      display: flex;
      justify-content: center;
      align-items: center;
    }}
    .cover-mockup-wrap img {{
      height: 120mm;
      width: auto;
      border-radius: 12px;
      box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.22), 0 0 0 1px rgba(0,0,0,0.04);
    }}
    .cover-features-bar {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      width: 100%;
      margin-top: 8px;
    }}
    .cover-feature-pill {{
      background: #FFFFFF;
      border: 1.5px solid #BFDBFE;
      border-radius: 10px;
      padding: 6px 8px;
      font-size: 8.5pt;
      font-weight: 800;
      color: #1E40AF;
      box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }}
    .cover-bottom-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      border-top: 1.5px solid #E2E8F0;
      padding-top: 8px;
      font-size: 8.5pt;
      color: #64748B;
    }}

    /* =========================================
       PAGE 2: ACCESS & DRIVE LINKS
       ========================================= */
    .access-banner {{
      background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
      color: #FFFFFF;
      border-radius: 14px;
      padding: 14px 18px;
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .access-banner h2 {{
      font-family: 'Fredoka', sans-serif;
      font-size: 16pt;
      margin-bottom: 2px;
    }}
    .access-banner p {{
      font-size: 9.5pt;
      opacity: 0.92;
    }}
    .access-global-btn {{
      background: #10B981;
      color: #FFFFFF;
      text-decoration: none;
      font-weight: 800;
      font-size: 10pt;
      padding: 9px 16px;
      border-radius: 10px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 10px rgba(16, 185, 129, 0.4);
      white-space: nowrap;
    }}

    .phases-access-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      flex-grow: 1;
    }}
    .phase-link-card {{
      background: #FAFAFA;
      border: 1.5px solid #E5E7EB;
      border-radius: 12px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .phase-link-card.f1 {{ border-left: 5px solid #3B82F6; background: #F8FAFC; }}
    .phase-link-card.f2 {{ border-left: 5px solid #8B5CF6; background: #FAF5FF; }}
    .phase-link-card.f3 {{ border-left: 5px solid #F59E0B; background: #FFFBEB; }}
    .phase-link-card.f4 {{ border-left: 5px solid #06B6D4; background: #ECFEFF; }}
    .phase-link-card.f5 {{ border-left: 5px solid #EC4899; background: #FDF2F8; }}
    .phase-link-card.f6 {{ border-left: 5px solid #10B981; background: #F0FDF4; }}

    .phase-badge-tag {{
      font-size: 8pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 2px;
    }}
    .phase-link-title {{
      font-family: 'Fredoka', sans-serif;
      font-size: 11pt;
      font-weight: 700;
      color: #1F2937;
      margin-bottom: 6px;
    }}
    .drive-file-btn {{
      display: flex;
      align-items: center;
      gap: 6px;
      text-decoration: none;
      background: #FFFFFF;
      border: 1px solid #CBD5E1;
      border-radius: 8px;
      padding: 5px 8px;
      margin-bottom: 4px;
      font-size: 8pt;
      font-weight: 700;
      color: #2563EB;
      transition: all 0.2s;
    }}
    .drive-file-btn span.file-icon {{
      font-size: 10pt;
    }}

    .instructions-box {{
      background: #FFFBEB;
      border: 1.5px solid #FDE68A;
      border-radius: 10px;
      padding: 8px 12px;
      margin-top: 10px;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      font-size: 8pt;
    }}
    .instructions-box strong {{
      color: #92400E;
      display: block;
      font-size: 8.5pt;
      margin-bottom: 2px;
    }}

    /* =========================================
       PAGES 3 - 8: CRONOGRAMA POR FASES
       ========================================= */
    .phase-intro-header {{
      border-radius: 10px;
      padding: 8px 12px;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .phase-intro-header.fase1 {{ background: #EFF6FF; border: 1.5px solid #BFDBFE; }}
    .phase-intro-header.fase2 {{ background: #FAF5FF; border: 1.5px solid #E9D5FF; }}
    .phase-intro-header.fase3 {{ background: #FFFBEB; border: 1.5px solid #FDE68A; }}
    .phase-intro-header.fase4 {{ background: #ECFEFF; border: 1.5px solid #A5F3FC; }}
    .phase-intro-header.fase5 {{ background: #FDF2F8; border: 1.5px solid #FBCFE8; }}
    .phase-intro-header.fase6 {{ background: #F0FDF4; border: 1.5px solid #A7F3D0; }}

    .phase-intro-title {{
      font-family: 'Fredoka', sans-serif;
      font-size: 13pt;
      font-weight: 700;
      color: #1F2937;
    }}
    .phase-intro-sub {{
      font-size: 9pt;
      font-weight: 700;
      color: #6B7280;
    }}
    .phase-intro-badge {{
      font-size: 8.5pt;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 999px;
      color: #FFFFFF;
    }}
    .fase1 .phase-intro-badge {{ background: #3B82F6; }}
    .fase2 .phase-intro-badge {{ background: #8B5CF6; }}
    .fase3 .phase-intro-badge {{ background: #F59E0B; }}
    .fase4 .phase-intro-badge {{ background: #06B6D4; }}
    .fase5 .phase-intro-badge {{ background: #EC4899; }}
    .fase6 .phase-intro-badge {{ background: #10B981; }}

    .class-cards-container {{
      display: flex;
      flex-direction: column;
      gap: 7px;
      flex-grow: 1;
    }}
    .class-card {{
      border: 1.5px solid #E5E7EB;
      border-radius: 9px;
      padding: 7px 10px;
      background: #FFFFFF;
      box-shadow: 0 1px 3px rgba(0,0,0,0.02);
      display: grid;
      grid-template-columns: 2.1fr 1.9fr;
      gap: 10px;
      align-items: start;
    }}
    .class-card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 2px;
    }}
    .class-number-title {{
      font-family: 'Fredoka', sans-serif;
      font-size: 10pt;
      font-weight: 700;
      color: #111827;
    }}
    .class-bncc-pill {{
      font-size: 7.5pt;
      font-weight: 800;
      color: #1E40AF;
      background: #EFF6FF;
      border: 1px solid #DBEAFE;
      padding: 1px 6px;
      border-radius: 6px;
    }}
    .class-desc-item {{
      font-size: 8pt;
      color: #374151;
      line-height: 1.25;
      margin-top: 2px;
    }}
    .class-desc-item strong {{
      color: #1F2937;
      font-weight: 800;
    }}

    /* =========================================
       PAGE 9: MASTER WORKSHEET - CLASE 01
       ========================================= */
    .worksheet-wrap {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      height: 100%;
    }}
    .ws-header {{
      border: 2px solid #3B82F6;
      border-radius: 12px;
      padding: 7px 12px;
      background: #F0F7FF;
      display: flex;
      flex-direction: column;
      gap: 5px;
    }}
    .ws-header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .ws-brand {{
      font-family: 'Fredoka', sans-serif;
      font-size: 16pt;
      font-weight: 700;
      color: #1D4ED8;
    }}
    .ws-brand span {{
      font-size: 9.5pt;
      color: #F59E0B;
      font-weight: 800;
      text-transform: uppercase;
      margin-left: 6px;
    }}
    .ws-bncc {{
      background: #3B82F6;
      color: #FFFFFF;
      font-weight: 800;
      font-size: 9pt;
      padding: 3px 10px;
      border-radius: 999px;
    }}
    .ws-fields {{
      display: grid;
      grid-template-columns: 2fr 1fr 1fr;
      gap: 8px;
      font-size: 9pt;
      font-weight: 700;
      color: #4B5563;
      border-top: 1px dashed #BFDBFE;
      padding-top: 4px;
    }}
    .ws-line {{
      border-bottom: 1.5px dotted #93C5FD;
      display: inline-block;
      width: 60%;
      height: 12px;
    }}

    .ws-concept {{
      border: 2px solid #FCD34D;
      background: #FFFDF0;
      border-radius: 10px;
      padding: 8px 12px;
      display: grid;
      grid-template-columns: 1.8fr 1fr;
      gap: 10px;
      align-items: center;
    }}
    .ws-concept-tag {{
      font-size: 9.5pt;
      font-weight: 800;
      color: #D97706;
      text-transform: uppercase;
    }}
    .ws-concept-title {{
      font-family: 'Fredoka', sans-serif;
      font-size: 13pt;
      font-weight: 700;
      color: #111827;
      margin: 1px 0 3px 0;
    }}
    .ws-concept-p {{
      font-size: 9.5pt;
      color: #374151;
      line-height: 1.25;
    }}

    .ws-practice-title {{
      font-family: 'Fredoka', sans-serif;
      font-size: 11.5pt;
      font-weight: 700;
      color: #1E40AF;
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 2px;
    }}
    .ws-practice-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }}
    .ws-task-card {{
      border: 1.5px solid #E5E7EB;
      border-radius: 10px;
      padding: 6px 10px;
      background: #FAFAFA;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 82px;
    }}
    .ws-task-top {{
      font-size: 9pt;
      font-weight: 800;
      color: #4B5563;
      display: flex;
      justify-content: space-between;
    }}
    .ws-items-box {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      align-items: center;
      justify-content: center;
      background: #FFFFFF;
      border: 1px dashed #D1D5DB;
      border-radius: 6px;
      padding: 4px;
      margin: 4px 0;
      font-size: 13pt;
    }}
    .ws-ans-row {{
      display: flex;
      justify-content: flex-end;
      align-items: center;
      gap: 6px;
      font-size: 9.5pt;
      font-weight: 800;
    }}
    .ws-input-box {{
      width: 34px;
      height: 26px;
      border: 1.5px solid #3B82F6;
      border-radius: 6px;
      background: #FFFFFF;
    }}

    .ws-match-box {{
      border: 1.5px solid #CBD5E1;
      background: #F8FAFC;
      border-radius: 10px;
      padding: 7px 10px;
    }}
    .ws-match-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      text-align: center;
      margin-top: 4px;
    }}
    .ws-match-col {{
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 6px;
      padding: 4px;
      font-size: 8pt;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
    }}
    .ws-match-num {{
      font-family: 'Fredoka', sans-serif;
      font-size: 13pt;
      font-weight: 700;
      color: #2563EB;
      background: #EFF6FF;
      border: 1px solid #BFDBFE;
      border-radius: 6px;
      padding: 1px 8px;
    }}

    .ws-problem {{
      border: 2px solid #10B981;
      background: #F0FDF4;
      border-radius: 10px;
      padding: 7px 10px;
    }}
    .ws-problem-title {{
      font-family: 'Fredoka', sans-serif;
      font-size: 10.5pt;
      font-weight: 700;
      color: #047857;
      margin-bottom: 2px;
    }}
    .ws-problem-text {{
      font-size: 9pt;
      color: #1F2937;
      line-height: 1.3;
      margin-bottom: 5px;
    }}
    .ws-problem-cols {{
      display: grid;
      grid-template-columns: 1.8fr 1.2fr;
      gap: 8px;
      align-items: center;
    }}
    .ws-drawing-area {{
      background: #FFFFFF;
      border: 1.5px dashed #6EE7B7;
      border-radius: 6px;
      height: 52px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 8pt;
      color: #9CA3AF;
      font-style: italic;
    }}
    .ws-answer-calc {{
      background: #FFFFFF;
      border: 1px solid #A7F3D0;
      border-radius: 6px;
      padding: 5px 8px;
      font-size: 8.5pt;
      font-weight: 700;
      color: #065F46;
    }}
  </style>
</head>
<body>

  <!-- =========================================================
       PAGE 1: PORTADA OFICIAL
       ========================================================= -->
  <div class="page cover-page">
    <div class="cover-top-logo">
      <img src="{logo_horiz}" alt="Lecciones Kids">
    </div>

    <div>
      <div class="cover-badge-top">
        <span>★</span> 1º AL 5º GRADO • CURRÍCULO COMPLETO Y BNCC <span>★</span>
      </div>
      <h1 class="cover-main-title">CRONOGRAMA PEDAGÓGICO<br><span>DETALLADO (30 CLASES)</span></h1>
      <p class="cover-sub">¡Incluye Solucionario y Enlaces a Materiales de Referencia!</p>
    </div>

    <div class="cover-mockup-wrap">
      <img src="{capa_img}" alt="Cuaderno 30 Clases">
    </div>

    <div class="cover-features-bar">
      <div class="cover-feature-pill">✓ 30 Clases Estructuradas</div>
      <div class="cover-feature-pill">✓ 6 Fases Pedagógicas</div>
      <div class="cover-feature-pill">✓ Fichas Imprimibles A4</div>
      <div class="cover-feature-pill">✓ Solucionario Completo</div>
    </div>

    <div class="cover-bottom-bar">
      <span><strong>Lecciones Kids</strong> • Todos los derechos reservados</span>
      <span>Guía Didáctica para Docentes y Familias</span>
    </div>
  </div>

  <!-- =========================================================
       PAGE 2: ACCESO Y MATERIALES EN GOOGLE DRIVE
       ========================================================= -->
  <div class="page">
    <div class="doc-header">
      <div class="doc-header-logo">
        <img src="{logo_horiz}" alt="Logo">
      </div>
      <div class="doc-header-info">
        <div class="doc-header-title">Materiales de Referencia Digitales</div>
        <div class="doc-header-badge">Google Drive • Acceso Permanente</div>
      </div>
    </div>

    <div class="access-banner">
      <div>
        <h2>Biblioteca Central de Materiales</h2>
        <p>Haz clic en cada botón para abrir directamente los PDFs oficiales en Google Drive.</p>
      </div>
      <a href="https://drive.google.com/drive/folders/1mpgI1cNmZ6rXFff4ryLuCyiSPCsskUd6?usp=sharing" target="_blank" class="access-global-btn">
        Abrir Carpeta Completa ➜
      </a>
    </div>

    <div class="phases-access-grid">
      <!-- Fase 1 -->
      <div class="phase-link-card f1">
        <div>
          <span class="phase-badge-tag" style="color: #2563EB;">Fase 1 • 1º Grado / Transición</span>
          <div class="phase-link-title">Alfabetización Numérica</div>
          <a href="https://drive.google.com/file/d/1KkMIUQCeU_ZqHv7mwaXcxtGZJ_yy4LBX/view?usp=drivesdk&utm_source=gemini" target="_blank" class="drive-file-btn">
            <span class="file-icon">📄</span> Conhecendo os números e sinais.pdf
          </a>
          <a href="https://drive.google.com/file/d/1sXW7rWzGX0t6plt5LYITqHRnp3q66nID/view?usp=drivesdk&utm_source=gemini" target="_blank" class="drive-file-btn">
            <span class="file-icon">📄</span> Matemática 1° ano.pdf
          </a>
          <a href="https://drive.google.com/file/d/1VdrRiZ_67ikXI53Rh2pV_wgu7cXwQHlr/view?usp=drivesdk&utm_source=gemini" target="_blank" class="drive-file-btn">
            <span class="file-icon">📄</span> Situações-problema 1° Ano.pdf
          </a>
        </div>
        <div style="font-size: 7.5pt; color: #64748B;">Clases 01 a 07 • Conteo hasta 100, suma/resta inicial</div>
      </div>

      <!-- Fase 2 -->
      <div class="phase-link-card f2">
        <div>
          <span class="phase-badge-tag" style="color: #7C3AED;">Fase 2 • 2º y 3º Grado</span>
          <div class="phase-link-title">Consolidación Decimal y CDU</div>
          <a href="https://drive.google.com/file/d/1ig2O8kBztwFN6BC_7S_kU1-OI_jlqxFm/view?usp=drivesdk&utm_source=gemini" target="_blank" class="drive-file-btn">
            <span class="file-icon">📄</span> Adição e Subtração 2° e 3° ano.pdf
          </a>
          <a href="https://drive.google.com/file/d/1GAt95yykajEG3pk7y7nMuGaDonq9n9nR/view?usp=drivesdk&utm_source=gemini" target="_blank" class="drive-file-btn">
            <span class="file-icon">📄</span> Situações-problema 2º e 3º ano.pdf
          </a>
        </div>
        <div style="font-size: 7.5pt; color: #64748B;">Clases 08 a 13 • Algoritmo con llevada, problemas y gráficos</div>
      </div>

      <!-- Fase 3 -->
      <div class="phase-link-card f3">
        <div>
          <span class="phase-badge-tag" style="color: #D97706;">Fase 3 • 2º a 5º Grado</span>
          <div class="phase-link-title">Multiplicación y Tablas</div>
          <a href="https://drive.google.com/file/d/1PrM-IkuOsxjI9AClDLWTNBIrbmQi1Wgf/view?usp=drivesdk&utm_source=gemini" target="_blank" class="drive-file-btn">
            <span class="file-icon">📄</span> Mural da tabuada.pdf
          </a>
          <a href="https://drive.google.com/file/d/1TYHYRPkgl0Oxmo-31fa4q4qpeIXpuLDf/view?usp=drivesdk&utm_source=gemini" target="_blank" class="drive-file-btn">
            <span class="file-icon">📄</span> Multiplicação 2° e 5° ano.pdf
          </a>
        </div>
        <div style="font-size: 7.5pt; color: #64748B;">Clases 14 a 18 • Tablas 1 al 10, Pitagórica y algoritmo</div>
      </div>

      <!-- Fase 4 -->
      <div class="phase-link-card f4">
        <div>
          <span class="phase-badge-tag" style="color: #0891B2;">Fase 4 • 3º a 5º Grado</span>
          <div class="phase-link-title">División y Relaciones</div>
          <a href="https://drive.google.com/file/d/1dedsRgaNXc8xYZgX46pGU8m8YFyZHwr8/view?usp=drivesdk&utm_source=gemini" target="_blank" class="drive-file-btn">
            <span class="file-icon">📄</span> Divisão 3º ao 5º ano.pdf
          </a>
        </div>
        <div style="font-size: 7.5pt; color: #64748B;">Clases 19 a 23 • Reparto, residuo y división larga</div>
      </div>

      <!-- Fase 5 -->
      <div class="phase-link-card f5">
        <div>
          <span class="phase-badge-tag" style="color: #DB2777;">Fase 5 • 4º y 5º Grado</span>
          <div class="phase-link-title">Fracciones y Racionales</div>
          <a href="https://drive.google.com/file/d/14GIh9jrptnUM02So3rHoheUkGdn7nX8j/view?usp=drivesdk&utm_source=gemini" target="_blank" class="drive-file-btn">
            <span class="file-icon">📄</span> Frações.pdf
          </a>
        </div>
        <div style="font-size: 7.5pt; color: #64748B;">Clases 24 a 27 • Parte-todo, recta numérica y equivalencias</div>
      </div>

      <!-- Fase 6 -->
      <div class="phase-link-card f6">
        <div>
          <span class="phase-badge-tag" style="color: #059669;">Fase 6 • 4º y 5º Grado</span>
          <div class="phase-link-title">Síntesis y Retos de las 4 Operaciones</div>
          <a href="https://drive.google.com/file/d/1jWkv1mWhsqbhZLmkJ7amIhKTNhY4sf-D/view?usp=drivesdk&utm_source=gemini" target="_blank" class="drive-file-btn">
            <span class="file-icon">📄</span> Situações-problema 4° e 5° ano.pdf
          </a>
        </div>
        <div style="font-size: 7.5pt; color: #64748B;">Clases 28 a 30 • Razonamiento en dos pasos y Desafío Final</div>
      </div>
    </div>

    <div class="instructions-box">
      <div>
        <strong>1. Clic para Descargar</strong>
        Haz clic sobre cualquiera de los botones para abrir el archivo en tu navegador.
      </div>
      <div>
        <strong>2. Guardar en tu Equipo</strong>
        Pulsa el icono de descarga dentro de Google Drive para tener copia local en PDF.
      </div>
      <div>
        <strong>3. Acceso Vitalicio</strong>
        Los enlaces permanecen activos las 24 horas y puedes guardarlos en tus favoritos.
      </div>
    </div>

    <div class="doc-footer">
      <span>Página 2 • Acceso a la Biblioteca Digital</span>
      <span><strong>Lecciones Kids</strong> • Matemáticas 1º a 5º Grado</span>
    </div>
  </div>

  <!-- =========================================================
       PAGE 3: FASE 1 (CLASES 01 A 07)
       ========================================================= -->
  <div class="page">
    <div class="doc-header">
      <div class="doc-header-logo">
        <img src="{logo_horiz}" alt="Logo">
      </div>
      <div class="doc-header-info">
        <div class="doc-header-title">Cronograma Pedagógico Detallado</div>
        <div class="doc-header-badge">Fase 1 • Alfabetización Numérica</div>
      </div>
    </div>

    <div class="phase-intro-header fase1">
      <div>
        <div class="phase-intro-title">Fase 1: Alfabetización Numérica y Primeros Descubrimientos</div>
        <div class="phase-intro-sub">1º Grado / Transición • Conteo, regularidades y nociones iniciales de cálculo</div>
      </div>
      <div class="phase-intro-badge">Clases 01 a 07</div>
    </div>

    <div class="class-cards-container">
      <!-- C01 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 01 – Del 1 al 20: Cantidad y Numerales</span>
            <span class="class-bncc-pill">EF01MA01</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Conteo de conjuntos hasta 20 y escritura numérica correspondiente.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Flashcards con dedos de las manos, dados y animales agrupados.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Unir numeral con cantidad y colorear grupos de elementos.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Conhecendo_os_números_e_sinais.pdf</div>
        </div>
      </div>

      <!-- C02 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 02 – El Camino hasta el 50 y Escritura en Palabras</span>
            <span class="class-bncc-pill">EF01MA01</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Recta numérica del 1 al 50, antecesor y sucesor numérico.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Pista de carreras con casillas numeradas y números faltantes.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Completar casillas en la pista y asociar numeral con su nombre escrito.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Matemática_1°_ano.pdf</div>
        </div>
      </div>

      <!-- C03 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 03 – El Tablero Numérico del 1 al 100</span>
            <span class="class-bncc-pill">EF01MA02</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Tabla 10x10, conteo de 10 en 10, regularidades y decenas exactas.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Cuadrícula 10x10 con decenas destacadas en tonos pastel contrastados.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Búsqueda de números ocultos y coloreado por patrones de columnas.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Matemática_1°_ano.pdf</div>
        </div>
      </div>

      <!-- C04 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 04 – Signos Matemáticos: ¿Mayor, Menor o Igual?</span>
            <span class="class-bncc-pill">EF01MA03</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Comparación de cantidades utilizando los signos =, &gt;, &lt;, ≠.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Personaje de la "boca del cocodrilo" que come al número mayor.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Colocar signos entre parejas de ilustraciones y números comparativos.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Conhecendo_os_números_e_sinais.pdf</div>
        </div>
      </div>

      <!-- C05 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 05 – Primeros Pasos de la Suma y la Resta</span>
            <span class="class-bncc-pill">EF01MA06</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Nociones de juntar y quitar; significado de los signos + y -.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Canastas de frutas con flechas ("llegaron más" y "se comieron").</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Operaciones horizontales con figuras de apoyo para tachar o sumar.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Situações-problema_1_Ano.pdf</div>
        </div>
      </div>

      <!-- C06 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 06 – Situaciones-Problema Ilustradas I: Juntar y Agregar</span>
            <span class="class-bncc-pill">EF01MA08</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Problemas cotidianos de juntar (juguetes, dulces, aves en el nido).</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Viñetas tipo historieta con personajes infantiles narrando el reto.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Lectura guiada, dibujo de las cantidades y respuesta numérica final.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Situações-problema_1_Ano.pdf</div>
        </div>
      </div>

      <!-- C07 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 07 – Situaciones-Problema Ilustradas II: Separar y Comparar</span>
            <span class="class-bncc-pill">EF01MA08</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Sustracción contextualizada ("¿cuántos quedaron?", diferencia).</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Estantes con objetos tachados con 'X' que representan los retirados.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Resolución gráfica con recuadro para dibujar el razonamiento infantil.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Situações-problema_1_Ano.pdf</div>
        </div>
      </div>
    </div>

    <div class="doc-footer">
      <span>Página 3 • Fase 1 (1º Grado)</span>
      <span><strong>Lecciones Kids</strong> • Cronograma Pedagógico 30 Clases</span>
    </div>
  </div>

  <!-- =========================================================
       PAGE 4: FASE 2 (CLASES 08 A 13)
       ========================================================= -->
  <div class="page">
    <div class="doc-header">
      <div class="doc-header-logo">
        <img src="{logo_horiz}" alt="Logo">
      </div>
      <div class="doc-header-info">
        <div class="doc-header-title">Cronograma Pedagógico Detallado</div>
        <div class="doc-header-badge">Fase 2 • Consolidación Decimal y CDU</div>
      </div>
    </div>

    <div class="phase-intro-header fase2">
      <div>
        <div class="phase-intro-title">Fase 2: Consolidación Decimal, CDU y Razonamiento Narrativo</div>
        <div class="phase-intro-sub">2º y 3º Grado • Valor posicional, algoritmos con reserva y estadística básica</div>
      </div>
      <div class="phase-intro-badge">Clases 08 a 13</div>
    </div>

    <div class="class-cards-container">
      <!-- C08 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 08 – El Castillo de la Centena, Decena y Unidad</span>
            <span class="class-bncc-pill">EF02MA04</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Descomposición numérica hasta 999 en C, D y U (245 = 200 + 40 + 5).</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Casitas de valor posicional y piezas del Material Base 10.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Descomponer números en sumandos y colorear placas, barras y cubos.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Adição_e_Subtração_2°_e_3°_ano.pdf</div>
        </div>
      </div>

      <!-- C09 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 09 – Adición en CDU con y sin Reagrupación</span>
            <span class="class-bncc-pill">EF02MA06 / EF03MA06</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Algoritmo de la suma en columnas CDU y regla de "llevar uno".</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Casillas verticales con círculo superior de reserva sobre las decenas.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> 8 sumas verticales con progresión de dificultad (2 y 3 dígitos).</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Adição_e_Subtração_2°_e_3°_ano.pdf</div>
        </div>
      </div>

      <!-- C10 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 10 – Sustracción en CDU con y sin Reagrupación</span>
            <span class="class-bncc-pill">EF02MA06 / EF03MA06</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Algoritmo de la resta vertical y "pedir prestado" al orden vecino.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Casillas con líneas tachadas para anotar la transformación de decenas.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Ejercicios prácticos de resta con casillas de verificación.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Adição_e_Subtração_2°_e_3°_ano.pdf</div>
        </div>
      </div>

      <!-- C11 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 11 – Estadística Básica: Gráficos de Barras y Tablas</span>
            <span class="class-bncc-pill">EF02MA22</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Lectura de tablas simples, recuento y completado de gráficos de barras.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Gráficos ilustrados de deportes, mascotas y frutas preferidas.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Responder preguntas sobre el más votado, menos votado y diferencias.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Situações-problema_2º_e_3º_ano.pdf</div>
        </div>
      </div>

      <!-- C12 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 12 – Desafíos: Búsqueda del Tesoro en el Parque</span>
            <span class="class-bncc-pill">EF02MA06</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Problemas encadenados en varios pasos para descifrar pistas.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Mapa ilustrado con caminos, cofres del tesoro y llaves numéricas.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Sumar y restar elementos recolectados por Pedro y Ana en el mapa.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Situações-problema_2º_e_3º_ano.pdf</div>
        </div>
      </div>

      <!-- C13 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 13 – Desafíos: El Picnic y la Fiesta en el Bosque</span>
            <span class="class-bncc-pill">EF03MA06</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Adición, sustracción y reparto intuitivo en eventos festivos.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Canastas de picnic, mantel cuadriculado y animalitos del bosque.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Resolver situaciones narrativas sobre cantidades totales y faltantes.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Situações-problema_2º_e_3º_ano.pdf</div>
        </div>
      </div>
    </div>

    <div class="doc-footer">
      <span>Página 4 • Fase 2 (2º y 3º Grado)</span>
      <span><strong>Lecciones Kids</strong> • Cronograma Pedagógico 30 Clases</span>
    </div>
  </div>

  <!-- =========================================================
       PAGE 5: FASE 3 (CLASES 14 A 18)
       ========================================================= -->
  <div class="page">
    <div class="doc-header">
      <div class="doc-header-logo">
        <img src="{logo_horiz}" alt="Logo">
      </div>
      <div class="doc-header-info">
        <div class="doc-header-title">Cronograma Pedagógico Detallado</div>
        <div class="doc-header-badge">Fase 3 • Multiplicación y Tablas</div>
      </div>
    </div>

    <div class="phase-intro-header fase3">
      <div>
        <div class="phase-intro-title">Fase 3: Multiplicación, Patrones y Tablas</div>
        <div class="phase-intro-sub">2º a 5º Grado • Suma repetida, tablas 1 al 10, disposición rectangular y algoritmo</div>
      </div>
      <div class="phase-intro-badge">Clases 14 a 18</div>
    </div>

    <div class="class-cards-container">
      <!-- C14 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 14 – ¿Qué es Multiplicar? Sumandos Iguales y Doble</span>
            <span class="class-bncc-pill">EF02MA07</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Convertir sumas repetidas (2 + 2 + 2 = 6) en multiplicaciones (3 x 2 = 6).</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Cajas de huevos, pares de zapatos y ruedas de bicicleta agrupadas.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Reescribir sumas largas en multiplicaciones abreviadas y resolver.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Multiplicação_2°_e_5°_ano.pdf</div>
        </div>
      </div>

      <!-- C15 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 15 – Dominando las Tablas: Del 1 al 5 y Neutro</span>
            <span class="class-bncc-pill">EF03MA07</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Tablas del 1 (elemento neutro), 2 (doble), 3, 4 y 5 (terminación 0 y 5).</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Tableros verticales con código de colores y resultados destacados.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Completar ruedas de multiplicación y retos de cálculo mental rápido.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Mural_da_tabuada.pdf</div>
        </div>
      </div>

      <!-- C16 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 16 – Tablas del 6 al 10 y Propiedad Conmutativa</span>
            <span class="class-bncc-pill">EF03MA07</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Tablas del 6 al 10, regla del cero y conmutatividad (6 x 4 = 4 x 6).</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Tabla Pitagórica (cuadrícula 10x10) con patrones diagonales.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Llenado de la Tabla Pitagórica e identificación de regularidades.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Mural_da_tabuada.pdf</div>
        </div>
      </div>

      <!-- C17 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 17 – Disposición Rectangular y Proporcionalidad</span>
            <span class="class-bncc-pill">EF04MA06</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Organización en Filas x Columnas (asientos de cine, baldosas, chocolates).</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Cuadrículas coloreadas destacando áreas rectangulares base x altura.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Calcular el total sin contar uno a uno multiplicando filas por columnas.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Multiplicação_2°_e_5°_ano.pdf</div>
        </div>
      </div>

      <!-- C18 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 18 – El Algoritmo Estándar de la Multiplicación</span>
            <span class="class-bncc-pill">EF04MA06 / EF05MA08</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Multiplicación vertical de 2 y 3 dígitos por 1 y 2 cifras con llevada.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Cuentas alineadas con flechas que guían unidades y luego decenas.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Resolución de cuentas verticales y problemas prácticos de compras.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Multiplicação_2°_e_5°_ano.pdf</div>
        </div>
      </div>
    </div>

    <div class="doc-footer">
      <span>Página 5 • Fase 3 (2º a 5º Grado)</span>
      <span><strong>Lecciones Kids</strong> • Cronograma Pedagógico 30 Clases</span>
    </div>
  </div>

  <!-- =========================================================
       PAGE 6: FASE 4 (CLASES 19 A 23)
       ========================================================= -->
  <div class="page">
    <div class="doc-header">
      <div class="doc-header-logo">
        <img src="{logo_horiz}" alt="Logo">
      </div>
      <div class="doc-header-info">
        <div class="doc-header-title">Cronograma Pedagógico Detallado</div>
        <div class="doc-header-badge">Fase 4 • División y Operaciones</div>
      </div>
    </div>

    <div class="phase-intro-header fase4">
      <div>
        <div class="phase-intro-title">Fase 4: División y Relaciones Operatorias</div>
        <div class="phase-intro-sub">3º a 5º Grado • Reparto equitativo, operación inversa, residuo y método de la casilla</div>
      </div>
      <div class="phase-intro-badge">Clases 19 a 23</div>
    </div>

    <div class="class-cards-container">
      <!-- C19 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 19 – Concepto de Dividir: Reparto Equitativo y Medida</span>
            <span class="class-bncc-pill">EF03MA08</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Repartir en partes iguales y determinar cuántos grupos caben en un total.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Monedas en alcancías y figuritas distribuidas en sobres iguales.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Encerrar grupos iguales y formular la división (Total ÷ Grupos = Cantidad).</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Divisão_3º_ao_5º_ano.pdf</div>
        </div>
      </div>

      <!-- C20 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 20 – División Exacta y Relación Inversa</span>
            <span class="class-bncc-pill">EF03MA08</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Operaciones inversas: "Si 4 x 5 = 20, entonces 20 ÷ 5 = 4".</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Triángulos de familias operativas relacionando 3 números clave.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Crucigramas y esquemas conectando multiplicaciones y divisiones.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Divisão_3º_ao_5º_ano.pdf</div>
        </div>
      </div>

      <!-- C21 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 21 – Cuando Sobra: Entendiendo el Residuo</span>
            <span class="class-bncc-pill">EF04MA07</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Dividendo, Divisor, Cociente y Residuo; propiedad: Residuo &lt; Divisor.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Conjuntos cerrados con sobrantes ubicados fuera de los círculos.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Identificar cociente y residuo visual y numéricamente en ejercicios prácticos.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Divisão_3º_ao_5º_ano.pdf</div>
        </div>
      </div>

      <!-- C22 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 22 – Algoritmo de la División Larga (Casilla)</span>
            <span class="class-bncc-pill">EF04MA07</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Secuencia del algoritmo tradicional: Estimar, Multiplicar, Restar y Bajar.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Cajas de algoritmo esquematizadas en 4 pasos con código de color.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Resolver divisiones de 2 y 3 cifras entre 1 dígito paso a paso.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Divisão_3º_ao_5º_ano.pdf</div>
        </div>
      </div>

      <!-- C23 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 23 – División Avanzada: Divisores de 2 Dígitos</span>
            <span class="class-bncc-pill">EF05MA08</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Divisores como 12, 15, 20 y 25 mediante estimación con múltiplos.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Espacio lateral reservado para la tabla auxiliar de apoyo del divisor.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Problemas de embalaje, almacenamiento de cajas y reparto escolar.</div>
          <div class="class-desc-item"><strong>Material de Referencia:</strong> Divisão_3º_ao_5º_ano.pdf</div>
        </div>
      </div>
    </div>

    <div class="doc-footer">
      <span>Página 6 • Fase 4 (3º a 5º Grado)</span>
      <span><strong>Lecciones Kids</strong> • Cronograma Pedagógico 30 Clases</span>
    </div>
  </div>

  <!-- =========================================================
       PAGE 7: FASE 5 & 6 (CLASES 24 A 30)
       ========================================================= -->
  <div class="page">
    <div class="doc-header">
      <div class="doc-header-logo">
        <img src="{logo_horiz}" alt="Logo">
      </div>
      <div class="doc-header-info">
        <div class="doc-header-title">Cronograma Pedagógico Detallado</div>
        <div class="doc-header-badge">Fases 5 y 6 • Fracciones y Síntesis</div>
      </div>
    </div>

    <div class="phase-intro-header fase5" style="margin-bottom: 6px;">
      <div>
        <div class="phase-intro-title">Fase 5: Números Racionales – Fracciones (4º y 5º Grado)</div>
        <div class="phase-intro-sub">Parte-todo, numerador/denominador, recta numérica y equivalencias</div>
      </div>
      <div class="phase-intro-badge">Clases 24 a 27</div>
    </div>

    <div class="class-cards-container" style="gap: 5px;">
      <!-- C24 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 24 – ¿Qué es una Fracción? Concepto de Parte-Todo</span>
            <span class="class-bncc-pill">EF04MA09</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> División de la unidad en partes exactamente iguales; 1/2, 1/3, 1/4.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Barras de chocolate y pizzas seccionadas en porciones iguales.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Pintar partes indicadas y verificar partes iguales vs desiguales.</div>
          <div class="class-desc-item"><strong>Material:</strong> Frações.pdf</div>
        </div>
      </div>

      <!-- C25 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 25 – El Lenguaje Fraccionario: Numerador y Denominador</span>
            <span class="class-bncc-pill">EF04MA09</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Nomenclatura (medio, tercio, cuarto) y lectura formal de fracciones.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Infografía con flechas diferenciando numerador y denominador.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Escribir fracciones en palabras y números a partir de figuras gráficas.</div>
          <div class="class-desc-item"><strong>Material:</strong> Frações.pdf</div>
        </div>
      </div>

      <!-- C26 & C27 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clases 26 y 27 – Recta Numérica y Fracciones Equivalentes</span>
            <span class="class-bncc-pill">EF05MA04 / EF05MA05</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Ubicar fracciones entre 0 y 1; equivalencias (1/2 = 2/4 = 4/8).</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Regla ampliada con marcas y muro de tiras fraccionarias apiladas.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Marcar puntos en la recta y comparar ingredientes en recetas de cocina.</div>
          <div class="class-desc-item"><strong>Material:</strong> Frações.pdf</div>
        </div>
      </div>
    </div>

    <!-- FASE 6 -->
    <div class="phase-intro-header fase6" style="margin-top: 8px; margin-bottom: 6px;">
      <div>
        <div class="phase-intro-title">Fase 6: Síntesis y Desafíos Integrados (4º y 5º Grado)</div>
        <div class="phase-intro-sub">Problemas de varios pasos, integración de operaciones y evaluación formativa</div>
      </div>
      <div class="phase-intro-badge">Clases 28 a 30</div>
    </div>

    <div class="class-cards-container" style="gap: 5px;">
      <!-- C28 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 28 – Problemas en Dos Pasos: Suma, Resta y Multiplicación</span>
            <span class="class-bncc-pill">EF04MA06 / EF05MA08</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Operación intermedia requerida antes de responder la pregunta principal.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Diagrama de flujo en 2 etapas ("Paso 1: Total" ➔ "Paso 2: Gasto").</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Resolver situaciones de presupuestos de compras y paseos escolares.</div>
          <div class="class-desc-item"><strong>Material:</strong> Situações-problema_4°_e_5°_ano.pdf</div>
        </div>
      </div>

      <!-- C29 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 29 – Desafíos Integrando División y Fracciones</span>
            <span class="class-bncc-pill">EF05MA08</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Fracción de una cantidad (1/3 de 60 estudiantes) y reparto proporcional.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Cuadros organizadores de datos con casillas para ordenar el cálculo.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> Situaciones de economía familiar, cosechas e inventarios de tienda.</div>
          <div class="class-desc-item"><strong>Material:</strong> Situações-problema_4°_e_5°_ano.pdf</div>
        </div>
      </div>

      <!-- C30 -->
      <div class="class-card">
        <div>
          <div class="class-card-header">
            <span class="class-number-title">Clase 30 – El Gran Desafío Matemático: Diagnóstico y Maestría</span>
            <span class="class-bncc-pill">EF05MA08</span>
          </div>
          <div class="class-desc-item"><strong>Contenido:</strong> Repaso integral de las 4 operaciones y fracciones en misiones globales.</div>
          <div class="class-desc-item"><strong>Elementos Visuales:</strong> Formato de "Pasaporte de Habilidades Matemáticas" con sellos coleccionables.</div>
        </div>
        <div>
          <div class="class-desc-item"><strong>Actividad:</strong> 5 misiones evaluativas con diploma final de Maestro Matemático Kids.</div>
          <div class="class-desc-item"><strong>Material:</strong> Solucionario y Cuaderno Maestro</div>
        </div>
      </div>
    </div>

    <div class="doc-footer">
      <span>Página 7 • Fases 5 y 6 (4º y 5º Grado)</span>
      <span><strong>Lecciones Kids</strong> • Cronograma Pedagógico 30 Clases</span>
    </div>
  </div>

  <!-- =========================================================
       PAGE 8: FICHA MODELO DIDÁCTICA (CLASE 01)
       ========================================================= -->
  <div class="page">
    <div class="worksheet-wrap">
      <!-- HEADER -->
      <div class="ws-header">
        <div class="ws-header-top">
          <div class="ws-brand">
            Lecciones Kids <span>★ Ficha Didáctica Imprimible</span>
          </div>
          <div class="ws-bncc">BNCC EF01MA01</div>
        </div>
        <div class="ws-fields">
          <div>Estudiante: <span class="ws-line" style="width: 68%;"></span></div>
          <div>Fecha: <span class="ws-line" style="width: 50%;"></span></div>
          <div>Grado: <span class="ws-line" style="width: 45%;"></span></div>
        </div>
      </div>

      <!-- CONCEPT -->
      <div class="ws-concept">
        <div>
          <div class="ws-concept-tag">Clase 01 • 1º Grado / Transición</div>
          <div class="ws-concept-title">Del 1 al 20: Conteo y Relación Número-Objeto</div>
          <p class="ws-concept-p">
            <strong>¡Aprende Rápido!</strong> Cada número representa una cantidad fija de objetos. Al contar, señalamos cada elemento con el dedo una sola vez hasta llegar al total.
          </p>
        </div>
        <div style="background: #FFFFFF; border: 1.5px solid #FDE68A; border-radius: 8px; padding: 5px; text-align: center;">
          <div style="font-size: 8pt; font-weight: 800; color: #D97706;">EJEMPLO GUIADO</div>
          <div style="font-size: 15pt; margin: 2px 0;">🖐️ 🖐️ ➔ <strong style="color: #2563EB;">10</strong></div>
          <div style="font-size: 7.5pt; color: #4B5563;">10 dedos = Numeral 10</div>
        </div>
      </div>

      <!-- PRACTICE 1 -->
      <div class="ws-practice-title">
        <span>1. ¡Vamos a Practicar Juntos! Cuenta los elementos y escribe el número:</span>
      </div>

      <div class="ws-practice-grid">
        <div class="ws-task-card">
          <div class="ws-task-top"><span>A. Manzanas en la cesta</span><span>🍎</span></div>
          <div class="ws-items-box">🍎 🍎 🍎 🍎 🍎 🍎 🍎 🍎</div>
          <div class="ws-ans-row"><span>Total:</span><div class="ws-input-box"></div></div>
        </div>
        <div class="ws-task-card">
          <div class="ws-task-top"><span>B. Estrellas brillantes</span><span>⭐</span></div>
          <div class="ws-items-box">⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐</div>
          <div class="ws-ans-row"><span>Total:</span><div class="ws-input-box"></div></div>
        </div>
        <div class="ws-task-card">
          <div class="ws-task-top"><span>C. Fichas de juego</span><span>🔵</span></div>
          <div class="ws-items-box">🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵</div>
          <div class="ws-ans-row"><span>Total:</span><div class="ws-input-box"></div></div>
        </div>
        <div class="ws-task-card">
          <div class="ws-task-top"><span>D. Lápices escolares</span><span>✏️</span></div>
          <div class="ws-items-box">✏️ ✏️ ✏️ ✏️ ✏️ ✏️ ✏️</div>
          <div class="ws-ans-row"><span>Total:</span><div class="ws-input-box"></div></div>
        </div>
      </div>

      <!-- PRACTICE 2 -->
      <div class="ws-match-box">
        <div style="font-size: 9.5pt; font-weight: 800; color: #334155;">2. Traza una línea recta para unir cada grupo con su numeral:</div>
        <div class="ws-match-grid">
          <div class="ws-match-col">
            <div style="font-size: 11pt;">🚗 🚗 🚗 🚗</div>
            <span style="color: #64748B;">4 autos</span>
            <div class="ws-match-num">9</div>
          </div>
          <div class="ws-match-col">
            <div style="font-size: 11pt;">🎈 🎈 🎈 🎈 🎈 🎈</div>
            <span style="color: #64748B;">6 globos</span>
            <div class="ws-match-num">4</div>
          </div>
          <div class="ws-match-col">
            <div style="font-size: 11pt;">⚽ ⚽ ⚽ ⚽ ⚽ ⚽ ⚽ ⚽ ⚽</div>
            <span style="color: #64748B;">9 pelotas</span>
            <div class="ws-match-num">14</div>
          </div>
          <div class="ws-match-col">
            <div style="font-size: 10pt;">🐟 🐟 🐟 🐟 🐟 🐟 🐟 🐟 🐟 🐟 🐟 🐟 🐟 🐟</div>
            <span style="color: #64748B;">14 peces</span>
            <div class="ws-match-num">6</div>
          </div>
        </div>
      </div>

      <!-- STORY PROBLEM -->
      <div class="ws-problem">
        <div class="ws-problem-title">🚀 Reto de Lucas y su Colección:</div>
        <p class="ws-problem-text">
          Lucas tenía <strong>11</strong> botones en su frasco. En el recreo, su amigo Mateo le regaló <strong>4</strong> botones más. ¿Cuántos botones tiene Lucas en total?
        </p>
        <div class="ws-problem-cols">
          <div class="ws-drawing-area">Dibuja aquí tus botones o marcas para contar</div>
          <div class="ws-answer-calc">
            <div>11 + 4 = <span style="display:inline-block; border-bottom:1.5px solid #059669; width:30px;"></span></div>
            <div style="margin-top:2px;">Respuesta: <span style="display:inline-block; border-bottom:1.5px solid #059669; width:30px;"></span> botones.</div>
          </div>
        </div>
      </div>

      <!-- FOOTER -->
      <div class="doc-footer" style="margin-top: auto;">
        <span>Lecciones Kids © Ficha de Clase Modelo • Imprimible A4</span>
        <span>Clase 01 de 30 • Alfabetización Numérica</span>
      </div>
    </div>
  </div>

</body>
</html>
"""
    html_path = os.path.join(base_dir, "cronograma_30_clases.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML generated at: {html_path}")
    return html_path

def compile_pdf(html_path):
    base_dir = r"d:\dev\LECCIONES KIDS"
    pdf_path = os.path.join(base_dir, "Cronograma_Pedagogico_30_Clases.pdf")
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    print("Compiling PDF with Chrome headless...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(pdf_path):
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"PDF successfully generated: {pdf_path} ({size_kb:.1f} KB)")
        
        # Render previews if pdfium is available
        if pdfium:
            doc = pdfium.PdfDocument(pdf_path)
            print(f"Total pages rendered: {len(doc)}")
            for idx in range(len(doc)):
                page = doc[idx]
                bitmap = page.render(scale=1.5)
                pil_img = bitmap.to_pil()
                preview_file = os.path.join(base_dir, f"preview_cronograma_p{idx+1}.png")
                pil_img.save(preview_file)
            doc.close()
            print("Previews saved successfully.")
        return pdf_path
    else:
        print(f"Error compiling PDF: {res.stderr}")
        return None

if __name__ == "__main__":
    h = generate_html()
    compile_pdf(h)
