import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Search,
  PlusCircle,
  FileText,
  AlertTriangle,
  ShieldCheck,
  ShieldAlert,
  HelpCircle,
  ArrowRight,
  GitFork,
  Dna,
  RefreshCw,
  Sparkles
} from 'lucide-react';
import { api } from '../api/client';
import DemoBadge from '../components/DemoBadge';

export default function Dashboard() {
  const navigate = useNavigate();
  const [investigations, setInvestigations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [quickClaim, setQuickClaim] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getInvestigations();
      setInvestigations(data || []);
    } catch (err) {
      setError(err.message || 'Failed to load investigations');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleQuickSubmit = (e) => {
    e.preventDefault();
    if (!quickClaim.trim()) return;
    navigate(`/verify?claim=${encodeURIComponent(quickClaim.trim())}`);
  };

  // Metrics calculation
  const total = investigations.length;
  const supported = investigations.filter(i => i.verdict === 'Supported' || i.verdict === 'Mostly supported').length;
  const contradicted = investigations.filter(i => i.verdict === 'Contradicted' || i.verdict === 'Mostly contradicted').length;
  const unverified = investigations.filter(i => i.verdict === 'Unverified' || !i.score).length;
  const totalVersions = investigations.reduce((acc, i) => acc + (i.versions?.length || 1), 0);

  return (
    <div className="space-y-8 pb-12">
      {/* Top Banner with Quick Submission Bar */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <div className="max-w-2xl mb-4">
          <span className="text-[11px] font-bold text-blue-600 uppercase tracking-wider">
            Investigative Intelligence Hub
          </span>
          <h2 className="text-xl font-bold text-slate-900 mt-0.5">
            Claim Verification & Evolution Console
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Submit a statement, extract its Rumour DNA, identify contradictory evidence, and track how it mutates.
          </p>
        </div>

        <form onSubmit={handleQuickSubmit} className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
            <input
              type="text"
              value={quickClaim}
              onChange={(e) => setQuickClaim(e.target.value)}
              placeholder="Paste any forwarded message, viral headline, or official statement..."
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm placeholder:text-slate-400 shadow-inner"
            />
          </div>
          <button
            type="submit"
            className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs transition-colors shrink-0 flex items-center justify-center gap-2 shadow-sm"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Start Investigation</span>
          </button>
        </form>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
            Total Investigations
          </div>
          <div className="text-2xl font-extrabold text-slate-900 mt-1 font-mono">
            {total}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">
            {totalVersions} evolutionary versions indexed
          </div>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
          <div className="text-[11px] font-semibold text-emerald-700 uppercase tracking-wider flex items-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5" />
            Supported Claims
          </div>
          <div className="text-2xl font-extrabold text-emerald-700 mt-1 font-mono">
            {supported}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Corroborated by sources</div>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
          <div className="text-[11px] font-semibold text-rose-700 uppercase tracking-wider flex items-center gap-1">
            <ShieldAlert className="w-3.5 h-3.5" />
            Contradicted Claims
          </div>
          <div className="text-2xl font-extrabold text-rose-700 mt-1 font-mono">
            {contradicted}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Disproven or escalated</div>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-600 uppercase tracking-wider flex items-center gap-1">
            <HelpCircle className="w-3.5 h-3.5" />
            Unverified
          </div>
          <div className="text-2xl font-extrabold text-slate-700 mt-1 font-mono">
            {unverified}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Insufficient proof found</div>
        </div>
      </div>

      {/* Investigations Table */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-900">Recent Claim Investigations</h3>
            <p className="text-xs text-slate-500">Track and inspect records in the local investigative database</p>
          </div>
          <button
            onClick={loadData}
            className="p-2 text-slate-500 hover:text-slate-800 rounded-lg hover:bg-slate-100 transition-colors"
            title="Refresh database records"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>

        {error && (
          <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-rose-700 text-xs flex items-center justify-between">
            <span>{error}</span>
            <button onClick={loadData} className="font-semibold underline">Retry</button>
          </div>
        )}

        {loading ? (
          <div className="text-center py-12 text-slate-400 text-xs">
            Loading investigation registry...
          </div>
        ) : investigations.length === 0 ? (
          <div className="text-center py-12 bg-slate-50 rounded-xl border border-dashed border-slate-200 space-y-3">
            <p className="text-xs text-slate-500">No investigations recorded yet.</p>
            <Link
              to="/verify"
              className="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-600 text-white rounded-lg text-xs font-semibold hover:bg-blue-700"
            >
              <PlusCircle className="w-3.5 h-3.5" /> Verify First Claim
            </Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 border-b border-slate-200 font-semibold uppercase text-[10px] tracking-wider">
                <tr>
                  <th className="py-3 px-4">Subject / Claim Assertion</th>
                  <th className="py-3 px-4">Verdict</th>
                  <th className="py-3 px-4">Credibility Score</th>
                  <th className="py-3 px-4">Evolution</th>
                  <th className="py-3 px-4">Origin / Type</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {investigations.map((inv) => {
                  const latestVersion = inv.versions?.[inv.versions.length - 1];
                  const versionCount = inv.versions?.length || 1;

                  return (
                    <tr key={inv.id} className="hover:bg-slate-50/80 transition-colors group">
                      <td className="py-3.5 px-4 max-w-sm">
                        <Link
                          to={`/report/${inv.id}`}
                          className="font-semibold text-slate-900 group-hover:text-blue-600 transition-colors line-clamp-1 text-xs"
                        >
                          {inv.title}
                        </Link>
                        <p className="text-[11px] text-slate-500 line-clamp-1 mt-0.5">
                          {latestVersion?.claim_text || inv.summary}
                        </p>
                      </td>

                      <td className="py-3.5 px-4 whitespace-nowrap">
                        <span
                          className={`px-2 py-0.5 rounded text-[11px] font-semibold uppercase ${
                            inv.verdict === 'Supported' || inv.verdict === 'Mostly supported'
                              ? 'bg-emerald-100 text-emerald-800'
                              : inv.verdict === 'Mixed evidence'
                              ? 'bg-amber-100 text-amber-800'
                              : inv.verdict === 'Unverified'
                              ? 'bg-slate-100 text-slate-700'
                              : 'bg-rose-100 text-rose-800'
                          }`}
                        >
                          {inv.verdict}
                        </span>
                      </td>

                      <td className="py-3.5 px-4 font-mono whitespace-nowrap">
                        {inv.score !== null ? (
                          <span className="font-bold text-slate-800 text-xs">
                            {inv.score} <span className="text-[10px] text-slate-400 font-normal">/ 100</span>
                          </span>
                        ) : (
                          <span className="text-slate-400 text-[11px] italic">Unassessed</span>
                        )}
                      </td>

                      <td className="py-3.5 px-4 whitespace-nowrap">
                        <span className="inline-flex items-center gap-1 font-mono text-[11px] bg-slate-100 px-2 py-0.5 rounded text-slate-700">
                          <GitFork className="w-3 h-3 text-slate-500" />
                          {versionCount} {versionCount === 1 ? 'version' : 'versions'}
                        </span>
                      </td>

                      <td className="py-3.5 px-4 whitespace-nowrap">
                        <DemoBadge isDemo={inv.is_demo} />
                      </td>

                      <td className="py-3.5 px-4 text-right whitespace-nowrap space-x-2">
                        <Link
                          to={`/report/${inv.id}`}
                          className="inline-flex items-center gap-1 px-2.5 py-1 bg-slate-100 hover:bg-blue-50 text-slate-700 hover:text-blue-700 rounded text-xs font-medium transition-colors"
                        >
                          <FileText className="w-3.5 h-3.5" />
                          <span>Report</span>
                        </Link>
                        <Link
                          to={`/journey?id=${inv.id}`}
                          className="inline-flex items-center gap-1 px-2.5 py-1 bg-slate-100 hover:bg-blue-50 text-slate-700 hover:text-blue-700 rounded text-xs font-medium transition-colors"
                        >
                          <GitFork className="w-3.5 h-3.5" />
                          <span>Journey</span>
                        </Link>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
