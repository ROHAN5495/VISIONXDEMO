import React, { useEffect, useState } from 'react';
import { Menu, PlusCircle, CheckCircle2, AlertCircle, RefreshCw, Sparkles } from 'lucide-react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { api } from '../api/client';

export default function Navbar({ onToggleSidebar }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [backendStatus, setBackendStatus] = useState('checking'); // 'healthy', 'error', 'checking'
  const [liveSearchActive, setLiveSearchActive] = useState(false);

  const checkHealth = async () => {
    try {
      setBackendStatus('checking');
      const res = await api.getHealth();
      if (res && res.status === 'healthy') {
        setBackendStatus('healthy');
        setLiveSearchActive(Boolean(res.live_search_configured));
      } else {
        setBackendStatus('error');
      }
    } catch (e) {
      setBackendStatus('error');
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  const getPageTitle = () => {
    const p = location.pathname;
    if (p === '/') return 'Mission Overview';
    if (p === '/dashboard') return 'Investigation Dashboard';
    if (p === '/verify') return 'Verify a Claim';
    if (p.startsWith('/report')) return 'Investigation Report';
    if (p === '/dna') return 'Feature A: Rumour DNA Fingerprint';
    if (p === '/mutations') return 'Feature B: Mutation Detector';
    if (p === '/journey') return 'Feature C: Rumour Journey Map';
    if (p === '/evidence') return 'Evidence Explorer';
    if (p === '/history') return 'Investigation History';
    return 'Investigation';
  };

  return (
    <header className="sticky top-0 z-30 h-16 bg-white border-b border-slate-200 px-4 lg:px-8 flex items-center justify-between shadow-xs">
      {/* Left: Mobile Toggle & Page Title */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-lg text-slate-600 hover:bg-slate-100 lg:hidden focus:outline-none"
          aria-label="Toggle menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div>
          <h1 className="text-base font-bold text-slate-900 leading-none">
            {getPageTitle()}
          </h1>
          <span className="text-[11px] font-medium text-slate-400 hidden sm:inline">
            EVOLUTION TRACKER 2.0 • Vision X
          </span>
        </div>
      </div>

      {/* Right: Actions & Health Status */}
      <div className="flex items-center gap-3">
        {/* Backend Status indicator */}
        <div
          onClick={checkHealth}
          className="cursor-pointer flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-mono border transition-colors bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"
          title={liveSearchActive ? "Backend connected and live web search provider (Tavily) is active" : "Backend connected in offline demo mode (no live search key configured)"}
        >
          {backendStatus === 'healthy' ? (
            liveSearchActive ? (
              <>
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                <span className="text-emerald-700 font-semibold hidden md:inline">API & Live Search Ready</span>
              </>
            ) : (
              <>
                <span className="w-2 h-2 rounded-full bg-amber-500" />
                <span className="text-amber-700 font-semibold hidden md:inline">API Ready (Offline Demo)</span>
              </>
            )
          ) : backendStatus === 'checking' ? (
            <>
              <RefreshCw className="w-3 h-3 text-slate-400 animate-spin" />
              <span className="text-slate-500 hidden md:inline">Checking</span>
            </>
          ) : (
            <>
              <AlertCircle className="w-3.5 h-3.5 text-rose-500" />
              <span className="text-rose-600 font-semibold hidden md:inline">Backend Offline</span>
            </>
          )}
        </div>

        {/* Quick Demo Button */}
        <button
          onClick={() => navigate('/report?demo=demo-1')}
          className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-amber-800 bg-amber-50 hover:bg-amber-100 border border-amber-300 transition-colors"
        >
          <Sparkles className="w-3.5 h-3.5 text-amber-600" />
          <span>Launch Demo</span>
        </button>

        {/* Primary CTA: New Verification */}
        <Link
          to="/verify"
          className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 shadow-sm transition-all focus:ring-2 focus:ring-blue-500 focus:ring-offset-1"
        >
          <PlusCircle className="w-4 h-4" />
          <span>New Claim</span>
        </Link>
      </div>
    </header>
  );
}
