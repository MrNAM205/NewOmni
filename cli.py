# omniverobrix/cli/commands.py

import argparse
import json
from Agent_Core.tool_registry import global_tool_registry
from Agent_Core.reasoning_loop import ReasoningLoop
from Agent_Core.register_phase1_tools import register_phase1_tools
from Intelligence_Layer.scanner import scan_folder

def cli_entrypoint():
    parser = argparse.ArgumentParser(
        prog="omniverobrix",
        description="OmniVeroBrix Sovereign Intelligence CLI"
    )

    sub = parser.add_subparsers(dest="command")

    # ---------------------------------------------------------
    # SCAN
    # ---------------------------------------------------------
    scan_cmd = sub.add_parser("scan", help="Scan a folder and produce a JSON report")
    scan_cmd.add_argument("folder", help="Folder to scan")
    scan_cmd.add_argument("--out", required=True, help="Output JSON report path")

    # ---------------------------------------------------------
    # INGEST
    # ---------------------------------------------------------
    ingest_cmd = sub.add_parser("ingest", help="Ingest a scanner report into the database")
    ingest_cmd.add_argument("report", help="Path to scanner JSON report")
    ingest_cmd.add_argument("--mission-id", type=int, help="Optional mission ID")

    # ---------------------------------------------------------
    # INDEX
    # ---------------------------------------------------------
    index_cmd = sub.add_parser("index", help="Generate embeddings for all unindexed documents")

    # ---------------------------------------------------------
    # TIMELINE
    # ---------------------------------------------------------
    timeline_cmd = sub.add_parser("timeline", help="Extract timeline events from all documents")

    # ---------------------------------------------------------
    # ENTITIES
    # ---------------------------------------------------------
    entities_cmd = sub.add_parser("entities", help="Extract entities from all documents")

    # ---------------------------------------------------------
    # ASK (Reasoning Loop)
    # ---------------------------------------------------------
    ask_cmd = sub.add_parser("ask", help="Ask OmniVeroBrix a question")
    ask_cmd.add_argument("query", help="Your question")

    # ---------------------------------------------------------
    # PARSE ARGS
    # ---------------------------------------------------------
    args = parser.parse_args()

    # ---------------------------------------------------------
    # COMMAND ROUTING
    # ---------------------------------------------------------
    register_phase1_tools("omniverobrix.db", scan_folder)

    if args.command == "scan":
        result = global_tool_registry.call("scan_folder", folder_path=args.folder)
        with open(args.out, 'w') as f:
            f.write(result)
        print(f"Scan complete. Report saved to {args.out}")
        return

    if args.command == "ingest":
        global_tool_registry.call(
            "ingest_scanner_report",
            report_path=args.report,
            mission_id=args.mission_id
        )
        print("Ingestion complete.")
        return

    if args.command == "index":
        count = global_tool_registry.call("index_documents")
        print(f"Indexed {count} documents.")
        return

    if args.command == "timeline":
        count = global_tool_registry.call("build_timeline")
        print(f"Extracted {count} timeline events.")
        return

    if args.command == "entities":
        count = global_tool_registry.call("extract_entities")
        print(f"Extracted {count} entities.")
        return

    if args.command == "ask":
        loop = ReasoningLoop(db_path="omniverobrix.db")
        response = loop.handle_query(args.query)
        print(json.dumps(response, indent=2))
        return

    parser.print_help()

if __name__ == "__main__":
    cli_entrypoint()
