import React, { useEffect, useState } from 'react';
import { useParams, useSearchParams, Link, useNavigate } from 'react-router-dom';
import {
  FileText,
  Dna,
  GitCompare,
  GitFork,
  ArrowRight,
  PlusCircle,
  Calendar,
  Shield,
  AlertTriangle,
  RefreshCw,
  Share2,
  Printer,
  ChevronRight,
  HelpCircle
} from 'lucide-react';
import { api } from '../api/client';
import DemoBadge from '../components/DemoBadge';
import CredibilityScoreGauge from '../components/CredibilityScoreGauge';
import EvidenceCard from '../components/EvidenceCard';
import DiffHighlighter from '../components/DiffHighlighter';
import KeyEvidenceSummary from '../components/KeyEvidenceSummary';

export default function InvestigationReport() {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const [investigation, setInvestigation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Modal for adding a subsequent version
  const [showAddModal, setShowAddModal] = useState(false);
  const [newVersionText, setNewVersionText] = useState('');
  const [newVersionOrigin, setNewVersionOrigin] = useState('Forwarded Message');
  const [isAddingVersion, setIsAddingVersion] = useState(false);

  const demoId = searchParams.get('demo');

  const fetchInvestigation = async () => {
    try {
      setLoading(true);
      setError(null);

      let data;
      if (demoId) {
        data = await api.getDemo(demoId);
      } else if (id) {
        data = await api.getInvestigation(id);
      } else {
        // Fallback: load latest or Demo 1
        const all = await api.getInvestigations();
        if (all && all.length > 0) {
          data = await api.getInvestigation(all[0].id);
        } else {
          data = await api.getDemo('demo-1');
        }
      }

      setInvestigation(data);
    } catch (err) {
      setError(err.message || 'Failed to load investigation report.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInvestigation();
  }, [id, demoId]);

  const handleAddVersionSubmit = async (e) => {
    e.preventDefault();
    if (!newVersionText.trim() || newVersionText.trim().length < 5) return;

    try {
      setIsAddingVersion(true);
      const updated = await api.addVersion(investigation.id, {
        claim_text: newVersionText.trim(),
        source_origin: newVersionOrigin,
        recorded_date: new Date().toISOString().split('T')[0],
      });
      setInvestigation(updated);
      setShowAddModal(false);
      setNewVersionText('');
    } catch (err) {
      alert(err.message || 'Error adding version.');
    } finally {
      setIsAddingVersion(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-24 space-y-3">
        <RefreshCw className="w-8 h-8 text-blue-600 animate-spin" />
        <p className="text-sm font-semibold text-slate-700">Synthesizing Investigation Report...</p>
        <p className="text-xs text-slate-400">Verifying evidence records and tracing mutations</p>
      </div>
    );
  }

  if (error || !investigation) {
    return (
      <div className="max-w-2xl mx-auto py-12 text-center space-y-4">
        <div className="p-4 bg-rose-50 text-rose-700 rounded-xl border border-rose-200 text-xs">
          {error || 'Investigation could not be found.'}
        </div>
        <div className="space-x-3">
          <button
            onClick={fetchInvestigation}
            className="px-4 py-2 bg-slate-800 text-white rounded-lg text-xs font-semibold"
          >
            Retry
          </button>
          <Link
            to="/dashboard"
            className="px-4 py-2 bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold"
          >
            Return to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  const versions = investigation.versions || [];
  const evidence = investigation.evidence || [];
  const latestVersion = versions[versions.length - 1];
  const rootVersion = versions[0];
  const latestMutation = latestVersion?.changes_from_previous;

  // Determine coherent evidence mode
  const hasLive = evidence.some(e => !e.is_demo);
  const hasDemo = evidence.some(e => e.is_demo);
  const derivedMode = investigation.evidence_mode || (
    (hasLive && hasDemo) ? 'mixed' : (hasLive ? 'live' : 'offline_demo')
  );

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-16">
      {/* Header Info Banner */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 md:p-8 shadow-sm space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-blue-600 uppercase tracking-wider font-mono">
              Investigation Dossier #{investigation.id.slice(0, 8)}
            </span>
            <DemoBadge mode={derivedMode} isDemo={derivedMode === 'offline_demo'} />
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => window.print()}
              className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 rounded-lg text-xs font-semibold text-slate-700 transition-colors flex items-center gap-1.5"
            >
              <Printer className="w-3.5 h-3.5" />
              <span>Print Dossier</span>
            </button>
            <button
              onClick={() => setShowAddModal(true)}
              className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold transition-colors flex items-center gap-1.5 shadow-xs"
            >
              <PlusCircle className="w-3.5 h-3.5" />
              <span>Track Next Evolution</span>
            </button>
          </div>
        </div>

        <div>
          <h2 className="text-2xl font-extrabold text-slate-900 leading-snug">
            {investigation.title}
          </h2>
          <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 mt-2">
            <span className="flex items-center gap-1">
              <Calendar className="w-3.5 h-3.5 text-slate-400" />
              Recorded: {new Date(investigation.created_at).toLocaleDateString()}
            </span>
            <span className="flex items-center gap-1">
              <GitFork className="w-3.5 h-3.5 text-slate-400" />
              Lineage: {versions.length} recorded version(s)
            </span>
            <span className="flex items-center gap-1">
              <Shield className="w-3.5 h-3.5 text-slate-400" />
              Evidence records: {evidence.length} sources
            </span>
          </div>
        </div>

        {/* Root Statement Card */}
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-sm">
          <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1">
            Current Investigated Statement:
          </div>
          <p className="font-semibold text-slate-900 leading-relaxed">
            "{latestVersion?.claim_text || investigation.summary}"
          </p>
          <div className="mt-2 text-xs text-slate-500 flex items-center gap-2">
            <span>Origin: {latestVersion?.source_origin || 'Direct Submission'}</span>
            <span>•</span>
            <span className="capitalize">Type: {latestVersion?.origin_type || 'User Submitted'}</span>
          </div>
        </div>
      </div>

      {/* Main Investigation Summary Section: Verdict, Confidence, Reason, and Score */}
      <CredibilityScoreGauge
        score={investigation.score}
        verdict={investigation.verdict}
        confidence={investigation.confidence}
        confidenceScore={investigation.confidence_score}
        verdictReason={investigation.verdict_reason}
        analysisMode={investigation.analysis_mode}
        scoreBreakdown={investigation.score_breakdown}
      />

      {/* Main Summary: Curated Top Excerpts Driving The Verdict */}
      <KeyEvidenceSummary
        excerpts={investigation.key_excerpts || investigation.score_breakdown?.key_excerpts}
      />

      {/* Feature D: Human Truth Explanation */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 md:p-8 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div>
            <div className="text-[11px] font-bold text-blue-600 uppercase tracking-wider">
              Feature D — Human Truth Explanation
            </div>
            <h3 className="text-lg font-bold text-slate-900 mt-0.5">
              Evidence-First Truth Summary
            </h3>
          </div>
          <span className="text-xs text-slate-400 font-mono">No AI Buzzwords</span>
        </div>

        <div className="bg-blue-50/50 border border-blue-200/60 rounded-xl p-5 text-sm md:text-base text-slate-800 leading-relaxed font-sans">
          {investigation.human_explanation || (
            <span className="text-slate-500 italic">No human explanation generated yet.</span>
          )}
        </div>

        <div className="text-xs text-slate-500 flex items-center gap-2 pt-1">
          <HelpCircle className="w-4 h-4 text-slate-400" />
          <span>
            Writing Rules Enforced: Evidence presented before conclusions • Honest uncertainty admitted • Plain language for non-technical readers.
          </span>
        </div>
      </div>

      {/* Quick Feature Jump Navigation */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Link
          to={`/mutations?original=${encodeURIComponent(rootVersion?.claim_text || '')}&modified=${encodeURIComponent(latestVersion?.claim_text || '')}`}
          className="p-4 bg-white rounded-xl border border-slate-200 hover:border-blue-400 hover:shadow-sm transition-all group flex items-center justify-between"
        >
          <div>
            <div className="text-[11px] font-bold text-amber-600 uppercase tracking-wider">Feature B</div>
            <div className="text-sm font-bold text-slate-900 mt-0.5 group-hover:text-blue-600">Mutation Detector</div>
            <div className="text-[11px] text-slate-500 mt-0.5">Inspect 4-color diff analysis</div>
          </div>
          <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all" />
        </Link>

        <Link
          to={`/journey?id=${investigation.id}`}
          className="p-4 bg-white rounded-xl border border-slate-200 hover:border-blue-400 hover:shadow-sm transition-all group flex items-center justify-between"
        >
          <div>
            <div className="text-[11px] font-bold text-emerald-600 uppercase tracking-wider">Feature C</div>
            <div className="text-sm font-bold text-slate-900 mt-0.5 group-hover:text-blue-600">Rumour Journey Map</div>
            <div className="text-[11px] text-slate-500 mt-0.5">Interactive timeline of {versions.length} versions</div>
          </div>
          <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all" />
        </Link>

        <Link
          to={`/dna?id=${investigation.id}`}
          className="p-4 bg-white rounded-xl border border-slate-200 hover:border-blue-400 hover:shadow-sm transition-all group flex items-center justify-between"
        >
          <div>
            <div className="text-[11px] font-bold text-indigo-600 uppercase tracking-wider">Feature A</div>
            <div className="text-sm font-bold text-slate-900 mt-0.5 group-hover:text-blue-600">Rumour DNA</div>
            <div className="text-[11px] text-slate-500 mt-0.5">Fingerprint & visual family tree</div>
          </div>
          <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all" />
        </Link>
      </div>

      {/* Feature B: Mutation Details Preview if multiple versions exist */}
      {latestMutation && latestMutation.has_mutation && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 md:p-8 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <div className="text-[11px] font-bold text-amber-600 uppercase tracking-wider">
                Feature B — Mutation Details
              </div>
              <h3 className="text-lg font-bold text-slate-900 mt-0.5">
                Modifications Detected From Previous Version
              </h3>
            </div>
            <Link
              to={`/mutations?original=${encodeURIComponent(rootVersion?.claim_text || '')}&modified=${encodeURIComponent(latestVersion?.claim_text || '')}`}
              className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1"
            >
              Full Mutation View <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <DiffHighlighter diffTokens={latestMutation.diff_tokens} showLegend={true} />

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 space-y-2">
            <div><strong>Ordinary Language Explanation:</strong> {latestMutation.explanation}</div>
            <div className="flex flex-wrap gap-4 pt-1 text-[11px] text-slate-600">
              <span><strong>Scope Shift:</strong> {latestMutation.scope_change.from} → {latestMutation.scope_change.to} ({latestMutation.scope_change.direction})</span>
              {latestMutation.missing_conditions.length > 0 && (
                <span><strong>Conditions Stripped:</strong> {latestMutation.missing_conditions.join(', ')}</span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Full Verifiable Evidence Registry (Full source details preserved) */}
      <div className="space-y-4 pt-6 border-t border-slate-200">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-slate-900">Full Verifiable Evidence Registry</h3>
            <p className="text-xs text-slate-500">
              Complete catalog of all indexed sources, reliability assessments, snippets, and provenance
            </p>
          </div>
          <span className="text-xs font-mono text-slate-500 bg-slate-100 px-2.5 py-1 rounded-full">
            {evidence.length} Full Records
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {evidence.map((rec, idx) => (
            <EvidenceCard key={rec.id || idx} evidence={rec} />
          ))}
        </div>
      </div>

      {/* Add Version Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 space-y-4">
            <div>
              <span className="text-[11px] font-bold text-blue-600 uppercase tracking-wider">
                Evolution Tracker
              </span>
              <h3 className="text-lg font-bold text-slate-900 mt-0.5">
                Add Next Version to Claim Timeline
              </h3>
              <p className="text-xs text-slate-500">
                Track how this rumour mutated in subsequent forwards or social shares.
              </p>
            </div>

            <form onSubmit={handleAddVersionSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  New Version Claim Text <span className="text-rose-500">*</span>
                </label>
                <textarea
                  rows={3}
                  required
                  value={newVersionText}
                  onChange={(e) => setNewVersionText(e.target.value)}
                  placeholder="Enter the modified statement..."
                  className="w-full p-3 rounded-lg border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Forward Source / Origin
                </label>
                <input
                  type="text"
                  value={newVersionOrigin}
                  onChange={(e) => setNewVersionOrigin(e.target.value)}
                  placeholder="e.g. WhatsApp Group, Facebook Post"
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                />
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isAddingVersion}
                  className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5"
                >
                  <PlusCircle className="w-4 h-4" />
                  <span>{isAddingVersion ? 'Detecting Mutations...' : 'Append Version'}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
