def detect_global_risks(snapshots):
    risks = []

    for snap in snapshots:
        supervisor = snap.get("supervisor", {})
        issues = supervisor.get("issues", [])

        for issue in issues:
            if issue.get("severity") == "high":
                risks.append({
                    "case_id": snap.get("case_id"),
                    "issue": issue
                })

    return risks
