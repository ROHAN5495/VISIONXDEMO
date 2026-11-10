import React from 'react';
import { AlertTriangle, ShieldCheck, Layers } from 'lucide-react';

export default function DemoBadge({ isDemo = true, mode = null, className = "" }) {
  const currentMode = mode || (isDemo ? 'offline_demo' : 'live');

  if (currentMode === 'live') {
    return (
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 shadow-xs ${className}`}>
        <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
        <span>Live Web Verified</span>
      </span>
    );
  }

  if (currentMode === 'mixed') {
    return (
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-sky-50 text-sky-800 border border-sky-300 shadow-xs ${className}`} title="This investigation combines live web records with offline reference sources.">
        <Layers className="w-3.5 h-3.5 text-sky-600" />
        <span>Mixed Evidence (Live & Offline)</span>
      </span>
    );
  }

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-800 border border-amber-300 shadow-xs ${className}`} title="This investigation uses prepared fictional or offline demonstration records.">
      <AlertTriangle className="w-3.5 h-3.5 text-amber-600 animate-pulse-slow" />
      <span>DEMO INVESTIGATION</span>
      <span className="text-[10px] font-normal text-amber-700 opacity-80">(Offline Mode)</span>
    </span>
  );
}
