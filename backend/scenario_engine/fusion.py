def fuse_scenarios(evaluated):
    # pick the highest score as recommended path
    best = max(evaluated, key=lambda e: e["score"])
    return {
        "scenarios": evaluated,
        "recommended": best,
    }
