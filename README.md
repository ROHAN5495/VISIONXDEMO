# EVOLUTION TRACKER 2.0 — VISION X

> **"Don't just verify the claim. Track how it changed."**  
> **Official Tagline:** `VERIFY BEFORE YOU SHARE.`

---

## 🏆 Hackathon Overview

- **Team Name:** VISION X  
- **Official Track:** Automated FactChecking & Misinformation  
- **Mandate:** *"Build a claim-verification platform that compares a statement against trusted sources, identifies contradictory evidence, and traces how a claim changes as it spreads."*

---

## 1. Product Differentiation & Core Philosophy

Most fact-checking tools only return a simplistic label: `True` or `False`. 

**Evolution Tracker** answers the deeper investigative question:
> *"How did a statement change, what qualifiers or conditions were removed, and when did it become misleading?"*

Misinformation rarely starts out 100% fabricated. It usually begins as a localized, routine, or tentative report that mutates through forwards, social media posts, and sensationalized re-shares. Evolution Tracker investigates that entire journey.

---

## 2. Four Signature Features

### 🧬 Feature A — Rumour DNA
Every statement is broken down into a structured factual fingerprint:
- **Main Subject:** Core topic (e.g., School Closure, Public Health, Disaster Relief).
- **Named Entities:** Organizations, Persons, Locations, Dates, Quantities.
- **Geographical Scope:** `specific` → `local` → `district` → `statewide` → `national` → `global`.
- **Factual Assertion:** The core predicate of the message.
- **Semantic Hash:** Stable identifier for tracking variant families.
- **Visual Family Tree:** Discovers related claims even when their wording differs.

### 🔬 Feature B — Mutation Detector
Compares two claim versions side-by-side using an intuitive **4-Color Code**:
- 🟩 **Green:** Added information or details.
- 🟥 **Red:** Removed information.
- 🟨 **Amber:** Potentially misleading change (scope escalation, alarming modifiers, stripped caveats).
- 🟦 **Blue:** Contextual modification (minor phrasing adjustments).
- **Plain Language Explanation:** Summarizes modifications in everyday words without prematurely accusing legitimate corrections of being misinformation.

### 🗺️ Feature C — Rumour Journey Map
Interactive chronological timeline connecting versions (v1 → v2 → v3):
- **Version Number & Recorded Date**
- **Submission Origin** (e.g., School Parent Portal, WhatsApp forward, Viral post)
- **Origin Transparency:** Strictly distinguishes **Observed Notice**, **User-Submitted Forward**, and **AI-Inferred Relationship**.
- **Evidence Status:** Supported, Contradicted, or Altered.
- *Strict Rule:* Never invents fake social media propagation paths, authors, or timestamps.

### 💬 Feature D — Human Truth Explanation
An explanation engine designed for everyday people:
- Short, natural sentences.
- Evidence explained **before** stating conclusions.
- Honest admission of uncertainty when sources are insufficient.
- Zero AI buzzwords, repetitive intros, or pseudo-scientific probabilities.

---

## 3. Honest Credibility Scoring (0–100)

We do not present our score as a statistically calibrated probability of absolute truth. Instead, it is an empirical assessment of verifiable records using 6 transparent signals:

1. **Source Reliability (0–25 pts):** Reputation and verification tier of publishing authorities.
2. **Direct Relevance (0–20 pts):** How directly the evidence refutes or supports the assertion.
3. **Independent Corroboration (0–20 pts):** Multiple non-circular publishers confirming the facts.
4. **Contradictory Evidence Penalty (0 to -45 pts):** Heavy deduction for direct factual contradictions.
5. **Recency (0–10 pts):** Freshness of indexed records.
6. **Verification Completeness (0–10 pts):** Full entity and condition coverage.

### Possible Verdicts:
- **Supported** (80–100 pts)
- **Mostly Supported** (65–79 pts)
- **Mixed Evidence** (45–64 pts)
- **Mostly Contradicted** (25–44 pts)
- **Contradicted** (0–24 pts)
- **Unverified:** Displayed whenever evidence is missing or unreliable:
  > *"Not enough reliable evidence to assess this claim."* (No artificial score forced)

---

## 4. Demonstration Mode (100% Offline Ready)

Judges can explore the platform immediately without paid API keys, internet connectivity, or account registration.

### 🎪 Prepared Demonstrations:
1. **DEMO 1 — School Closure Rumour Escalation:**
   - *v1:* Oakridge High School will remain closed for two days for routine preventive pest fumigation. (Observed notice)
   - *v2:* All schools in the district are closed until further notice due to severe chemical health hazards. (WhatsApp forward)
   - *v3:* State Government has declared indefinite emergency holidays for all educational institutions statewide. (Viral fake seal)
