def run_enrichers(snapshot):
    enriched = {}

    # If timeline has upcoming deadlines, enrich mission
    deadlines = [e for e in snapshot["timeline"] if e.get("days_until", 99) <= 7]
    if deadlines:
        enriched["mission_deadline_note"] = "Upcoming deadlines detected within 7 days."

    # If entities include IRS, enrich mission with payment caution
    if "IRS" in snapshot["entities"]:
        enriched["mission_financial_note"] = "Verify payment channels and retain receipts."

    return enriched
