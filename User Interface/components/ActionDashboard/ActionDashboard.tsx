import React from 'react';
import { PostureIndicator } from './PostureIndicator';
import { StepList } from './StepList';
import { ExecutionTimeline } from './ExecutionTimeline';
import { TriggerFeed } from './TriggerFeed';

const mockState = {
  posture: "in_progress",
  steps: {
    "Review document": "completed",
    "Prepare materials": "in_progress",
    "Verify entities": "pending"
  },
  triggers: [
    { type: "blocked", message: "Dependency not met" }
  ]
};

export function ActionDashboard({ caseId }) {
  const state = mockState;

  if (!state) return &lt;div&gt;Loading...&lt;/div&gt;;

  return (
    &lt;div className="action-dashboard"&gt;
      &lt;PostureIndicator posture={state.posture} /&gt;
      &lt;StepList steps={state.steps} /&gt;
      &lt;ExecutionTimeline steps={state.steps} /&gt;
      &lt;TriggerFeed triggers={state.triggers} /&gt;
    &lt;/div&gt;
  );
}
