import { useEffect, useState } from "react";
import Sidebar from "./Sidebar";
import SummaryPanel from "./SummaryPanel";
import AskBox from "./AskBox";
import Tabs from "./Tabs";

export default function App() {
  const [missions, setMissions] = useState([]);
  const [activeMissionId, setActiveMissionId] = useState(null);
  const [missionData, setMissionData] = useState(null);
  const [activePersona, setActivePersona] = useState("private_individual");

  // Load missions on startup
  useEffect(() => {
    window.api.invoke("missions:list").then(setMissions);
  }, []);

  // When mission changes, load mission data
  useEffect(() => {
    if (!activeMissionId) return;
    window.api.invoke("houseDefense:run", { missionId: activeMissionId })
      .then(setMissionData);
  }, [activeMissionId]);

  const handleSelectMission = async (id) => {
    const res = await window.api.invoke("missions:activate", { missionId: id });
    if (res.ok) {
      setActiveMissionId(id);
    }
  };

  const handleSelectPersona = async (personaName) => {
    await window.api.invoke("persona:set", { personaName });
    setActivePersona(personaName);

    // Re-run mission to apply persona shaping
    if (activeMissionId) {
      const data = await window.api.invoke("houseDefense:run", { missionId: activeMissionId });
      setMissionData(data);
    }
  };

  const handleAsk = async (query) => {
    const response = await window.api.invoke("reasoning:ask", { query });
    // If it's a house_defense response, hydrate missionData
    if (response.type === "house_defense") {
      setMissionData(response.result);
    }
    // Later: show short answers in a panel
  };

  return (
    <div className="app">
      <Sidebar
        missions={missions}
        activeMissionId={activeMissionId}
        onSelectMission={handleSelectMission}
        activePersona={activePersona}
        onSelectPersona={handleSelectPersona}
      />

      <main className="main">
        {missionData && (
          <>
            <SummaryPanel summary={missionData.summary} />
            <AskBox onAsk={handleAsk} />
            <Tabs missionData={missionData} />
          </>
        )}
      </main>
    </div>
  );
}