2. **DEMO 2 — Disaster Relief Grant Condition Stripping:**
   - *v1:* $5,000 grant for registered homeowners in 3 flood-hit counties who filed before Feb 15.
   - *v2:* Government announces immediate $5,000 cash grant for all state residents, no prior registration required.
3. **DEMO 3 — Clinical Trial Exaggeration to 'Miracle Cure':**
   - *v1:* In an 18-patient Phase 1 trial, compound TX-94 demonstrated safe preliminary tolerability; efficacy testing not begun.
   - *v2:* Miracle cure TX-94 receives breakthrough approval after curing terminal cancer patients in clinical trials.

All demo records are prominently labeled with a **DEMO INVESTIGATION** badge.

---

## 5. Technology Stack

- **Backend:** Python 3.10+, FastAPI, Pydantic v2, SQLAlchemy (modular SQLite database).
- **Frontend:** React 18, Vite, Tailwind CSS, React Router v6, Lucide React, Recharts.
- **Runtimes:** Fully compatible with Windows (Command Prompt / PowerShell) and Unix/macOS.

---

## 6. Exact Startup Commands (Step-by-Step for VISION X)

### Step 1: Clone or Open Workspace
Open a PowerShell terminal in the project directory:
```powershell
cd c:\Users\debab\OneDrive\Desktop\VISIONX01
```

### Step 2: Start the Backend Server (Terminal 1)
```powershell
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- Backend starts at: `http://127.0.0.1:8000`
- Interactive Swagger API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/health`

### Step 3: Start the Frontend Application (Terminal 2)
```powershell
$env:PATH = "$PWD\.tools\node;$env:PATH"
cd frontend
npm run dev
```
- Open your browser at: `http://localhost:5173`

---

## 7. Running Automated Tests

### Backend Tests (pytest)
```powershell
python -m pytest backend/tests -v
```
*Covers:* Empty claim validation, valid submission, database persistence, DNA extraction, mutation detector diffing, credibility score signals, and error handling.

### Frontend Tests (vitest)
```powershell
$env:PATH = "$PWD\.tools\node;$env:PATH"
cd frontend
npx vitest run
```
*Covers:* Demo badge rendering, honest scoring without forced numbers, 4-color diff highlighters, evidence cards, 7-step pipeline stepper, and landing page elements.

### Production Build Verification
```powershell
$env:PATH = "$PWD\.tools\node;$env:PATH"
cd frontend
npm run build
```

---

## 8. External API Configuration (Optional)

Copy `.env.example` to `.env` if you wish to configure live search providers:
```env
# Optional Live Search Providers
# If unset, the platform operates seamlessly in offline demonstration mode.
SERPAPI_API_KEY=your_serpapi_key_here
TAVILY_API_KEY=your_tavily_key_here
```
*Note:* External search outputs are treated as untrusted data to protect against prompt injection.

---

## 9. Required Application Pages

1. **Landing Page (`/`):** Mission overview, core question, signature feature highlights, and direct demo launchers.
2. **Investigation Dashboard (`/dashboard`):** Real-time claim statistics, quick verification search bar, and recent investigations registry.
3. **Verify a Claim (`/verify`):** Multi-version submission form supporting single claims or full evolutionary sequences.
4. **Investigation Report (`/report/:id`):** Full investigative dossier with credibility gauge, truth explanation, mutation diff, and evidence cards.
5. **Rumour DNA (`/dna`):** Interactive fingerprint analyzer and visual family tree map.
6. **Mutation Detector (`/mutations`):** Side-by-side claim comparison with 4-color visual tokens and natural language summary.
7. **Rumour Journey Map (`/journey`):** Interactive chronological lineage map (v1 → v2 → v3) with origin transparency.
8. **Evidence Explorer (`/evidence`):** Filterable source registry (supporting, contradictory, contextual, publisher reliability).
9. **Investigation History (`/history`):** Persistent database archive with search, filter, and deletion.

---

## 10. Known Limitations & Roadmap

- **Multi-lingual Entity Expansion:** Currently optimized for English public notices and viral claims.
- **MySQL / PostgreSQL Migration:** Database operations are written with modular SQLAlchemy ORM queries for one-line configuration switching to MySQL in enterprise deployments.

---

**Developed with ❤️ by VISION X for the Misinformation & Automated FactChecking Hackathon.**  
*VERIFY BEFORE YOU SHARE.*
