import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  ShieldCheck,
  Dna,
  GitCompare,
  GitFork,
  MessageSquare,
  ArrowRight,
  Sparkles,
  ExternalLink,
  Search,
  CheckCircle2,
  AlertTriangle,
  History
} from 'lucide-react';
import DemoBadge from '../components/DemoBadge';

export default function LandingPage() {
  const navigate = useNavigate();

  const handleLaunchDemo = (demoId) => {
    navigate(`/report?demo=${demoId}`);
  };

  return (
    <div className="space-y-12 pb-16">
      {/* Investigative Hero Section */}
      <section className="bg-gradient-to-b from-[#0B132B] to-[#1C2541] text-white rounded-2xl p-8 md:p-12 shadow-xl border border-slate-800 relative overflow-hidden">
        <div className="absolute right-0 top-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="max-w-3xl relative z-10 space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 border border-blue-400/30 text-blue-300 text-xs font-semibold uppercase tracking-wider">
            <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
            VISION X • College Hackathon Platform
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight text-white">
            Don't just verify the claim. <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-sky-300">
              Track how it changed.
            </span>
          </h1>

          <p className="text-base sm:text-lg text-slate-300 leading-relaxed">
            Most fact-checking websites only display whether a claim is true or false.
            <strong className="text-white font-semibold"> Evolution Tracker</strong> investigates the journey of information:
            how a statement was modified, what conditions were stripped, and the exact moment it turned into misinformation.
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-4">
            <Link
              to="/verify"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm shadow-lg shadow-blue-600/30 transition-all hover:translate-y-[-1px]"
            >
              <Search className="w-4 h-4" />
              <span>Verify a Claim</span>
            </Link>

            <button
              onClick={() => handleLaunchDemo('demo-1')}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[#141E3C] hover:bg-[#1E2D5A] text-blue-200 font-bold text-sm border border-blue-400/30 transition-all"
            >
              <Sparkles className="w-4 h-4 text-amber-400" />
              <span>Explore Offline Demo</span>
            </button>
          </div>

          <div className="pt-4 flex items-center gap-2 text-xs font-semibold text-slate-400 font-mono tracking-wider">
            <span>OFFICIAL TAGLINE:</span>
            <span className="text-white px-2 py-0.5 rounded bg-blue-500/30 border border-blue-400/40">
              VERIFY BEFORE YOU SHARE.
            </span>
          </div>
        </div>
      </section>

      {/* 4 Signature Features Grid */}
      <section className="space-y-6">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Four Signature Investigative Pillars</h2>
          <p className="text-sm text-slate-500">Built specifically to solve the core hackathon mandate</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Feature A */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm hover:border-blue-300 transition-all flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center mb-4">
                <Dna className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-900 mb-1">Feature A — Rumour DNA</h3>
              <p className="text-xs text-slate-600 leading-relaxed mb-4">
                Creates a unique fingerprint for every claim. Extracts subject, entities, locations, dates, numbers, scope, and semantic hash to connect related claims in a visual family.
              </p>
            </div>
            <Link to="/dna" className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1">
              Explore Rumour DNA <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Feature B */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm hover:border-blue-300 transition-all flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center mb-4">
                <GitCompare className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-900 mb-1">Feature B — Mutation Detector</h3>
              <p className="text-xs text-slate-600 leading-relaxed mb-4">
                Compares versions using 4-color coded tokens (Green = added, Red = removed, Amber = misleading escalation, Blue = context). Pinpoints stripped conditions and changed numbers.
              </p>
            </div>
            <Link to="/mutations" className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1">
              Test Mutation Detector <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Feature C */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm hover:border-blue-300 transition-all flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center mb-4">
                <GitFork className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-900 mb-1">Feature C — Rumour Journey Map</h3>
              <p className="text-xs text-slate-600 leading-relaxed mb-4">
                Interactive timeline connecting claim versions. Strictly distinguishes observed, user-submitted, and AI-inferred steps without fabricating fake timestamps or social propagation.
              </p>
            </div>
            <Link to="/journey" className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1">
              View Journey Maps <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Feature D */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm hover:border-blue-300 transition-all flex flex-col justify-between">
            <div>
              <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center mb-4">
                <MessageSquare className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-900 mb-1">Feature D — Human Truth Engine</h3>
              <p className="text-xs text-slate-600 leading-relaxed mb-4">
                Natural, jargon-free explanations. States the evidence first before presenting conclusions, acknowledges uncertainty honestly, and eliminates AI buzzword fluff.
              </p>
            </div>
            <Link to="/report" className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1">
              Read Truth Reports <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Demonstration Investigations (Work 100% Offline) */}
      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold text-slate-900">Prepared Demonstration Investigations</h2>
              <DemoBadge isDemo={true} />
            </div>
            <p className="text-sm text-slate-500">
              Judges can explore these 3 prepared scenarios immediately without an account or external API keys
            </p>
          </div>
          <span className="text-xs text-slate-400 font-mono">100% OFFLINE READY</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Demo 1 */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition-all">
            <div>
              <div className="flex items-center justify-between text-xs text-slate-500 mb-2">
                <span className="font-mono font-semibold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                  DEMO 1
                </span>
                <span>3 Evolutionary Versions</span>
              </div>
              <h3 className="text-base font-bold text-slate-900 mb-2">
                School Closure Rumour Escalation
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed mb-4">
                Traces how a 2-day preventive pest fumigation notice for a single campus mutated across WhatsApp forwards into a fabricated statewide emergency school holiday.
              </p>
              <div className="space-y-1.5 text-[11px] text-slate-500 bg-slate-50 p-3 rounded-lg border border-slate-100 mb-4">
                <div><strong>v1:</strong> "Oakridge High School closed for 2 days for fumigation..."</div>
                <div><strong>v2:</strong> "All schools in the district are closed..."</div>
                <div><strong>v3:</strong> "State Government declared emergency holidays statewide..."</div>
              </div>
            </div>
            <button
              onClick={() => handleLaunchDemo('demo-1')}
              className="w-full py-2 px-3 rounded-lg text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-colors flex items-center justify-center gap-1.5"
            >
              <span>Launch Demo 1</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Demo 2 */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition-all">
            <div>
              <div className="flex items-center justify-between text-xs text-slate-500 mb-2">
                <span className="font-mono font-semibold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                  DEMO 2
                </span>
                <span>Condition Stripping</span>
              </div>
              <h3 className="text-base font-bold text-slate-900 mb-2">
                Disaster Relief Grant Condition Stripping
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed mb-4">
                Demonstrates how a targeted flood grant requiring prior homeownership registration in 3 specific counties had all conditions removed to announce universal free cash.
              </p>
              <div className="space-y-1.5 text-[11px] text-slate-500 bg-slate-50 p-3 rounded-lg border border-slate-100 mb-4">
                <div><strong>v1:</strong> "$5,000 grant for registered homeowners in 3 counties filed by Feb 15."</div>
                <div><strong>v2:</strong> "Immediate $5,000 cash grant for all state residents, no registration."</div>
              </div>
            </div>
            <button
              onClick={() => handleLaunchDemo('demo-2')}
              className="w-full py-2 px-3 rounded-lg text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-colors flex items-center justify-center gap-1.5"
            >
              <span>Launch Demo 2</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Demo 3 */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition-all">
            <div>
              <div className="flex items-center justify-between text-xs text-slate-500 mb-2">
                <span className="font-mono font-semibold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                  DEMO 3
                </span>
                <span>Context Omission</span>
              </div>
              <h3 className="text-base font-bold text-slate-900 mb-2">
                Clinical Trial Exaggeration to 'Miracle Cure'
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed mb-4">
                Exposes how an early-stage phase 1 safety study of compound TX-94 with 18 volunteers had caveats erased to deceptively proclaim an FDA-approved cure for terminal cancer.
              </p>
              <div className="space-y-1.5 text-[11px] text-slate-500 bg-slate-50 p-3 rounded-lg border border-slate-100 mb-4">
                <div><strong>v1:</strong> "18-patient Phase 1 trial showed safety; efficacy testing not begun."</div>
                <div><strong>v2:</strong> "Miracle cure TX-94 receives breakthrough FDA approval after curing cancer."</div>
              </div>
            </div>
            <button
              onClick={() => handleLaunchDemo('demo-3')}
              className="w-full py-2 px-3 rounded-lg text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-colors flex items-center justify-center gap-1.5"
            >
              <span>Launch Demo 3</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </section>

      {/* Evidence-First & Scoring Standards */}
      <section className="bg-slate-100/70 border border-slate-200 rounded-2xl p-8 space-y-6">
        <div>
          <h2 className="text-lg font-bold text-slate-900">Evidence-First AI Integrity Principles</h2>
          <p className="text-xs text-slate-600">Strict engineering rules preventing hallucinated fact-checking</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-slate-700">
          <div className="space-y-2">
            <h4 className="font-bold text-slate-900 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              LLM Is Never Source of Truth
            </h4>
            <p className="leading-relaxed">
              Every factual assertion must trace back to indexed gazettes, official bulletins, or independent publisher records. The system never makes up facts or sources.
            </p>
          </div>

          <div className="space-y-2">
            <h4 className="font-bold text-slate-900 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              Honest Credibility Scoring (0–100)
            </h4>
            <p className="leading-relaxed">
              Transparent assessment calculated from source reliability, direct relevance, independent corroboration, and contradiction penalties. If evidence is missing, the system states uncertainty openly.
            </p>
          </div>

          <div className="space-y-2">
            <h4 className="font-bold text-slate-900 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              Origin Transparency
            </h4>
            <p className="leading-relaxed">
              Clearly distinguishes observed circulars, user-submitted forwards, and AI-inferred relations. We never fabricate social propagation pathways or authors.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
