import datetime
from typing import List, Dict, Any
from backend.app.services.claim_extraction import extract_rumour_dna
from backend.app.services.mutation_analysis import analyze_mutations
from backend.app.services.credibility_scoring import calculate_evidence_score
from backend.app.services.report_generator import generate_human_explanation
from backend.app.schemas.claim import EvidenceRecordSchema

DEMO_INVESTIGATIONS: List[Dict[str, Any]] = [
    {
        "demo_id": "demo-1",
        "title": "School Closure Rumour Escalation",
        "category": "Education & Public Safety",
        "summary": "Traces how a localized, routine two-day pest fumigation notice for a single campus mutated across WhatsApp forwards into a fabricated statewide emergency school shutdown.",
        "versions": [
            {
                "version_number": 1,
                "claim_text": "Oakridge High School will remain closed for two days for routine preventive pest fumigation.",
                "source_origin": "Official School Parent Portal Notice",
                "recorded_date": "2026-03-10",
                "origin_type": "observed",
                "evidence_status": "supported"
            },
            {
                "version_number": 2,
                "claim_text": "All schools in the district are closed until further notice due to severe chemical health hazards.",
                "source_origin": "Forwarded WhatsApp Audio & Text Message",
                "recorded_date": "2026-03-12",
                "origin_type": "user_submitted",
                "evidence_status": "contradicted"
            },
            {
                "version_number": 3,
                "claim_text": "State Government has declared indefinite emergency holidays for all educational institutions statewide.",
                "source_origin": "Viral Social Media Post with Fake Seal",
                "recorded_date": "2026-03-14",
                "origin_type": "user_submitted",
                "evidence_status": "contradicted"
            }
        ],
        "evidence": [
            {
                "url": "https://education.state.gov/bulletins/2026-03-notice-412",
                "publisher": "State Department of School Education",
                "title": "Clarification: Operational Notice Regarding Oakridge High School",
                "publication_date": "2026-03-12",
                "retrieval_date": "2026-03-14",
                "excerpt": "Only Oakridge High School was scheduled for a 2-day preventive pest fumigation. No statewide holiday or district-wide closure has been ordered by the Department.",
                "classification": "contradictory",
                "relevance_reason": "Directly refutes the claim that all schools or all institutions statewide are closed.",
                "reliability_score": 96,
                "is_demo": True,
                "is_independent": True
            },
            {
                "url": "https://citypress.org/news/oakridge-school-maintenance-clarification",
                "publisher": "City Press Independent Bureau",
                "title": "Local School Reopens After Brief Cleaning: Rumours of State Shutdown Refuted",
                "publication_date": "2026-03-13",
                "retrieval_date": "2026-03-14",
                "excerpt": "Officials confirmed classes across all other 4,200 institutions in the state are functioning as normal according to official academic calendar schedules.",
                "classification": "contradictory",
                "relevance_reason": "Corroborates the Department notice by confirming all other campuses remain active.",
                "reliability_score": 91,
                "is_demo": True,
                "is_independent": True
            },
            {
                "url": "https://tribune-dispatch.net/local/health-inspection-oakridge",
                "publisher": "Tribune Dispatch",
                "title": "Routine Sanitation Undertaken at Oakridge Campus",
                "publication_date": "2026-03-11",
                "retrieval_date": "2026-03-14",
                "excerpt": "Administration at Oakridge High issued a private circular to parents regarding classroom deep-cleaning on Thursday and Friday.",
                "classification": "supporting",
                "relevance_reason": "Verifies that Version 1 was accurate regarding the single campus cleaning.",
                "reliability_score": 88,
                "is_demo": True,
                "is_independent": True
            }
        ]
    },
    {
        "demo_id": "demo-2",
        "title": "Disaster Relief Grant Condition Stripping",
        "category": "Government Grants & Finance",
        "summary": "Tracks how a strictly conditioned $5,000 flood relief grant with income caps and residency thresholds had all eligibility criteria removed to create viral false hopes.",
        "versions": [
            {
                "version_number": 1,
                "claim_text": "State Disaster Authority announces $5,000 relief grant for registered homeowners in 3 flood-hit counties who filed before Feb 15.",
                "source_origin": "Official State Gazette Notification",
                "recorded_date": "2026-02-18",
                "origin_type": "observed",
                "evidence_status": "supported"
            },
            {
                "version_number": 2,
                "claim_text": "Government announces immediate $5,000 cash grant for all state residents, no prior registration required.",
                "source_origin": "Forwarded SMS with Suspicious Claim Link",
                "recorded_date": "2026-02-21",
                "origin_type": "user_submitted",
                "evidence_status": "contradicted"
            }
        ],
        "evidence": [
            {
                "url": "https://disaster-management.gov/grants/flood-relief-guidelines-2026",
                "publisher": "State Disaster Management Authority",
                "title": "Official Guidelines: Targeted Flood Assistance Program",
                "publication_date": "2026-02-18",
                "retrieval_date": "2026-02-22",
                "excerpt": "The $5,000 emergency grant is restricted exclusively to primary homeowners in the three declared disaster counties who registered prior to February 15. It is not an unconditional universal payout.",
                "classification": "contradictory",
                "relevance_reason": "Directly refutes the forwarded claim that all state residents qualify unconditionally.",
                "reliability_score": 98,
                "is_demo": True,
                "is_independent": True
            },
            {
                "url": "https://publicaudit-watch.org/reports/disaster-fund-criteria",
                "publisher": "Public Accountability Monitor",
                "title": "Factsheet: Verifying Eligibility Rules for Disaster Relief",
                "publication_date": "2026-02-20",
                "retrieval_date": "2026-02-22",
                "excerpt": "Social media posts claiming the deadline was extended to March 30 or that income limits were waived are false according to verified gazette notifications.",
                "classification": "contradictory",
                "relevance_reason": "Verifies that claims omitting filing requirements are misleading.",
                "reliability_score": 90,
                "is_demo": True,
                "is_independent": True
            }
        ]
    },
    {
        "demo_id": "demo-3",
        "title": "Clinical Trial Exaggeration to 'Miracle Cure'",
        "category": "Healthcare & Medical Science",
        "summary": "Demonstrates how an early-stage phase 1 safety study with 18 volunteers was stripped of all trial qualifications to deceptively proclaim an FDA-approved cancer cure.",
        "versions": [
            {
                "version_number": 1,
                "claim_text": "In an 18-patient Phase 1 clinical trial, compound TX-94 demonstrated safe preliminary tolerability; efficacy testing has not yet begun.",
                "source_origin": "Peer-Reviewed Medical Journal Abstract",
                "recorded_date": "2026-01-15",
                "origin_type": "observed",
                "evidence_status": "supported"
            },
            {
                "version_number": 2,
                "claim_text": "Miracle cure TX-94 receives breakthrough approval after curing terminal cancer patients in clinical trials.",
                "source_origin": "Sensational Wellness Blog & Instagram Reel",
                "recorded_date": "2026-01-20",
                "origin_type": "user_submitted",
                "evidence_status": "contradicted"
            }
        ],
        "evidence": [
            {
                "url": "https://fda.gov/drugs/regulatory-updates/tx94-advisory",
                "publisher": "Food & Drug Administration (FDA)",
                "title": "Regulatory Statement Regarding Unapproved Compound TX-94",
                "publication_date": "2026-01-22",
                "retrieval_date": "2026-01-25",
                "excerpt": "TX-94 has NOT received FDA approval for general clinical use or cancer cure therapy. Consumer warnings have been issued against clinics marketing it as a cure.",
                "classification": "contradictory",
                "relevance_reason": "Contradicts claims of FDA approval and marketing as a proven cure.",
                "reliability_score": 99,
                "is_demo": True,
                "is_independent": True
            },
            {
                "url": "https://health-journal.org/trials/oncology-phase1-results",
                "publisher": "Journal of Oncology Research",
                "title": "Phase 1 Dose Escalation Safety Profile of Compound TX-94",
                "publication_date": "2026-01-15",
                "retrieval_date": "2026-01-25",
                "excerpt": "TX-94 demonstrated acceptable tolerability in a cohort of 18 terminal cancer patients. Phase 2 efficacy testing has not commenced and no curative claims are warranted.",
                "classification": "contextual",
                "relevance_reason": "Confirms the initial early trial existence, while debunking cure claims.",
                "reliability_score": 97,
                "is_demo": True,
                "is_independent": True
            }
        ]
    }
]

