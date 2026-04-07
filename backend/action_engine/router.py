from .planner import build_primary_plan
from .dependencies import attach_dependencies
from .branches import build_branches
from .fallback import build_fallbacks
from .fusion import fuse_action_plan

def run_action_engine(snapshot):
    primary = build_primary_plan(snapshot)
    deps = attach_dependencies(primary, snapshot)
    branches = build_branches(snapshot)
    fallbacks = build_fallbacks(snapshot)
    fused = fuse_action_plan(primary, deps, branches, fallbacks)
    return fused
