import os
import shutil

def compare_output(
    original_pdf,
    optimized_pdf
):

    original_size = os.path.getsize(
        original_pdf
    )

    optimized_size = os.path.getsize(
        optimized_pdf
    )

    saving = (
        (original_size - optimized_size) / original_size * 100
    )

    if saving >= -20:
        return {
            "accepted":
            True,
            "original_size":
            original_size,
            "optimized_size":
            optimized_size,
            "saving":
            round(
                saving,
                2
            )
        }

    else:
        return {
            "accepted":
            False,
            "original_size":
            original_size,
            "optimized_size":
            optimized_size,
            "saving":
            round(
                saving,
                2
            )
        }
