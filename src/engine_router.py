from src.pdf_rebuilder import rebuild_pdf
from src.engines.ghostscript_engine import optimize_with_ghostscript


def route_engine(
    input_pdf,
    safe_candidate_pdf,
    optimized_candidate_pdf,
    analysis
):

    pdf_type = analysis.get(
        "pdf_type",
        "UNKNOWN"
    )

    print()
    print(">> Engine routing...")
    print(
        "PDF Type:",
        pdf_type
    )

    # Kandidat aman selalu dibuat lebih dulu. Kandidat ini menjadi
    # fallback bila Ghostscript gagal atau hasilnya tidak layak.
    print("Selected base engine: PikePDF -> MuPDF")

    safe_result = rebuild_pdf(
        input_pdf,
        safe_candidate_pdf
    )

    result = {
        "success": safe_result.get(
            "success",
            False
        ),
        "safe_result": safe_result,
        "safe_candidate": safe_candidate_pdf,
        "optimized_result": None,
        "optimized_candidate": None,
        "pdf_type": pdf_type,
        "engine_used": "PikePDF -> MuPDF"
    }

    if not result["success"]:
        result["error"] = safe_result.get(
            "error",
            "Safe rebuild failed"
        )
        return result

    # Ghostscript hanya merupakan kandidat tambahan untuk dokumen
    # berbasis gambar. Ia tidak boleh menghapus kandidat aman.
    if pdf_type in [
        "IMAGE_HEAVY",
        "SCANNED_DOCUMENT"
    ]:

        print("\nSelected optimization engine: Ghostscript")

        optimized_result = optimize_with_ghostscript(
            safe_candidate_pdf,
            optimized_candidate_pdf
        )

        result["optimized_result"] = optimized_result

        if (
            optimized_result.get("success")
            and optimized_candidate_pdf
        ):

            result["optimized_candidate"] = (
                optimized_candidate_pdf
            )

    return result
