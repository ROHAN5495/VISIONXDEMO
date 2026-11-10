import React from 'react';
import { ExternalLink, CheckCircle2, XCircle, HelpCircle, Shield, BookmarkCheck } from 'lucide-react';

export default function KeyEvidenceSummary({ excerpts = [] }) {
  if (!excerpts || excerpts.length === 0) {
    return null;
  }

  const getBadge = (cls) => {
    switch (cls) {
      case 'supporting':
        return {
          icon: <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />,
          label: 'Supports Claim',
          style: 'bg-emerald-50 text-emerald-800 border-emerald-200'
        };
      case 'contradictory':
        return {
          icon: <XCircle className="w-3.5 h-3.5 text-rose-600" />,
          label: 'Contradicts Claim',
          style: 'bg-rose-50 text-rose-800 border-rose-200'
        };
      case 'contextual':
        return {
          icon: <HelpCircle className="w-3.5 h-3.5 text-sky-600" />,
          label: 'Contextual',
          style: 'bg-sky-50 text-sky-800 border-sky-200'
        };
      default:
        return {
          icon: <HelpCircle className="w-3.5 h-3.5 text-slate-500" />,
          label: 'Irrelevant',
          style: 'bg-slate-100 text-slate-700 border-slate-300'
        };
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 md:p-8 shadow-sm space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <BookmarkCheck className="w-5 h-5 text-blue-600" />
          <div>
            <div className="text-[11px] font-bold text-blue-600 uppercase tracking-wider font-mono">
              Key Evidence Highlights
            </div>
            <h3 className="text-base md:text-lg font-bold text-slate-900 mt-0.5">
              Crucial Source Quotations Driving This Verdict
            </h3>
          </div>
        </div>
        <span className="text-xs text-slate-400 font-mono hidden sm:inline">
          Curated Top {excerpts.length} Excerpt(s)
        </span>
      </div>

      <div className="space-y-3.5">
        {excerpts.map((item, idx) => {
          const badge = getBadge(item.classification);
          return (
            <div
              key={idx}
              className="p-4 rounded-xl border border-slate-200/90 bg-slate-50/60 hover:bg-white hover:border-slate-300 hover:shadow-xs transition-all space-y-2.5"
            >
              {/* Header: Publisher + Snippet Tag + Classification + External Link */}
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-xs text-slate-800 flex items-center gap-1.5">
                    <Shield className="w-3.5 h-3.5 text-slate-500" />
                    {item.publisher}
                  </span>
                  <span className="text-[10px] font-mono uppercase font-bold text-slate-400 bg-slate-200/60 px-1.5 py-0.5 rounded">
                    Search Snippet
                  </span>
                </div>

                <div className="flex items-center gap-2">
                  <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold border ${badge.style}`}>
                    {badge.icon}
                    <span>{badge.label}</span>
                  </span>
                  {item.url && (
                    <a
                      href={item.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs font-semibold text-blue-600 hover:text-blue-800 flex items-center gap-1 hover:underline"
                    >
                      <span>Open Source</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                </div>
              </div>

              {/* Faithfully Quoted Snippet */}
              <div className="text-xs md:text-sm text-slate-800 italic bg-white p-3 rounded-lg border border-slate-200/70 border-l-4 border-l-blue-500">
                "{item.excerpt}"
              </div>

              {/* Direct Relevance Reason */}
              {item.relevance_reason && (
                <div className="text-[11px] text-slate-600">
                  <strong className="text-slate-700">Relevance: </strong>
                  {item.relevance_reason}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
