# omniverobrix/core/reasoning_loop.py

from typing import Dict, Any
from omniverobrix.core.tool_registry import global_tool_registry
from omniverobrix.core.context_manager import ContextManager
from omniverobrix.missions.house_defense.module import HouseDefenseModule
from omniverobrix.persona.engine import PersonaEngine
from omniverobrix.missions.manager.manager import MissionManager


class ReasoningLoop:
    """
    Phase 2 Reasoning Loop (v2):
    - Detects intent (search, timeline, entities, ingest, house_defense)
    - Routes to tools or mission modules
    - Produces structured responses
    - Tracks context (last query, last results, active mission)
    """

    def __init__(self, db_path: str):
        self.context = ContextManager(db_path=db_path)
        self.db_path = db_path
        self.persona_engine = PersonaEngine(db_path=db_path)
        self.mission_manager = MissionManager(db_path=db_path)
        
        persona_name = self.context.get("active_persona")
        if persona_name:
            self.persona_engine.set_persona(persona_name)

    # ---------------------------------------------------------
    # PUBLIC ENTRY POINT
    # ---------------------------------------------------------

    def handle_query(self, query: str) -> Dict[str, Any]:
        """
        Main reasoning entry point.
        Returns a structured response dict.
        """
        self.context.set("last_query", query)
        intent = self._detect_intent(query)

        response: Dict[str, Any]

        if intent == "house_defense":
            response = self._handle_house_defense(query)

        elif intent == "timeline":
            response = self._handle_timeline_request()

        elif intent == "entities":
            response = self._handle_entity_request()

        elif intent == "ingest":
            response = self._handle_ingest_request(query)

        else:  # Default: semantic search
            response = self._handle_semantic_search(query)
        
        return self.persona_engine.shape_response(response)

    # ---------------------------------------------------------
    # INTENT DETECTION (v2)
    # ---------------------------------------------------------

    def _detect_intent(self, query: str) -> str:
        q = query.lower()

        # House Defense mission
        house_keywords = [
            "house", "home", "property", "tax", "taxes",
            "deed", "title", "probate", "uncle", "dad's house",
            "father's house", "keep the house"
        ]
        if any(k in q for k in house_keywords):
            return "house_defense"

        if "timeline" in q or "when" in q:
            return "timeline"

        if "who" in q or "entities" in q or "people" in q:
            return "entities"

        if "ingest" in q or "scan" in q:
            return "ingest"

        return "search"

    # ---------------------------------------------------------
    # HANDLERS
    # ---------------------------------------------------------

    def _handle_semantic_search(self, query: str) -> Dict[str, Any]:
        results = global_tool_registry.call("semantic_search", query=query)
        self.context.set("last_results", results)

        return {
            "type": "semantic_search",
            "query": query,
            "results": [
                {"document_id": doc_id, "score": score}
                for doc_id, score in results
            ],
        }

    def _handle_timeline_request(self) -> Dict[str, Any]:
        count = global_tool_registry.call("build_timeline")
        return {
            "type": "timeline",
            "events_extracted": count,
            "message": f"Extracted {count} timeline events."
        }

    def _handle_entity_request(self) -> Dict[str, Any]:
        count = global_tool_registry.call("extract_entities")
        return {
            "type": "entities",
            "entities_extracted": count,
            "message": f"Extracted {count} entities."
        }

    def _handle_ingest_request(self, query: str) -> Dict[str, Any]:
        return {
            "type": "ingest",
            "message": "Ingestion requires a scanner report path. Use CLI for now."
        }

    def _handle_house_defense(self, query: str) -> Dict[str, Any]:
        """
        Route to House Defense mission.
        Requires an active mission_id in context_state.
        """
        mission_id = self.mission_manager.get_active(self.context)
        if mission_id is None:
            return {
                "type": "house_defense",
                "error": "no_active_mission",
                "message": (
                    "No active mission is set. "
                    "Create a mission and activate it using 'mission activate <id>'."
                ),
            }

        # Validate that the active mission is a 'house_defense' mission
        mission_info = self.mission_manager.info(mission_id)
        if not mission_info or mission_info.get("name") != "house_defense":
            return {
                "type": "house_defense",
                "error": "wrong_mission_type",
                "message": (
                    f"Active mission {mission_id} is not a 'house_defense' mission. "
                    "Please activate a valid mission."
                )
            }

        module = HouseDefenseModule(db_path=self.db_path)
        result = module.run(mission_id=mission_id)

        self.context.set("last_house_defense_result", result)

        return {
            "type": "house_defense",
            "query": query,
            "mission_id": mission_id,
            "result": result,
        }
