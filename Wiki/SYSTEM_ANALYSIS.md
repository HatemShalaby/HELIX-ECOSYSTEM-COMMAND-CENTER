# Helix Ecosystem — Enterprise Automation Architecture  
## Comprehensive System Analysis & Design Document  

**Version:** 2.0  
**Date:** 26 June 2026  
**Author:** System Architecture Review  
**Status:** Strategic Blueprint — Source of Truth  

---

# 📋 TABLE OF CONTENTS

1. [Project Identity & Objectives](#1-project-identity--objectives)
2. [Complete System Architecture](#2-complete-system-architecture)
3. [Module‑by‑Module Deep Dive](#3-module‑by‑module-deep-dive)
4. [Dynamic Workflow Maps (Input → Process → Output)](#4-dynamic-workflow-maps)
5. [Data Flow & Storage Architecture](#5-data-flow--storage-architecture)
6. [Model Routing Layer — Dynamic Discovery Design](#6-model-routing-layer--dynamic-discovery-design)
7. [Human‑in‑the‑Loop Philosophy & Save/Discard Protocol](#7-human‑in‑the‑loop-philosophy--savediscard-protocol)
8. [Current State Audit — What Exists vs. What’s Broken](#8-current-state-audit)
9. [Gap Analysis — Bugs, Violations & Missing Pieces](#9-gap-analysis)
10. [Target State Design — The Rebuilt Learning System](#10-target-state-design)
11. [Path Centralization & Configuration Management](#11-path-centralization--configuration-management)
12. [Metacognitive Layer — Self‑Improvement Wiring](#12-metacognitive-layer)
13. [Integration Map — Command Center ↔ Learning System](#13-integration-map)
14. [File Manifest — Complete Project Tree](#14-file-manifest)

---

# 1. PROJECT IDENTITY & OBJECTIVES

## 🎯 Core Mission

| Pillar | Description |
|--------|-------------|
| **Primary System** | Helix Ecosystem — Business Demand Automation Engine |
| **Current Active Project** | Command Center + Learning System (self‑study education engine) |
| **Future Layer** | Metacognitive monitor that observes & improves its own performance |
| **North Star** | Zero manual configuration. All model routing is dynamic. Human only decides what to learn and whether to save results. |

## 🔒 Non‑Negotiable Clean‑Code Constitution

1. **No hardcoded model names** — not as strings, not as substrings, not anywhere in source.
2. **No hardcoded absolute paths** — exactly one path‑constants file; all modules import from it.
3. **No disk writes without explicit human consent** — quiz results, lesson notes, and records are held in volatile memory until the human says “Save”.
4. **No answer leakage** — correct answers must never be embedded in the client‑side HTML or JavaScript.
5. **Dynamic discovery only** — models are discovered at runtime via REST API; routing tables are built from live registry responses.
6. **Sequential resource isolation** — LLM generation and Playwright browser execution never overlap; VRAM/RAM caps enforced.

---

# 2. COMPLETE SYSTEM ARCHITECTURE
┌──────────────────────────────────────────────────────────────────┐
│ HELIX ECOSYSTEM (H:) │
├──────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────┐ ┌──────────────────────────────┐ │
│ │ Command Center │ │ Learning System │ │
│ │ (00_command_ │ │ (02_learning_system/ │ │
│ │ center/) │ │ browser_engine/) │ │
│ │ │ │ │ │
│ │ • engine.py │ │ • orchestrator.py (brain) │ │
│ │ • ResourceGuard │ │ • education_engine.py │ │
│ │ • Action Parser │ │ • quiz_generator.py │ │
│ │ • JSON Logging │ │ • renderer.py (HTML) │ │
│ │ │ │ • feedback_handler.py │ │
│ │ │ │ • model_registry.py │ │
│ └─────────┬───────────┘ │ • quiz_automator.py │ │
│ │ │ • cleanup_env.py │ │
│ │ │ • path_config.py (NEW) │ │
│ │ └──────────────┬───────────────┘ │
│ │ │ │
│ ┌─────────▼───────────────────────────────▼───────────────┐ │
│ │ Shared Infrastructure │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │ │
│ │ │ 06_memory/ │ │ 05_archive/ │ │ config/ │ │ │
│ │ │ • command_ │ │ • old │ │ • model_ │ │ │
│ │ │ center_ │ │ sessions │ │ roles.json │ │ │
│ │ │ log.json │ │ │ │ • path_ │ │ │
│ │ │ • metacog- │ │ │ │ config.py │ │ │
│ │ │ nitive_ │ │ │ │ │ │ │
│ │ │ log.json │ │ │ │ │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────┘ │ │
│ └──────────────────────────────────────────────────────────┘ │
│ │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Model Serving Layer │ │
│ │ ┌────────────────┐ ┌─────────────────────────┐ │ │
│ │ │ Ollama │ │ LM Studio Models │ │ │
│ │ │ (port 11434) │ │ (imported via GGUF) │ │ │
│ │ │ │ │ │ │ │
│ │ │ • lfm2.5:8b │ │ • gemma16k (12B, 7.2G) │ │ │
│ │ │ • qwen3:8b │ │ • ministral10k (14B,9.1G)│ │ │
│ │ │ • local-agent- │ │ • granite (7B, 4.2G) │ │ │
│ │ │ qwen3 │ │ │ │ │
│ │ │ • qwen3.6:35b │ │ │ │ │
│ │ │ • deepseek-r1 │ │ │ │ │
│ │ │ • qwen2.5-coder │ │ │ │ │
│ │ └────────────────┘ └─────────────────────────┘ │ │
│ │ │ │
│ │ All models accessible via unified REST API │ │
│ │ GET /api/tags → live model registry │ │
│ │ POST /api/chat → inference │ │
│ └──────────────────────────────────────────────────────────┘ │
│ │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Wiki / Documentation │ │
│ │ • PROJECT_STATUS.md • HANDOFF_TO_NEXT_MODEL.md │ │
│ │ • COMMAND_CENTER.md • LEARNING_SYSTEM_ARCHITECTURE.md│ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘

text

---

# 3. MODULE‑BY‑MODULE DEEP DIVE

## 🅰️ Module A — Ingestion Layer (Future)

| Aspect | Detail |
|--------|--------|
| **Purpose** | Ingest unstructured business demands, validate schema, produce immutable JSON payloads |
| **Current Status** | Not yet implemented. Blueprint specifies regex fallbacks + schema validation. |
| **Output** | Validated JSON → feeds Module B |

## 🅱️ Module B — Command Center Engine (In Progress)

| File | Responsibility |
|------|----------------|
| `00_command_center/engine.py` | Accepts validated JSON payloads, parses action steps, executes sequentially, logs all actions |
| `ResourceGuard` class | Checks `psutil.virtual_memory().percent`; stalls if > 80% threshold |
| `command_center_log.json` | Structured execution log stored in `06_memory/` |

**Dynamic Model Usage:** The engine imports `ModelRegistry` from the learning system (no duplication) to obtain an LLM for reasoning tasks. It never hardcodes a model name.

**Current Gaps:**
- Metacognitive wiring not yet connected — quiz outcomes don’t feed back into the engine’s log.
- `engine.py` currently logs only to `command_center_log.json`, ignoring `metacognitive_log.json`.

## 🅲️ Module C — Browser Automation (Shared)

| File | Purpose |
|------|---------|
| `renderer.py` | Converts Markdown lessons into interactive HTML with embedded quiz engine |
| `quiz_automator.py` | Orchestrates Playwright headless browser for automated quiz testing |
| `orchestrator.py` | Top‑level coordinator — decides between human mode and auto‑test mode |

**Resource Throttling:** Playwright blocks images, media, fonts, and third‑party trackers to stay within VRAM limits. Browser execution is strictly sequential with LLM inference.

## 🅳️ Module D — Dynamic Discovery Engine (Design Phase)

| Component | Function |
|-----------|----------|
| `model_registry.py` | Queries Ollama REST API (`/api/tags`) at boot; builds dynamic routing table |
| `config/model_roles.json` | Maps logical roles (lesson, quiz, grading) to model preferences |
| Fallback logic | If config missing, selects smallest available model; never hardcodes names |

**This module must be rebuilt** — current implementation has two competing functions and hardcoded `"lfm2.5:8b"` string.

---

# 4. DYNAMIC WORKFLOW MAPS

## 📚 Learning System — Human Mode
INPUT PROCESS OUTPUT
───── ─────── ──────
User runs: ┌─────────────────────────────────┐ ┌──────────────┐
python orchestrator.py │ 1. ModelRegistry queries │ │ lessons/ │
"Machine Learning" │ Ollama /api/tags │ │ machine_ │
│ → builds live model table │ │ learning.md │
│ │ │ │
│ 2. education_engine.py │ │ lessons/ │
│ → LLM generates lesson │ │ machine_ │
│ → saves to lessons/.md │ │ learning. │
│ │ │ html │
│ 3. quiz_generator.py │ │ │
│ → LLM generates quiz │ │ Flask server │
│ → appends to same .md │ │ starts on │
│ → answers NOT embedded │ │ port 5000 │
│ → answers stored server-side │ │ │
│ │ │ Browser opens│
│ 4. renderer.py │ │ to interactive│
│ → converts .md to .html │ │ quiz page │
│ → quiz answers fetched via │ │ │
│ API (never in HTML) │ │ │
│ │ │ │
│ 5. Flask server starts │ │ │
│ → serves static HTML │ │ │
│ → /submit endpoint grades │ │ │
│ via LLM (server-side) │ │ │
│ → returns score + feedback │ │ │
│ → holds answers in RAM │ │ │
│ │ │ │
│ 6. Human completes quiz │ │ │
│ → sees "Save / Discard / │ │ │
│ Retake" buttons │ │ │
│ │ │ │
│ 7. Human clicks "Save" │ │ learning- │
│ → /save_session writes full │ │ records/ │
│ record to learning-records/ │ │ session_.md │
│ → updates metacognitive log │ │ │
└─────────────────────────────────┘ └──────────────┘

text

## 🤖 Learning System — Auto‑Test Mode
INPUT PROCESS OUTPUT
───── ─────── ──────
python orchestrator.py ┌─────────────────────────────────┐ ┌──────────────┐
"Topic" --test │ Steps 1‑5 identical to human │ │ All lesson │
│ mode above │ │ files created│
│ │ │ │
│ 6. Playwright launches headless │ │ learning- │
│ → iterates through questions │ │ records/ │
│ → submits mock answers │ │ session_*.md │
│ → receives grades via /submit │ │ │
│ │ │ command_ │
│ 7. Auto‑calls /save_session │ │ center_log │
│ → writes record to disk │ │ updated │
│ → updates metacognitive log │ │ │
│ │ │ │
│ 8. Prints summary, exits clean │ │ ✅ Test │
└─────────────────────────────────┘ │ complete │
└──────────────┘

text

## 🏗️ Command Center Engine Workflow
INPUT PROCESS OUTPUT
───── ─────── ──────
JSON payload: ┌─────────────────────────────────┐ ┌──────────────┐
[ │ 1. Engine validates payload │ │ 06_memory/ │
{"type":"log", │ schema │ │ command_ │
"params":{"msg": │ │ │ center_log. │
"Task started"}}, │ 2. For each action step: │ │ json │
{"type":"wait", │ → ResourceGuard.check_memory() │ │ │
"params":{"sec":5}},│ → if type="log": log message │ │ Console │
{"type":"reason", │ → if type="wait": sleep │ │ summary of │
"params":{"q": │ → if type="reason": call LLM │ │ execution │
"Summarize..."}} │ via ModelRegistry │ │ │
] │ │ │ │
│ 3. Logs all steps to JSON │ │ │
│ → appends timestamp, status │ │ │
└─────────────────────────────────┘ └──────────────┘

text

---

# 5. DATA FLOW & STORAGE ARCHITECTURE
┌─────────────────────────────────────────────────────────────┐
│ DATA STORAGE MAP │
├─────────────────────────────────────────────────────────────┤
│ │
│ lessons/ learning-records/ │
│ ├── topic.md ├── session_topic_date.md │
│ └── topic.html └── (written ONLY on Save) │
│ │
│ 06_memory/ 05_archive/ │
│ ├── command_center_log.json ├── (old sessions) │
│ └── metacognitive_log.json │
│ │
│ config/ │
│ └── model_roles.json │
│ { │
│ "lesson_model": "gemma16k", │
│ "quiz_model": "lfm2.5:8b", │
│ "grading_model": "lfm2.5:8b" │
│ } │
│ │
│ RAM (volatile — cleared on server stop) │
│ ├── current session answers │
│ ├── current quiz questions (with correct answers hidden) │
│ └── ModelRegistry cached model list │
└─────────────────────────────────────────────────────────────┘

text

---

# 6. MODEL ROUTING LAYER — DYNAMIC DISCOVERY DESIGN

## 🔌 The Correct Architecture
┌──────────────────────────────────────────────────────────┐
│ ModelRegistry (singleton) │
├──────────────────────────────────────────────────────────┤
│ │
│ init(): │
│ 1. GET http://127.0.0.1:11434/api/tags │
│ 2. Parse JSON response → list of {name, size, ...} │
│ 3. Load config/model_roles.json (if exists) │
│ 4. If missing, build fallback map from available models│
│ → Select smallest model for each role │
│ → NEVER hardcode any model name │
│ │
│ get_model(role: str) → str: │
│ 1. Look up role in loaded config │
│ 2. Verify model exists in live tag list │
│ 3. If not found, fall back to smallest available │
│ 4. Return model name │
│ │
│ refresh(): │
│ → Re‑query /api/tags (called when new model pulled) │
│ │
└──────────────────────────────────────────────────────────┘

text

## 🚫 What Must Be Removed

| Current Violation | Fix |
|-------------------|-----|
| `get_model()` hardcodes `"lfm2.5:8b"` | Delete function entirely |
| Three defensive parsing branches for `ollama.list()` | Use REST API only (stable JSON) |
| No support for LM‑Studio‑imported models | All models now served by Ollama; registry sees them all |

## 📋 The Unified Model Fleet

All models are registered in Ollama and appear in `/api/tags`:

| Model Name | Size | Best Role |
|------------|------|-----------|
| `gemma16k` | 7.2 GB | Lesson generation, complex grading |
| `ministral10k` | 9.1 GB | Deep reasoning, strategic planning |
| `lfm2.5:8b` | 5.2 GB | Fast quiz generation, lightweight grading |
| `qwen3:8b` | 5.2 GB | Alternative general-purpose |
| `local-agent-qwen3` | 5.0 GB | Agentic tool‑use tasks |
| `granite-4-h-tiny` | 4.2 GB | Ultra‑fast simple queries |
| `qwen3.6:35b-A3B` | 23 GB | Only for offline deep analysis (partial GPU) |

---

# 7. HUMAN‑IN‑THE‑LOOP PHILOSOPHY

## 🧑‍🎓 The Sole Decision Points
┌─────────────────────────────────────────────────────────┐
│ HUMAN CONTROL BOUNDARY │
├─────────────────────────────────────────────────────────┤
│ │
│ 1. CHOOSE TOPIC │
│ → "python orchestrator.py 'Reinforcement Learning'" │
│ │
│ 2. ANSWER QUESTIONS │
│ → Interactive browser session │
│ → Each answer graded in real‑time │
│ │
│ 3. DECIDE OUTCOME │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ SAVE │ │ DISCARD │ │ RETAKE │ │
│ └────┬─────┘ └────┬─────┘ └────┬─────┘ │
│ │ │ │ │
│ ▼ ▼ ▼ │
│ Write to Clear RAM Restart quiz │
│ learning- nothing fresh │
│ records/ written │
│ │
│ ⚠️ NOTHING is written to disk until human clicks SAVE │
└─────────────────────────────────────────────────────────┘

text

## 🔐 Answer Leakage Prevention

| Problem | Solution |
|---------|----------|
| Correct answers visible in HTML source | Answers stored **only** in server RAM; quiz page fetches question text via API; correct answers never sent to client |
| Quiz markdown contains answer key | `quiz_generator.py` separates questions and answers; only questions go into rendered HTML; answers stay in server memory |
| Browser DevTools can reveal answers | There’s nothing to reveal — the client never receives correct answers |

---

# 8. CURRENT STATE AUDIT

## ✅ What Works

| Component | Status |
|-----------|--------|
| Lesson generation via LLM | ✅ Functional |
| Quiz generation and appending to markdown | ✅ Functional |
| Markdown → HTML rendering | ✅ Functional |
| Headless Playwright browser automation | ✅ Functional (with quiz‑completion detection) |
| Flask feedback server (basic grading) | ⚠️ Partially functional |
| Model registry (concept) | ❌ Broken — two competing implementations |
| Session record writing | ⚠️ Writes automatically — violates human‑in‑the‑loop |
| Path management | ❌ Absolute paths duplicated across 6+ files |
| Answer leakage prevention | ❌ Not implemented — answers embedded in markdown |

## 📁 Actual File Inventory
H:\AI Automation Engineering
├── architecture_blueprint.md
├── Rawzone/
│ └── skills/
└── Command Center Project/
├── Raw/
├── Wiki/
├── Index/
├── .clinerules
├── 00_command_center/
│ ├── engine.py
│ └── test_engine.py
├── 01_personal_context/
├── 02_learning_system/
│ ├── LEARNING_TRACKER.md
│ ├── NOTES.md
│ ├── RESOURCES.md
│ ├── assets/
│ ├── docs/
│ ├── lessons/
│ ├── learning-records/
│ ├── reference/
│ └── browser_engine/
│ ├── .venv/
│ ├── .vscode/
│ ├── pycache/
│ ├── orchestrator.py ← needs refactor
│ ├── education_engine.py ← needs review
│ ├── quiz_generator.py ← needs answer separation
│ ├── quiz_automator.py
│ ├── renderer.py ← needs path fix
│ ├── feedback_handler.py ← needs grade_answer + save gate
│ ├── model_registry.py ← needs full rebuild
│ ├── test_integration.py
│ └── cleanup_env.py
├── 03_skills_system/
├── 04_helix_mini/
├── 05_archive/
└── 06_memory/
├── command_center_log.json
└── metacognitive_log.json ← needs wiring

text

---

# 9. GAP ANALYSIS

## 🔴 Critical Bugs

| # | Bug | Location | Impact |
|---|-----|----------|--------|
| 1 | `get_model()` hardcodes `"lfm2.5:8b"` | `model_registry.py` | Violates clean‑code constitution; breaks when model not present |
| 2 | `grade_answer` imported but doesn’t exist | `feedback_handler.py` → `education_engine.py` | **Crashes on first quiz submission** |
| 3 | Correct answers embedded in rendered HTML | `quiz_generator.py` + `renderer.py` | Answer leakage — human can see correct answers in page source |
| 4 | Session written to disk on every answer | `feedback_handler.py` | Violates human‑in‑the‑loop; no save/discard gate |
| 5 | Absolute paths duplicated 6+ times | `orchestrator.py`, `renderer.py`, `quiz_generator.py`, `education_engine.py`, `feedback_handler.py`, `cleanup_env.py` | Any folder rename breaks entire project |

## 🟡 Design Gaps

| # | Gap | Description |
|---|-----|-------------|
| 6 | No path centralization | Every file constructs its own `H:\AI Automation Engineering\...` string |
| 7 | Model registry is Ollama‑only | LM‑Studio‑imported models (Granite, Gemma, Ministral) invisible to registry even though they’re now in Ollama |
| 8 | `metacognitive_log.json` marked “future” | Quiz outcomes don’t feed back into any self‑improvement loop |
| 9 | `orchestrator.py` uses `input()` for real mode | Human‑facing flow should be browser‑based, not terminal |
| 10 | No config file for model roles | Preferences must be editable without touching source code |

---

# 10. TARGET STATE DESIGN

## 🎯 The Rebuilt Learning System — Complete Specification

### File Changes Required

| File | Action | Reason |
|------|--------|--------|
| `path_config.py` | **CREATE** | Single source of truth for all project paths |
| `model_registry.py` | **REWRITE** | Remove hardcoding, use REST API, add role config |
| `config/model_roles.json` | **CREATE** | Editable role→model mapping |
| `feedback_handler.py` | **REWRITE** | Add `grade_answer()`, add save/discard endpoints, remove auto‑write |
| `quiz_generator.py` | **MODIFY** | Separate questions from answers; store answers server‑side |
| `renderer.py` | **MODIFY** | Remove answer embedding; fetch via API; use path_config |
| `orchestrator.py` | **REWRITE** | Human mode = prepare + serve; auto mode = full headless test + auto‑save |
| `education_engine.py` | **MODIFY** | Use path_config; ensure no hardcoded paths |
| `quiz_automator.py` | **MODIFY** | Use path_config |
| `cleanup_env.py` | **MODIFY** | Use path_config |
| `06_memory/metacognitive_log.json` | **INITIALIZE** | Empty structured array ready for writes |

### Human‑Mode Page Flow
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Lesson │ │ Quiz │ │ Results │ │ Decision │
│ Display │────▶│ (one by │────▶│ Summary │────▶│ Page │
│ │ │ one) │ │ │ │ │
│ Read-only │ │ Type │ │ Score per │ │ [Save] │
│ content │ │ answers │ │ question │ │ [Discard] │
│ │ │ Submit │ │ + tips │ │ [Retake] │
└─────────────┘ └─────────────┘ └─────────────┘ └──────┬──────┘
│
┌─────────▼─────────┐
│ Save → writes │
│ learning-records │
│ + metacognitive │
│ log update │
│ │
│ Discard → clear │
│ RAM, no writes │
│ │
│ Retake → restart │
│ quiz from Q1 │
└───────────────────┘

text

### API Endpoints (Flask Server)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Serves the interactive lesson+quiz HTML page |
| `/api/questions?topic=X` | GET | Returns question texts ONLY (no answers) |
| `/api/submit` | POST | Accepts answer; returns score + feedback |
| `/api/save_session` | POST | Writes accumulated answers to disk |
| `/api/discard_session` | POST | Clears session memory without writing |
| `/api/retake` | POST | Resets quiz state for same topic |

---

# 11. PATH CENTRALIZATION

## `browser_engine/path_config.py` — The Single Source of Truth
Variable → Resolves To
────────────────────────────────────────────────────────────────
BASE_DIR → H:\AI Automation Engineering\Command Center Project
LEARNING_SYS_DIR → BASE_DIR\02_learning_system
LESSONS_DIR → LEARNING_SYS_DIR\lessons
RECORDS_DIR → LEARNING_SYS_DIR\learning-records
MEMORY_DIR → BASE_DIR\06_memory
CONFIG_DIR → BASE_DIR\config
BROWSER_ENGINE_DIR → LEARNING_SYS_DIR\browser_engine

text

**Rule:** Every `.py` file imports from `path_config`. No file constructs its own absolute path. A single folder rename updates exactly one file.

---

# 12. METACOGNITIVE LAYER

## Self‑Improvement Wiring
Quiz Session Complete
│
▼
┌──────────────────────────────┐
│ /save_session endpoint │
│ (triggered by human "Save") │
└──────────────┬───────────────┘
│
▼
┌──────────────────────────────┐
│ 1. Write session record │
│ → learning-records/ │
│ session_topic_date.md │
│ │
│ 2. Compute metrics: │
│ • Average score │
│ • Per‑question scores │
│ • LLM latencies │
│ • Model used │
│ • Errors encountered │
│ │
│ 3. Append to: │
│ 06_memory/ │
│ metacognitive_log.json │
│ │
│ 4. (Future) Read by │
│ orchestrator to adjust │
│ model selection, quiz │
│ difficulty, or flag │
│ anomalies │
└──────────────────────────────┘

text

---

# 13. INTEGRATION MAP
┌──────────────────────────────────────────────────────────────┐
│ CROSS‑MODULE INTEGRATION POINTS │
├──────────────────────────────────────────────────────────────┤
│ │
│ ModelRegistry │
│ ├── imported by: education_engine, quiz_generator, │
│ │ feedback_handler, engine.py │
│ └── reads: config/model_roles.json │
│ │
│ path_config.py │
│ ├── imported by: EVERY .py file in browser_engine │
│ └── imported by: 00_command_center/engine.py │
│ │
│ feedback_handler.py │
│ ├── imports: ModelRegistry, path_config │
│ ├── endpoints called by: renderer.py (client‑side JS), │
│ │ orchestrator.py (auto‑save) │
│ └── writes to: learning-records/ (on save), │
│ metacognitive_log.json (on save) │
│ │
│ engine.py (Command Center) │
│ ├── imports: ModelRegistry, path_config │
│ └── logs to: command_center_log.json │
│ │
└──────────────────────────────────────────────────────────────┘

text

---

# 14. FILE MANIFEST — COMPLETE PROJECT TREE
H:\AI Automation Engineering
│
├── architecture_blueprint.md ← System blueprint (source of truth)
│
├── Rawzone/
│ └── skills/
│
└── Command Center Project/
│
├── config/ ← NEW: Centralized configuration
│ └── model_roles.json ← Role → model mapping
│
├── 00_command_center/
│ ├── engine.py ← Orchestration engine
│ └── test_engine.py ← Pytest tests
│
├── 01_personal_context/
│
├── 02_learning_system/
│ ├── LEARNING_TRACKER.md
│ ├── NOTES.md
│ ├── RESOURCES.md
│ ├── assets/
│ ├── docs/
│ ├── lessons/ ← Generated .md + .html files
│ ├── learning-records/ ← Saved session records
│ ├── reference/
│ │
│ └── browser_engine/
│ ├── .venv/
│ ├── path_config.py ← NEW: Single source of paths
│ ├── model_registry.py ← REWRITE: Dynamic discovery
│ ├── orchestrator.py ← REWRITE: Human/auto modes
│ ├── education_engine.py ← MODIFY: Use path_config
│ ├── quiz_generator.py ← MODIFY: Separate answers
│ ├── quiz_automator.py ← MODIFY: Use path_config
│ ├── renderer.py ← MODIFY: No answer leakage
│ ├── feedback_handler.py ← REWRITE: grade_answer + save gate
│ ├── test_integration.py
│ └── cleanup_env.py ← MODIFY: Use path_config
│
├── 03_skills_system/
├── 04_helix_mini/
├── 05_archive/
│
├── 06_memory/
│ ├── command_center_log.json ← Engine execution logs
│ └── metacognitive_log.json ← Quiz performance metrics
│
├── Wiki/
│ ├── PROJECT_STATUS.md
│ ├── HANDOFF_TO_NEXT_MODEL.md
│ ├── COMMAND_CENTER.md
│ └── LEARNING_SYSTEM_ARCHITECTURE.md ← NEW
│
├── Raw/
├── Index/
└── .clinerules

text

---

# 📌 SUMMARY — THE PATH FORWARD

| Priority | Task | Effort |
|----------|------|--------|
| 🔴 P0 | Rewrite `model_registry.py` — remove hardcoding, use REST API | High |
| 🔴 P0 | Rewrite `feedback_handler.py` — add `grade_answer()`, save/discard endpoints | High |
| 🔴 P0 | Modify `quiz_generator.py` — separate questions from answers | Medium |
| 🔴 P0 | Create `path_config.py` — update all files to import from it | Medium |
| 🟡 P1 | Rewrite `orchestrator.py` — human mode = serve, auto mode = test + auto‑save | High |
| 🟡 P1 | Modify `renderer.py` — remove answer embedding, fetch via API | Medium |
| 🟡 P1 | Create `config/model_roles.json` — editable role mapping | Low |
| 🟢 P2 | Wire metacognitive log updates into `/save_session` | Low |
| 🟢 P2 | Update all Wiki documentation | Low |

---

*This document serves as the definitive source of truth for the Helix Ecosystem architecture. All implementation decisions must reference this specification. No code shall be written that violates the Clean‑Code Constitution stated in Section 1.*