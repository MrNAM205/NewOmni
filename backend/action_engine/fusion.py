def fuse_action_plan(primary, deps, branches, fallbacks):
    return {
        "primary_plan": primary,
        "dependencies": deps,
        "branches": branches,
        "fallbacks": fallbacks
    }
