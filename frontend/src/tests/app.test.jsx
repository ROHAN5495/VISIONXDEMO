import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

import DemoBadge from '../components/DemoBadge';
import CredibilityScoreGauge from '../components/CredibilityScoreGauge';
import DiffHighlighter from '../components/DiffHighlighter';
import EvidenceCard from '../components/EvidenceCard';
import KeyEvidenceSummary from '../components/KeyEvidenceSummary';
import WorkflowStepper from '../components/WorkflowStepper';
import VisualFamilyTree from '../components/VisualFamilyTree';
import LandingPage from '../pages/LandingPage';

describe('Evolution Tracker Frontend Test Suite', () => {
  // 1. DemoBadge test
  it('renders DemoBadge properly in demo mode, mixed mode, and live mode', () => {
    const { rerender } = render(<DemoBadge isDemo={true} />);
    expect(screen.getByText(/DEMO INVESTIGATION/i)).toBeDefined();

    rerender(<DemoBadge isDemo={false} />);
    expect(screen.getByText(/Live Web Verified/i)).toBeDefined();

    rerender(<DemoBadge mode="mixed" />);
    expect(screen.getByText(/Mixed Evidence/i)).toBeDefined();
  });

  // 2. CredibilityScoreGauge: Verdict Categories & Confidence Indicators
  it('renders honest insufficient evidence state when score is null (UNVERIFIED / LOW)', () => {
    render(
      <CredibilityScoreGauge
        score={null}
        verdict="UNVERIFIED"
        confidence="LOW"
        confidenceScore={15}
        scoreBreakdown={null}
      />
    );
    expect(screen.getByText(/Not enough reliable evidence to assess this claim/i)).toBeDefined();
    expect(screen.getByText(/UNVERIFIED/i)).toBeDefined();
    expect(screen.getByText(/LOW CONFIDENCE/i)).toBeDefined();
  });

  it('renders LIKELY TRUE verdict, HIGH confidence, and numerical score when reliable evidence exists', () => {
    const breakdown = {
      source_reliability: 24,
      direct_relevance: 20,
      independent_corroboration: 20,
      contradictory_penalty: 0,
      recency: 9,
      completeness: 8,
      verdict_reason: 'NASA records confirm solar motion mechanics.',
      status_label: 'Corroborated by Verified Evidence'
    };
    render(
      <CredibilityScoreGauge
        score={81}
        verdict="LIKELY TRUE"
        confidence="HIGH"
        confidenceScore={90}
        verdictReason={breakdown.verdict_reason}
        analysisMode="live_search_rules"
        scoreBreakdown={breakdown}
      />
    );
    expect(screen.getByText('81')).toBeDefined();
    expect(screen.getByText('LIKELY TRUE')).toBeDefined();
    expect(screen.getByText(/HIGH CONFIDENCE/i)).toBeDefined();
    expect(screen.getByText(/NASA records confirm solar motion mechanics/i)).toBeDefined();
  });

  it('renders LIKELY FALSE verdict and reason when contradictory evidence is detected', () => {
    render(
      <CredibilityScoreGauge
        score={20}
        verdict="LIKELY FALSE"
        confidence="HIGH"
        confidenceScore={90}
        verdictReason="Verified records directly contradict this statement."
        analysisMode="live_search_rules"
        scoreBreakdown={{ status_label: 'Directly Contradicted by Trusted Sources' }}
      />
    );
    expect(screen.getByText('LIKELY FALSE')).toBeDefined();
    expect(screen.getByText(/HIGH CONFIDENCE/i)).toBeDefined();
    expect(screen.getByText(/Verified records directly contradict this statement/i)).toBeDefined();
  });

  // 3. KeyEvidenceSummary: Curated Top Snippets
  it('renders KeyEvidenceSummary with search snippet tags and source links', () => {
    const excerpts = [
      {
        publisher: 'NASA Science',
        title: 'Solar System Dynamics',
        url: 'https://science.nasa.gov/sun',
        excerpt: 'The Sun appears to rise in the east because Earth rotates on its axis eastward.',
        classification: 'supporting',
        relevance_reason: 'Corroborates sunrise orientation.',
        is_snippet: true
      }
    ];
    render(<KeyEvidenceSummary excerpts={excerpts} />);
    expect(screen.getByText(/Key Evidence Highlights/i)).toBeDefined();
    expect(screen.getByText('NASA Science')).toBeDefined();
    expect(screen.getByText(/Search Snippet/i)).toBeDefined();
    expect(screen.getByText(/Supports Claim/i)).toBeDefined();
    expect(screen.getByText(/Open Source/i)).toBeDefined();
  });

  // 4. DiffHighlighter: 4-color coded tokens
  it('renders 4-color diff tokens and color legend', () => {
    const tokens = [
      { type: 'equal', text: 'School will be' },
      { type: 'misleading', text: 'closed statewide' },
      { type: 'added', text: 'immediately' },
      { type: 'removed', text: '[-for fumigation-]' },
      { type: 'context', text: 'accordingly' },
    ];
    render(<DiffHighlighter diffTokens={tokens} showLegend={true} />);
    expect(screen.getByText(/Mutation Color Code:/i)).toBeDefined();
    expect(screen.getByText(/Green/i)).toBeDefined();
    expect(screen.getByText(/Red/i)).toBeDefined();
    expect(screen.getByText(/Amber/i)).toBeDefined();
    expect(screen.getByText(/Blue/i)).toBeDefined();
    expect(screen.getByText(/closed statewide/i)).toBeDefined();
  });

  // 5. EvidenceCard: Full evidence registry card
  it('renders full evidence registry card with publisher, excerpt, reliability and snippet disclaimer', () => {
    const ev = {
      url: 'https://education.state.gov/bulletin/12',
      publisher: 'Department of School Education',
      title: 'Clarification on Oakridge Maintenance',
      publication_date: '2026-03-12',
      retrieval_date: '2026-03-14',
      excerpt: 'Only Oakridge High School had a 2-day pest cleaning.',
      classification: 'contradictory',
      relevance_reason: 'Refutes statewide closure claims.',
      reliability_score: 95,
      is_demo: true,
      is_independent: true
    };
    render(<EvidenceCard evidence={ev} />);
    expect(screen.getByText('Department of School Education')).toBeDefined();
    expect(screen.getByText(/Only Oakridge High School had a 2-day pest cleaning/i)).toBeDefined();
    expect(screen.getByText(/Contradictory Evidence/i)).toBeDefined();
    expect(screen.getByText(/Search Snippet/i)).toBeDefined();
    expect(screen.getByText('95%')).toBeDefined();
  });

  // 6. WorkflowStepper: 7-stage protocol
  it('renders 7-step investigation protocol', () => {
    render(<WorkflowStepper currentStep="verify" />);
    expect(screen.getByText('Submit')).toBeDefined();
    expect(screen.getByText('Understand')).toBeDefined();
    expect(screen.getByText('Retrieve')).toBeDefined();
    expect(screen.getByText('Verify')).toBeDefined();
    expect(screen.getByText('Compare')).toBeDefined();
    expect(screen.getByText('Explain')).toBeDefined();
    expect(screen.getByText('Track')).toBeDefined();
  });

  // 7. VisualFamilyTree: Rumour DNA Family
  it('renders Rumour DNA visual family links', () => {
    const root = {
      claim_text: 'Oakridge School closed for fumigation',
      dna: { scope: 'specific', subject: 'School Closure', semantic_hash: 'abc123456789' }
    };
    const family = [
      {
        claim_text: 'All schools closed in the district',
        similarity_score: 0.75,
        scope: 'district',
        connection_reason: 'Shares subject and entities'
      }
    ];
    render(
      <BrowserRouter>
        <VisualFamilyTree targetVersion={root} familyMembers={family} />
      </BrowserRouter>
    );
    expect(screen.getByText(/Rumour DNA Family Map/i)).toBeDefined();
    expect(screen.getByText('75% Similarity')).toBeDefined();
  });

  // 8. LandingPage: Mission, Tagline, Demo Triggers
  it('renders LandingPage with official tagline and demo options', () => {
    render(
      <BrowserRouter>
        <LandingPage />
      </BrowserRouter>
    );
    expect(screen.getByText(/VERIFY BEFORE YOU SHARE/i)).toBeDefined();
    expect(screen.getByText(/Don't just verify the claim/i)).toBeDefined();
    expect(screen.getByText(/Track how it changed/i)).toBeDefined();
    expect(screen.getByText(/Feature A — Rumour DNA/i)).toBeDefined();
    expect(screen.getByText(/Feature B — Mutation Detector/i)).toBeDefined();
    expect(screen.getByText(/Feature C — Rumour Journey Map/i)).toBeDefined();
    expect(screen.getByText(/Feature D — Human Truth Engine/i)).toBeDefined();
    expect(screen.getByText(/School Closure Rumour Escalation/i)).toBeDefined();
  });
});
