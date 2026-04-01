import { useState } from "react";
import DocumentsTab from "./tabs/DocumentsTab";
import TimelineTab from "./tabs/TimelineTab";
import EntitiesTab from "./tabs/EntitiesTab";
import QuestionsTab from "./tabs/QuestionsTab";

export default function Tabs({ missionData }) {
  const [active, setActive] = useState("documents");

  return (
    <div className="tabs">
      <div className="tab-buttons">
        <button onClick={() => setActive("documents")}>Documents</button>
        <button onClick={() => setActive("timeline")}>Timeline</button>
        <button onClick={() => setActive("entities")}>Entities</button>
        <button onClick={() => setActive("questions")}>Questions</button>
      </div>

      {active === "documents" && (
        <DocumentsTab documentGroups={missionData.document_groups} />
      )}
      {active === "timeline" && (
        <TimelineTab timeline={missionData.timeline} />
      )}
      {active === "entities" && (
        <EntitiesTab entities={missionData.entities} />
      )}
      {active === "questions" && (
        <QuestionsTab questions={missionData.questions} />
      )}
    </div>
  );
}
