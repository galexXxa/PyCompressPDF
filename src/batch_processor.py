import os
from tqdm import tqdm
from src.google_optimizer import optimize_for_google

def scan_pdf(folder):
    files = []
    for root, dirs, filenames in os.walk(folder):
        for filename in filenames:
            if filename.lower().endswith(".pdf"):
                files.append(
                    os.path.join(
                        root,
                        filename
                    )
                )
    return files

def process_batch(
    input_folder,
    output_folder,
    report
):
    pdf_files = scan_pdf(
        input_folder
    )

    print()
    print("=" * 50)
    print(" PDF BATCH PROCESSOR")
    print(" By GalexXxa")
    print("=" * 50)
    print(
        f"Total PDF : {len(pdf_files)}"
    )

    success = 0
    failed = 0

    for index, pdf in enumerate(
        tqdm(
            pdf_files,
            desc="Processing"
        ),

        start=1
    ):
        filename = os.path.basename(
            pdf
        )

        try:
            result = optimize_for_google(
                pdf,
                output_folder
            )

            if result["success"]:
                success += 1

                report.add_result(
                    result
                )

                decision = result.get(
                    "compression_decision",
                    {}
                ).get(
                    "decision",
                    "ACCEPT"
                )

                result_label = {
                    "ACCEPT": "ACCEPT",
                    "SAFE_FALLBACK": "SAFE FALLBACK",
                    "ORIGINAL_FALLBACK": "ORIGINAL FALLBACK"
                }.get(
                    decision,
                    decision
                )

                print()
                print("=" * 50)
                print(
                    f"[{index}/{len(pdf_files)}] {filename}"
                )
                print(
                    "  Type   :",
                    result.get(
                        "pdf_type",
                        "-"
                    )
                )
                print(
                    "  Engine :",
                    result.get(
                        "engine_used",
                        "-"
                    )
                )
                print(
                    "  Result :",
                    result_label
                )

                if decision == "ORIGINAL_FALLBACK":
                    print(
                        "  Reason :",
                        result.get(
                            "compression_decision",
                            {}
                        ).get(
                            "reason",
                            "No rebuilt candidate passed validation"
                        )
                    )

            else:
                failed += 1

                print()
                print("=" * 50)
                print(
                    f"[{index}/{len(pdf_files)}] {filename}"
                )
                print(
                    "  Result : FAILED"
                )
                print(
                    "  Error  :",
                    result.get(
                        "error",
                        "-"
                    )
                )

                report.add_result({
                    "success":
                    False,
                    "file":
                    pdf,
                    "error":
                    result.get(
                        "error",
                        "Unknown error"
                    )
                })

        except Exception as e:
            failed += 1

            print()
            print("=" * 50)
            print(
                f"[{index}/{len(pdf_files)}] {filename}"
            )
            print(
                "  Result : ERROR"
            )
            print(
                "  Error  :",
                str(e)
            )

            report.add_result({
                "success":
                False,
                "file":
                pdf,
                "error":
                str(e)
            })

    print()
    print("=" * 50)
    print(" BATCH RESULT")
    print("=" * 50)
    print(
        "Total  :",
        len(pdf_files)
    )
    print(
        "Sukses :",
        success
    )
    print(
        "Gagal  :",
        failed
    )

    return {
        "total":
        len(pdf_files),
        "success":
        success,
        "failed":
        failed
    }
