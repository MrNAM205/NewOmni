from .validators import run_validations
from .enrichers import run_enrichers
from .resolvers import run_resolvers
from .fusion import fuse_outputs

def run_cognitive_mesh(snapshot):
    issues = run_validations(snapshot)
    enriched = run_enrichers(snapshot)
    resolved = run_resolvers(snapshot, issues)
    fused = fuse_outputs(snapshot, enriched, resolved)
    return fused
