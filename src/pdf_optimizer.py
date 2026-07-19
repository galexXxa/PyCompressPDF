import pikepdf
import os


def optimize_pdf(input_pdf, output_pdf):

    with pikepdf.open(input_pdf) as pdf:

        pdf.save(
            output_pdf,
            object_stream_mode=pikepdf.ObjectStreamMode.generate,
            compress_streams=True,
            recompress_flate=True
        )


    original = os.path.getsize(input_pdf)

    compressed = os.path.getsize(output_pdf)


    saved = (
        1 - (compressed / original)
    ) * 100


    return {

        "original_mb": round(
            original / 1024 / 1024,
            2
        ),

        "compressed_mb": round(
            compressed / 1024 / 1024,
            2
        ),

        "saved_percent": round(
            saved,
            2
        )

    }