import fitz
import re
import os

def slugify(text):
    # lowercase
    text = text.lower()

    # hapus karakter bukan huruf angka
    text = re.sub(
        r'[^a-z0-9\s-]',
        '',
        text
    )

    # spasi menjadi -
    text = re.sub(
        r'\s+',
        '-',
        text
    )

    # hapus dash ganda
    text = re.sub(
        r'-+',
        '-',
        text
    )

    return text.strip('-')

def generate_filename(pdf_path):
    doc = fitz.open(pdf_path)
    metadata = doc.metadata
    doc.close()

    title = metadata.get(
        "title",
        ""
    )

    if not title:
        title = os.path.splitext(
            os.path.basename(pdf_path)
        )[0]

    filename = slugify(
        title
    )

    return filename + ".pdf"