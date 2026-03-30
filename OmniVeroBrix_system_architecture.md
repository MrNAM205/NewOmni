### OmniVeroBrix system architecture document  

---

## 1. Purpose and scope

**Goal:** Define a coherent, sovereign, local‑first architecture for OmniVeroBrix—a resident agent that unifies scanning, ingestion, semantic intelligence, remedy generation, and AI chat into a single cockpit.

**Scope:**

- Runs locally on user devices  
- Uses modular tools (scanner, ingester, generators, analyzers)  
- Embeds a persona‑driven agent core  
- Supports mission‑based workflows (e.g., house defense)  

---

## 2. High‑level architecture

```text
OmniVeroBrix/
│
├── Agent Core
│   ├── Reasoning Loop
│   ├── Persona Engine
│   ├── Memory Engine
│   ├── Context Manager
│   └── Tool Registry
│
├── Intelligence Layer
│   ├── Scanner
│   ├── Ingestion Engine
│   ├── Semantic Indexer
│   ├── Timeline Builder
│   └── Entity & Definition Extractor
│
├── Remedy Engine
│   ├── Document Generator
│   ├── Notice & Letter Builder
│   ├── Procedural Map Engine
│   └── Deadline & Milestone Tracker
│
├── Mission Modules
│   ├── House Defense Module
│   ├── Identity & Capacity Module
│   ├── Trust & Estate Module
│   ├── Administrative Challenge Module
│   └── Evidence & Document Review Module
│
├── User Interface
│   ├── Chat Interface
│   ├── Mission Selector
│   ├── Document & Timeline Viewer
│   └── Logs & Session History
│
└── Deployment Layer
    ├── Local Runtime & Storage
    ├── Device Adapter
    └── Installer / Packaging
```

---

## 3. Agent core

### 3.1 Reasoning loop

- **Input:** user message, mission context, active persona, relevant documents.  
- **Process:**  
  - Retrieve context from memory and semantic index  
  - Select tools via Tool Registry  
  - Call tools, integrate results  
  - Generate structured response + optional actions (e.g., “scan folder”, “summarize docs”).  
- **Output:**  
  - Chat response  
  - Updated memory  
  - Updated mission state  

### 3.2 Persona engine

- **Personas:**  
  - **Private Individual Persona** (you as living man, private capacity)  
  - **Representative Persona** (heir, executor, agent, trustee)  
  - **Analyst Persona** (cold legal/structural analysis)  
- **Responsibilities:**  
  - Enforce capacity boundaries (what this persona can and cannot assume)  
  - Shape tone, focus, and risk posture  
  - Control which tools and data are visible in a given mode  

### 3.3 Memory engine

- **Short‑term:** current session context, active mission, current documents.  
- **Long‑term:**  
  - Document embeddings / semantic index  
  - Mission histories (e.g., “House Defense – Session 1”)  
  - Key facts (dates, parties, roles, properties).  

### 3.4 Context manager

- Tracks:  
  - Active mission  
  - Active persona  
  - Active document set  
  - Current step in a workflow (e.g., “collect documents”, “build timeline”).  

### 3.5 Tool registry

- Central registry of callable tools:  
  - Scanner, ingester, indexer, generator, analyzers, etc.  
- Each tool has:  
  - Name, description, input schema, output schema  
  - Permissions (which persona/mission can use it)  

---

## 4. Intelligence layer

### 4.1 Scanner (already built)

- **Function:**  
  - Walks folders, filters files, extracts text (text, PDFs, images via OCR).  
  - Detects duplicates and folder‑level clones.  
- **Output:**  
  - JSON report of files, hashes, locations, duplicate groups.  
  - Markdown report for human review.  

### 4.2 Ingestion engine

- **Function:**  
  - Takes scanner output and ingests documents into the system.  
- **Steps:**  
  - Normalize text  
  - Extract metadata (file path, type, dates, parties)  
  - Store in local document store  

### 4.3 Semantic indexer

- **Function:**  
  - Build embeddings / semantic index over ingested documents.  
- **Use:**  
  - Fast retrieval for chat, timelines, mission modules.  

### 4.4 Timeline builder

- **Function:**  
  - Extract dates + events from documents.  
- **Output:**  - Chronological list of events (who, what, when, source document).  

### 4.5 Entity & definition extractor

- **Function:**  
  - Identify parties (you, uncle, county, court, etc.).  
  - Identify key terms (tax, notice, deed, hearing).  
  - Optionally link to definitions (from legal dictionaries, statutes).  

