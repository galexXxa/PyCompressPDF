import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

class ReportGenerator:
    def __init__(self, report_file):
        self.report_file = report_file
        self.data = []

    def add_result(self, result):
        if not result.get("success"):
            self.data.append({
                "original_file":
                result.get(
                    "file",
                    "-"
                ),
                "output_file": "-",
                "pdf_type":
                result.get(
                    "pdf_type",
                    "-"
                ),
                "engine":
                result.get(
                    "engine_used",
                    "-"
                ),
                "original_mb": "-",
                "optimized_mb": "-",
                "saving": "-",
                "pages": "-",
                "text": "-",
                "images_before": "-",
                "images_after": "-",
                "objects_before": "-",
                "objects_after": "-",
                "google_score": "-",
                "validation": "FAILED",
                "decision":
                str(
                    result.get(
                        "error",
                        "Unknown error"
                    )
                )
            })

            return

        original = result["original"]
        optimized = result["optimized"]

        original_size = original["size"]
        optimized_size = optimized["size"]

        saving = (
            (original_size - optimized_size)
            /
            original_size
            *
            100
        )

        self.data.append({
            "original_file":
            original["file"],
            "output_file":
            os.path.basename(
                result["output_file"]
            ),
            "pdf_type":
            result.get(
                "pdf_type",
                "-"
            ),
            "engine":
            result.get(
                "engine_used",
                "-"
            ),
            "original_mb":
            round(
                original_size / 1024 / 1024,
                2
            ),
            "optimized_mb":
            round(
                optimized_size / 1024 / 1024,
                2
            ),
            "saving":
            round(
                saving,
                2
            ),
            "pages":
            original["pages"],
            "text":
            original["text"],
            "images_before":
            original["images"],
            "images_after":
            optimized["images"],
            "objects_before":
            original.get(
                "object_count",
                "-"
            ),
            "objects_after":
            optimized.get(
                "object_count",
                "-"
            ),
            "google_score":
            result["google_score"],
            "validation":
            "PASS"
            if result["validation"]["status"]
            else "FAILED",
            "decision":
            result.get(
                "compression_decision",
                {}
            ).get(
                "decision",
                "-"
            )
        })

    def save(self):
        wb = Workbook()
        ws = wb.active
        ws.title = "Google Optimizer"

        headers = [
            "Original File",
            "Output File",
            "PDF Type",
            "Engine",
            "Original MB",
            "Optimized MB",
            "Saving %",
            "Pages",
            "Text Length",
            "Images Before",
            "Images After",
            "Objects Before",
            "Objects After",
            "Google Score",
            "Validation",
            "Compression Decision"
        ]

        ws.append(headers)

        for cell in ws[1]:
            cell.font = Font(
                bold=True
            )
            cell.alignment = Alignment(
                horizontal="center"
            )

        for item in self.data:
            ws.append([
                item["original_file"],
                item["output_file"],
                item["pdf_type"],
                item["engine"],
                item["original_mb"],
                item["optimized_mb"],
                item["saving"],
                item["pages"],
                item["text"],
                item["images_before"],
                item["images_after"],
                item["objects_before"],
                item["objects_after"],
                item["google_score"],
                item["validation"],
                item["decision"]
            ])

        for col in ws.columns:
            max_length = 0
            letter = col[0].column_letter

            for cell in col:
                if cell.value:
                    max_length = max(
                        max_length,
                        len(str(cell.value))
                    )

            ws.column_dimensions[
                letter
            ].width = max_length + 3

        wb.save(
            self.report_file
        )

        return self.report_file
