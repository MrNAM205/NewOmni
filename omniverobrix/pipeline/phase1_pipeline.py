# omniverobrix/pipeline/phase1_pipeline.py

import json
from pathlib import Path

from omniverobrix.core.tool_registry import global_tool_registry
from omniverobrix.core.reasoning_loop import ReasoningLoop


class Phase1Pipeline:
    """
    Full Phase‑1 pipeline:
        1. Scan folder
        2. Ingest scanner report
        3. Index documents (embeddings)
        4. Extract timeline events
        5. Extract entities
        6. Return summary
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.loop = ReasoningLoop(db_path=db_path)

    # ---------------------------------------------------------
    # MAIN PIPELINE
    # ---------------------------------------------------------

    def run(self, folder: str, mission_id: int = None) -> dict:
        """
        Execute the full Phase‑1 pipeline.
        Returns a structured summary dict.
        """

        # 1. Scan folder
        scan_report = self._scan_folder(folder)

        # 2. Ingest documents
        self._ingest(scan_report, mission_id)

        # 3. Index documents
        indexed_count = global_tool_registry.call("index_documents")

        # 4. Build timeline
        timeline_count = global_tool_registry.call("build_timeline")

        # 5. Extract entities
        entity_count = global_tool_registry.call("extract_entities")

        # 6. Return summary
        return {
            "folder": folder,
            "mission_id": mission_id,
            "indexed_documents": indexed_count,
            "timeline_events": timeline_count,
            "entities_extracted": entity_count,
            "message": "Phase‑1 pipeline complete."
        }

    # ---------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------

    def _scan_folder(self, folder: str) -> str:
        """
        Run scanner and return path to JSON report.
        """
        out_path = f"{Path(folder).name}_scan.json"
        global_tool_registry.call("scan_folder", folder=folder, out=out_path)
        return out_path

    def _ingest(self, report_path: str, mission_id: int = None):
        """
        Ingest scanner report into DB.
        """
        global_tool_registry.call(
            "ingest_scanner_report",
            report_path=report_path,
            mission_id=mission_id
        )


# ---------------------------------------------------------
# OPTIONAL CLI ENTRYPOINT
# ---------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OmniVeroBrix Phase‑1 Pipeline")
    parser.add_argument("--db", required=True, help="Path to SQLite database")
    parser.add_argument("--folder", required=True, help="Folder to process")
    parser.add_argument("--mission-id", type=int, help="Optional mission ID")

    args = parser.parse_args()

    pipeline = Phase1Pipeline(db_path=args.db)
    summary = pipeline.run(folder=args.folder, mission_id=args.mission_id)

    print(json.dumps(summary, indent=2))
