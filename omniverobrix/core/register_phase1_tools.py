# omniverobrix/core/register_phase1_tools.py

from tool_registry import global_tool_registry
from ..intelligence.ingestion import IngestionEngine
from ..intelligence.semantic_indexer import SemanticIndexer
from ..intelligence.timeline_builder import TimelineBuilder
from ..intelligence.entity_extractor import EntityExtractor

# Example embedding function
# from omniverobrix.models.embedding import embed_text
def embed_text(text):
    import numpy as np
    return np.random.rand(384).astype(np.float32)


def register_phase1_tools(db_path: str, scanner_func):
    ingestion = IngestionEngine(db_path=db_path)
    indexer = SemanticIndexer(db_path=db_path, embed_fn=embed_text)
    timeline = TimelineBuilder(db_path=db_path)
    extractor = EntityExtractor(db_path=db_path)

    # Scanner
    global_tool_registry.register(
        name="scan_folder",
        func=scanner_func,
        description="Scan a folder and produce a JSON report.",
    )

    # Ingestion
    global_tool_registry.register(
        name="ingest_scanner_report",
        func=ingestion.ingest_from_scanner_report,
        description="Ingest documents from a scanner JSON report.",
    )

    # Semantic Indexing
    global_tool_registry.register(
        name="index_documents",
        func=indexer.index_all_unembedded_documents,
        description="Generate embeddings for all unindexed documents.",
    )

    global_tool_registry.register(
        name="semantic_search",
        func=indexer.search,
        description="Search documents semantically.",
    )

    # Timeline
    global_tool_registry.register(
        name="build_timeline",
        func=timeline.build_timeline_for_all_documents,
        description="Extract timeline events from all documents.",
    )

    # Entities
    global_tool_registry.register(
        name="extract_entities",
        func=extractor.extract_entities_for_all_documents,
        description="Extract entities from all documents.",
    )
