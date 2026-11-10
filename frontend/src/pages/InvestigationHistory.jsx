import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  History,
  Search,
  Filter,
  FileText,
  GitFork,
  Dna,
  Trash2,
  Calendar,
  AlertTriangle,
  RefreshCw,
  PlusCircle
} from 'lucide-react';
import { api } from '../api/client';
import DemoBadge from '../components/DemoBadge';

export default function InvestigationHistory() {
  const [investigations, setInvestigations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [verdictFilter, setVerdictFilter] = useState('all');
  const [demoFilter, setDemoFilter] = useState('all');
  const [deleteId, setDeleteId] = useState(null);

  const loadData = async () => {
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
    loadData();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this investigation and all its evolutionary versions?')) {
      return;
    }
    try {
      await api.deleteInvestigation(id);
      setInvestigations(investigations.filter((i) => i.id !== id));
    } catch (err) {
      alert(err.message || 'Error deleting investigation');
    }
  };

  const filtered = investigations.filter((inv) => {
    if (verdictFilter !== 'all' && inv.verdict !== verdictFilter) return false;
    if (demoFilter === 'demo' && !inv.is_demo) return false;
    if (demoFilter === 'live' && inv.is_demo) return false;
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const match = (inv.title + ' ' + (inv.summary || '') + ' ' + inv.verdict).toLowerCase();
      if (!match.includes(q)) return false;
    }
    return true;
  });

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-16">
      {/* Header */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 md:p-8 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="p-3 bg-slate-100 text-slate-700 rounded-xl">
              <History className="w-8 h-8" />
            </div>
            <div>
              <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                Audit Trail & Archives
              </span>
              <h2 className="text-2xl font-extrabold text-slate-900 mt-0.5">
                Investigation History
              </h2>
              <p className="text-xs text-slate-500 mt-1 max-w-xl leading-relaxed">
                Persistent database records of all verified claims, multi-stage evolution timelines, and evidence assessments.
              </p>
            </div>
          </div>

          <Link
            to="/verify"
            className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-semibold self-start sm:self-auto transition-colors shadow-xs"
          >
            <PlusCircle className="w-4 h-4" />
            <span>New Investigation</span>
          </Link>
        </div>

        {/* Search & Filters */}
        <div className="mt-6 pt-6 border-t border-slate-100 flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search history by title, keywords..."
              className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-300 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-inner"
            />
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <select
              value={verdictFilter}
              onChange={(e) => setVerdictFilter(e.target.value)}
              className="px-3 py-2 rounded-xl border border-slate-300 text-xs bg-slate-50 focus:outline-none"
            >
              <option value="all">All Verdicts</option>
              <option value="Supported">Supported</option>
              <option value="Mostly supported">Mostly Supported</option>
              <option value="Mixed evidence">Mixed Evidence</option>
              <option value="Mostly contradicted">Mostly Contradicted</option>
              <option value="Contradicted">Contradicted</option>
              <option value="Unverified">Unverified</option>
            </select>

            <select
              value={demoFilter}
              onChange={(e) => setDemoFilter(e.target.value)}
              className="px-3 py-2 rounded-xl border border-slate-300 text-xs bg-slate-50 focus:outline-none"
            >
              <option value="all">All Sources</option>
              <option value="demo">Demo Data Only</option>
              <option value="live">Live User Claims</option>
            </select>

            <button
              onClick={loadData}
              className="p-2 border border-slate-200 rounded-xl hover:bg-slate-100 text-slate-600 transition-colors"
              title="Refresh"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>
      </div>

      {/* History Table */}
      <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
        {loading ? (
          <div className="text-center py-16 text-slate-400 text-xs">
            Loading investigation archives...
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-16 space-y-2">
            <p className="text-sm font-semibold text-slate-700">No matching investigation records found.</p>
            <p className="text-xs text-slate-400">Try modifying search filters or submit a new verification.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 border-b border-slate-200 font-semibold uppercase text-[10px] tracking-wider">
                <tr>
                  <th className="py-3.5 px-4">Subject & Claim Summary</th>
                  <th className="py-3.5 px-4">Verdict</th>
                  <th className="py-3.5 px-4">Evidence Score</th>
                  <th className="py-3.5 px-4">Versions</th>
                  <th className="py-3.5 px-4">Date Recorded</th>
                  <th className="py-3.5 px-4">Origin Status</th>
                  <th className="py-3.5 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filtered.map((inv) => (
                  <tr key={inv.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-4 px-4 max-w-sm">
                      <Link
                        to={`/report/${inv.id}`}
                        className="font-bold text-slate-900 hover:text-blue-600 transition-colors line-clamp-1"
                      >
                        {inv.title}
                      </Link>
                      <p className="text-[11px] text-slate-500 line-clamp-1 mt-0.5">
                        {inv.summary}
                      </p>
                    </td>

                    <td className="py-4 px-4 whitespace-nowrap">
                      <span
                        className={`px-2.5 py-0.5 rounded text-[11px] font-semibold uppercase ${
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

                    <td className="py-4 px-4 font-mono whitespace-nowrap">
                      {inv.score !== null ? (
                        <span className="font-bold text-slate-800 text-xs">
                          {inv.score} <span className="text-[10px] text-slate-400 font-normal">/ 100</span>
                        </span>
                      ) : (
                        <span className="text-slate-400 italic text-[11px]">Unassessed</span>
                      )}
                    </td>

                    <td className="py-4 px-4 whitespace-nowrap">
                      <span className="font-mono text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                        {inv.versions?.length || 1} v
                      </span>
                    </td>

                    <td className="py-4 px-4 text-slate-500 font-mono text-[11px] whitespace-nowrap">
                      {new Date(inv.created_at).toLocaleDateString()}
                    </td>

                    <td className="py-4 px-4 whitespace-nowrap">
                      <DemoBadge isDemo={inv.is_demo} />
                    </td>

                    <td className="py-4 px-4 text-right whitespace-nowrap space-x-1">
                      <Link
                        to={`/report/${inv.id}`}
                        className="p-1.5 inline-block text-slate-500 hover:text-blue-600 rounded hover:bg-slate-100"
                        title="View Report"
                      >
                        <FileText className="w-4 h-4" />
                      </Link>
                      <Link
                        to={`/journey?id=${inv.id}`}
                        className="p-1.5 inline-block text-slate-500 hover:text-emerald-600 rounded hover:bg-slate-100"
                        title="Journey Map"
                      >
                        <GitFork className="w-4 h-4" />
                      </Link>
                      <button
                        onClick={() => handleDelete(inv.id)}
                        className="p-1.5 inline-block text-slate-400 hover:text-rose-600 rounded hover:bg-slate-100"
                        title="Delete Dossier"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
