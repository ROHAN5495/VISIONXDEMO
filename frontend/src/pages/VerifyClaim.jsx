import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  Send,
  Plus,
  Trash2,
  Sparkles,
  HelpCircle,
  Dna,
  ShieldAlert,
  Calendar,
  Layers,
  ArrowRight
} from 'lucide-react';
import { api } from '../api/client';
import WorkflowStepper from '../components/WorkflowStepper';

export default function VerifyClaim() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  // Root Claim (Version 1)
  const [claimText, setClaimText] = useState('');
  const [sourceOrigin, setSourceOrigin] = useState('User WhatsApp Forward');
  const [originType, setOriginType] = useState('user_submitted');
  const [recordedDate, setRecordedDate] = useState(new Date().toISOString().split('T')[0]);

  // Subsequent Evolution Versions (e.g. v2, v3)
  const [subsequentVersions, setSubsequentVersions] = useState([]);

  // Rumour DNA preview on demand
  const [dnaPreview, setDnaPreview] = useState(null);
  const [previewLoading, setPreviewLoading] = useState(false);

  // Submission state
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  // Pre-fill from query params if passed
  useEffect(() => {
    const passedClaim = searchParams.get('claim');
    if (passedClaim) {
      setClaimText(passedClaim);
    }
  }, [searchParams]);

  // Handle adding a subsequent version
  const handleAddVersion = () => {
    setSubsequentVersions([
      ...subsequentVersions,
      {
        claim_text: '',
        source_origin: `Follow-up Forward #${subsequentVersions.length + 2}`,
        origin_type: 'user_submitted',
        recorded_date: new Date().toISOString().split('T')[0],
      }
    ]);
  };

  const handleRemoveVersion = (index) => {
    setSubsequentVersions(subsequentVersions.filter((_, idx) => idx !== index));
  };

  const handleSubsequentChange = (index, field, value) => {
    const updated = [...subsequentVersions];
    updated[index][field] = value;
    setSubsequentVersions(updated);
  };

  // Generate on-demand DNA preview for Root Claim
  const handlePreviewDNA = async () => {
    if (!claimText.trim() || claimText.trim().length < 5) {
      setError('Please enter at least 5 characters to extract Rumour DNA.');
      return;
    }
    try {
      setPreviewLoading(true);
      setError(null);
      const res = await api.getClaimDNA(claimText.trim());
      setDnaPreview(res);
    } catch (err) {
      setError(err.message || 'Failed to extract Rumour DNA');
    } finally {
      setPreviewLoading(false);
    }
  };

  // Submit full investigation
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!claimText.trim() || claimText.trim().length < 5) {
      setError('Please enter a valid claim statement (minimum 5 characters).');
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);

      const payload = {
        claim_text: claimText.trim(),
        source_origin: sourceOrigin,
        origin_type: originType,
        recorded_date: recordedDate,
        is_demo: false,
        subsequent_versions: subsequentVersions.filter(v => v.claim_text.trim().length >= 5)
      };

      const result = await api.createInvestigation(payload);
      if (result && result.id) {
        navigate(`/report/${result.id}`);
      } else {
        throw new Error('Failed to create investigation.');
      }
    } catch (err) {
      setError(err.message || 'An error occurred during verification.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Load a quick example template
  const loadExampleTemplate = (type) => {
    if (type === 'school') {
      setClaimText('Oakridge High School will remain closed for two days for preventive pest fumigation.');
      setSourceOrigin('Parent Circular');
      setOriginType('observed');
      setSubsequentVersions([
        {
          claim_text: 'All schools in the district are closed until further notice due to health hazards.',
          source_origin: 'Forwarded Voice Note',
          origin_type: 'user_submitted',
          recorded_date: new Date().toISOString().split('T')[0]
        }
      ]);
    } else if (type === 'grant') {
      setClaimText('State Disaster Authority announces $5,000 relief grant for registered homeowners in 3 flood-hit counties.');
      setSourceOrigin('Gazette Notification');
      setOriginType('observed');
      setSubsequentVersions([
        {
          claim_text: 'Government announces immediate $5,000 cash grant for all state residents, no registration required.',
          source_origin: 'Viral Text Message',
          origin_type: 'user_submitted',
          recorded_date: new Date().toISOString().split('T')[0]
        }
      ]);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-16">
      {/* Visual Pipeline Protocol Header */}
      <WorkflowStepper currentStep="submit" />

      {/* Main Verification Card */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 md:p-8 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6 pb-4 border-b border-slate-100">
          <div>
            <span className="text-[11px] font-bold text-blue-600 uppercase tracking-wider">
              Step 1: Submit Claim
            </span>
            <h2 className="text-xl font-bold text-slate-900 mt-0.5">
              Initiate Misinformation Investigation
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Compare statement against trusted sources, detect contradictory evidence, and track mutations.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400 font-medium hidden sm:inline">Templates:</span>
            <button
              type="button"
              onClick={() => loadExampleTemplate('school')}
              className="text-xs px-2.5 py-1 bg-slate-100 hover:bg-slate-200 rounded text-slate-700 font-medium transition-colors"
            >
              School Closure
            </button>
            <button
              type="button"
              onClick={() => loadExampleTemplate('grant')}
              className="text-xs px-2.5 py-1 bg-slate-100 hover:bg-slate-200 rounded text-slate-700 font-medium transition-colors"
            >
              Relief Grant
            </button>
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-rose-50 border border-rose-200 rounded-xl text-rose-700 text-xs flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 shrink-0 text-rose-600" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Version 1: Root Claim */}
          <div className="p-5 rounded-xl border border-slate-200 bg-slate-50/50 space-y-4">
            <div className="flex items-center justify-between">
              <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800">
                <span className="w-2 h-2 rounded-full bg-blue-600" />
                Version 1 (Initial / Observed Statement)
              </span>
              <span className="text-[11px] text-slate-400 font-mono">ROOT ANCHOR</span>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Statement / Message Text <span className="text-rose-500">*</span>
              </label>
              <textarea
                rows={3}
                required
                value={claimText}
                onChange={(e) => setClaimText(e.target.value)}
                placeholder="Example: Oakridge High School will remain closed for two days for routine preventive pest fumigation..."
                className="w-full p-3.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm shadow-inner bg-white"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div>
                <label className="block text-[11px] font-semibold text-slate-600 mb-1">
                  Source / Origin
                </label>
                <input
                  type="text"
                  value={sourceOrigin}
                  onChange={(e) => setSourceOrigin(e.target.value)}
                  placeholder="e.g. Official Circular, WhatsApp"
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs bg-white"
                />
              </div>

              <div>
                <label className="block text-[11px] font-semibold text-slate-600 mb-1">
                  Evidence Origin Type
                </label>
                <select
                  value={originType}
                  onChange={(e) => setOriginType(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs bg-white"
                >
                  <option value="observed">Observed (Direct official notice)</option>
                  <option value="user_submitted">User-Submitted (Forwarded message)</option>
                  <option value="ai_inferred">AI-Inferred (Algorithmic cluster)</option>
                </select>
              </div>

              <div>
                <label className="block text-[11px] font-semibold text-slate-600 mb-1">
                  Date Recorded
                </label>
                <input
                  type="date"
                  value={recordedDate}
                  onChange={(e) => setRecordedDate(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs bg-white"
                />
              </div>
            </div>

            {/* Live DNA extraction button */}
            <div className="pt-2 flex items-center justify-between">
              <button
                type="button"
                onClick={handlePreviewDNA}
                disabled={previewLoading || !claimText.trim()}
                className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-600 hover:text-blue-800 disabled:opacity-50"
              >
                <Dna className="w-3.5 h-3.5" />
                <span>{previewLoading ? 'Extracting DNA...' : 'Preview Rumour DNA Fingerprint'}</span>
              </button>

              {dnaPreview && (
                <span className="text-[11px] font-mono text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  Subject: {dnaPreview.subject} | Scope: {dnaPreview.scope}
                </span>
              )}
            </div>

            {/* DNA Card Preview if generated */}
            {dnaPreview && (
              <div className="p-4 bg-white rounded-lg border border-blue-200 text-xs space-y-2 mt-2">
                <div className="font-bold text-slate-800">Rumour DNA Fingerprint Preview:</div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-slate-600">
                  <div><strong>Subject:</strong> {dnaPreview.subject}</div>
                  <div><strong>Scope:</strong> {dnaPreview.scope}</div>
                  <div><strong>Location:</strong> {dnaPreview.location || 'None'}</div>
                  <div><strong>Dates:</strong> {dnaPreview.date_time || 'None'}</div>
                </div>
                <div className="text-[11px] text-slate-500 font-mono">
                  Semantic Hash: {dnaPreview.semantic_hash}
                </div>
              </div>
            )}
          </div>

          {/* Subsequent Evolutionary Versions */}
          {subsequentVersions.map((v, index) => (
            <div key={index} className="p-5 rounded-xl border border-amber-200 bg-amber-50/30 space-y-4 relative">
              <div className="flex items-center justify-between">
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-900 border border-amber-300">
                  <span className="w-2 h-2 rounded-full bg-amber-600" />
                  Version {index + 2} (Evolved Forward / Modified Mutation)
                </span>
                <button
                  type="button"
                  onClick={() => handleRemoveVersion(index)}
                  className="p-1 text-slate-400 hover:text-rose-600 transition-colors"
                  title="Remove this version"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                  Forwarded Text <span className="text-rose-500">*</span>
                </label>
                <textarea
                  rows={2}
                  value={v.claim_text}
                  onChange={(e) => handleSubsequentChange(index, 'claim_text', e.target.value)}
                  placeholder="Example: All schools in the district are closed until further notice due to health hazards..."
                  className="w-full p-3 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm shadow-inner bg-white"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="block text-[11px] font-semibold text-slate-600 mb-1">
                    Forward Origin
                  </label>
                  <input
                    type="text"
                    value={v.source_origin}
                    onChange={(e) => handleSubsequentChange(index, 'source_origin', e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs bg-white"
                  />
                </div>

                <div>
                  <label className="block text-[11px] font-semibold text-slate-600 mb-1">
                    Origin Type
                  </label>
                  <select
                    value={v.origin_type}
                    onChange={(e) => handleSubsequentChange(index, 'origin_type', e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs bg-white"
                  >
                    <option value="user_submitted">User-Submitted</option>
                    <option value="observed">Observed</option>
                    <option value="ai_inferred">AI-Inferred</option>
                  </select>
                </div>

                <div>
                  <label className="block text-[11px] font-semibold text-slate-600 mb-1">
                    Recorded Date
                  </label>
                  <input
                    type="date"
                    value={v.recorded_date}
                    onChange={(e) => handleSubsequentChange(index, 'recorded_date', e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs bg-white"
                  />
                </div>
              </div>
            </div>
          ))}

          {/* Add Another Version Button */}
          <div className="flex justify-start">
            <button
              type="button"
              onClick={handleAddVersion}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg border border-dashed border-slate-300 text-xs font-semibold text-slate-600 hover:text-slate-900 hover:border-slate-400 bg-white hover:bg-slate-50 transition-colors"
            >
              <Plus className="w-4 h-4 text-blue-600" />
              <span>Add Subsequent Evolution Version (Track Spread)</span>
            </button>
          </div>

          {/* Submit Action */}
          <div className="pt-6 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="text-xs text-slate-500">
              <strong className="text-slate-700">Protocol: </strong>
              Autonomous retrieval, contradiction check, and mutation analysis will execute immediately.
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full sm:w-auto px-8 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm shadow-md transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              <Send className="w-4 h-4" />
              <span>{isSubmitting ? 'Analyzing Claim Journey...' : 'Run Investigation Workflow'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
