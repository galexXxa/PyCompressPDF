from src.engines.pikepdf_engine import repair_with_pikepdf
from src.engines.mupdf_engine import rebuild_with_mupdf
from src.temp_manager import TempManager

def rebuild_pdf(
    input_pdf,
    output_pdf,
    clean=True
):

    pipeline = []

    # ======================================
    # TEMP WORKSPACE
    # ======================================

    with TempManager() as temp:
        repaired_pdf = temp.file(
            "repaired.pdf"
        )
        optimize_source = input_pdf

        # ======================================
        # STEP 1
        # PikePDF Repair
        # ======================================

        print()
        print(">>> PikePDF Repair")

        repair_result = repair_with_pikepdf(
            input_pdf,
            repaired_pdf
        )

        if repair_result["success"]:
            print(
                "PikePDF repair SUCCESS"
            )

            optimize_source = repaired_pdf

            pipeline.append(
                "PikePDF"
            )

        else:
            print(
                "PikePDF repair FAILED"
            )
            print(
                repair_result.get(
                    "error"
                )
            )
            print(
                "Continue using original PDF..."
            )

        # ======================================
        # STEP 2
        # MuPDF Optimize
        # ======================================

        print()
        print(">>> MuPDF Optimizer")

        mupdf_result = rebuild_with_mupdf(
            optimize_source,
            output_pdf,
            clean
        )

        if mupdf_result["success"]:
            pipeline.append(
                "MuPDF"
            )

            mupdf_result["pipeline"] = pipeline

            return mupdf_result

        return {
            "success": False,
            "engine": "Pipeline",
            "pipeline": pipeline,
            "error":
                mupdf_result.get(
                    "error",
                    "MuPDF failed"
                )
        }