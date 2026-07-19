import fitz
import os


def scan_pdf(pdf_path):

    file_size = os.path.getsize(pdf_path)


    doc = fitz.open(pdf_path)


    image_count = 0
    image_bytes = 0

    drawing_count = 0
    text_length = 0

    font_list = set()



    for page in doc:


        # =====================
        # Images
        # =====================

        images = page.get_images(full=True)


        for img in images:

            image_count += 1

            xref = img[0]


            try:

                image_data = doc.extract_image(xref)


                image_bytes += len(
                    image_data["image"]
                )


            except Exception:

                pass



        # =====================
        # Vector Drawing
        # =====================

        drawings = page.get_drawings()

        drawing_count += len(drawings)



        # =====================
        # Text
        # =====================

        text = page.get_text()

        text_length += len(text)



        # =====================
        # Fonts
        # =====================

        blocks = page.get_text("dict")["blocks"]


        for block in blocks:


            if "lines" not in block:
                continue


            for line in block["lines"]:


                for span in line["spans"]:


                    font_list.add(
                        span["font"]
                    )



    metadata = doc.metadata


    result = {


        "file":
        os.path.basename(pdf_path),


        "path":
        pdf_path,


        "pages":
        len(doc),


        "size":
        file_size,


        "images":
        image_count,


        "image_bytes":
        image_bytes,


        "drawings":
        drawing_count,


        "text_length":
        text_length,


        "fonts":
        list(font_list),


        "font_count":
        len(font_list),


        "metadata":
        metadata

    }


    doc.close()


    return result