# EVOLUTION TRACKER 2.0 — VISION X

> **"Don't just verify the claim. Track how it changed."**  
> **Official Tagline:** `VERIFY BEFORE YOU SHARE.`

---

## 🏆 Hackathon Overview

- **Team Name:** VISION X
- **Team Members:** 1.
- **                 ** 2.
-   **             **   3.
-   **               ** 4.
-              
- **Official Track:** Automated FactChecking & Misinformation  
- **Mandate:** *"Build a claim-verification platform that compares a statement against trusted sources, identifies contradictory evidence, and traces how a claim changes as it spreads."*

---

## 1. Product Differentiation & Core Philosophy

Most traditional fact-checking websites only display whether a claim is True or False.

**Evolution Tracker** investigates the complete evolutionary journey of information:
> *"How did a statement change, what qualifiers or conditions were removed, and when did it become misleading?"*

Misinformation rarely starts out 100% fabricated. It usually begins as a localized, routine, or tentative report that mutates through forwards, social media posts, and sensationalized re-shares:
- Caveats like *"in lab animals"* or *"only campus #1"* are stripped away.
- Scope escalates from *"one school"* to *"all schools statewide"*.
- Unsubstantiated claims are appended to authentic news.

Evolution Tracker fingerprints the claim, detects mutations, maps the contagion timeline, and grounds every verdict in verifiable evidence.

---

## 2. Signature Features

```
┌────────────────────────────────────────────────────────────────────────┐
│                      FOUR SIGNATURE INNOVATIONS                        │
│                                                                        │
│   🧬 FEATURE A: RUMOUR DNA       🔬 FEATURE B: MUTATION DETECTOR       │
│   Genomic fingerprinting &        4-color diff engine isolating added, │
│   visual claim families.          removed, & inflated factual claims.  │
│                                                                        │
│   🗺️ FEATURE C: JOURNEY MAP      🛡️ FEATURE D: EVIDENCE & AI          │
│   Interactive timeline from       Grounded live web search + Google    │
│   local fact to viral panic.      Gemini 3.5 AI & rule-based fallback. │
└────────────────────────────────────────────────────────────────────────┘
```

### 🧬 Feature A — Rumour DNA
Every statement is decomposed into a structured factual fingerprint:
- **Main Subject:** Core topic (e.g., School Closure, Public Health, Disaster Relief).
- **Named Entities:** Organizations, Persons, Locations, Dates, Quantities.
- **Geographical Scope:** `specific` → `local` → `district` → `statewide` → `national` → `global`.
- **Factual Assertion:** The core predicate of the message.
- **Semantic Hash:** Stable identifier for tracking variant families.
- **Visual Family Tree:** Discovers related claims even when wording differs.
- *Anti-Assumption Safeguard:* The system never assumes similar wording means identical facts—it actively highlights divergent numbers, dates, or altered scopes.

### 🔬 Feature B — Mutation Detector
Compares two claim versions side-by-side using an intuitive **4-Color Diff Engine**:
- 🟩 **Green (+): Added Information** — New entities, secondary assertions, or unverified claims.
- 🟥 **Red (-): Removed Information** — Dropped conditions, missing caveats, or deleted context.
- 🟨 **Amber (!): Misleading Mutation** — Scope inflation (*"one school"* $\rightarrow$ *"all schools"*), extreme quantifiers, or exaggerated numbers.
- 🟦 **Blue (i): Contextual Modification** — Grammar cleanups, timestamps, or legitimate corrections.
- **Neutral, Non-Accusatory Tone:** Explains changes in plain language without blindly labeling every edit as malicious.

### 🗺️ Feature C — Rumour Journey Map
Interactive chronological timeline connecting versions ($v_1 \rightarrow v_2 \rightarrow v_3$):
- **Version Number & Timestamp**
- **Submission Origin:** (e.g., School Parent Notice $\rightarrow$ WhatsApp forward $\rightarrow$ Viral post)
- **Origin Transparency:** Strictly distinguishes **Observed Notice**, **User-Submitted Forward**, and **AI-Inferred Relationship**.
- **Evidence Status:** Supported, Contradicted, or Altered.
- *Strict Rule:* Never invents fake social media propagation paths, authors, or timestamps.

### 💬 Feature D — Human Truth Explanation & Curated Excerpts
An explanation engine designed for everyday users:
- **Two-Tier Evidence Layout:**
  - **Curated Key Evidence Highlights (Top 2–3):** Most relevant excerpts prominently displayed with an explicit `Search Snippet` badge, stance label, and publisher citation.
  - **Full Verifiable Evidence Registry (Bottom):** Complete database of all retrieved sources, domain reliability scores, publication dates, and original URLs.
- **Honest Uncertainty:** Clearly explains what documented records establish *before* stating conclusions.

---

## 3. Calibrated Claim Verdict & Multi-Factor Confidence

Instead of forcing nuanced claims into an arbitrary binary label, Evolution Tracker delivers:

