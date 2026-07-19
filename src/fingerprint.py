import os
import hashlib
import fitz
import pikepdf

class PDFFingerprint:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    # ---------------------
    # HASH
    # ---------------------

    def sha256(self):
        h = hashlib.sha256()
        with open(self.pdf_path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                h.update(chunk)

        return h.hexdigest()

    def md5(self):
        h = hashlib.md5()
        with open(self.pdf_path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                h.update(chunk)

        return h.hexdigest()

    # ---------------------
    # PDF
    # ---------------------

    def analyze(self):
        fitz_doc = fitz.open(self.pdf_path)
        pike_doc = pikepdf.open(self.pdf_path)
        metadata = fitz_doc.metadata
        fonts = set()
        images = 0
        drawings = 0
        text = 0

        for page in fitz_doc:
            images += len(
                page.get_images(full=True)
            )
            drawings += len(
                page.get_drawings()
            )
            text += len(
                page.get_text()
            )
            blocks = page.get_text("dict")["blocks"]

            for block in blocks:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        fonts.add(
                            span["font"]
                        )

        structure = get_pdf_structure(
            self.pdf_path
        )

        result = {
            "file":
            os.path.basename(self.pdf_path),
            "size":
            os.path.getsize(self.pdf_path),
            "pages":
            len(fitz_doc),
            "images":
            images,
            "drawings":
            drawings,
            "text":
            text,
            "fonts":
            sorted(fonts),
            "font_count":
            len(fonts),
            "creator":
            metadata.get("creator"),
            "producer":
            metadata.get("producer"),
            "title":
            metadata.get("title"),
            "author":
            metadata.get("author"),
            "subject":
            metadata.get("subject"),
            "keywords":
            metadata.get("keywords"),
            "pdf_version":
            str(pike_doc.pdf_version),
            "encrypted":
            pike_doc.is_encrypted,
            "allow":
            str(pike_doc.allow),
            "sha256":
            self.sha256(),
            "md5":
            self.md5()
        }

        fitz_doc.close()
        pike_doc.close()
        result.update(
            structure
        )

        return result

def compare_fingerprint(before, after):
    report = {}

    for key in before.keys():
        report[key] = {
            "before": before[key],
            "after": after[key],
            "changed": before[key] != after[key]
        }

    return report

def get_pdf_structure(pdf_path):
    with pikepdf.open(pdf_path) as pdf:
        info = {}
        info["object_count"] = len(pdf.objects)
        info["pdf_version"] = pdf.pdf_version
        info["trailer_id"] = None

        if "/ID" in pdf.trailer:
            info["trailer_id"] = str(
                pdf.trailer["/ID"]
            )

        info["has_xmp"] = (
            pdf.open_metadata()
            is not None
        )

        return info