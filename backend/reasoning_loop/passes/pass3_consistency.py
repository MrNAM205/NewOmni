def refine_consistency(text, context):
    # If timeline contradicts mission, add a note
    timeline = context.get("timeline", [])
    if timeline:
        last_date = timeline[-1].get("date")
        if last_date and str(last_date) not in text:
            text += f"

[Mesh Note] Timeline indicates last event on {last_date}."
    return text
