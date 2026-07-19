from src.batch_processor import process_batch
from src.report_generator import ReportGenerator
from src.logger import debug, success, error

report = ReportGenerator(
    "report/google_optimizer_report.xlsx"
)

try:
    result = process_batch(
        "input",
        "output",
        report
    )
finally:
    report.save()
