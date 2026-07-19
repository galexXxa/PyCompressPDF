import fitz
import os
from src.logger import debug, success, error

def rebuild_with_mupdf(
    input_pdf,
    output_pdf,
    clean=True
):
    
    debug("Input:")
    debug(input_pdf)

    try:
        doc = fitz.open(input_pdf)
    except Exception as e:
        return {
            "success": False,
            "error": f"Gagal membuka PDF: {e}"
        }

    debug(f"Pages: {len(doc)}")

    # ==========================
    # SCRUB (opsional)
    # ==========================

    if clean:
        try:
            print("Cleaning objects tak digunakan...")

            doc.scrub(
                attached_files=True,
                clean_pages=True,
                embedded_files=True,
                hidden_text=True,
                metadata=True,
                xml_metadata=True
            )

        except Exception as e:
            print(f"[WARNING] Scrub gagal: {e}")
            print("Lanjut tanpa scrub...")

    # ==========================
    # SMART SAVE
    # ==========================

    save_profiles = [
        {
            "name": "Aggressive",
            "garbage": 4,
            "clean": True,
            "deflate": True,
            "deflate_images": False,
            "deflate_fonts": True
        },
        {
            "name": "Balanced",
            "garbage": 3,
            "clean": True,
            "deflate": True,
            "deflate_images": False,
            "deflate_fonts": True
        },
        {
            "name": "Safe",
            "garbage": 2,
            "clean": True,
            "deflate": True,
            "deflate_images": False,
            "deflate_fonts": True
        },
        {
            "name": "Minimal",
            "garbage": 1,
            "clean": False,
            "deflate": True,
            "deflate_images": False,
            "deflate_fonts": True
        },
        {
            "name": "Compatibility",
            "garbage": 0,
            "clean": False,
            "deflate": False,
            "deflate_images": False,
            "deflate_fonts": False
        }
    ]

    last_error = None

    for profile in save_profiles:
        print(f"Coba dengan profile: {profile['name']}")

        try:
            if os.path.exists(output_pdf):
                os.remove(output_pdf)

            doc.save(
                output_pdf,
                garbage=profile["garbage"],
                clean=profile["clean"],
                deflate=profile["deflate"],
                deflate_images=profile["deflate_images"],
                deflate_fonts=profile["deflate_fonts"],
                incremental=False
            )

            doc.close()

            print(f"SUCCESS ({profile['name']})")

            return {
                "success": True,
                "profile": profile["name"],
                "input_size": os.path.getsize(input_pdf),
                "output_size": os.path.getsize(output_pdf)
            }

        except Exception as e:

            print(f"FAILED ({profile['name']})")
            print(e)

            last_error = str(e)

    doc.close()

    return {
        "success": False,
        "error": last_error
    }
