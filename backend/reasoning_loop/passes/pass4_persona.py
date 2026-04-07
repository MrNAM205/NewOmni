from backend.persona.router import persona_wrap

def refine_persona(text, context):
    return persona_wrap(text, context)
