import React, { useState } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  HelpCircle,
  AlertTriangle,
  ChevronDown,
  ChevronUp,
  Sparkles,
  Cpu,
  Layers,
  Award
} from 'lucide-react';

export default function CredibilityScoreGauge({
  score,
  verdict,
  confidence,
  confidenceScore,
  verdictReason,
  analysisMode,
  scoreBreakdown
}) {
  const [showDetails, setShowDetails] = useState(false);

  // Normalize verdict
  const v = (verdict || scoreBreakdown?.verdict || 'UNVERIFIED').toUpperCase();
  const isLikelyTrue = v.includes('TRUE') || v.includes('SUPPORTED');
  const isLikelyFalse = v.includes('FALSE') || v.includes('CONTRADICTED');
  const isMixed = v.includes('MIXED') || v.includes('PARTIAL');
  const isUnverified = !isLikelyTrue && !isLikelyFalse && !isMixed;

  // Normalized display label
  const displayVerdict = isLikelyTrue
    ? 'LIKELY TRUE'
    : isLikelyFalse
    ? 'LIKELY FALSE'
    : isMixed
    ? 'MIXED / PARTIALLY TRUE'
    : 'UNVERIFIED';

  // Confidence & Reason resolution
  const confLevel = (confidence || scoreBreakdown?.confidence || (isUnverified ? 'LOW' : 'MEDIUM')).toUpperCase();
  const confPct = confidenceScore ?? scoreBreakdown?.confidence_score ?? (confLevel === 'HIGH' ? 90 : confLevel === 'MEDIUM' ? 70 : 25);
  const reasonText = verdictReason || scoreBreakdown?.verdict_reason || scoreBreakdown?.explanation || '';
  const currentAnalysisMode = analysisMode || scoreBreakdown?.analysis_mode || 'offline_fallback';

  // Analysis mode badge rendering
  const renderAnalysisModeBadge = () => {
    if (currentAnalysisMode === 'live_search_ai') {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-purple-50 text-purple-700 border border-purple-200">
          <Sparkles className="w-3.5 h-3.5 text-purple-600" />
          <span>Live web search + AI-assisted analysis</span>
        </span>
      );
    }
    if (currentAnalysisMode === 'live_search_rules') {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
          <Cpu className="w-3.5 h-3.5 text-emerald-600" />
          <span>Live web search + rule-based analysis</span>
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-amber-50 text-amber-800 border border-amber-300">
        <Layers className="w-3.5 h-3.5 text-amber-600" />
        <span>Offline fallback analysis</span>
      </span>
    );
  };

  // Verdict style mapping
  const getVerdictStyle = () => {
    if (isLikelyTrue) {
      return {
        bg: 'bg-emerald-50/70',
        border: 'border-emerald-300',
        badgeBg: 'bg-emerald-600 text-white',
        text: 'text-emerald-950',
        barColor: 'bg-emerald-500',
        icon: <ShieldCheck className="w-8 h-8 text-emerald-600" />
      };
    }
    if (isLikelyFalse) {
      return {
        bg: 'bg-rose-50/70',
        border: 'border-rose-300',
        badgeBg: 'bg-rose-600 text-white',
        text: 'text-rose-950',
        barColor: 'bg-rose-500',
        icon: <ShieldAlert className="w-8 h-8 text-rose-600" />
      };
    }
    if (isMixed) {
      return {
        bg: 'bg-amber-50/70',
        border: 'border-amber-300',
        badgeBg: 'bg-amber-600 text-white',
        text: 'text-amber-950',
        barColor: 'bg-amber-500',
        icon: <AlertTriangle className="w-8 h-8 text-amber-600" />
      };
    }
    return {
      bg: 'bg-slate-50',
      border: 'border-slate-300',
      badgeBg: 'bg-slate-700 text-white',
      text: 'text-slate-900',
      barColor: 'bg-slate-400',
      icon: <HelpCircle className="w-8 h-8 text-slate-500" />
    };
  };

  const style = getVerdictStyle();

  const getConfidenceBadge = () => {
    if (confLevel === 'HIGH') {
      return {
        badge: 'bg-emerald-100 text-emerald-800 border-emerald-300',
        label: 'HIGH CONFIDENCE',
        bar: 'bg-emerald-500'
      };
    }
    if (confLevel === 'MEDIUM') {
      return {
        badge: 'bg-sky-100 text-sky-800 border-sky-300',
        label: 'MEDIUM CONFIDENCE',
        bar: 'bg-sky-500'
      };
    }
    return {
      badge: 'bg-slate-200 text-slate-700 border-slate-300',
      label: 'LOW CONFIDENCE',
      bar: 'bg-slate-400'
    };
  };

  const confStyle = getConfidenceBadge();

  return (
    <div className={`rounded-2xl border ${style.border} ${style.bg} p-6 md:p-8 shadow-sm space-y-6 transition-all`}>
      {/* Top Meta Bar: Analysis Mode */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200/70 pb-3">
        <div className="flex items-center gap-2">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 font-mono">
            Evidence Interpretation Engine
          </span>
        </div>
        {renderAnalysisModeBadge()}
      </div>

      {/* Main Verdict & Confidence Core */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
        <div className="flex items-start gap-4 flex-1">
          <div className="p-3 bg-white rounded-xl shadow-xs border border-slate-200/80 shrink-0">
            {style.icon}
          </div>

          <div className="space-y-1.5 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <span className={`px-3 py-1 rounded-md text-xs font-black uppercase tracking-wider ${style.badgeBg} shadow-xs`}>
                {displayVerdict}
              </span>
              <span className={`px-2.5 py-0.5 rounded text-[11px] font-bold uppercase border ${confStyle.badge}`}>
                {confStyle.label} ({confPct}%)
              </span>
            </div>

            <h3 className={`text-xl md:text-2xl font-black ${style.text} leading-tight pt-1`}>
              {scoreBreakdown?.status_label || (isUnverified ? "Not enough reliable evidence to assess this claim." : `${displayVerdict} by Available Evidence`)}
            </h3>

            {reasonText && (
              <p className="text-sm md:text-base text-slate-700 font-medium leading-relaxed bg-white/70 p-3 rounded-lg border border-slate-200/60 mt-2">
                <strong>Verdict Reason: </strong>{reasonText}
              </p>
            )}
          </div>
        </div>

        {/* Confidence & Score Dial */}
        <div className="flex flex-col sm:flex-row items-center gap-4 bg-white p-4 rounded-xl border border-slate-200 shadow-xs shrink-0 justify-between min-w-[240px]">
          {/* Confidence bar */}
          <div className="space-y-1 w-full sm:w-auto">
            <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              Evidence Confidence
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-extrabold text-slate-900 font-mono">{confLevel}</span>
              <span className="text-xs text-slate-500 font-mono">({confPct}%)</span>
            </div>
            <div className="w-28 h-2 bg-slate-100 rounded-full overflow-hidden">
              <div
                className={`h-full ${confStyle.bar} transition-all duration-700`}
                style={{ width: `${Math.min(100, Math.max(5, confPct))}%` }}
              />
            </div>
          </div>

          <div className="hidden sm:block w-px h-10 bg-slate-200 mx-2" />

          {/* Credibility score */}
          <div className="space-y-1 w-full sm:w-auto">
            <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              Reliability Score
            </div>
            <div className="flex items-baseline gap-1">
              <span className="text-2xl font-black text-slate-900 font-mono">
                {score !== null && score !== undefined ? score : '—'}
              </span>
              <span className="text-xs text-slate-400 font-mono">/ 100</span>
            </div>
            <div className="w-24 h-2 bg-slate-100 rounded-full overflow-hidden">
              <div
                className={`h-full ${style.barColor} transition-all duration-700`}
                style={{ width: `${score !== null && score !== undefined ? Math.min(100, Math.max(0, score)) : 0}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Signal Breakdown Toggle */}
      {scoreBreakdown && (
        <div className="pt-2 border-t border-slate-200/60">
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="flex items-center gap-1.5 text-xs font-bold text-slate-700 hover:text-slate-900 transition-colors"
          >
            {showDetails ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            <span>{showDetails ? 'Hide' : 'Inspect'} 6-Factor Signal Breakdown</span>
          </button>

          {showDetails && (
            <div className="mt-3 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5 pt-2 animate-fadeIn">
              <div className="bg-white p-3 rounded-lg border border-slate-200 shadow-xs">
                <div className="text-[10px] text-slate-500 font-bold uppercase">Source Reliability</div>
                <div className="text-sm font-bold text-slate-800 font-mono mt-0.5">
                  {scoreBreakdown.source_reliability ?? 0} <span className="text-[10px] text-slate-400">/ 25</span>
                </div>
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200 shadow-xs">
                <div className="text-[10px] text-slate-500 font-bold uppercase">Direct Relevance</div>
                <div className="text-sm font-bold text-slate-800 font-mono mt-0.5">
                  {scoreBreakdown.direct_relevance ?? 0} <span className="text-[10px] text-slate-400">/ 20</span>
                </div>
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200 shadow-xs">
                <div className="text-[10px] text-slate-500 font-bold uppercase">Corroboration</div>
                <div className="text-sm font-bold text-slate-800 font-mono mt-0.5">
                  {scoreBreakdown.independent_corroboration ?? 0} <span className="text-[10px] text-slate-400">/ 20</span>
                </div>
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200 shadow-xs">
                <div className="text-[10px] text-slate-500 font-bold uppercase">Contradiction Penalty</div>
                <div className="text-sm font-bold text-rose-600 font-mono mt-0.5">
                  {scoreBreakdown.contradictory_penalty ?? 0} <span className="text-[10px] text-slate-400">pts</span>
                </div>
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200 shadow-xs">
                <div className="text-[10px] text-slate-500 font-bold uppercase">Source Recency</div>
                <div className="text-sm font-bold text-slate-800 font-mono mt-0.5">
                  {scoreBreakdown.recency ?? 0} <span className="text-[10px] text-slate-400">/ 10</span>
                </div>
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200 shadow-xs">
                <div className="text-[10px] text-slate-500 font-bold uppercase">Completeness</div>
                <div className="text-sm font-bold text-slate-800 font-mono mt-0.5">
                  {scoreBreakdown.completeness ?? 0} <span className="text-[10px] text-slate-400">/ 10</span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
