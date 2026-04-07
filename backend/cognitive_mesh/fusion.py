def fuse_outputs(snapshot, enriched, resolved):
    fused = snapshot.copy()
    fused["mesh"] = {
        "enriched": enriched,
        "resolved": resolved,
    }
    return fused
