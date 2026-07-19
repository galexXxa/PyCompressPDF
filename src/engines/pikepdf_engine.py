import os
import pikepdf
from src.logger import debug, success, error

def repair_with_pikepdf(
    input_pdf,
    repaired_pdf
):

    debug("Input:")
    debug(input_pdf)

    try:
        pdf = pikepdf.open(input_pdf)
        try:
            pdf.remove_unreferenced_resources()
        except Exception:
            pass

        pdf.save(
            repaired_pdf,
            compress_streams=True,
            object_stream_mode=pikepdf.ObjectStreamMode.generate,
            recompress_flate=True
        )

        pdf.close()

        print("Rekonstruksi ulang file...")

        return {
            "success": True,
            "engine": "PikePDF",
            "output": repaired_pdf,
            "input_size": os.path.getsize(input_pdf),
            "output_size": os.path.getsize(repaired_pdf)
        }

    except Exception as e:

        return {
            "success": False,
            "engine": "PikePDF",
            "error": str(e)
        }