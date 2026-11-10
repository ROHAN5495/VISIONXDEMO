import React, { useState, useEffect } from 'react';
import {
  Database,
  Search,
  Filter,
  CheckCircle2,
  XCircle,
  HelpCircle,
  ExternalLink,
  Shield,
  Award,
  RefreshCw
} from 'lucide-react';
import { api } from '../api/client';
import EvidenceCard from '../components/EvidenceCard';

export default function EvidenceExplorer() {
  const [investigations, setInvestigations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState('all'); // 'all', 'supporting', 'contradictory', 'contextual'
  const [searchQuery, setSearchQuery] = useState('');
  const [demoFilter, setDemoFilter] = useState('all'); // 'all', 'demo', 'live'

  const loadEvidence = async () => {
    try {
      setLoading(true);
      const data = await api.getInvestigations();
      setInvestigations(data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvidence();
  }, []);

  // Flatten all evidence records
  const allEvidence = [];
  investigations.forEach((inv) => {
    (inv.evidence || []).forEach((ev) => {
      allEvidence.push({
        ...ev,
        investigationTitle: inv.title,
        investigationId: inv.id,
      });
    });
  });

  // Filter evidence
  const filteredEvidence = allEvidence.filter((e) => {
    if (filterType !== 'all' && e.classification !== filterType) return false;
    if (demoFilter === 'demo' && !e.is_demo) return false;
    if (demoFilter === 'live' && e.is_demo) return false;
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchText = (e.title + ' ' + e.excerpt + ' ' + e.publisher + ' ' + e.investigationTitle).toLowerCase();
      if (!matchText.includes(q)) return false;
    }
    return true;
  });

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-16">
      {/* Header */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 md:p-8 shadow-sm">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-blue-50 text-blue-600 rounded-xl">
            <Database className="w-8 h-8" />
          </div>
          <div>
            <span className="text-[11px] font-bold text-blue-600 uppercase tracking-wider">
              Evidence-First Architecture
            </span>
            <h2 className="text-2xl font-extrabold text-slate-900 mt-0.5">
              Verifiable Evidence Explorer
            </h2>
            <p className="text-xs text-slate-500 mt-1 max-w-2xl leading-relaxed">
              Every factual finding must trace back to indexed source evidence. Browse, filter, and inspect verified publisher circulars, contradiction refutations, and independent corroborations.
            </p>
          </div>
        </div>

        {/* Filter and Search Bar */}
        <div className="mt-6 pt-6 border-t border-slate-100 flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search evidence by publisher, title, topic keywords..."
              className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-300 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-inner"
            />
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-3 py-2 rounded-xl border border-slate-300 text-xs bg-slate-50 focus:outline-none"
            >
              <option value="all">All Classifications</option>
              <option value="supporting">Supporting Evidence</option>
              <option value="contradictory">Contradictory Evidence</option>
              <option value="contextual">Contextual Background</option>
            </select>

            <select
              value={demoFilter}
              onChange={(e) => setDemoFilter(e.target.value)}
              className="px-3 py-2 rounded-xl border border-slate-300 text-xs bg-slate-50 focus:outline-none"
            >
              <option value="all">All Evidence Modes</option>
              <option value="demo">Demo Records (Offline)</option>
              <option value="live">Live Web Records</option>
            </select>

            <button
              onClick={loadEvidence}
              className="p-2 border border-slate-200 rounded-xl hover:bg-slate-100 text-slate-600 transition-colors"
              title="Refresh evidence"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>
      </div>

      {/* Evidence Stats Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
            Indexed Records
          </div>
          <div className="text-xl font-bold text-slate-900 mt-1 font-mono">{allEvidence.length}</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-[11px] font-semibold text-emerald-700 uppercase tracking-wider flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Supporting
          </div>
          <div className="text-xl font-bold text-emerald-700 mt-1 font-mono">
            {allEvidence.filter(e => e.classification === 'supporting').length}
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-[11px] font-semibold text-rose-700 uppercase tracking-wider flex items-center gap-1">
            <XCircle className="w-3.5 h-3.5" />
            Contradictory
          </div>
          <div className="text-xl font-bold text-rose-700 mt-1 font-mono">
            {allEvidence.filter(e => e.classification === 'contradictory').length}
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-[11px] font-semibold text-sky-700 uppercase tracking-wider flex items-center gap-1">
            <HelpCircle className="w-3.5 h-3.5" />
            Contextual
          </div>
          <div className="text-xl font-bold text-sky-700 mt-1 font-mono">
            {allEvidence.filter(e => e.classification === 'contextual').length}
          </div>
        </div>
      </div>

      {/* Evidence Cards Grid */}
      {loading ? (
        <div className="text-center py-16 text-slate-400 text-xs">
          Querying evidence registry...
        </div>
      ) : filteredEvidence.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl border border-dashed border-slate-200 space-y-2">
          <p className="text-sm font-semibold text-slate-700">No matching evidence records found.</p>
          <p className="text-xs text-slate-400">Try adjusting your search query or filter settings.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredEvidence.map((ev, index) => (
            <EvidenceCard key={ev.id || index} evidence={ev} />
          ))}
        </div>
      )}
    </div>
  );
}
