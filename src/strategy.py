from enum import Enum


class CompressionStrategy(Enum):
    GOOGLE_SAFE = "google_safe"
    IMAGE = "image"
    PDF = "pdf"
    RENDER = "render"
    SKIP = "skip"


def choose_strategy(analysis):

    pdf_type = analysis["pdf_type"]

    confidence = analysis["confidence"]


    # -------------------------
    # Publisher PDF
    # -------------------------

    if pdf_type == "PUBLISHER_VECTOR":

        return {
            "strategy": CompressionStrategy.GOOGLE_SAFE,
            "reason": "Publisher PDF detected"
        }


    # -------------------------
    # Image Heavy
    # -------------------------

    if pdf_type == "IMAGE_HEAVY":

        return {
            "strategy": CompressionStrategy.IMAGE,
            "reason": "Large image content"
        }


    # -------------------------
    # Scan PDF
    # -------------------------

    if pdf_type == "SCANNED_DOCUMENT":

        return {
            "strategy": CompressionStrategy.RENDER,
            "reason": "Scanned document"
        }


    # -------------------------
    # Unknown
    # -------------------------

    if confidence < 40:

        return {
            "strategy": CompressionStrategy.SKIP,
            "reason": "Unknown PDF type"
        }


    # -------------------------
    # Default
    # -------------------------

    return {
        "strategy": CompressionStrategy.PDF,
        "reason": "General PDF"
    }