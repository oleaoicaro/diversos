#!/usr/bin/env python3
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "profile.yaml"
TEMPLATES = ROOT / "templates"
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)


def build(lang):
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=False)
    tpl = env.get_template(f"executive_{lang}.html")
    html = tpl.render(cv=data[lang])
    html_path = OUTPUT / f"Icaro_Leao_CV_{lang.upper()}.html"
    html_path.write_text(html, encoding="utf-8")
    print(f"[OK] HTML gerado: {html_path}")
    pdf_path = OUTPUT / f"Icaro_Leao_CV_{lang.upper()}.pdf"
    try:
        from weasyprint import HTML
        HTML(string=html, base_url=str(TEMPLATES)).write_pdf(str(pdf_path))
        print(f"[OK] PDF gerado via WeasyPrint: {pdf_path}")
        return
    except Exception as e:
        print(f"[WARN] WeasyPrint falhou para {lang}: {e}")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{html_path.resolve()}")
            page.pdf(
                path=str(pdf_path),
                format="A4",
                margin={"top": "18mm", "bottom": "22mm", "left": "20mm", "right": "20mm"},
                print_background=True,
            )
            browser.close()
        print(f"[OK] PDF gerado via Playwright: {pdf_path}")
        return
    except Exception as e:
        print(f"[WARN] Playwright falhou para {lang}: {e}")
    print(f"[INFO] PDF não gerado para {lang}. Abra o HTML no Chrome e use Ctrl+P → PDF A4.")


if __name__ == "__main__":
    for lg in ("pt", "en"):
        build(lg)
