#!/usr/bin/env python3
"""Build CV PDFs (HTML→PDF) via WeasyPrint with Playwright fallback."""
import logging
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "profile.yaml"
TEMPLATES = ROOT / "templates"
FONTS_DIR = TEMPLATES / "styles" / "fonts"
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)


def log_fonts():
    """Log which font files are present."""
    if FONTS_DIR.exists():
        fonts = sorted(FONTS_DIR.glob("*"))
        if fonts:
            log.info("Fonts directory: %s", FONTS_DIR)
            for f in fonts:
                log.info("  font: %s (%d KB)", f.name, f.stat().st_size // 1024)
        else:
            log.warning("Fonts directory is empty — using system fonts only")
    else:
        log.warning("Fonts directory not found — using system fonts only")


def build(lang: str) -> None:
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=False)
    tpl = env.get_template(f"executive_{lang}.html")
    html = tpl.render(cv=data[lang])

    html_path = OUTPUT / f"Icaro_Leao_CV_{lang.upper()}.html"
    html_path.write_text(html, encoding="utf-8")
    log.info("HTML generated: %s", html_path)

    pdf_path = OUTPUT / f"Icaro_Leao_CV_{lang.upper()}.pdf"

    # Primary: WeasyPrint — base_url must point at TEMPLATES so relative
    # paths like styles/executive.css and styles/fonts/… resolve correctly.
    try:
        import weasyprint
        log.info("WeasyPrint version: %s", weasyprint.__version__)
        from weasyprint import HTML
        HTML(string=html, base_url=str(TEMPLATES) + "/").write_pdf(str(pdf_path))
        log.info("PDF generated via WeasyPrint: %s", pdf_path)
        return
    except Exception as exc:
        log.warning("WeasyPrint failed for %s: %s", lang, exc)

    # Fallback: Playwright (Chromium)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{html_path.resolve()}")
            page.pdf(
                path=str(pdf_path),
                format="A4",
                margin={"top": "16mm", "bottom": "18mm", "left": "18mm", "right": "18mm"},
                print_background=True,
            )
            browser.close()
        log.info("PDF generated via Playwright: %s", pdf_path)
        return
    except Exception as exc:
        log.warning("Playwright failed for %s: %s", lang, exc)

    log.error(
        "PDF not generated for %s. Open the HTML in Chrome and use Ctrl+P → Save as PDF (A4).",
        lang,
    )


if __name__ == "__main__":
    log_fonts()
    for lg in ("pt", "en"):
        build(lg)
