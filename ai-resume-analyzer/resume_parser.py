# resume_parser.py

import PyPDF2

def extract_text_from_pdf(uploaded_file):
    text = ""

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    return text
