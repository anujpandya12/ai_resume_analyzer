


import os
import docx
import pdfplumber
import pytesseract

from pdf2image import convert_from_path


# WINDOWS TESSERACT PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf(filepath):

    text = ""

    try:

        # First Try Normal Extraction
        with pdfplumber.open(filepath) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted + "\n"

        # If Empty → OCR
        if text.strip() == "":

            images = convert_from_path(filepath)

            for image in images:

                text += pytesseract.image_to_string(image)

    except Exception as e:

        text = f"PDF Error: {str(e)}"

    return text


def extract_text_from_docx(filepath):

    text = ""

    try:

        doc = docx.Document(filepath)

        for para in doc.paragraphs:

            text += para.text + "\n"

    except Exception as e:

        text = f"DOCX Error: {str(e)}"

    return text


def extract_text_from_file(filepath):

    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".pdf":

        return extract_text_from_pdf(filepath)

    elif extension == ".docx":

        return extract_text_from_docx(filepath)

    else:

        return "Unsupported File Format"