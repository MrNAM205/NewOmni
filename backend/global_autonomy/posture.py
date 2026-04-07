def compute_global_posture(snapshots):
    posture_counts = {}

    for snap in snapshots:
        posture = snap.get("posture", "unknown")
        posture_counts[posture] = posture_counts.get(posture, 0) + 1

    return posture_counts
