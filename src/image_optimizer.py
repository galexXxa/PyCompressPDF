import fitz
from PIL import Image
import io
import os

def optimize_images(
    input_pdf,
    output_pdf,
    quality=50
):

    doc = fitz.open(input_pdf)
    replaced = 0

    for page in doc:
        images = page.get_images(
            full=True
        )

        for img in images:
            xref = img[0]

            try:
                base_image = (
                    doc.extract_image(xref)
                )
                image_bytes = (
                    base_image["image"]
                )
                image = Image.open(
                    io.BytesIO(image_bytes)
                )

                # hanya proses image besar

                if (
                    image.width > 1000
                    or
                    image.height > 1000
                ):

                    new_image = io.BytesIO()
                    image.convert(
                        "RGB"
                    ).save(
                        new_image,
                        format="JPEG",
                        quality=quality,
                        optimize=True
                    )

                    doc.update_stream(
                        xref,
                        new_image.getvalue()
                    )

                    replaced += 1

            except Exception as e:
                print(
                    "Skip image:",
                    e
                )

    doc.save(
        output_pdf,
        garbage=4,
        deflate=True
    )

    doc.close()

    return replaced