import React from 'react';
import { Send, Eye, Search, CheckSquare, GitCompare, MessageSquare, LineChart } from 'lucide-react';

const STEPS = [
  { id: 'submit', label: 'Submit', icon: Send, desc: 'Input claim statement' },
  { id: 'understand', label: 'Understand', icon: Eye, desc: 'Extract Rumour DNA' },
  { id: 'retrieve', label: 'Retrieve', icon: Search, desc: 'Search trusted records' },
  { id: 'verify', label: 'Verify', icon: CheckSquare, desc: 'Detect contradictions' },
  { id: 'compare', label: 'Compare', icon: GitCompare, desc: 'Analyze mutations' },
  { id: 'explain', label: 'Explain', icon: MessageSquare, desc: 'Natural truth synthesis' },
  { id: 'track', label: 'Track', icon: LineChart, desc: 'Evolution Journey Map' },
];

export default function WorkflowStepper({ currentStep = 'track' }) {
  const currentIndex = STEPS.findIndex(s => s.id === currentStep);

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm mb-6">
      <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-3">
        Standard Investigation Protocol
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-2">
        {STEPS.map((step, idx) => {
          const Icon = step.icon;
          const isDone = currentIndex > idx || currentIndex === -1;
          const isCurrent = currentIndex === idx;

          let badgeColor = 'bg-slate-100 text-slate-500 border-slate-200';
          if (isCurrent) {
            badgeColor = 'bg-electric-500 text-white border-electric-600 shadow-sm';
          } else if (isDone) {
            badgeColor = 'bg-slate-800 text-slate-100 border-slate-700';
          }

          return (
            <div
              key={step.id}
              className={`flex flex-col items-center text-center p-2 rounded-lg border transition-all ${
                isCurrent ? 'bg-electric-50/60 border-electric-300' : 'bg-slate-50/50 border-slate-100'
              }`}
            >
              <div className={`w-7 h-7 rounded-full flex items-center justify-center mb-1 text-xs font-bold border ${badgeColor}`}>
                <Icon className="w-3.5 h-3.5" />
              </div>
              <span className={`text-xs font-bold ${isCurrent ? 'text-electric-700' : 'text-slate-800'}`}>
                {step.label}
              </span>
              <span className="text-[10px] text-slate-400 mt-0.5 line-clamp-1">{step.desc}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
