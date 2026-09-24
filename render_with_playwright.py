import os
from playwright.sync_api import sync_playwright

def render():
    base_dir = r"d:\dev\LECCIONES KIDS"
    html_file = os.path.join(base_dir, "cronograma_30_clases.html")
    pdf_out = os.path.join(base_dir, "Cronograma_Pedagogico_30_Clases.pdf")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 1600})
        page.goto(f"file:///{html_file.replace(os.sep, '/')}")
        
        # Wait for web fonts and network idle
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        
        # Take screenshot of each .page div
        pages = page.query_selector_all(".page")
        print(f"Found {len(pages)} pages in HTML.")
        for idx, p_el in enumerate(pages):
            out_img = os.path.join(base_dir, f"preview_cronograma_p{idx+1}.png")
            p_el.screenshot(path=out_img)
            print(f"Saved: {out_img}")
            
        # Export pixel-perfect print PDF
        page.pdf(
            path=pdf_out,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True
        )
        print(f"Generated PDF via Playwright: {pdf_out} ({os.path.getsize(pdf_out)/1024:.1f} KB)")
        browser.close()

if __name__ == "__main__":
    render()
