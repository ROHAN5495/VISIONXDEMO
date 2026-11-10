import React from 'react';
import { NavLink, Link, useNavigate } from 'react-router-dom';
import {
  Compass,
  LayoutDashboard,
  Search,
  FileText,
  Dna,
  GitCompare,
  GitFork,
  Database,
  History,
  Shield,
  Sparkles,
  ExternalLink
} from 'lucide-react';

const NAV_ITEMS = [
  { name: 'Investigation Mission', path: '/', icon: Compass, exact: true },
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Verify a Claim', path: '/verify', icon: Search },
  { name: 'Investigation Report', path: '/report', icon: FileText },
  { name: 'Rumour DNA', path: '/dna', icon: Dna },
  { name: 'Mutation Detector', path: '/mutations', icon: GitCompare },
  { name: 'Rumour Journey Map', path: '/journey', icon: GitFork },
  { name: 'Evidence Explorer', path: '/evidence', icon: Database },
  { name: 'Investigation History', path: '/history', icon: History },
];

export default function Sidebar({ isOpen, onClose }) {
  const navigate = useNavigate();

  const handleLaunchDemo = (demoId) => {
    navigate(`/report?demo=${demoId}`);
    if (onClose) onClose();
  };

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-72 bg-[#0B132B] border-r border-[#1C2541] text-slate-300 flex flex-col transition-transform duration-300 ease-in-out lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand Header */}
        <div className="p-5 border-b border-[#1C2541]">
          <Link to="/" className="flex items-center gap-3 group" onClick={onClose}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center text-white shadow-lg shadow-blue-500/20 group-hover:scale-105 transition-transform">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-extrabold text-white text-base tracking-tight font-sans">
                  EVOLUTION TRACKER
                </span>
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 font-mono">
                  2.0
                </span>
              </div>
              <div className="text-[11px] font-semibold text-slate-400 tracking-wider">
                VISION X RESEARCH LABS
              </div>
            </div>
          </Link>

          <div className="mt-3 px-2.5 py-1.5 rounded-lg bg-[#141E3C] border border-[#212E54] text-[11px] font-semibold text-blue-300 text-center uppercase tracking-wider">
            VERIFY BEFORE YOU SHARE
          </div>
        </div>

        {/* Main Navigation Links */}
        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
          <div className="px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-slate-500">
            Investigative Suite
          </div>

          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.exact}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-blue-600 text-white font-semibold shadow-md shadow-blue-600/30'
                      : 'text-slate-300 hover:text-white hover:bg-[#162244]'
                  }`
                }
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.name}</span>
              </NavLink>
            );
          })}

          {/* Quick Demo Section for Judges */}
          <div className="pt-5 mt-4 border-t border-[#1C2541]">
            <div className="px-3 pb-2 flex items-center justify-between text-[10px] font-bold uppercase tracking-wider text-slate-400">
              <span className="flex items-center gap-1">
                <Sparkles className="w-3 h-3 text-amber-400" />
                Judge Demo Sandbox
              </span>
              <span className="text-[9px] text-amber-300 bg-amber-500/10 px-1.5 py-0.5 rounded border border-amber-500/20">
                Offline
              </span>
            </div>

            <div className="space-y-1 px-1">
              <button
                onClick={() => handleLaunchDemo('demo-1')}
                className="w-full text-left px-3 py-2 rounded-lg text-xs text-slate-300 hover:text-white hover:bg-[#162244] transition-colors flex items-center justify-between group"
              >
                <span className="truncate">Demo 1: School Closure Rumour</span>
                <span className="text-[10px] text-slate-500 group-hover:text-blue-400">3 v</span>
              </button>
              <button
                onClick={() => handleLaunchDemo('demo-2')}
                className="w-full text-left px-3 py-2 rounded-lg text-xs text-slate-300 hover:text-white hover:bg-[#162244] transition-colors flex items-center justify-between group"
              >
                <span className="truncate">Demo 2: Relief Grant Eligibility</span>
                <span className="text-[10px] text-slate-500 group-hover:text-blue-400">2 v</span>
              </button>
              <button
                onClick={() => handleLaunchDemo('demo-3')}
                className="w-full text-left px-3 py-2 rounded-lg text-xs text-slate-300 hover:text-white hover:bg-[#162244] transition-colors flex items-center justify-between group"
              >
                <span className="truncate">Demo 3: Clinical Trial Exaggeration</span>
                <span className="text-[10px] text-slate-500 group-hover:text-blue-400">2 v</span>
              </button>
            </div>
          </div>
        </nav>

        {/* Footer info */}
        <div className="p-4 border-t border-[#1C2541] text-[11px] text-slate-400 bg-[#080E21]">
          <div className="flex items-center justify-between">
            <span className="font-semibold text-slate-300">Hackathon Edition</span>
            <span className="flex items-center gap-1 text-emerald-400 font-mono text-[10px]">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              Engine Online
            </span>
          </div>
          <div className="mt-1 text-[10px] text-slate-500">
            "Don't just verify the claim. Track how it changed."
          </div>
        </div>
      </aside>
    </>
  );
}
