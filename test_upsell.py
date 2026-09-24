import os
from playwright.sync_api import sync_playwright

def test_upsell():
    base_dir = r"d:\dev\LECCIONES KIDS"
    html_path = os.path.join(base_dir, "upsell.html")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # Desktop preview
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(f"file:///{html_path.replace(os.sep, '/')}")
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        
        desktop_img = os.path.join(base_dir, "preview_upsell_desktop.png")
        page.screenshot(path=desktop_img, full_page=True)
        print(f"Desktop screenshot saved: {desktop_img}")
        
        # Mobile preview (iPhone 14 style)
        page_mobile = browser.new_page(viewport={"width": 390, "height": 844})
        page_mobile.goto(f"file:///{html_path.replace(os.sep, '/')}")
        page_mobile.wait_for_load_state("networkidle")
        page_mobile.evaluate("document.fonts.ready")
        
        mobile_img = os.path.join(base_dir, "preview_upsell_mobile.png")
        page_mobile.screenshot(path=mobile_img, full_page=True)
        print(f"Mobile screenshot saved: {mobile_img}")
        
        browser.close()

if __name__ == "__main__":
    test_upsell()
