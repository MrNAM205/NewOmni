def classify_scenario(text: str) -> str:
    """
    Classifies the user's situation or document into a scenario type.
    Example outputs:
      - 'dept_revenue_collection_warning'
      - 'traffic_court_failure_to_appear'
      - 'debt_collector_initial_contact'
      - 'property_tax_delinquency'
    """
    text_lower = text.lower()

    if "department of revenue" in text_lower and "collection" in text_lower:
        return "dept_revenue_collection_warning"

    if "failure to appear" in text_lower or "fta" in text_lower:
        return "traffic_court_failure_to_appear"

    if "debt collector" in text_lower or "attempt to collect" in text_lower:
        return "debt_collector_initial_contact"

    if "property tax" in text_lower and "delinquent" in text_lower:
        return "property_tax_delinquency"

    return "unknown"
