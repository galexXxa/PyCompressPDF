import os
import shutil

from src.engine_router import route_engine
from src.validator import validate_pdf
from src.fingerprint import (
    PDFFingerprint,
    compare_fingerprint
)
from src.filename_generator import generate_filename
from src.scanner import scan_pdf
from src.analyzer import analyze_pdf
from src.compression_decision import compare_output
from src.temp_manager import TempManager


def optimize_for_google(
    input_pdf,
    output_folder
):

    print("\n")

    output_name = generate_filename(
        input_pdf
    )

    output_pdf = os.path.join(
        output_folder,
        output_name
    )

    print("\n[1/6] Reading original fingerprint...")

    original_fp = PDFFingerprint(
        input_pdf
    ).analyze()

    info = scan_pdf(
        input_pdf
    )

    analysis = analyze_pdf(
        info
    )

    # Semua kandidat dikerjakan di workspace sementara. Hanya pemenang
    # yang disalin ke output/, sehingga candidate file tidak tertinggal.
    with TempManager() as temp:

        safe_candidate = temp.file(
            "safe_rebuilt.pdf"
        )

        ghostscript_candidate = temp.file(
            "ghostscript.pdf"
        )

        print("\n[2/6] Building candidates...")

        route_result = route_engine(
            input_pdf,
            safe_candidate,
            ghostscript_candidate,
            analysis
        )

        safe_validation = None
        safe_fp = None
        safe_size_result = None

        if (
            route_result.get("success")
            and os.path.exists(safe_candidate)
        ):

            print("\n[3/6] Validating safe candidate...")

            safe_validation = validate_pdf(
                input_pdf,
                safe_candidate
            )

            if safe_validation["status"]:
                safe_fp = PDFFingerprint(
                    safe_candidate
                ).analyze()

                safe_size_result = compare_output(
                    input_pdf,
                    safe_candidate
                )

        optimized_validation = None
        optimized_fp = None
        optimized_size_result = None
        optimized_candidate = route_result.get(
            "optimized_candidate"
        )

        if optimized_candidate and os.path.exists(
            optimized_candidate
        ):

            print("\n[4/6] Validating Ghostscript candidate...")

            optimized_validation = validate_pdf(
                input_pdf,
                optimized_candidate
            )

            if optimized_validation["status"]:
                optimized_fp = PDFFingerprint(
                    optimized_candidate
                ).analyze()

                optimized_size_result = compare_output(
                    input_pdf,
                    optimized_candidate
                )

        # Pilih Ghostscript hanya jika valid dan memenuhi batas ukuran.
        # Kandidat aman tetap dipakai bila Ghostscript gagal/tidak layak.
        if (
            optimized_fp is not None
            and optimized_size_result["accepted"]
        ):

            final_source = optimized_candidate
            final_fp = optimized_fp
            final_validation = optimized_validation
            engine_used = "PikePDF -> MuPDF -> Ghostscript"
            size_result = optimized_size_result
            size_result["decision"] = "ACCEPT"

        elif safe_fp is not None:

            final_source = safe_candidate
            final_fp = safe_fp
            final_validation = safe_validation
            engine_used = "PikePDF -> MuPDF"
            size_result = safe_size_result
            size_result["decision"] = "SAFE_FALLBACK"

        else:

            # Original hanya dipakai jika tidak ada kandidat rebuilt yang
            # lolos validasi.
            final_source = input_pdf
            final_fp = original_fp
            final_validation = validate_pdf(
                input_pdf,
                input_pdf
            )
            engine_used = "Original fallback"
            size_result = {
                "accepted": False,
                "original_size": original_fp["size"],
                "optimized_size": original_fp["size"],
                "saving": 0.0,
                "decision": "ORIGINAL_FALLBACK",
                "reason": route_result.get(
                    "error",
                    "No rebuilt candidate passed validation"
                )
            }

        print("\n[5/6] Saving output...")

        if os.path.exists(output_pdf):
            os.remove(
                output_pdf
            )

        shutil.copy2(
            final_source,
            output_pdf
        )

    print("\n[6/6] Comparing fingerprint...")

    # Ambil fingerprint dari file final yang benar-benar tersimpan.
    optimized_fp = PDFFingerprint(
        output_pdf
    ).analyze()

    fingerprint_diff = compare_fingerprint(
        original_fp,
        optimized_fp
    )

    score = calculate_google_score(
        fingerprint_diff
    )

    return {
        "success": True,
        "output_file": output_pdf,
        "original": original_fp,
        "optimized": optimized_fp,
        "validation": final_validation,
        "fingerprint": fingerprint_diff,
        "google_score": score,
        "engine_used": engine_used,
        "pdf_type": analysis.get(
            "pdf_type",
            "-"
        ),
        "compression_decision": size_result
    }


def calculate_google_score(diff):

    score = 0

    if diff["sha256"]["changed"]:
        score += 30

    if diff["md5"]["changed"]:
        score += 10

    if diff.get(
        "object_count",
        {}
    ).get("changed"):
        score += 25

    if diff.get(
        "trailer_id",
        {}
    ).get("changed"):
        score += 25

    if diff["size"]["changed"]:
        score += 10

    return min(
        score,
        100
    )
