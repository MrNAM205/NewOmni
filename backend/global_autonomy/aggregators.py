def aggregate_triggers(snapshots):
    aggregated = []

    for snap in snapshots:
        execution = snap.get("execution", {})
        triggers = execution.get("triggers", [])

        for trig in triggers:
            aggregated.append({
                "case_id": snap.get("case_id"),
                "trigger": trig
            })

    return aggregated