def build_demo_investigation(raw_demo: Dict[str, Any]) -> Dict[str, Any]:
    """
    Constructs a fully populated, verified investigation data object
    from raw demo template, including DNA, mutations, scores and explanations.
    """
    built_versions = []
    prev_v_dna = None
    prev_v_text = None
    
    for v in raw_demo["versions"]:
        text = v["claim_text"]
        dna = extract_rumour_dna(text)
        
        mut_report = None
        if prev_v_text:
            mut_report = analyze_mutations(prev_v_text, text, prev_v_dna, dna)
            
        built_versions.append({
            "version_number": v["version_number"],
            "claim_text": text,
            "source_origin": v["source_origin"],
            "recorded_date": v["recorded_date"],
            "origin_type": v["origin_type"],
            "evidence_status": v["evidence_status"],
            "dna": dna.model_dump(),
            "changes_from_previous": mut_report.model_dump() if mut_report else None
        })
        prev_v_dna = dna
        prev_v_text = text

    # Convert evidence to EvidenceRecordSchema
    ev_records = [EvidenceRecordSchema(**e) for e in raw_demo["evidence"]]
    
    # Target latest version for primary evaluation
    latest_v = built_versions[-1]
    latest_dna = extract_rumour_dna(latest_v["claim_text"])
    latest_mut = built_versions[-1]["changes_from_previous"]
    if latest_mut:
        from backend.app.schemas.claim import MutationReportSchema
        latest_mut_obj = MutationReportSchema(**latest_mut)
    else:
        latest_mut_obj = None

    score_breakdown = calculate_evidence_score(latest_dna, ev_records)
    explanation = generate_human_explanation(latest_dna, ev_records, score_breakdown, latest_mut_obj)

    return {
        "demo_id": raw_demo["demo_id"],
        "title": raw_demo["title"],
        "summary": raw_demo["summary"],
        "is_demo": True,
        "verdict": score_breakdown.verdict,
        "score": score_breakdown.total_score,
        "score_breakdown": score_breakdown.model_dump(),
        "human_explanation": explanation,
        "status": "completed",
        "versions": built_versions,
        "evidence": [e.model_dump() for e in ev_records]
    }
