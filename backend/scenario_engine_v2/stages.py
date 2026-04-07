def identify_stage(scenario: str, text: str) -> str:
    """
    Determines the procedural stage of the scenario.
    """

    text_lower = text.lower()

    if scenario == "dept_revenue_collection_warning":
        if "intent to levy" in text_lower:
            return "stage_4_final_notice"
        if "impending collection" in text_lower:
            return "stage_3_warning"
        return "stage_1_balance_due"

    if scenario == "traffic_court_failure_to_appear":
        if "warrant" in text_lower:
            return "stage_3_warrant_issued"
        return "stage_2_missed_court_date"

    if scenario == "debt_collector_initial_contact":
        return "stage_1_initial_contact"

    if scenario == "property_tax_delinquency":
        if "sale" in text_lower:
            return "stage_3_tax_sale_pending"
        return "stage_1_delinquent"

    return "unknown"
