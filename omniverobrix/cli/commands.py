# omniverobrix/cli/commands.py

import argparse
import json
from omniverobrix.core.tool_registry import global_tool_registry
from omniverobrix.core.reasoning_loop import ReasoningLoop
from omniverobrix.missions.house_defense.module import HouseDefenseModule
from omniverobrix.core.context_manager import ContextManager
from omniverobrix.missions.manager.manager import MissionManager
from omniverobrix.core.document_manager import DocumentManager


def cli():
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
    # SCAN-NOW (Autonomous)
    # ---------------------------------------------------------
    sub.add_parser("scan-now", help="Autonomous scan of predefined cockpit folders")

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
    # MISSION
    # ---------------------------------------------------------
    mission_cmd = sub.add_parser("mission", help="Mission management commands")
    mission_sub = mission_cmd.add_subparsers(dest="mission_action")

    # Create
    mission_create = mission_sub.add_parser("create", help="Create a new mission")
    mission_create.add_argument("mission_type", help="Mission type (e.g., house_defense)")
    mission_create.add_argument("description", nargs="?", default="", help="Mission description")

    # List
    mission_sub.add_parser("list", help="List all missions")

    # Activate
    mission_activate = mission_sub.add_parser("activate", help="Activate a mission")
    mission_activate.add_argument("mission_id", type=int)

    # Info
    mission_info = mission_sub.add_parser("info", help="Show mission info")
    mission_info.add_argument("mission_id", type=int)

    # Attach documents
    mission_attach = mission_sub.add_parser("attach", help="Attach documents to a mission")
    mission_attach.add_argument("mission_id", type=int)
    mission_attach.add_argument("--docs", nargs="+", type=int, required=True)

    # ---------------------------------------------------------
    # MISSION: SET ACTIVE HOUSE MISSION
    # ---------------------------------------------------------
    set_house_cmd = sub.add_parser(
        "set-house",
        help="Set the active mission_id for the House Defense module"
    )
    set_house_cmd.add_argument(
        "mission_id",
        type=int,
        help="Mission ID to activate for House Defense"
    )

    # ---------------------------------------------------------
    # PERSONA
    # ---------------------------------------------------------
    persona_cmd = sub.add_parser("persona", help="Set active persona")
    persona_cmd.add_argument("persona_name", choices=["private_individual", "analyst", "representative"])

    # ---------------------------------------------------------
    # DOCUMENT
    # ---------------------------------------------------------
    doc_cmd = sub.add_parser("document", help="Document management commands")
    doc_sub = doc_cmd.add_subparsers(dest="document_action")
    
    # Get
    doc_get = doc_sub.add_parser("get", help="Get document content and metadata")
    doc_get.add_argument("document_id", type=int)


    # ---------------------------------------------------------
    # PARSE ARGS
    # ---------------------------------------------------------
    args = parser.parse_args()

    # ---------------------------------------------------------
    # COMMAND ROUTING
    # ---------------------------------------------------------

    if args.command == "scan":
        result = global_tool_registry.call("scan_folder", folder=args.folder, out=args.out)
        print(f"Scan complete. Report saved to {args.out}")
        return

    if args.command == "scan-now":
        loop = ReasoningLoop(db_path=r"C:\Users\Sir\Desktop\NewOmni\omniverobrix\omniverobrix.db")
        response = loop.handle_query("scan now")
        print(json.dumps(response, indent=2))
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
        loop = ReasoningLoop(db_path=r"C:\Users\Sir\Desktop\NewOmni\omniverobrix\omniverobrix.db")
        response = loop.handle_query(args.query)
        print(json.dumps(response, indent=2))
        return

    if args.command == "mission":
        mm = MissionManager(db_path=r"C:\Users\Sir\Desktop\NewOmni\omniverobrix\omniverobrix.db")
        ctx = ContextManager(db_path=r"C:\Users\Sir\Desktop\NewOmni\omniverobrix\omniverobrix.db")

        if args.mission_action == "create":
            mission_id = mm.create(args.mission_type, args.description)
            print(f"Created mission {mission_id} ({args.mission_type})")
            # Automatically activate the new mission
            if mm.activate(mission_id, ctx):
                print(f"Activated mission {mission_id}")
            return

        if args.mission_action == "list":
            missions = mm.list()
            print(json.dumps(missions, indent=2))
            return

        if args.mission_action == "activate":
            if mm.activate(args.mission_id, ctx):
                print(f"Activated mission {args.mission_id}")
            else:
                print(f"Mission {args.mission_id} does not exist.")
            return

        if args.mission_action == "info":
            info = mm.info(args.mission_id)
            if info:
                print(json.dumps(info, indent=2))
            else:
                print(f"Mission {args.mission_id} not found.")
            return

        if args.mission_action == "attach":
            count = mm.attach_documents(args.mission_id, args.docs)
            print(f"Attached {count} documents to mission {args.mission_id}")
            return
        
        # If no action is specified, print help for the 'mission' command
        mission_cmd.print_help()
        return

    if args.command == "set-house":
        ctx = ContextManager(db_path=r"C:\Users\Sir\Desktop\NewOmni\omniverobrix\omniverobrix.db")

        # Validate mission exists
        conn = ctx._connect()
        cur = conn.cursor()
        cur.execute("SELECT id FROM missions WHERE id = ?", (args.mission_id,))
        row = cur.fetchone()
        conn.close()

        if not row:
            print(f"Mission {args.mission_id} does not exist.")
            return

        ctx.set("active_house_mission_id", str(args.mission_id))
        print(f"Active House Defense mission set to {args.mission_id}")
        return

    if args.command == "persona":
        ctx = ContextManager(db_path=r"C:\Users\Sir\Desktop\NewOmni\omniverobrix\omniverobrix.db")
        ctx.set("active_persona", args.persona_name)
        print(f"Active persona set to {args.persona_name}")
        return

    if args.command == "document":
        dm = DocumentManager(db_path=r"C:\Users\Sir\Desktop\NewOmni\omniverobrix\omniverobrix.db")
        if args.document_action == "get":
            doc = dm.get(args.document_id)
            print(json.dumps(doc, indent=2))
        return

    parser.print_help()

if __name__ == "__main__":
    cli()
