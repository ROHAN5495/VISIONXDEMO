import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import {
  GitFork,
  Calendar,
  Layers,
  ArrowRight,
  ShieldCheck,
  ShieldAlert,
  AlertCircle,
  HelpCircle,
  Clock,
  Sparkles,
  Info,
  Maximize2
} from 'lucide-react';
import { api } from '../api/client';
import DemoBadge from '../components/DemoBadge';
import DiffHighlighter from '../components/DiffHighlighter';

export default function RumourJourneyMap() {
  const [searchParams, setSearchParams] = useSearchParams();
  const investigationId = searchParams.get('id');

  const [investigations, setInvestigations] = useState([]);
  const [selectedInv, setSelectedInv] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load available investigations
  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const list = await api.getInvestigations();
        setInvestigations(list || []);

        let target = null;
        if (investigationId) {
          target = list.find(i => i.id === investigationId);
          if (!target) {
            target = await api.getInvestigation(investigationId);
          }
        } else if (list.length > 0) {
          target = list[0];
        } else {
          target = await api.getDemo('demo-1');
        }

        setSelectedInv(target);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [investigationId]);

  const handleSelectInvestigation = async (id) => {
    setSearchParams({ id });
    try {
      const data = await api.getInvestigation(id);
      setSelectedInv(data);
    } catch (err) {
      console.error(err);
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'supported':
        return {
          bg: 'bg-emerald-100 text-emerald-800 border-emerald-300',
          icon: <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />,
          label: 'Supported Evidence'
        };
      case 'contradicted':
        return {
          bg: 'bg-rose-100 text-rose-800 border-rose-300',
          icon: <ShieldAlert className="w-3.5 h-3.5 text-rose-600" />,
          label: 'Contradicted by Facts'
        };
      case 'altered':
      default:
        return {
          bg: 'bg-amber-100 text-amber-800 border-amber-300',
          icon: <AlertCircle className="w-3.5 h-3.5 text-amber-600" />,
          label: 'Altered Mutation'
        };
    }
  };

  const getOriginBadge = (originType) => {
    switch (originType) {
      case 'observed':
        return {
          bg: 'bg-indigo-50 text-indigo-700 border-indigo-200',
          label: 'Observed Notice'
        };
      case 'ai_inferred':
        return {
          bg: 'bg-purple-50 text-purple-700 border-purple-200',
          label: 'AI-Inferred Relationship'
        };
      case 'user_submitted':
      default:
        return {
          bg: 'bg-slate-100 text-slate-700 border-slate-200',
          label: 'User-Submitted Forward'
        };
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-16">
      {/* Header */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 md:p-8 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl">
              <GitFork className="w-8 h-8" />
            </div>
            <div>
              <span className="text-[11px] font-bold text-emerald-600 uppercase tracking-wider">
                Signature Feature C
              </span>
              <h2 className="text-2xl font-extrabold text-slate-900 mt-0.5">
                Rumour Journey Map & Evolution Timeline
              </h2>
              <p className="text-xs text-slate-500 mt-1 max-w-xl leading-relaxed">
                Connects claim versions as they spread. Traces added claims, stripped qualifiers, and clearly distinguishes observed records from user-forwarded text without fabricating propagation pathways.
              </p>
            </div>
          </div>

          {/* Quick Investigation Switcher */}
          {investigations.length > 0 && (
            <div className="min-w-[220px]">
              <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1">
                Select Dossier Timeline:
              </label>
              <select
                value={selectedInv?.id || ''}
                onChange={(e) => handleSelectInvestigation(e.target.value)}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs bg-slate-50 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                {investigations.map((i) => (
                  <option key={i.id} value={i.id}>
                    {i.title.slice(0, 35)}... ({i.versions?.length || 1} v)
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>

        {/* Ethical Disclaimer Box */}
        <div className="mt-6 p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-600 flex items-start gap-2.5">
          <Info className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
          <div className="leading-relaxed">
            <strong className="text-slate-800">Investigative Transparency Rule: </strong>
            A claim version's recorded date is not proof of when or where the rumour originally started.
            Evolution Tracker strictly labels <em>Observed</em> vs <em>User-Submitted</em> origins and never invents fake author handles or social propagation trees.
          </div>
        </div>
      </div>

      {/* Selected Investigation Journey */}
      {selectedInv && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-bold text-slate-900">{selectedInv.title}</h3>
              <p className="text-xs text-slate-500">
                Displaying {selectedInv.versions?.length || 1} chronological version nodes
              </p>
            </div>
            <DemoBadge isDemo={selectedInv.is_demo} />
          </div>

          {/* Interactive Timeline Container */}
          <div className="relative pl-6 sm:pl-10 before:absolute before:left-3 sm:before:left-5 before:top-4 before:bottom-4 before:w-1 before:bg-gradient-to-b before:from-blue-500 before:via-amber-400 before:to-rose-500 space-y-8">
            {selectedInv.versions?.map((v, index) => {
              const status = getStatusBadge(v.evidence_status);
              const origin = getOriginBadge(v.origin_type);
              const isFirst = index === 0;
              const isLast = index === selectedInv.versions.length - 1;
              const mutation = v.changes_from_previous;

              return (
                <div key={v.id || index} className="relative group">
                  {/* Timeline Pin Dot */}
                  <div
                    className={`absolute -left-6 sm:-left-10 top-5 w-7 h-7 rounded-full border-4 border-white shadow-md flex items-center justify-center text-xs font-mono font-bold text-white transition-transform group-hover:scale-110 ${
                      isFirst
                        ? 'bg-blue-600'
                        : isLast
                        ? 'bg-rose-600'
                        : 'bg-amber-500'
                    }`}
                  >
                    {v.version_number}
                  </div>

                  {/* Card Content */}
                  <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm hover:shadow-md transition-all space-y-4">
                    {/* Top Meta Badges */}
                    <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-extrabold text-slate-900 font-mono">
                          VERSION {v.version_number}
                        </span>
                        <span className={`px-2 py-0.5 rounded text-[11px] font-semibold border ${status.bg} flex items-center gap-1`}>
                          {status.icon}
                          {status.label}
                        </span>
                      </div>

                      <div className="flex items-center gap-2">
                        <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-medium border ${origin.bg}`}>
                          {origin.label}
                        </span>
                        <span className="text-xs text-slate-400 font-mono flex items-center gap-1">
                          <Calendar className="w-3.5 h-3.5 text-slate-400" />
                          {v.recorded_date}
                        </span>
                      </div>
                    </div>

                    {/* Claim Text */}
                    <div className="space-y-1">
                      <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                        Recorded Claim Statement
                      </div>
                      <blockquote className="text-sm sm:text-base font-semibold text-slate-800 leading-relaxed italic border-l-2 border-slate-300 pl-3">
                        "{v.claim_text}"
                      </blockquote>
                    </div>

                    {/* Source and Origin details */}
                    <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500">
                      <span><strong>Submission Origin:</strong> {v.source_origin}</span>
                      {v.dna && (
                        <span><strong>Scope:</strong> <span className="capitalize">{v.dna.scope}</span></span>
                      )}
                    </div>

                    {/* Mutation diff against previous version if present */}
                    {mutation && mutation.has_mutation && (
                      <div className="pt-3 border-t border-slate-100 space-y-3">
                        <div className="text-xs font-bold text-amber-700 flex items-center gap-1">
                          <span>Detected Mutations vs Version {v.version_number - 1}:</span>
                        </div>

                        <DiffHighlighter diffTokens={mutation.diff_tokens} showLegend={false} />

                        <div className="p-3 bg-amber-50/60 rounded-xl border border-amber-200/60 text-xs text-amber-900 leading-relaxed">
                          {mutation.explanation}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          <div className="pt-4 flex justify-end">
            <Link
              to={`/report/${selectedInv.id}`}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-semibold shadow-sm transition-colors"
            >
              <span>View Full Evidence Dossier</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
