def analyze_pdf(info):
    size = info["size"]
    pages = info["pages"]
    images = info["images"]
    image_bytes = info["image_bytes"]
    drawings = info["drawings"]
    text_length = info["text_length"]
    font_count = info["font_count"]
    metadata = info["metadata"]
    creator = (
        metadata.get("creator") or ""
    ).lower()
    producer = (
        metadata.get("producer") or ""
    ).lower()

    # ==========================
    # Basic Calculation
    # ==========================

    if size > 0:
        image_ratio = (image_bytes / size)
    else:
        image_ratio = 0

    if pages > 0:
        image_per_page = (images / pages)
        drawing_per_page = (drawings / pages)
    else:
        image_per_page = 0
        drawing_per_page = 0

    # ==========================
    # Scoring
    # ==========================

    score = 0

    reasons = []
    pdf_type = "UNKNOWN"
    recommendation = "PDF_OPTIMIZE"

    # ==========================
    # Publisher PDF
    # ==========================

    if (
        "indesign" in creator
        or
        "illustrator" in creator
        or
        "quark" in creator
    ):

        score += 40

        reasons.append(
            "Publisher software detected"
        )

        pdf_type = "PUBLISHER_VECTOR"

        recommendation = (
            "GOOGLE_SAFE_OPTIMIZE"
        )

    # ==========================
    # Text Layer
    # ==========================

    if text_length > 1000:

        score += 15

        reasons.append(
            "Text layer exists"
        )

    else:
        reasons.append(
            "Low text content"
        )

    # ==========================
    # Fonts
    # ==========================

    if font_count > 0:

        score += 10

        reasons.append(
            "Font detected"
        )

    # ==========================
    # Vector Heavy
    # ==========================

    if drawing_per_page > 1000:

        score += 20

        reasons.append(
            "Vector heavy document"
        )

        if pdf_type == "UNKNOWN":
            pdf_type = (
                "VECTOR_HEAVY"
            )

            recommendation = (
                "GOOGLE_SAFE_OPTIMIZE"
            )

    # ==========================
    # Image Heavy
    # ==========================

    if image_ratio > 0.5:

        score += 25

        reasons.append(
            "Large image content"
        )

        pdf_type = (
            "IMAGE_HEAVY"
        )

        recommendation = (
            "IMAGE_OPTIMIZE"
        )

    # ==========================
    # Scan Detection
    # ==========================

    if (
        "scanner" in producer
        or
        "scan" in producer
    ):

        score += 30

        reasons.append(
            "Scanner detected"
        )

        pdf_type = (
            "SCANNED_DOCUMENT"
        )

        recommendation = (
            "RENDER_COMPRESS"
        )

    # ==========================
    # Confidence
    # ==========================

    if score > 100:

        score = 100

    return {
        "pdf_type":
        pdf_type,
        "confidence":
        score,
        "recommendation":
        recommendation,
        "image_ratio":
        round(
            image_ratio * 100,
            2
        ),
        "image_per_page":
        round(
            image_per_page,
            2
        ),
        "drawing_per_page":
        round(
            drawing_per_page,
            2
        ),
        "reasons":
        reasons
    }