import { useEffect, useState } from "react";
import Sidebar from "./Sidebar";
import SummaryPanel from "./SummaryPanel";
import AskBox from "./AskBox";
import Tabs from "./Tabs";
import { ToastHost } from "./Notifications/ToastHost";
import { AlertCenter } from "./Notifications/AlertCenter";
import FileUpload from "./FileUpload";

export default function App() {
  const [missions, setMissions] = useState([]);
  const [activeMissionId, setActiveMissionId] = useState(null);
  const [missionData, setMissionData] = useState(null);
  const [activePersona, setActivePersona] = useState("private_individual");
  const [toasts, setToasts] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [globalIntel, setGlobalIntel] = useState(null);

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

  const pushAlerts = (newAlerts) => {
    // Assuming newAlerts is an array
    const highPriorityAlerts = newAlerts.filter(a => a.priority === 'high');
    const mediumPriorityAlerts = newAlerts.filter(a => a.priority === 'medium');

    // Add high-priority to toasts
    setToasts(prev => [...prev, ...highPriorityAlerts]);

    // Add high and medium to alerts
    setAlerts(prev => [...prev, ...highPriorityAlerts, ...mediumPriorityAlerts]);
};

  useEffect(() => {
    window.omniEvents.onUpdate((event) => {
      switch (event.type) {
        case "global_intelligence":
          setGlobalIntel(event.payload);
          break;

        case "case_update":
          // Assuming the payload is a full missionData object
          if (activeMissionId && event.payload.id === activeMissionId) {
            setMissionData(event.payload);
          }
          break;

        case "alert":
          pushAlerts(event.payload);
          break;
      }
    });
  }, [activeMissionId]); // Re-subscribe if activeMissionId changes to capture it in the closure

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
      <ToastHost toasts={toasts} />
      <Sidebar
        missions={missions}
        activeMissionId={activeMissionId}
        onSelectMission={handleSelectMission}
        activePersona={activePersona}
        onSelectPersona={handleSelectPersona}
      />

      <main className="main">
        <FileUpload />
        {missionData && (
          <>
            <SummaryPanel summary={missionData.summary} />
            <AskBox onAsk={handleAsk} />
            <Tabs missionData={missionData} />
          </>
        )}
        <AlertCenter alerts={alerts} />
      </main>
    </div>
  );
}