---

## 5. Remedy engine

### 5.1 Document generator

- **Inputs:**  
  - Mission type (e.g., “prepare questions for nonprofit”, “summarize house situation”).  
  - Selected documents + timeline.  
- **Outputs:**  
  - Summaries  
  - Question lists  
  - Draft letters / notes (for you to use with humans)  

### 5.2 Notice & letter builder

- **Function:**  
  - Generate structured, plain‑language documents like:  
    - “Summary of facts”  
    - “Questions to ask a lawyer/nonprofit”  
    - “Personal statement of situation”  

### 5.3 Procedural map engine

- **Function:**  
  - For a given mission, outline typical procedural steps (non‑advisory, general).  
  - Example: “In property tax matters, there are usually: assessment → notice → opportunity to contest → etc.”  

### 5.4 Deadline & milestone tracker

- **Function:**  
  - Track dates extracted from documents (e.g., “hearing date”, “response by”).  
  - Present them in a simple timeline view.  

---

## 6. Mission modules

### 6.1 House defense module (priority)

- **Purpose:**  
  - Help you understand and organize everything related to your inherited house.  
- **Capabilities:**  
  - Ingest all house‑related docs into one “case space”  
  - Build a timeline (deed, death, taxes, uncle’s actions, any court references)  
  - Group documents by topic (ownership, taxes, family, court)  
  - Generate:  
    - Plain‑language situation summary  
    - Questions to ask nonprofits / lawyers  
    - A “what I know / what I don’t know yet” list  

### 6.2 Identity & capacity module

- Map roles: you, uncle, county, court, etc.  
- Clarify: heir, payer, owner of record, etc. (in neutral, descriptive terms).  

### 6.3 Trust & estate module

- For later: organizing estate documents, wills, trusts, beneficiaries.  

### 6.4 Administrative challenge module

- For later: general patterns of dealing with agencies, notices, etc.  

### 6.5 Evidence & document review module

- For later: deeper analysis of document sets, contradictions, missing pieces.  

---

## 7. User interface

### 7.1 Chat interface

- Central interaction point with OmniVeroBrix.  
- Shows:  
  - Conversation  
  - Relevant documents / excerpts  
  - Suggested actions (e.g., “scan folder”, “build timeline”).  

### 7.2 Mission selector

- Simple menu:  
  - “Start House Defense”  
  - “Review Identity & Capacity”  
  - “General Document Review”  

### 7.3 Document & timeline viewer

- View:  
  - List of documents  
  - Timeline of events  
  - Key entities and roles  

### 7.4 Logs & session history

- Keep a record of:  
  - What was ingested  
  - What missions were run  
  - What summaries were generated  

---

## 8. Deployment layer

### 8.1 Local runtime & storage

- All data stored locally (e.g., SQLite + file system).  
- No automatic external calls.  

### 8.2 Device adapter

- Abstracts OS‑specific details (paths, permissions, etc.).  

### 8.3 Installer / packaging

- Packaged as a desktop app (e.g., Electron + Python backend, or similar).  
- Agent “lives inside” the app and becomes resident once installed.  

---

## 9. Data flow (end‑to‑end example)

1. **You choose a folder** (e.g., `House-Defense/`).  
2. **Scanner** runs → finds files → extracts text → outputs JSON.  
3. **Ingestion engine** ingests JSON → stores documents + metadata.  
4. **Semantic indexer** builds embeddings.  
5. **Timeline builder** extracts events.  
6. **House Defense Module**:  
   - Pulls documents + timeline  
   - Generates summary + questions + lists.  
7. **Chat interface** lets you ask:  
   - “What do these documents say about my uncle paying taxes?”  
   - “What are the key dates I should be aware of?”  

---

## 10. Phase sequence (what I’ll design next)

You asked for the rest “in the order I see fit.” Here’s the sequence I’ll follow next:

1. **Phase 1 build plan**  
   - Concrete steps to implement Intelligence Layer + minimal Agent Core.  
2. **House Defense Module design**  
   - Detailed spec for the first mission module tailored to your situation.  
3. **Tool Registry spec**  
   - How tools are defined, registered, and called by the agent.  
4. **Persona Engine spec**  
   - How personas are modeled, switched, and enforced.  
5. **Reasoning Loop design**  
   - How the agent decides what to retrieve, which tools to call, and how to respond.

If you’re good with this architecture, I’ll move straight into **Phase 1 build plan** next.
