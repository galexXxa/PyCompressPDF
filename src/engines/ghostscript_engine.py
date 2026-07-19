import subprocess
import os
from src.logger import debug, success, error

def optimize_with_ghostscript(
    input_pdf,
    output_pdf,
    profile="ebook"
):

    debug("")
    debug("=" * 50)
    debug("GHOSTSCRIPT ENGINE")
    debug("=" * 50)
    debug(
        f"Input: {input_pdf}"
    )

    profiles = {
        "screen":
        {
            "dpi": 72,
            "setting":
            "/screen"
        },

        "ebook":
        {
            "dpi": 150,
            "setting":
            "/ebook"
        },

        "printer":
        {
            "dpi": 300,
            "setting":
            "/printer"
        }
    }

    selected = profiles.get(
        profile,
        profiles["ebook"]
    )

    cmd = [
        "gswin64c",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-dPDFSETTINGS={selected['setting']}",
        "-dDetectDuplicateImages=true",
        "-dCompressFonts=true",
        "-dSubsetFonts=true",
        f"-sOutputFile={output_pdf}",
        input_pdf
    ]

    try:
        print()
        print(">>> Running Ghostscript...")

        subprocess.run(
            cmd,
            check=True
        )

        if os.path.exists(output_pdf):
            input_size = os.path.getsize(
                input_pdf
            )

            output_size = os.path.getsize(
                output_pdf
            )

            if output_size >= input_size:
                print(
                    "Ghostscript result larger than original"
                )

                os.remove(
                    output_pdf
                )

                return {
                    "success": False,
                    "engine": "Ghostscript(SKIPPED)",
                    "profile": profile,
                    "input_size": input_size,
                    "output_size": input_size,
                    "skipped": True,
                    "error": "Ghostscript output is not smaller than its input"
                }

            print(
                "Ghostscript SUCCESS"
            )

            return {
                "success": True,
                "engine": "Ghostscript",
                "profile": profile,
                "input_size":
                os.path.getsize(
                    input_pdf
                ),
                "output_size":
                os.path.getsize(
                    output_pdf
                )
            }
        else:
            return {
                "success": False,
                "error":
                "Output not created"
            }

    except Exception as e:
        return {
            "success": False,
            "error":
            str(e)
        }
