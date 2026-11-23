

import io

from pypdf import PdfReader
from docx import Document


def _get_file_bytes(file):
    """Return raw bytes from a Streamlit upload, a file object, or a path."""
    if hasattr(file, "getvalue"):          # Streamlit UploadedFile
        return file.getvalue()

    if hasattr(file, "read"):              # Any other file-like object
        try:
            file.seek(0)
        except Exception:
            pass
        return file.read()

    with open(file, "rb") as f:            # A normal file path
        return f.read()


def _get_file_name(file):
    return str(getattr(file, "name", file)).lower()


def extract_text_from_pdf(file):
    data = _get_file_bytes(file)
    reader = PdfReader(io.BytesIO(data))

    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception:
            raise ValueError("This PDF is password-protected. Please upload an unlocked copy.")

    pages = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            pages.append(page_text)

    return "\n".join(pages).strip()


def extract_text_from_docx(file):
    data = _get_file_bytes(file)
    document = Document(io.BytesIO(data))

    lines = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            lines.append(paragraph.text)

    for table in document.tables:
        for row in table.rows:
            cells = []
            for cell in row.cells:
                cell_text = cell.text.strip()
                if cell_text and cell_text not in cells:   # skip merged-cell duplicates
                    cells.append(cell_text)
            if cells:
                lines.append(" | ".join(cells))

    return "\n".join(lines).strip()


def extract_resume_text(file):
    """
    Extract text from an uploaded resume.

    Returns the extracted text (empty string if nothing readable was found).
    Raises ValueError / Exception on problems, so the app can show a real
    error instead of treating an error message as resume content.
    """
    name = _get_file_name(file)

    if name.endswith(".pdf"):
        return extract_text_from_pdf(file)

    if name.endswith(".docx"):
        return extract_text_from_docx(file)

    raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")
