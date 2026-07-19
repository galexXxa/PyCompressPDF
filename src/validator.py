import fitz
import hashlib
import os

def sha256(file_path):
    h = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()

def validate_pdf(original_pdf, optimized_pdf):
    result = {
        "status": True,
        "errors": []
    }

    try:
        original = fitz.open(original_pdf)
        optimized = fitz.open(optimized_pdf)

    except Exception as e:
        result["status"] = False
        result["errors"].append(str(e))

        return result

    # ==========================
    # Pages
    # ==========================

    result["original_pages"] = len(original)
    result["optimized_pages"] = len(optimized)

    if len(original) != len(optimized):
        result["status"] = False
        result["errors"].append(
            "Page count mismatch"
        )

    # ==========================
    # Text Layer
    # ==========================

    original_text = ""
    optimized_text = ""

    for page in original:
        original_text += page.get_text()

    for page in optimized:
        optimized_text += page.get_text()

    result["original_text"] = len(original_text)
    result["optimized_text"] = len(optimized_text)

    if len(optimized_text) < len(original_text) * 0.95:
        result["status"] = False
        result["errors"].append(
            "Text layer reduced significantly"
        )

    # ==========================
    # Images
    # ==========================

    original_images = 0
    optimized_images = 0

    for page in original:
        original_images += len(
            page.get_images(full=True)
        )

    for page in optimized:
        optimized_images += len(
            page.get_images(full=True)
        )

    result["original_images"] = original_images
    result["optimized_images"] = optimized_images

    # ==========================
    # Fonts
    # ==========================

    def get_fonts(doc):
        fonts = set()

        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        fonts.add(
                            span["font"]
                        )

        return fonts

    fonts_original = get_fonts(original)
    fonts_optimized = get_fonts(optimized)

    result["original_fonts"] = len(fonts_original)
    result["optimized_fonts"] = len(fonts_optimized)

    # ==========================
    # SHA
    # ==========================

    result["original_sha"] = sha256(original_pdf)
    result["optimized_sha"] = sha256(optimized_pdf)

    result["original_size"] = os.path.getsize(original_pdf)
    result["optimized_size"] = os.path.getsize(optimized_pdf)

    original.close()
    optimized.close()

    return result