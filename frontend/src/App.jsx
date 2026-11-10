import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';

// 9 Application Pages
import LandingPage from './pages/LandingPage';
import Dashboard from './pages/Dashboard';
import VerifyClaim from './pages/VerifyClaim';
import InvestigationReport from './pages/InvestigationReport';
import RumourDNA from './pages/RumourDNA';
import MutationDetector from './pages/MutationDetector';
import RumourJourneyMap from './pages/RumourJourneyMap';
import EvidenceExplorer from './pages/EvidenceExplorer';
import InvestigationHistory from './pages/InvestigationHistory';

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-[#F8FAFC] flex text-slate-900 font-sans antialiased">
        {/* Dark Navy Investigative Sidebar */}
        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
        />

        {/* Content Wrapper */}
        <div className="flex-1 flex flex-col lg:pl-72 min-w-0">
          {/* Top Navbar */}
          <Navbar onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} />

          {/* Main View Area */}
          <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/verify" element={<VerifyClaim />} />
              <Route path="/report" element={<InvestigationReport />} />
              <Route path="/report/:id" element={<InvestigationReport />} />
              <Route path="/dna" element={<RumourDNA />} />
              <Route path="/mutations" element={<MutationDetector />} />
              <Route path="/journey" element={<RumourJourneyMap />} />
              <Route path="/evidence" element={<EvidenceExplorer />} />
              <Route path="/history" element={<InvestigationHistory />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}
