def run_resolvers(snapshot, issues):
    resolutions = []

    for issue in issues:
        if issue["type"] == "deadline_mismatch":
            resolutions.append("Use timeline date as authoritative source.")

        if issue["type"] == "entity_missing":
            resolutions.append("Flag posture for review.")

    return resolutions
