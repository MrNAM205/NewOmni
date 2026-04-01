# OmniVeroBrix: A Sovereign Intelligence Cockpit

OmniVeroBrix is a local-first, modular, and sovereign intelligence analysis system designed to operate as a personal command center. It processes unstructured documents, extracts intelligence, and provides procedural guidance through a unified, multi-organ architecture.

## Core Architecture

The system is composed of several interoperable "organs," each with a specific function. The Intelligence Loop ensures that when new data is ingested, the entire analytical cascade is triggered automatically, keeping the cockpit's mission guidance continuously updated.

### Key Organs & Their Functions

-   **Model Router:** Provides a unified, fallback-aware interface to various local and cloud-based language models.
-   **Scenario Router:** Interprets real-world situations (e.g., traffic tickets, bills) and applies procedural templates.
-   **Document Reasoner:** The "eyes" of the cockpit. Extracts structured data like dates, amounts, agencies, and reference numbers from documents.
-   **Timeline Intelligence:** The "temporal brain." Builds chronological event narratives and tracks deadlines.
-   **Entity Intelligence:** The "relational brain." Identifies, extracts, and maps key actors (people, organizations, agencies).
-   **Case Memory:** The persistent memory layer. Stores all extracted intelligence (documents, events, entities) in a local SQLite database.
-   **Cross-Document Synthesis:** The "analyst brain." Fuses intelligence from multiple documents to create case-level summaries and detect patterns.
-   **Mission Engine:** The "navigator." Converts synthesized intelligence into actionable, procedural guidance, including next steps, checklists, and risk assessments.
-   **Supervisor (Overwatch Organ):** Monitors the health and integrity of the entire intelligence stack, flagging issues with data consistency, loop health, or field completeness.
-   **Autonomy Layer:** The "proactive brain." Runs on a loop to detect critical changes (e.g., approaching deadlines, high-risk conditions) and issue alerts.
-   **Persona Layer:** The "voice" of the cockpit. A multi-stage pipeline that shapes all output with a consistent, adaptive, and learnable persona that adjusts to context, urgency, and user preference.
-   **Intelligence Loop:** The "heartbeat." An orchestration engine that automatically runs the entire intelligence pipeline whenever new data is ingested, ensuring the cockpit is always up-to-date.

## Core Principles

-   **Sovereign:** Operates locally on your machine, with optional connections to external services.
-   **Local-First:** All core data (cases, intelligence, memory) is stored in a local database.
-   **Modular:** The organ-based design allows for easy extension and maintenance.
-   **Cockpit-Grade:** Designed for clarity, efficiency, and operational focus.
