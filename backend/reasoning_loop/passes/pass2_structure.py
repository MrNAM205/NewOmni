def refine_structure(text, context):
    # Ensure required sections exist
    required = ["Next Steps", "Checklist", "Risks", "Clarity"]
    for section in required:
        if section not in text:
            text += f"

{section}:
No data available."
    return text
