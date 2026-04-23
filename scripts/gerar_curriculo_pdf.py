"""Gera curriculo.pdf a partir do HTML do currículo para alimentar o ai-job-agent."""
from pathlib import Path

from weasyprint import HTML

HTML_INPUT = Path(__file__).parent.parent / "cv" / "output" / "Icaro_Leao_CV_PT.html"
PDF_OUTPUT = Path(__file__).parent.parent / "curriculo.pdf"


def main():
    if not HTML_INPUT.exists():
        raise FileNotFoundError(
            f"Arquivo HTML não encontrado: {HTML_INPUT}\n"
            "Execute 'python cv/scripts/build_cv.py' para gerar o HTML antes de converter para PDF."
        )
    HTML(str(HTML_INPUT), base_url=str(HTML_INPUT.parent) + "/").write_pdf(str(PDF_OUTPUT))
    print(f"Gerado: {PDF_OUTPUT}")


if __name__ == "__main__":
    main()
