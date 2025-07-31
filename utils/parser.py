# utils/parser.py
import os
import tempfile
from pathlib import Path

import pdfplumber
from docx import Document


def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = Path(tmp.name)

    if file_type == "pdf":
        return extract_text_from_pdf(tmp_path)
    elif file_type == "docx":
        return extract_text_from_docx(tmp_path)
    elif file_type == "txt":
        return tmp_path.read_text(encoding="utf-8", errors="ignore")
    else:
        return "Unsupported file format."


def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])
