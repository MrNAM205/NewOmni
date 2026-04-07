def build_branches(snapshot):
    risks = snapshot.get("supervisor", {}).get("issues", [])

    if any(r["severity"] == "high" for r in risks):
        return [
            {
                "condition": "High-risk supervisor issue detected",
                "action": "Escalate case for manual review."
            }
        ]

    return []
