import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  GitCompare,
  ArrowRight,
  AlertTriangle,
  CheckCircle,
  HelpCircle,
  Plus,
  Minus,
  Maximize2,
  Calendar,
  Hash,
  MapPin,
  Users
} from 'lucide-react';
import { api } from '../api/client';
import DiffHighlighter from '../components/DiffHighlighter';

export default function MutationDetector() {
  const [searchParams] = useSearchParams();

  const [originalText, setOriginalText] = useState(
    'Oakridge High School will remain closed for two days for routine preventive pest fumigation.'
  );
  const [modifiedText, setModifiedText] = useState(
    'All schools in the district are closed until further notice due to severe chemical health hazards.'
  );

  const [mutationReport, setMutationReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const orig = searchParams.get('original');
    const mod = searchParams.get('modified');
    if (orig && mod) {
      setOriginalText(orig);
      setModifiedText(mod);
      handleCompare(orig, mod);
    } else {
      handleCompare(originalText, modifiedText);
    }
  }, [searchParams]);

  const handleCompare = async (orig = originalText, mod = modifiedText) => {
    if (!orig.trim() || !mod.trim()) return;

    try {
      setLoading(true);
      setError(null);
      const res = await api.compareClaims(orig.trim(), mod.trim());
      setMutationReport(res);
    } catch (err) {
      setError(err.message || 'Failed to analyze mutations.');
    } finally {
      setLoading(false);
    }
  };

  const loadPreset = (type) => {
    if (type === 'school') {
      const o = 'Oakridge High School will remain closed for two days for routine preventive pest fumigation.';
      const m = 'All schools in the district are closed until further notice due to severe chemical health hazards.';
      setOriginalText(o);
      setModifiedText(m);
      handleCompare(o, m);
    } else if (type === 'grant') {
      const o = 'State Disaster Authority announces $5,000 relief grant for registered homeowners in 3 flood-hit counties who filed before Feb 15.';
      const m = 'Government announces immediate $5,000 cash grant for all state residents, no prior registration required.';
      setOriginalText(o);
      setModifiedText(m);
      handleCompare(o, m);
    } else if (type === 'cure') {
      const o = 'In an 18-patient Phase 1 clinical trial, compound TX-94 demonstrated safe preliminary tolerability; efficacy testing has not yet begun.';
      const m = 'Miracle cure TX-94 receives breakthrough approval after curing terminal cancer patients in clinical trials.';
      setOriginalText(o);
      setModifiedText(m);
      handleCompare(o, m);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-16">
      {/* Header */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 md:p-8 shadow-sm">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-amber-50 text-amber-600 rounded-xl">
            <GitCompare className="w-8 h-8" />
          </div>
          <div>
            <span className="text-[11px] font-bold text-amber-600 uppercase tracking-wider">
              Signature Feature B
            </span>
            <h2 className="text-2xl font-extrabold text-slate-900 mt-0.5">
              Mutation Detector & Scope Differencing
            </h2>
            <p className="text-xs text-slate-500 mt-1 max-w-2xl leading-relaxed">
              Compare any two claim versions side-by-side. The mutation detector identifies added details, removed conditions, altered numbers, and scope escalation using color-coded visual tokens.
            </p>
          </div>
        </div>

        {/* Presets */}
        <div className="mt-6 pt-4 border-t border-slate-100 flex flex-wrap items-center gap-2 text-xs">
          <span className="text-slate-400 font-medium">Load Mutation Scenarios:</span>
          <button
            onClick={() => loadPreset('school')}
            className="px-3 py-1 bg-slate-100 hover:bg-slate-200 rounded-lg text-slate-700 font-medium transition-colors"
          >
            Scenario 1: School Scope Escalation
          </button>
          <button
            onClick={() => loadPreset('grant')}
            className="px-3 py-1 bg-slate-100 hover:bg-slate-200 rounded-lg text-slate-700 font-medium transition-colors"
          >
            Scenario 2: Eligibility Condition Stripped
          </button>
          <button
            onClick={() => loadPreset('cure')}
            className="px-3 py-1 bg-slate-100 hover:bg-slate-200 rounded-lg text-slate-700 font-medium transition-colors"
          >
            Scenario 3: Trial Exaggeration to Cure
          </button>
        </div>
      </div>

      {/* Input Comparison Fields */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Version A: Original */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              Version A (Original / Earlier Statement)
            </span>
            <span className="text-[10px] text-slate-400 font-mono">BASELINE</span>
          </div>
          <textarea
            rows={4}
            value={originalText}
            onChange={(e) => setOriginalText(e.target.value)}
            placeholder="Paste original claim..."
            className="w-full p-3 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 shadow-inner"
          />
        </div>

        {/* Version B: Modified */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-amber-700 uppercase tracking-wider">
              Version B (Modified / Forwarded Variant)
            </span>
            <span className="text-[10px] text-amber-500 font-mono">MUTATION</span>
          </div>
          <textarea
            rows={4}
            value={modifiedText}
            onChange={(e) => setModifiedText(e.target.value)}
            placeholder="Paste modified claim..."
            className="w-full p-3 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 shadow-inner"
          />
        </div>
      </div>

      <div className="flex justify-center">
        <button
          onClick={() => handleCompare(originalText, modifiedText)}
          disabled={loading}
          className="px-8 py-3 bg-amber-600 hover:bg-amber-700 text-white rounded-xl text-xs font-bold shadow-md transition-all flex items-center gap-2 disabled:opacity-50"
        >
          <GitCompare className="w-4 h-4" />
          <span>{loading ? 'Analyzing Mutations...' : 'Compare Claim Versions'}</span>
        </button>
      </div>

      {error && (
        <div className="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs">
          {error}
        </div>
      )}

      {/* Mutation Analysis Results */}
      {mutationReport && (
        <div className="space-y-6">
          {/* Visual Diff Card */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 md:p-8 shadow-sm space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                  Visual Differencing
                </span>
                <h3 className="text-base font-bold text-slate-900">4-Color Mutation Breakdown</h3>
              </div>
              <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                mutationReport.scope_change.direction === 'expanded'
                  ? 'bg-amber-100 text-amber-900 border border-amber-300'
                  : 'bg-slate-100 text-slate-700'
              }`}>
                Scope: {mutationReport.scope_change.from} → {mutationReport.scope_change.to} ({mutationReport.scope_change.direction})
              </span>
            </div>

            <DiffHighlighter diffTokens={mutationReport.diff_tokens} showLegend={true} />

            {/* Ordinary Language Explanation */}
            <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200/80 text-xs md:text-sm text-amber-950 leading-relaxed font-sans">
              <strong className="font-bold text-amber-900">Human Truth Explanation: </strong>
              {mutationReport.explanation}
            </div>
          </div>

          {/* Granular Mutation Dimensions Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
            {/* Scope Change */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
              <div className="flex items-center gap-1.5 text-xs text-slate-500 font-semibold mb-2">
                <Maximize2 className="w-3.5 h-3.5 text-blue-500" />
                Scope Shift
              </div>
              <div className="text-xs font-bold text-slate-900 capitalize">
                {mutationReport.scope_change.direction}
              </div>
              <div className="text-[11px] text-slate-500 mt-1">
                From {mutationReport.scope_change.from} to {mutationReport.scope_change.to}
              </div>
            </div>

            {/* Missing Conditions */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
              <div className="flex items-center gap-1.5 text-xs text-rose-600 font-semibold mb-2">
                <Minus className="w-3.5 h-3.5" />
                Conditions Stripped
              </div>
              {mutationReport.missing_conditions.length > 0 ? (
                <div className="flex flex-wrap gap-1">
                  {mutationReport.missing_conditions.map((c, i) => (
                    <span key={i} className="px-1.5 py-0.5 rounded bg-rose-50 text-rose-800 text-[11px] font-mono border border-rose-200">
                      {c}
                    </span>
                  ))}
                </div>
              ) : (
                <div className="text-[11px] text-slate-400 italic">None stripped</div>
              )}
            </div>

            {/* Unsupported Additions */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
              <div className="flex items-center gap-1.5 text-xs text-amber-600 font-semibold mb-2">
                <Plus className="w-3.5 h-3.5" />
                Escalating Modifiers
              </div>
              {mutationReport.unsupported_additions.length > 0 ? (
                <div className="flex flex-wrap gap-1">
                  {mutationReport.unsupported_additions.map((a, i) => (
                    <span key={i} className="px-1.5 py-0.5 rounded bg-amber-50 text-amber-800 text-[11px] font-mono border border-amber-200">
                      {a}
                    </span>
                  ))}
                </div>
              ) : (
                <div className="text-[11px] text-slate-400 italic">No alarming escalation</div>
              )}
            </div>

            {/* Changed Numbers */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
              <div className="flex items-center gap-1.5 text-xs text-indigo-600 font-semibold mb-2">
                <Hash className="w-3.5 h-3.5" />
                Numbers Altered
              </div>
              {mutationReport.changed_numbers.length > 0 ? (
                <div className="text-[11px] text-slate-700">
                  {mutationReport.changed_numbers[0].original.join(', ')} → {mutationReport.changed_numbers[0].modified.join(', ')}
                </div>
              ) : (
                <div className="text-[11px] text-slate-400 italic">Numbers consistent</div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
