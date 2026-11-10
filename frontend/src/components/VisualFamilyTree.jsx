import React from 'react';
import { Network, ArrowRight, Dna, GitCommit } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function VisualFamilyTree({ targetVersion, familyMembers = [] }) {
  if (!targetVersion) return null;

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
            <Network className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900">Rumour DNA Family Map</h3>
            <p className="text-xs text-slate-500">Related claims identified through entity extraction and semantic similarity</p>
          </div>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 rounded-full text-slate-600">
          {familyMembers.length} Related Variants Found
        </span>
      </div>

      {/* Root Node */}
      <div className="p-4 bg-investigative-900 text-white rounded-xl shadow-md border border-investigative-800 mb-6">
        <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
          <span className="flex items-center gap-1 font-mono uppercase tracking-wider text-electric-glow">
            <Dna className="w-3.5 h-3.5" />
            Root Claim Fingerprint
          </span>
          <span className="bg-investigative-800 px-2 py-0.5 rounded text-[11px] text-slate-300">
            Scope: {targetVersion.dna?.scope || 'Standard'}
          </span>
        </div>
        <p className="text-sm font-medium text-slate-100 leading-relaxed">
          "{targetVersion.claim_text}"
        </p>
        <div className="mt-3 flex flex-wrap gap-2 text-[11px]">
          <span className="bg-investigative-800/80 text-slate-300 px-2 py-0.5 rounded">
            Subject: {targetVersion.dna?.subject || 'Public Notice'}
          </span>
          <span className="bg-investigative-800/80 text-slate-300 px-2 py-0.5 rounded font-mono">
            DNA: {targetVersion.dna?.semantic_hash?.slice(0, 8)}...
          </span>
        </div>
      </div>

      {/* Branches to Family Members */}
      {familyMembers.length === 0 ? (
        <div className="text-center py-6 text-sm text-slate-500 bg-slate-50 rounded-lg border border-dashed border-slate-200">
          No related claims in the current database yet. As more statements are investigated, the visual family tree links evolving variants automatically.
        </div>
      ) : (
        <div className="space-y-3 relative before:absolute before:top-0 before:bottom-0 before:left-4 before:w-0.5 before:bg-slate-200">
          {familyMembers.map((member, idx) => (
            <div key={idx} className="relative pl-10">
              <div className="absolute left-2.5 top-5 w-5 h-0.5 bg-slate-200" />
              <div className="absolute left-3 top-4 w-2.5 h-2.5 rounded-full bg-electric-500 border-2 border-white shadow-sm" />

              <div className="bg-slate-50 hover:bg-slate-100/80 transition-colors border border-slate-200 rounded-lg p-4">
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="font-semibold text-slate-700 flex items-center gap-1">
                    <GitCommit className="w-3.5 h-3.5 text-slate-400" />
                    Variant Variant #{idx + 1}
                  </span>
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-mono font-semibold px-2 py-0.5 bg-electric-50 text-electric-700 rounded border border-electric-200">
                      {Math.round(member.similarity_score * 100)}% Similarity
                    </span>
                    <span className="text-[11px] text-slate-500">
                      Scope: {member.scope}
                    </span>
                  </div>
                </div>

                <p className="text-xs text-slate-800 font-medium leading-relaxed">
                  "{member.claim_text}"
                </p>

                <div className="mt-2 text-[11px] text-slate-500 flex items-center justify-between">
                  <span>Connection: {member.connection_reason}</span>
                  <Link
                    to={`/mutations?original=${encodeURIComponent(targetVersion.claim_text)}&modified=${encodeURIComponent(member.claim_text)}`}
                    className="inline-flex items-center gap-1 text-electric-600 hover:text-electric-700 font-semibold"
                  >
                    Compare Mutation <ArrowRight className="w-3 h-3" />
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
