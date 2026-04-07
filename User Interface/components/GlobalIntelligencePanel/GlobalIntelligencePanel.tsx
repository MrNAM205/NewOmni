import React, { useState, useEffect } from 'react';
import { GlobalPostureMap } from './GlobalPostureMap';
import { GlobalAlerts } from './GlobalAlerts';
import { GlobalRiskList } from './GlobalRiskList';
import { GlobalTriggerList } from './GlobalTriggerList';

export function GlobalIntelligencePanel() {
  const [data, setData] = useState(null);

  useEffect(() =&gt; {
    const fetchData = () =&gt; {
      if (window.omni &amp;&amp; window.omni.getGlobalIntelligence) {
        window.omni.getGlobalIntelligence().then(setData);
      }
    };

    fetchData(); // Initial fetch
    const interval = setInterval(fetchData, 3000); // Auto-refresh loop

    return () =&gt; clearInterval(interval);
  }, []);

  if (!data) return &lt;div&gt;Loading global intelligence…&lt;/div&gt;;

  return (
    &lt;div className="global-intelligence-panel"&gt;
      &lt;GlobalPostureMap posture={data.posture} /&gt;
      &lt;GlobalAlerts alerts={data.alerts} /&gt;
      &lt;GlobalRiskList risks={data.risks} /&gt;
      &lt;GlobalTriggerList triggers={data.triggers} /&gt;
    &lt;/div&gt;
  );
}
