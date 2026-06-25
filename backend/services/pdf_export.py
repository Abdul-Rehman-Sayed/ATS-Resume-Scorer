import io
import logging

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_INSTALLED = True
except (ImportError, OSError) as _exc:
    WEASYPRINT_INSTALLED = False
    _WEASYPRINT_IMPORT_ERROR = _exc

logger = logging.getLogger('ats_resume_scorer')

def generate_combined_pdf(html_docs: dict[str, str]) -> bytes:
    if not WEASYPRINT_INSTALLED:
        raise RuntimeError(
            "PDF generation is unavailable because WeasyPrint's system libraries "
            "(GTK/Pango) are not installed on this server. "
            f"Original error: {_WEASYPRINT_IMPORT_ERROR}"
        )

    if not html_docs:
        raise ValueError("No HTML documents provided to render into a PDF.")

    documents = []

    for name, html_str in html_docs.items():
        doc = HTML(string=html_str).render()
        documents.append(doc)

    first_doc = documents[0]
    for other_doc in documents[1:]:
        for page in other_doc.pages:
            first_doc.pages.append(page)
            
    pdf_bytes = first_doc.write_pdf()
    return pdf_bytes
