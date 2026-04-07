def recommend_actions(scenario: str, stage: str) -> list:
    """
    Returns recommended next steps based on scenario + stage.
    """

    if scenario == "dept_revenue_collection_warning":
        if stage == "stage_3_warning":
            return [
                "Call the Department of Revenue to request a payment plan.",
                "Gather recent tax filings and income documents.",
                "Check your online DOR portal for outstanding balances.",
                "Respond before the deadline to avoid levy action."
            ]

        if stage == "stage_4_final_notice":
            return [
                "Contact DOR immediately — this is the last step before levy.",
                "Request a temporary hold on collection.",
                "Prepare proof of income and hardship if needed.",
                "Consider filing an appeal or requesting reconsideration."
            ]

    if scenario == "traffic_court_failure_to_appear":
        return [
            "Contact the court clerk to request a new court date.",
            "Ask whether the warrant can be recalled voluntarily.",
            "Prepare any documents related to the original citation."
        ]

    if scenario == "debt_collector_initial_contact":
        return [
            "Request written validation of the debt.",
            "Do not admit liability until validation is received.",
            "Check your credit report for matching entries."
        ]

    if scenario == "property_tax_delinquency":
        return [
            "Check the county tax portal for exact balance.",
            "Request a payment plan if available.",
            "Confirm the tax sale date and redemption period."
        ]

    return ["No recommended actions available."]
