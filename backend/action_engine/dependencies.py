def attach_dependencies(steps, snapshot):
    deps = []

    for step in steps:
        if "Prepare materials" in step:
            deps.append({
                "step": step,
                "depends_on": "Review the latest document and confirm required response."
            })

    return deps