### ⚖️ Four Standardized Verdict Categories
1. **`LIKELY TRUE`** — Reliable, relevant evidence confirms the core assertion with no unresolved refutations.
2. **`LIKELY FALSE`** — Reliable, relevant evidence contradicts the assertion, identifies opposing facts, or debunks the claim.
3. **`MIXED / PARTIALLY TRUE`** — Part of the claim is factual while other assertions are refuted, unverified, or exaggerated.
4. **`UNVERIFIED`** — Available evidence is insufficient, irrelevant, purely contextual, or inconclusive (no artificial score is forced).

Directly below the verdict, an explicit **Verdict Rationale** explains the exact evidence-based reasoning.

### 🎯 Multi-Factor Confidence Indicator
Confidence reflects evidence quality and independent consensus—**not** a naive average of publisher trust scores:
- **`HIGH` ($\ge 80\%$):** Multiple independent root domains ($\ge 2$) agreeing on the stance with high relevance ($\ge 0.60$) and zero unresolved contradictions.
- **`MEDIUM` ($50\% - 79\%$):** Moderate evidence from 1–2 sources or mixed evidence where one stance holds preponderance.
- **`LOW` ($< 50\%$ or `None`):** Single source, low relevance, conflicting reports, contextual-only results, or offline fallback mode.
- **Syndication Deduplication:** Multiple republished wire copies from the same news organization are counted as a single source to prevent artificial consensus inflation.

---

## 4. Grounded AI Integration & Multi-Tier Fallback

Evolution Tracker integrates **Google Gemini 3.5 Flash** as an evidence interpretation assistant, backed by strict safeguards:

```
                  ┌───────────────────────────────┐
                  │    User Claim Submission      │
                  └──────────────┬────────────────┘
                                 │
                                 ▼
                  ┌───────────────────────────────┐
                  │  Tavily Live Web Search API   │
                  │  (Untrusted Data Sanitation)  │
                  └──────────────┬────────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
        [API Key Available]             [Missing / Quota / Timeout]
                 │                               │
                 ▼                               ▼
  ┌──────────────────────────────┐ ┌──────────────────────────────┐
  │ Google Gemini 3.5 AI Engine  │ │ Local Rule-Based NLP Engine  │
  │ • Strict snippet grounding   │ │ • Directional bound phrases  │
  │ • Disambiguates questions    │ │ • Concessive idiom filter    │
  │ • Multi-model fallback       │ │ • Question refutation rules  │
  └──────────────┬───────────────┘ └──────────────┬───────────────┘
                 │                               │
                 └───────────────┬───────────────┘
                                 │
                                 ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  Transparent Analysis Mode Tagging                           │
  │  [ live_search_ai  |  live_search_rules  |  offline_fallback ]│
  └──────────────────────────────────────────────────────────────┘
```

1. **Strict Snippet Grounding:** Operates strictly on retrieved search snippets. The AI is forbidden from claiming to have read full articles or hallucinating external facts.
2. **Multi-Model Resilience:** Defaults to `gemini-3.5-flash` with automatic fallback to `gemini-3.1-flash-lite` and `gemini-3-flash-preview` during high-demand 503 spikes.
3. **100% Uptime Local Rule Engine:** If the Gemini API key is unset, times out (>12s), or exhausts its quota (HTTP 429), the deterministic local NLP engine seamlessly analyzes the snippets without interrupting the user.
4. **Transparent Analysis Mode Badges:** Every report displays an explicit badge:
   - `Live web search + AI-assisted analysis`
   - `Live web search + rule-based analysis`
   - `Offline fallback analysis`

---

## 5. Demonstration Mode (100% Offline Ready)

Judges can explore the platform immediately with zero external API keys or internet access.

### 🎪 Prepared Demonstrations:
1. **DEMO 1 — School Closure Rumour Escalation:**
   - *$v_1$:* Oakridge High School will remain closed for two days for routine preventive pest fumigation. *(Observed notice)*
   - *$v_2$:* All schools in the district are closed until further notice due to severe chemical health hazards. *(WhatsApp forward)*
   - *$v_3$:* State Government has declared indefinite emergency holidays for all educational institutions statewide. *(Viral fake circular)*
2. **DEMO 2 — Clinical Trial Exaggeration to 'Miracle Cure':**
   - *$v_1$:* In an 18-patient Phase 1 trial, compound TX-94 demonstrated safe tolerability in laboratory animal trials.
   - *$v_2$:* Miracle cure TX-94 receives breakthrough approval after curing terminal cancer patients in clinical trials.
3. **DEMO 3 — Celebrity Outpatient Checkup Hoax:**
   - *$v_1$:* Veteran actor attended a routine scheduled medical checkup at City Hospital.
   - *$v_2$:* Actor admitted to ICU in critical condition following sudden collapse.
   - *$v_3$:* Tragic breaking news: Veteran actor passes away in hospital.
4. **DEMO 4 — Banknote Watermark Redesign Demonetization:**
   - *$v_1$:* Central Bank issues technical circular updating security watermark filaments for upcoming currency batches.
   - *$v_2$:* Central Bank to phase out current currency notes; citizens advised to exchange cash.
   - *$v_3$:* Sudden midnight demonetization announced: All existing banknotes void starting tomorrow!

