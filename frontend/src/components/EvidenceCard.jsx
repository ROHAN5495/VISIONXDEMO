import React from 'react';
import { ExternalLink, CheckCircle2, XCircle, HelpCircle, Shield, Award, Calendar, Clock } from 'lucide-react';
import DemoBadge from './DemoBadge';

export default function EvidenceCard({ evidence }) {
  if (!evidence) return null;

  const getClassificationBadge = (type) => {
    switch (type) {
      case 'supporting':
        return {
          icon: <CheckCircle2 className="w-4 h-4 text-emerald-600" />,
          label: 'Supporting Evidence',
          bg: 'bg-emerald-50 text-emerald-800 border-emerald-200'
        };
      case 'contradictory':
        return {
          icon: <XCircle className="w-4 h-4 text-rose-600" />,
          label: 'Contradictory Evidence',
          bg: 'bg-rose-50 text-rose-800 border-rose-200'
        };
      case 'contextual':
        return {
          icon: <HelpCircle className="w-4 h-4 text-sky-600" />,
          label: 'Contextual Information',
          bg: 'bg-sky-50 text-sky-800 border-sky-200'
        };
      case 'irrelevant':
      default:
        return {
          icon: <HelpCircle className="w-4 h-4 text-slate-500" />,
          label: 'Irrelevant Source',
          bg: 'bg-slate-100 text-slate-700 border-slate-300'
        };
    }
  };

  const badge = getClassificationBadge(evidence.classification);

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:border-slate-300 transition-all flex flex-col justify-between">
      <div>
        {/* Top Header: Badge + Demo Status */}
        <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
          <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold border ${badge.bg}`}>
            {badge.icon}
            {badge.label}
          </span>
          <DemoBadge isDemo={evidence.is_demo} />
        </div>

        {/* Title & Publisher */}
        <h4 className="text-base font-bold text-slate-900 leading-snug hover:text-electric-600 transition-colors">
          <a href={evidence.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-baseline gap-1.5 group">
            <span>{evidence.title}</span>
            <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-electric-500 inline shrink-0" />
          </a>
        </h4>

        <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 mt-2 mb-3">
          <span className="font-semibold text-slate-700 flex items-center gap-1">
            <Shield className="w-3.5 h-3.5 text-slate-400" />
            {evidence.publisher}
          </span>
          {evidence.publication_date && (
            <span className="flex items-center gap-1">
              <Calendar className="w-3 h-3 text-slate-400" />
              Published: {evidence.publication_date}
            </span>
          )}
          <span className="flex items-center gap-1">
            <Clock className="w-3 h-3 text-slate-400" />
            Retrieved: {evidence.retrieval_date}
          </span>
        </div>

        {/* Excerpt */}
        <div className="bg-slate-50 border-l-4 border-slate-300 p-3 rounded-r-md text-sm text-slate-700 italic my-3 relative">
          <div className="flex items-center justify-between gap-2 mb-1.5 not-italic">
            <span className="text-[10px] font-mono uppercase font-bold tracking-wider text-slate-400 bg-slate-200/60 px-1.5 py-0.5 rounded">
              Search Snippet
            </span>
          </div>
          "{evidence.excerpt}"
        </div>

        {/* Relevance Reason */}
        <div className="text-xs text-slate-600 mt-2">
          <strong className="text-slate-700">Investigation Relevance: </strong>
          {evidence.relevance_reason}
        </div>
      </div>

      {/* Footer Metrics */}
      <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
        <div className="flex items-center gap-2">
          <span>Source Reliability:</span>
          <div className="flex items-center gap-1">
            <div className="w-16 h-1.5 bg-slate-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-electric-500"
                style={{ width: `${evidence.reliability_score || 70}%` }}
              />
            </div>
            <span className="font-mono font-semibold text-slate-700">{evidence.reliability_score || 70}%</span>
          </div>
        </div>

        {evidence.is_independent && (
          <span className="inline-flex items-center gap-1 text-[11px] text-emerald-700 font-medium">
            <Award className="w-3 h-3" />
            Independent Publisher
          </span>
        )}
      </div>
    </div>
  );
}
