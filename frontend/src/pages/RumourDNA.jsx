import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Dna,
  Search,
  Sparkles,
  Layers,
  MapPin,
  Calendar,
  Hash,
  Globe,
  Tag,
  ShieldAlert,
  ArrowRight
} from 'lucide-react';
import { api } from '../api/client';
import VisualFamilyTree from '../components/VisualFamilyTree';

export default function RumourDNA() {
  const [searchParams] = useSearchParams();
  const investigationId = searchParams.get('id');

  const [inputClaim, setInputClaim] = useState(
    'Oakridge High School will remain closed for two days for preventive pest fumigation.'
  );
  const [dnaData, setDnaData] = useState(null);
  const [familyData, setFamilyData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // If investigation ID passed in query, fetch that investigation's DNA
  useEffect(() => {
    if (investigationId) {
      api.getInvestigation(investigationId).then((inv) => {
        if (inv && inv.versions && inv.versions.length > 0) {
          const v = inv.versions[inv.versions.length - 1];
          setInputClaim(v.claim_text);
          if (v.dna) {
            setDnaData(v.dna);
            if (v.id) {
              api.getClaimFamily(v.id).then(setFamilyData).catch(() => {});
            }
          }
        }
      }).catch(() => {});
    } else {
      handleAnalyze(inputClaim);
    }
  }, [investigationId]);

  const handleAnalyze = async (textToAnalyze) => {
    const text = textToAnalyze || inputClaim;
    if (!text.trim() || text.trim().length < 5) return;

    try {
      setLoading(true);
      setError(null);
      const res = await api.getClaimDNA(text.trim());
      setDnaData(res);
      // Fallback family lookup if no database version ID
      setFamilyData(null);
    } catch (err) {
      setError(err.message || 'Failed to extract Rumour DNA');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-16">
      {/* Header */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 md:p-8 shadow-sm">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl">
            <Dna className="w-8 h-8" />
          </div>
          <div>
            <span className="text-[11px] font-bold text-indigo-600 uppercase tracking-wider">
              Signature Feature A
            </span>
            <h2 className="text-2xl font-extrabold text-slate-900 mt-0.5">
              Rumour DNA & Entity Fingerprint
            </h2>
            <p className="text-xs text-slate-500 mt-1 max-w-2xl leading-relaxed">
              Every statement leaves a distinct semantic and factual imprint. Rumour DNA normalizes text, extracts key entities, identifies geographical scope, and clusters related claims into visual families even when phrasing shifts.
            </p>
          </div>
        </div>

        {/* Live Input Form */}
        <div className="mt-6 pt-6 border-t border-slate-100">
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
            Analyze Statement Rumour DNA
          </label>
          <div className="flex flex-col sm:flex-row gap-3">
            <input
              type="text"
              value={inputClaim}
              onChange={(e) => setInputClaim(e.target.value)}
              placeholder="Enter any claim to generate its Rumour DNA fingerprint..."
              className="flex-1 px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-inner"
            />
            <button
              onClick={() => handleAnalyze(inputClaim)}
              disabled={loading}
              className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold flex items-center justify-center gap-2 shadow-sm transition-colors disabled:opacity-50"
            >
              <Dna className="w-4 h-4" />
              <span>{loading ? 'Fingerprinting...' : 'Extract DNA'}</span>
            </button>
          </div>

          <div className="mt-3 flex flex-wrap gap-2 text-xs">
            <span className="text-slate-400">Try Quick Examples:</span>
            <button
              onClick={() => {
                const s = "Oakridge High School will remain closed for two days for routine preventive pest fumigation.";
                setInputClaim(s);
                handleAnalyze(s);
              }}
              className="text-indigo-600 hover:underline"
            >
              School Fumigation
            </button>
            <span>•</span>
            <button
              onClick={() => {
                const s = "All schools in the state are closed indefinitely by government order.";
                setInputClaim(s);
                handleAnalyze(s);
              }}
              className="text-indigo-600 hover:underline"
            >
              Statewide Shutdown
            </button>
            <span>•</span>
            <button
              onClick={() => {
                const s = "Miracle compound TX-94 receives breakthrough FDA approval after curing cancer.";
                setInputClaim(s);
                handleAnalyze(s);
              }}
              className="text-indigo-600 hover:underline"
            >
              Clinical Miracle Claim
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs flex items-center gap-2">
          <ShieldAlert className="w-4 h-4" />
          <span>{error}</span>
        </div>
      )}

      {/* DNA Breakdown Display */}
      {dnaData && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Core Properties Card */}
          <div className="md:col-span-2 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
            <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
              <div>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                  Fingerprint Analysis
                </span>
                <h3 className="text-base font-bold text-slate-900">Extracted Structural Dimensions</h3>
              </div>
              <span className="px-2.5 py-1 bg-indigo-50 text-indigo-700 text-xs font-mono font-semibold rounded-full border border-indigo-200">
                Hash: {dnaData.semantic_hash}
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-100">
                <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium mb-1">
                  <Tag className="w-3.5 h-3.5 text-indigo-500" />
                  Primary Subject
                </div>
                <div className="text-sm font-bold text-slate-900">{dnaData.subject}</div>
              </div>

              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-100">
                <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium mb-1">
                  <Globe className="w-3.5 h-3.5 text-blue-500" />
                  Geographic / Institutional Scope
                </div>
                <div className="text-sm font-bold text-slate-900 capitalize">
                  {dnaData.scope} Scope
                </div>
              </div>

              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-100">
                <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium mb-1">
                  <MapPin className="w-3.5 h-3.5 text-rose-500" />
                  Location
                </div>
                <div className="text-sm font-bold text-slate-900">
                  {dnaData.location || <span className="text-slate-400 font-normal italic">None identified</span>}
                </div>
              </div>

              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-100">
                <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium mb-1">
                  <Calendar className="w-3.5 h-3.5 text-emerald-500" />
                  Date / Time Anchor
                </div>
                <div className="text-sm font-bold text-slate-900">
                  {dnaData.date_time || <span className="text-slate-400 font-normal italic">None specified</span>}
                </div>
              </div>
            </div>

            {/* Factual Assertion Box */}
            <div className="p-4 bg-indigo-50/50 rounded-xl border border-indigo-100 text-xs space-y-1">
              <div className="font-bold text-indigo-900 uppercase tracking-wider text-[10px]">
                Core Factual Assertion (Predicate)
              </div>
              <p className="text-sm font-medium text-slate-800 leading-relaxed">
                "{dnaData.factual_assertion}"
              </p>
            </div>

            {/* Normalized Text */}
            <div className="text-xs text-slate-500">
              <strong className="text-slate-700">Normalized Text: </strong>
              <code className="text-slate-600 bg-slate-100 px-2 py-0.5 rounded font-mono text-[11px]">
                {dnaData.normalized_text}
              </code>
            </div>
          </div>

          {/* Named Entities Badge Stack */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
            <div>
              <div className="border-b border-slate-100 pb-3 mb-4">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                  Extracted Entities
                </span>
                <h3 className="text-base font-bold text-slate-900">Named Components</h3>
              </div>

              {dnaData.entities && dnaData.entities.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {dnaData.entities.map((ent, idx) => (
                    <span
                      key={idx}
                      className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold bg-slate-100 text-slate-800 border border-slate-200"
                    >
                      <span className="text-[10px] uppercase font-bold text-slate-400">
                        {ent.category}:
                      </span>
                      <span>{ent.name}</span>
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-400 italic">No named entities extracted.</p>
              )}

              {/* Quantities & Numbers */}
              <div className="mt-6 pt-4 border-t border-slate-100">
                <div className="text-xs font-bold text-slate-700 mb-2 flex items-center gap-1">
                  <Hash className="w-3.5 h-3.5 text-slate-400" />
                  Numbers & Statistics
                </div>
                {dnaData.numbers_stats && dnaData.numbers_stats.length > 0 ? (
                  <div className="flex flex-wrap gap-1.5">
                    {dnaData.numbers_stats.map((num, i) => (
                      <span key={i} className="px-2 py-0.5 bg-amber-50 text-amber-800 font-mono text-xs rounded border border-amber-200">
                        {num}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-slate-400 italic">No explicit numbers stated.</p>
                )}
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-100 text-[11px] text-slate-400 leading-relaxed">
              <strong>Rule:</strong> Do not assume similar wording means identical facts. Claims with overlapping subjects may have radically different scopes.
            </div>
          </div>
        </div>
      )}

      {/* Visual Family Tree Component */}
      <VisualFamilyTree
        targetVersion={{
          claim_text: inputClaim,
          dna: dnaData
        }}
        familyMembers={familyData?.family_members || []}
      />
    </div>
  );
}
