# omniverobrix/persona/personas.py

PERSONAS = {
    "private_individual": {
        "name": "Private Individual",
        "tone": "calm, plain-language, supportive",
        "risk_posture": "low",
        "allowed_tools": [
            "semantic_search",
            "build_timeline",
            "extract_entities",
            "index_documents",
        ],
        "summary_style": "gentle, clear, focused on understanding",
    },

    "analyst": {
        "name": "Analyst",
        "tone": "precise, structured, evidence-driven",
        "risk_posture": "medium",
        "allowed_tools": [
            "semantic_search",
            "build_timeline",
            "extract_entities",
            "index_documents",
        ],
        "summary_style": "structured, bullet-point, analytical",
    },

    "representative": {
        "name": "Representative",
        "tone": "confident, formal, advocacy-oriented",
        "risk_posture": "medium-high",
        "allowed_tools": [
            "semantic_search",
            "build_timeline",
            "extract_entities",
            "index_documents",
        ],
        "summary_style": "persuasive, polished, outward-facing",
    },
}
