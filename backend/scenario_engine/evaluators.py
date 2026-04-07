def evaluate_branch(branch, snapshot):
    timeline = snapshot.get("timeline", [])
    risks = snapshot.get("supervisor", {}).get("issues", [])

    score = 0
    if branch["type"] == "best_case":
        score = 90
    elif branch["type"] == "expected_case":
        score = 70
    elif branch["type"] == "worst_case":
        score = 30
    elif branch["type"] == "risk_case":
        score = 40 - len(risks)

    return {
        "branch": branch["type"],
        "assumptions": branch["assumptions"],
        "score": score,
        "risks": risks,
        "timeline": timeline,
    }
