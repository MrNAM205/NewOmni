from .passes.pass1_raw import generate_raw
from .passes.pass2_structure import refine_structure
from .passes.pass3_consistency import refine_consistency
from .passes.pass4_persona import refine_persona
from .passes.pass5_finalize import finalize_output

def run_reasoning_loop(generator, context):
    # generator is a function like handle_mission or handle_synthesis
    raw = generate_raw(generator, context)
    structured = refine_structure(raw, context)
    consistent = refine_consistency(structured, context)
    persona_aligned = refine_persona(consistent, context)
    final = finalize_output(persona_aligned)
    return final
