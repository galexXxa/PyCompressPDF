def calculate_size_saving(
    original_size,
    optimized_size
):

    if original_size == 0:
        return 0

    return (
        (original_size - optimized_size)
        /
        original_size
        *
        100
    )

def make_decision(
    original_fp,
    optimized_fp,
    validation,
    optimized_score
):

    original_size = (
        original_fp["size"]
    )
    optimized_size = (
        optimized_fp["size"]
    )

    # ==================================
    # Validation Check
    # ==================================

    if not validation["status"]:
        return {
            "winner":
            "ORIGINAL",
            "reason":
            "Optimized PDF failed validation",
            "use_optimized":
            False
        }

    # ==================================
    # Google Score Priority
    # ==================================

    original_score = 0

    # Original belum melalui optimizer
    # jadi baseline

    if original_fp.get(
        "sha256"
    ):
        original_score = 50

    if optimized_score > original_score:
        return {
            "winner":
            "OPTIMIZED",
            "reason":
            "Higher Google score",
            "use_optimized":
            True
        }

    elif optimized_score < original_score:
        return {
            "winner":
            "ORIGINAL",
            "reason":
            "Original has better score",
            "use_optimized":
            False
        }

    # ==================================
    # Score Sama
    # Gunakan ukuran
    # ==================================

    saving = calculate_size_saving(
        original_size,
        optimized_size
    )

    if saving > 0:
        return {
            "winner":
            "OPTIMIZED",
            "reason":
            "Same score but smaller size",
            "use_optimized":
            True
        }
    return {
        "winner":
        "ORIGINAL",
        "reason":
        "No improvement detected",
        "use_optimized":
        False
    }