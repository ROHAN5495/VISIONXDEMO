import React from 'react';

export default function DiffHighlighter({ diffTokens = [], showLegend = true }) {
  if (!diffTokens || diffTokens.length === 0) {
    return <span className="text-slate-500 italic">No diff tokens available.</span>;
  }

  const getTokenStyle = (type) => {
    switch (type) {
      case 'added':
        return 'bg-emerald-100 text-emerald-900 border-b-2 border-emerald-500 font-medium px-1 py-0.5 rounded mx-0.5';
      case 'removed':
        return 'bg-rose-100 text-rose-800 line-through border-b-2 border-rose-400 opacity-75 px-1 py-0.5 rounded mx-0.5';
      case 'misleading':
        return 'bg-amber-100 text-amber-950 font-semibold border-b-2 border-amber-500 px-1.5 py-0.5 rounded mx-0.5 shadow-sm';
      case 'context':
        return 'bg-sky-100 text-sky-900 border-b-2 border-sky-400 px-1 py-0.5 rounded mx-0.5';
      case 'equal':
      default:
        return 'text-slate-800';
    }
  };

  return (
    <div className="space-y-4">
      {/* Visual Text Output */}
      <div className="p-4 bg-white rounded-lg border border-slate-200 text-base leading-relaxed font-sans shadow-inner min-h-[80px]">
        {diffTokens.map((token, idx) => (
          <span key={idx} className={getTokenStyle(token.type)}>
            {token.text}{' '}
          </span>
        ))}
      </div>

      {/* Color Code Legend */}
      {showLegend && (
        <div className="flex flex-wrap items-center gap-3 text-xs text-slate-600 bg-slate-100/70 p-3 rounded-lg border border-slate-200">
          <span className="font-semibold text-slate-700">Mutation Color Code:</span>
          
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded bg-emerald-500 inline-block" />
            <span className="font-medium text-emerald-900">Green</span>
            <span className="text-slate-500">= Added information</span>
          </div>

          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded bg-rose-500 inline-block" />
            <span className="font-medium text-rose-900">Red</span>
            <span className="text-slate-500">= Removed information</span>
          </div>

          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded bg-amber-500 inline-block" />
            <span className="font-medium text-amber-900">Amber</span>
            <span className="text-slate-500">= Potentially misleading change</span>
          </div>

          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded bg-sky-500 inline-block" />
            <span className="font-medium text-sky-900">Blue</span>
            <span className="text-slate-500">= Contextual modification</span>
          </div>
        </div>
      )}
    </div>
  );
}
