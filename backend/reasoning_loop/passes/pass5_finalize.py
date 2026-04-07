def finalize_output(text):
    # Clean whitespace, ensure readability
    lines = [l.strip() for l in text.split("
") if l.strip()]
    return "
".join(lines)
