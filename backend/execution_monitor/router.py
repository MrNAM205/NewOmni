from .state import load_state, save_state
from .tracker import update_step_state
from .updater import update_mission_posture
from .triggers import check_triggers

def run_execution_monitor(case_id, action_plan, event):
    state = load_state(case_id)

    # event = { "step": "...", "status": "completed" }
    state = update_step_state(state, event)

    # update mission posture based on progress
    posture_update = update_mission_posture(state)

    # check for triggers (fallbacks, branches, alerts)
    triggers = check_triggers(state, action_plan)

    save_state(case_id, state)

    return {
        "state": state,
        "posture_update": posture_update,
        "triggers": triggers
    }
