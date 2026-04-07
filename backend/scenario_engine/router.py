from .generators import generate_branches
from .evaluators import evaluate_branch
from .fusion import fuse_scenarios

def run_scenario_engine(snapshot):
    branches = generate_branches(snapshot)
    evaluated = [evaluate_branch(b, snapshot) for b in branches]
    fused = fuse_scenarios(evaluated)
    return fused