All demo records are prominently labeled with a **DEMO INVESTIGATION** badge.

---

## 6. Local Network & Mobile Accessibility

Evolution Tracker can be accessed simultaneously from **smartphones, tablets, and other laptops** connected to the same local Wi-Fi or LAN:

- **Host Binding:** Configured to bind on `0.0.0.0` (all network interfaces).
- **Reverse Proxy:** Vite serves the frontend to any device and proxies `/api` calls directly to the local FastAPI backend.
- **Automatic IP Discovery:** Starting the backend with `python run.py` automatically detects and prints your LAN IP:
  ```text
  ===================================================
    EVOLUTION TRACKER 2.0 - VISION X BACKEND SERVER
    VERIFY BEFORE YOU SHARE
  ===================================================
  Local Host     : http://localhost:8000
  Network (LAN)  : http://10.125.147.120:8000
  Access Web App : http://10.125.147.120:5173
  ===================================================
  ```

---

## 7. Technology Stack

- **Backend:** Python 3.10+, FastAPI, Pydantic V2, SQLAlchemy ORM (modular SQLite with auto-migrations), HTTPX async client.
- **Frontend:** React 18, Vite, Tailwind CSS, React Router V6, Lucide React, Canvas-Confetti.
- **AI & Search:** Google Gemini Developer API (`gemini-3.5-flash`), Tavily Search API.
- **Runtimes:** Standalone portable Node.js runtime bundled in `.tools/node` (zero global installation required on Windows).

---

## 8. Exact Startup Commands

### Option A: Quick Start (Double-Click Batch Files)
1. **Start Backend:** Double-click `start_backend.bat` *(or run `python run.py`)*  
   $\rightarrow$ Runs on `http://127.0.0.1:8000` (and `http://<LAN_IP>:8000`).
2. **Start Frontend:** Double-click `start_frontend.bat`  
   $\rightarrow$ Runs on `http://localhost:5173` (and `http://<LAN_IP>:5173`).
3. Open browser to **`http://localhost:5173`** (or access from your phone using the LAN URL).

### Option B: Manual Terminal Execution (PowerShell)
```powershell
# Terminal 1 — Backend
python run.py

# Terminal 2 — Frontend
$env:PATH = "$PWD\.tools\node;$env:PATH"
cd frontend
npm run dev -- --host
```

---

## 9. Running Automated Tests

The codebase includes comprehensive test suites across backend and frontend:

### Backend Tests (34 Pytest Tests)
```powershell
python -m pytest backend/tests -v
```
*Covers:* Rumour DNA extraction, entity & scope detection, 4-color mutation diffs, evidence stance classification, directional bound phrases (*"The Sun rises in the west"* refutation test), negative statement handling, syndication deduplication, AI timeout & 503 fallback, and verdict calibration.

### Frontend Tests (10 Vitest Tests)
```powershell
$env:PATH = "$PWD\.tools\node;$env:PATH"
npm test --prefix frontend
```
*Covers:* Score gauge & verdict banners, confidence indicators, Key Evidence Highlights, Search Snippet disclaimers, Analysis Mode badges, and Visual Family Trees.

### Production Build Verification
```powershell
$env:PATH = "$PWD\.tools\node;$env:PATH"
npm run build --prefix frontend
```

---

## 10. External API Configuration (Optional)

Configure your API keys in `.env` in the project root:
```env
# Server Binding
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=*

# Database
DATABASE_URL=sqlite:///./evolution_tracker.db

# Live Search Provider (Optional)
TAVILY_API_KEY=your_tavily_api_key_here

# AI Interpretation Provider (Optional)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash
```

---

## 11. Application Pages & Routes

1. **Landing Page (`/`):** Mission overview, core question, signature feature highlights, and direct demo launchers.
2. **Investigation Dashboard (`/dashboard`):** Real-time claim statistics, quick verification search bar, and recent investigations registry.
3. **Verify a Claim (`/verify`):** Multi-version submission form supporting single claims or full evolutionary sequences.
4. **Investigation Report (`/report/:id`):** Full dossier with verdict banner, confidence rating, curated key excerpts, truth explanation, mutation diff, and full evidence registry.
5. **Rumour DNA (`/dna`):** Interactive fingerprint analyzer and visual family tree map.
6. **Mutation Detector (`/mutations`):** Side-by-side claim comparison with 4-color visual tokens and natural language summary.
7. **Rumour Journey Map (`/journey`):** Interactive chronological lineage map ($v_1 \rightarrow v_2 \rightarrow v_3$) with origin transparency.
8. **Evidence Explorer (`/evidence`):** Filterable source registry (supporting, contradictory, contextual, publisher reliability).
9. **Investigation History (`/history`):** Persistent database archive with search, filter, and deletion.

---

**Developed with ❤️ by VISION X for the Misinformation & Automated FactChecking Hackathon.**  
*VERIFY BEFORE YOU SHARE.*
