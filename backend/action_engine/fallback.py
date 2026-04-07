def build_fallbacks(snapshot):
    return [
        {
            "failure": "Missing documents",
            "action": "Request missing documents and pause timeline-dependent steps."
        }
    ]
