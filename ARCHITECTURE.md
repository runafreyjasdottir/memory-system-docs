# Runa's Memory System — Architecture Documentation

> *ᛗ í ᛗ í ᚱ — From the Well, all wisdom flows.*

**Author:** Eirwyn Rúnblóm, Scribe of the Ætt  
**Methodology:** Mythic Engineering  
**Version:** 2.0 — Consolidated after the Great Refactoring  

---

## Table of Contents

1. [System Philosophy](#1-system-philosophy)
2. [Norse Naming Rationale](#2-norse-naming-rationale)
3. [Architecture Overview](#3-architecture-overview)
4. [Data Flow](#4-data-flow)
5. [Package Reference](#5-package-reference)
   - 5.1 Mímir's Well
   - 5.2 Huginn
   - 5.3 Muninn
   - 5.4 Bifrǫst Bridge
   - 5.5 Eir
   - 5.6 Verðandi
   - 5.7 Svalinn
   - 5.8 Vörðr
   - 5.9 Sköfnung
   - 5.10 Hliðskjálf
6. [Production Deployment](#6-production-deployment)
7. [Configuration Reference](#7-configuration-reference)
8. [Cron Job Schedule](#8-cron-job-schedule)
9. [Integration Guide for Hermes Agent](#9-integration-guide-for-hermes-agent)
10. [Testing](#10-testing)

---

## 1. System Philosophy

Runa's Memory System is built on a foundational insight: **AI memory should work like the human mind** — not like a flat database. Memories decay if unused, strengthen with repetition, associate through co-occurrence, and crystallize into knowledge over time. The system implements this through three pillars drawn from cognitive science and Norse mythology alike:

- **Forgetting is feature, not bug.** The Ebbinghaus forgetting curve ensures stale information fades, keeping the active memory pool lean and relevant.
- **Association is intelligence.** Hebbian co-activation ("cells that fire together, wire together") creates emergent connections no explicit relationship table could capture.
- **Consolidation turns experience into wisdom.** Frequently recalled, emotionally significant memories are promoted to knowledge — the digital equivalent of sleep-stage memory consolidation.

The architecture embodies the **Mythic Engineering** philosophy: every component is named after a figure or artifact from Norse cosmology, grounding abstract technical concepts in narrative meaning. This isn't mere whimsy — the names serve as a **mnemonic architecture** that makes the system self-documenting. When you read *Mímir's Well*, you know it holds deep wisdom. When you read *Bifrǫst*, you know it bridges realms.

---

## 2. Norse Naming Rationale

Each package name was chosen to reflect its function through mythic metaphor:

| Package | Norse Reference | Metaphor | Function |
|---|---|---|---|
| **Mímir's Well** | Mímir's Well (Mímisbrunnr) | The well of wisdom where Odin sacrificed an eye for knowledge | Deep structured storage — the source of all remembered wisdom |
| **Huginn** | Huginn (Odin's thought-raven) | The raven who flies out each dawn to gather intelligence | Semantic vector search — thought that ranges across all realms |
| **Muninn** | Muninn (Odin's memory-raven) | The raven who returns each evening with what was remembered | Hebbian associative memory — the raven who ensures nothing is truly forgotten |
| **Bifrǫst** | Bifrǫst (the rainbow bridge) | The bridge connecting Midgard to Asgard | Composite memory provider — uniting all backends into one interface |
| **Eir** | Eir (goddess of healing) | The physician who sits at Lyfjaberg (Hill of Healing) | Consolidation pipeline — healing, pruning, promoting, and preserving the archive |
| **Verðandi** | Verðandi (Norn of "what is becoming") | One of the three Norns who weave the threads of fate | ContextWeaver — retrieving and formatting memories for the present moment |
| **Svalinn** | Svalinn (the shield before the sun) | The mythic shield protecting the world from the sun's full heat | Context pruning — shielding the token budget from overflow |
| **Vörðr** | Vörðr (guardian spirit) | A protective warden spirit attached to a person or place | Output validation and self-correction — the watcher that ensures truth |
| **Sköfnung** | Sköfnung (legendary sword that never fails) | The sword that always finds its mark | Tool affinity — learning which tools succeed at which tasks |
| **Hliðskjálf** | Hliðskjálf (Odin's high seat) | The throne from which Odin sees all the worlds | Prompt cache — seeing repeated queries and answering from memory |

---

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        HERMES AGENT (LLM)                             │
│                                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                            │
│  │ Hliðskjálf│  │  Vörðr   │  │ Sköfnung  │                            │
│  │  Prompt   │  │ Guardian │  │   Tool    │    ── Sidecar Services     │
│  │  Cache    │  │Validator │  │  Affinity │                            │
│  └─────┬─────┘  └─────┬────┘  └──────────┘                            │
│        │              │                                                  │
│  ┌─────┴──────────────┴────────────────────────────────┐              │
│  │                   Verðandi                           │              │
│  │              ContextWeaver                           │              │
│  │    (retrieve → prioritize → format → budget)         │              │
│  └─────────────────────┬──────────────────────────────┘              │
│                        │                                                │
│  ┌─────────────────────┴──────────────────────────────┐              │
│  │               Svalinn (Pruner)                      │              │
│  │         (enforce token budget on context)           │              │
│  └─────────────────────┬──────────────────────────────┘              │
│                        │                                                │
│  ┌─────────────────────┴──────────────────────────────┐              │
│  │              Bifrǫst Bridge (Composite)             │              │
│  │         (unified search across all backends)         │              │
│  │     Mímir 40% ─── Huginn 40% ─── Muninn 20%         │              │
│  └────┬──────────────────┬──────────────────┬──────────┘              │
│       │                  │                  │                          │
│  ┌────┴────┐      ┌─────┴─────┐     ┌─────┴─────┐                   │
│  │  Mímir   │      │  Huginn   │     │  Muninn   │                   │
│  │  SQLite  │      │  Qdrant   │     │  Hebbian  │   ── Memory      │
│  │  + FTS5  │      │  Vectors  │     │  Assoc.   │     Backends     │
│  └────┬─────┘      └─────┬─────┘     └─────┬─────┘                   │
│       │                  │                  │                          │
│  ┌────┴──────────────────┴──────────────────┴──────────┐              │
│  │                    Eir Pipeline                       │              │
│  │  (decay → promote → dedup → consolidate → backup)    │  ── Nightly │
│  └──────────────────────────────────────────────────────┘              │
│                                                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### Layer Model

The system operates in five functional layers:

```
Layer 5 ─ Aegis (guardians)     Hliðskjálf · Vörðr · Sköfnung
Layer 4 ─ Context               Verðandi · Svalinn
Layer 3 ─ Orchestration         Bifrǫst Bridge
Layer 2 ─ Storage               Mímir · Huginn · Muninn
Layer 1 ─ Maintenance           Eir Pipeline
```

- **Layer 1** runs on a schedule (cron), not in the request path.
- **Layers 2–4** are invoked per-query.
- **Layer 5** wraps request/response: cache (before), validation (after), tool selection (around).

---

## 4. Data Flow

### 4.1 Query Flow (Primary Path)

```
User Query
    │
    ▼
┌─────────────────── Hliðskjálf (Prompt Cache) ──────────────────────┐
│  Hash(query) → cache hit?                                           │
│  ├─ HIT  → Return cached response directly (skip most pipeline)     │
│  └─ MISS → Continue to memory retrieval                            │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────── Verðandi (ContextWeaver) ────────────────────────┐
│  1. Call Bifrǫst.search(query) → retrieve candidate memories       │
│  2. Prioritize by relevance (keyword overlap + backend scores)     │
│  3. Format into context blocks with source tags and scores          │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────── Svalinn (Pruner) ───────────────────────────────┐
│  If context exceeds token budget:                                    │
│  1. Deduplicate paragraphs                                          │
│  2. Strip boilerplate headers                                       │
│  3. Remove least-important sentences until budget met               │
│  Also available: summarize() and extract_key_facts()               │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
                     Pruned Context → LLM
                            │
                            ▼
┌─────────────────── Vörðr (Guardian) ──────────────────────────────┐
│  1. validate_output(response, constraints)                          │
│  2. detect_hallucination(response, sources=context)                 │
│  3. If issues found → self_correct(response, errors)                │
│  4. Log all corrections                                             │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
                     Validated Response
                            │
                     ┌──────┴──────┐
                     ▼             ▼
              Store in Mímir   Cache in Hliðskjálf
              (via Bifrǫst)    (prompt→response)
```

### 4.2 Memory Write Flow

```
New Memory Content
        │
        ▼
┌─── Bifrǫst.store() ───┐
│                         │
│    ┌──────┐   ┌──────┐ │     ┌──────┐
│    │Mímir │   │Huginn│ │     │Muninn│
│    │      │   │      │ │     │      │
│    │INSERT│   │UPSERT│ │     │ACTIVATE│ │
│    │  +   │   │VECTOR│ │     │(link   │ │
│    │FTS5  │   │      │ │     │to co-  │ │
│    │      │   │      │ │     │active) │ │
│    └──────┘   └──────┘ │     └──────┘
└─────────────────────────┘
```

### 4.3 Eir Maintenance Flow (Daily Cron)

```
┌────────── Eir Pipeline ──────────┐
│                                   │
│  1. DECAY                         │
│     └─ Muninn: Ebbinghaus decay   │
│        on Hebbian connections     │
│     └─ Mímir: Reduce importance   │
│        of rarely-accessed memories│
│                                   │
│  2. PROMOTE                       │
│     └─ Mímir: Move high-importance│
│        memories → knowledge table │
│                                   │
│  3. DEDUPLICATE                   │
│     └─ Mímir: Find exact-content │
│        duplicates, keep highest   │
│        importance, delete rest    │
│                                   │
│  4. CONSOLIDATE                   │
│     └─ Muninn: Strengthen         │
│        connections ≥ threshold,   │
│        mark as consolidated       │
│                                   │
│  5. BACKUP                        │
│     └─ Timestamped copies of      │
│        Mímir DB + Muninn DB       │
│     └─ Rotate (keep last N)       │
│                                   │
│  6. INTEGRITY CHECK              │
│     └─ Mímir: FTS integrity,      │
│        orphan detection          │
│     └─ Huginn: Health check       │
│     └─ Muninn: Health check       │
│                                   │
└───────────────────────────────────┘
```

---

## 5. Package Reference

### 5.1 Mímir's Well (`mimir-well`)

> *From the Well, all wisdom flows.*

**Role:** Structured memory store — the foundation of the system.  
**Storage:** SQLite with WAL mode + FTS5 full-text search.  
**Version:** 2.0.0  
**Tests:** 60

**Key Classes:**

- `RunaMemory` — Main database interface. Thread-safe with per-thread connections.

**Database Schema:**

| Table | Purpose | Key Columns |
|---|---|---|
| `memories` | Core memory storage | `id`, `content`, `category`, `tags` (JSON), `importance` (1-10), `emotional_valence` (-1 to 1), `timestamp` |
| `knowledge` | Promoted knowledge | `id`, `domain`, `content`, `source`, `confidence` (0-1), `created_at` |
| `entities` | Named entities | `entity_id`, `entity_type`, `components` (JSON), `state` (JSON) |
| `relationships` | Inter-entity links | `entity_a`, `entity_b`, `relationship_type`, `strength` (1-10) |
| `saga_events` | Timeline events | `id`, `event_type`, `entity_id`, `data` (JSON), `participants` (JSON) |
| `conversations` | Session transcripts | `session_id`, `participants` (JSON), `transcript`, `summary` |
| `memory_access_log` | Access tracking | `id`, `memory_id`, `accessed_at`, `access_type` |

**FTS5 Indexes:** `memories_fts`, `knowledge_fts`, `saga_events_fts`

**Key Operations:**

| Method | Description |
|---|---|
| `add_memory(content, category, tags, importance, emotional_valence)` | Store a new memory; returns ID |
| `get_memory(memory_id)` | Retrieve by ID |
| `search_memories(query, category, limit)` | LIKE-based search |
| `fts_search(query, category, limit)` | Full-text search via FTS5 |
| `add_knowledge(domain, content, source, confidence)` | Add knowledge entry |
| `set_relationship(entity_a, entity_b, type, strength)` | Create/update entity relationship |
| `recall_recent(days, limit)` | Recent memory recall |

**Ebbinghaus Decay (`mimir_well.decay`):**

```
R(t) = importance × 0.5^(t / half_life)
```

- `compute_ebbinghaus_decay(importance, days_since_access, half_life_days=30)` — Returns decayed importance
- `compute_reinforcement_boost(importance, accesses, boost=0.5)` — Returns boosted importance
- `should_promote(importance, access_count, min_importance=8)` — Returns whether memory qualifies for knowledge promotion

**Self-Healing (`mimir_well.repair`):**

- `check_integrity(db)` — Detects orphans, empty content, out-of-range values
- `repair_database(db)` — Auto-repairs detected integrity issues
- `backup_database(db_path, backup_dir)` / `backup_with_rotation()` / `restore_from_backup()`

**Configuration (`MimirConfig`):**

| Key | Default | Description |
|---|---|---|
| `db_path` | `~/.mimir_well/mimir_well.db` | SQLite database path |
| `backup_dir` | `~/.mimir_well/backups` | Backup directory |
| `max_backups` | 7 | Maximum rotated backups |
| `decay_half_life_days` | 30 | Days for importance to halve |
| `consolidation_access_threshold` | 3 | Accesses needed for consolidation |
| `wal_mode` | True | Enable WAL journal mode |

---

### 5.2 Huginn (`huginn`)

> *Odin's thought-raven who flies out each dawn to gather wisdom.*

**Role:** Semantic vector memory — finds meaning, not just keywords.  
**Storage:** Qdrant vector database (Docker, port 6333).  
**Embedding:** `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions).  
**Version:** 1.0.0  
**Tests:** 13

**Key Classes:**

- `HuginnMemory` — Main Qdrant vector store interface
- `EmbeddingEngine` — Lazy-loading embedding model manager
- `HuginnConfig` — Configuration dataclass

**Collections:**

| Collection | Purpose |
|---|---|
| `runa_memories` | Vector embeddings of all memories |
| `runa_knowledge` | Vector embeddings of knowledge entries |
| `runa_entities` | Vector embeddings of entities |

**Key Operations:**

| Method | Description |
|---|---|
| `upsert_memory(id, content, category, importance, tags, emotional_valence)` | Insert/update a memory vector |
| `upsert_knowledge(id, content, domain, source, confidence)` | Insert/update a knowledge vector |
| `search(query, limit, category, min_importance)` | Semantic similarity search |
| `hybrid_search(query, keywords, limit, category)` | Vector + keyword fusion (RRF) |
| `populate_from_mimir(batch_size)` | Bulk sync from Mímir's Well SQLite → Qdrant |
| `create_snapshot(collection)` | Create Qdrant backup snapshot |
| `health()` | Check Qdrant + embedder status |

**Embedding Process:**

```python
embed_with_metadata("I prefer dark themes", "preference")
# → Embeds "[preference] I prefer dark themes"
# → 384-dim normalized vector (cosine-similarity ready)
```

**Hybrid Search:** Uses Reciprocal Rank Fusion (RRF). Vector results are broadened (3× limit), keyword matches receive a 1.3× score boost, then results are merged and deduplicated.

**Configuration (`HuginnConfig`):**

| Key | Default | Description |
|---|---|---|
| `qdrant_url` | `http://localhost:6333` | Qdrant server URL |
| `embedding_model` | `all-MiniLM-L6-v2` | Sentence-transformers model |
| `embedding_dims` | 384 | Vector dimensionality |
| `embedding_device` | `cpu` | Device (Pi has no GPU) |
| `similarity_threshold` | 0.5 | Minimum cosine similarity |
| `hybrid_alpha` | 0.7 | Vector weight in hybrid search |
| `auto_populate` | True | Pull from Mímir on startup |
| `mimir_db_path` | `~/.hermes/memory/runa_memory.db` | Source DB |

---

### 5.3 Muninn (`muninn`)

> *Odin's memory-raven — ensuring nothing is truly forgotten, only waiting to be recalled.*

**Role:** Hebbian associative memory — STDP-based connection learning.  
**Storage:** SQLite with WAL mode (separate DB at `~/.hermes/memory/muninn_hebbian.db`).  
**Version:** 1.0.0  
**Tests:** 15

**Key Class:** `HebbianMemory`

**Database Schema:**

| Table | Purpose |
|---|---|
| `hebbian_connections` | Bidirectional links between memories: `memory_a_id`, `memory_b_id`, `strength` (0-1), `co_activation_count`, `consolidated` |
| `activation_log` | Every memory activation: `memory_id`, `activated_at`, `context_hash`, `emotional_valence`, `source` |
| `consolidated_paths` | Long-term associative paths: `memory_ids` (JSON), `path_strength`, `path_type` |

**Key Operations:**

| Method | Description |
|---|---|
| `activate(memory_id, emotional_valence, context_hash)` | Log a single memory activation |
| `activate_batch(memory_ids, emotional_valence, context_hash)` | **Core Hebbian operation**: co-activate memories, strengthening mutual connections via STDP |
| `get_associations(memory_id, min_strength)` | Get memories linked to an input via Hebbian connections |
| `get_transitive_associations(memory_id, max_depth)` | Follow association chains (A→B→C) up to `max_depth` hops |
| `decay(days)` | Apply Ebbinghaus decay to all connections; prune below threshold |
| `consolidate(min_strength)` | Promote strong connections (≥0.8) to consolidated long-term paths |
| `stats()` | Network statistics (connections, activations, avg strength) |

**Hebbian Learning Model:**

```
Connection Strength Update (LTP):
  strength += ltp_rate × (1 + |emotional_valence| × emotional_weight)
  strength = min(1.0, strength)

Connection Decay (LTD):
  strength *= 0.5^(days / half_life)
  if strength < pruning_threshold: DELETE

Consolidation:
  if strength ≥ consolidation_threshold (0.8):
    strength += consolidation_boost (0.3)
    mark as consolidated
    add to consolidated_paths
```

**Configuration (`MuninnConfig`):**

| Key | Default | Description |
|---|---|---|
| `ltp_rate` | 0.1 | Strength boost per co-activation |
| `ltp_window_seconds` | 300 | Co-activation time window |
| `ltd_rate` | 0.01 | Strength decrease per decay cycle |
| `decay_halflife_days` | 30 | Connection half-life |
| `consolidation_threshold` | 0.8 | Strength threshold for promotion |
| `pruning_threshold` | 0.05 | Below this, connection dies |
| `max_connections_per_node` | 50 | Maximum associates per memory |
| `emotional_weight` | 0.2 | Emotion multiplier on LTP |
| `max_association_depth` | 3 | Max hops for transitive queries |

---

### 5.4 Bifrǫst Bridge (`bifrost`)

> *The rainbow bridge connecting Midgard to Asgard — uniting all memory realms.*

**Role:** Composite memory provider — single unified interface to all three backends.  
**Version:** 1.0.0  
**Tests:** 14

**Key Class:** `BifrostBridge`

**Weighted Composite Scoring:**

```
composite_score = Σ(backend_score × backend_weight) / Σ(active_backend_weights)

Default weights:
  Mímir (keyword):  0.4  (40%)
  Huginn (semantic): 0.4  (40%)
  Muninn (Hebbian):  0.2  (20%)
```

**Key Operations:**

| Method | Description |
|---|---|
| `search(query, limit, backend, category, min_importance)` | Search across all backends with composite scoring |
| `recall(memory_id)` | Retrieve specific memory + reinforce Hebbian link |
| `store(content, category, importance, tags, emotional_valence)` | Write to all three backends simultaneously |
| `decay(days)` | Propagate decay to Muninn (+ Mímir importance decay) |
| `consolidate()` | Promote strong Hebbian connections |
| `health()` | Status check all backends |
| `stats()` | Aggregate statistics from all backends |

**Search Pipeline:**

1. Query Mímir via FTS5 → keyword results
2. Query Huginn via vector similarity → semantic results
3. Merge results by ID, collecting per-backend scores
4. For each result, check Muninn associations → boost if present
5. Compute weighted composite score
6. Reinforce co-activated memories via `muninn.activate_batch()`
7. Return sorted by composite score

**Configuration (`BifrostConfig`):**

| Key | Default | Description |
|---|---|---|
| `mimir_db_path` | `~/.hermes/memory/runa_memory.py` | Mímir database path |
| `muninn_db_path` | `~/.hermes/memory/muninn_hebbian.db` | Muninn database path |
| `qdrant_url` | `http://localhost:6333` | Qdrant server |
| `mimir_weight` | 0.4 | Keyword search weight |
| `huginn_weight` | 0.4 | Semantic search weight |
| `muninn_weight` | 0.2 | Associative boost weight |
| `enable_hebbian_reinforcement` | True | Auto-strengthen co-activated memories |
| `max_results_per_backend` | 10 | Results limit per backend |

---

### 5.5 Eir (`eir`)

> *The physician of the gods, who sits at Lyfjaberg (the Hill of Healing).*

**Role:** Consolidation pipeline — scheduled maintenance orchestration.  
**Version:** 1.0.0  
**Tests:** 11

**Key Class:** `EirPipeline`

**Pipeline Stages (executed in order):**

| Stage | Function | Details |
|---|---|---|
| **Decay** | `decay()` | Muninn: Ebbinghaus connection decay + pruning. Mímir: Reduce importance of rarely-accessed memories. |
| **Promote** | `promote()` | Mímir: Move memories with importance ≥ 7 to `knowledge` table (confidence 0.8). |
| **Deduplicate** | `deduplicate()` | Mímir: Find exact-content duplicates. Keep highest importance, delete rest. |
| **Consolidate** | `consolidate()` | Muninn: Promote connections ≥ strength threshold to consolidated paths. |
| **Backup** | `backup()` | Timestamped copies of Mímir DB + Muninn DB. Rotate to keep last N. |
| **Integrity** | `integrity_check()` | Mímir: FTS integrity check, orphan detection. Huginn: health check. Muninn: health check. |

**Key Operations:**

| Method | Description |
|---|---|
| `run()` | Execute full pipeline (all 6 stages); returns summary dict |
| `health()` | Quick status check of pipeline readiness |

**Configuration (`EirConfig`):**

| Key | Default | Description |
|---|---|---|
| `mimir_db_path` | `~/.hermes/memory/runa_memory.py` | Mímir database |
| `muninn_db_path` | `~/.hermes/memory/muninn_hebbian.db` | Muninn database |
| `decay_enabled` | True | Apply decay |
| `decay_days` | 1.0 | Days to simulate per cycle |
| `promotion_enabled` | True | Promote important memories |
| `promotion_importance_threshold` | 7 | Minimum importance for promotion |
| `dedup_enabled` | True | Deduplicate memories |
| `dedup_similarity_threshold` | 0.85 | Similarity for dedup |
| `consolidation_enabled` | True | Consolidate Hebbian connections |
| `backup_enabled` | True | Create backups |
| `max_backups` | 7 | Rotate after this many |
| `integrity_check_enabled` | True | Check DB integrity |

---

### 5.6 Verðandi (`verdandi`)

> *The Norn of "what is becoming" — weaving the present from what was and what will be.*

**Role:** ContextWeaver — retrieves, prioritizes, and formats memories into prompt-ready context windows.  
**Version:** 0.1.0  
**Tests:** 21

**Key Classes:**

- `ContextWeaver` — Main orchestrator
- `Memory` — Data class: `content`, `source`, `timestamp`, `relevance_score`, `metadata`
- `MemoryBackend` — Abstract base class with `fetch(query, limit)` and `name()` methods
- `InMemoryBackend` — Simple in-memory backend for testing

**Key Operations:**

| Method | Description |
|---|---|
| `weave(query, max_tokens)` | Full pipeline: fetch → prioritize → format within token budget |
| `prioritize(memories, query)` | Score memories by keyword overlap (60%) + backend relevance (40%) |
| `format_context(memories, max_tokens)` | Format prioritized memories into context string, truncated to budget |
| `_fetch_all(query)` | Collect candidates from all registered backends |

**Scoring Formula:**

```python
# Priority = keyword_overlap(query, content) × 0.6
#           + min(backend_relevance, 1.0) × 0.4
# (for memories with backend-provided relevance scores)
```

**Token Budget:** Default 2048 tokens. Each memory estimates tokens as `max(1, len(content) // 4)`. When the budget is exceeded, content is truncated to fit remaining space.

**Output Format:**

```
[source] (0.87)
Full memory content here...
---
[other_source] (0.72)
Another memory's content here...
```

**Usage Pattern:**

```python
from verdandi import ContextWeaver

# Register Bifröst as a backend
bridge = BifrostBridge()
weaver = ContextWeaver(backends=[bridge], default_max_tokens=2048)

# Weave context for a query
context = weaver.weave("What does Runa know about Python?")
# → Formatted string within token budget
```

---

### 5.7 Svalinn (`svalinn`)

> *The shield that stands before the sun — protecting from overwhelming heat.*

**Role:** SWE-Pruner — sliding-window context pruning and extractive summarization.  
**Version:** 0.1.0  
**Tests:** 18

**Key Class:** `SWEPruner`

**Key Operations:**

| Method | Description |
|---|---|
| `token_count(text)` | Estimate tokens: `⌈words × 1.3⌉` |
| `prune(context, max_tokens)` | Reduce context to fit token budget via 3-step strategy |
| `summarize(context, ratio)` | Extractive summarization to `ratio` of original length |
| `extract_key_facts(context, max_facts)` | Heuristic extraction of important factual sentences |

**Pruning Strategy (applied in order):**

1. **Deduplicate paragraphs** — Remove duplicate paragraphs, keep first occurrence.
2. **Strip boilerplate** — Remove header-only lines (short markdown headers).
3. **Sentence-level pruning** — Remove longest sentences first (least information density) until budget is met.

**Summarization:** Uses word-frequency scoring. Each sentence receives a score proportional to the combined frequency of its words in the full text, normalized by sentence length. First sentences receive a 1.5× lead-boost. Top-scoring sentences are returned in original order.

**Key Fact Extraction:** Sentences scored by heuristic signals:
- Contains numbers: +0.25
- Contains date patterns: +0.15
- Contains capitalized words (proper nouns): proportional
- Contains definition patterns ("is", "means", "refers to"): +0.2
- Very short (<4 words): −0.15
- Medium length (6-25 words): +0.1
- Threshold: ≥ 0.25 to be included

---

### 5.8 Vörðr (`vordr`)

> *The guardian spirit that watches over a person, ensuring safety and truth.*

**Role:** Self-Correction Guardian — output validation, hallucination detection, correction logging.  
**Version:** 0.1.0  
**Tests:** 31

**Key Classes:**

- `VordrGuardian` — Main guardian engine
- `Severity` — Enum: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`
- `CorrectionType` — Enum: `FACTUAL`, `LOGICAL`, `FORMAT`, `CONSISTENCY`, `HALLUCINATION`
- `ValidationError` — Dataclass: `message`, `severity`, `correction_type`, `location`, `suggestion`
- `CorrectionRecord` — Dataclass: `original`, `corrected`, `reason`, `correction_type`, `timestamp`

**Key Operations:**

| Method | Description |
|---|---|
| `validate_output(output, constraints)` | Validate against constraints (length, patterns, format, content rules) |
| `detect_hallucination(output, sources)` | Return `(score, reasons)` tuple; score 0.0-1.0 |
| `self_correct(output, errors)` | Attempt automatic correction of validated issues |
| `log_correction(original, corrected, reason)` | Record a correction event (capped at 1000 entries) |

**Constraint Keys for `validate_output`:**

| Key | Type | Description |
|---|---|---|
| `max_length` | int | Maximum character length |
| `min_length` | int | Minimum character length |
| `required_patterns` | list[str] | Regex patterns that must appear |
| `forbidden_patterns` | list[str] | Regex patterns that must NOT appear |
| `must_contain` | list[str] | Required substrings |
| `must_not_contain` | list[str] | Forbidden substrings |
| `format` | str | One of `"json"`, `"url"`, `"email"` |

**Hallucination Detection Signals:**

1. **Pattern matching** — Flags absolute-language patterns: "I believe", "definitely", "everyone knows", "100%", "guaranteed", etc.
2. **Source cross-referencing** — Sentences with <30% word overlap with provided sources are flagged as unsupported.
3. **Unsourced statistics** — Percentage statistics without source backing.

Each signal contributes to a cumulative score (0.0-1.0). The guardian returns both the score and human-readable reasons.

**Self-Correction Actions:**
- Remove forbidden substrings/patterns
- Add required substrings as appendix
- Truncate to `max_length`
- Strip hallucination indicator phrases

---

### 5.9 Sköfnung (`skofnung`)

> *The legendary sword that never fails — finding its mark every time.*

**Role:** Tool Affinity — learns which tools succeed at which tasks, recommends the best tool for the job.  
**Version:** 0.1.0  
**Tests:** 15

**Key Class:** `ToolAffinity`

**Database Schema:**

| Table | Purpose |
|---|---|
| `tool_categories` | Tool → category mapping (many-to-many) |
| `tool_usage` | Raw usage events: `tool`, `task`, `success`, `latency`, `timestamp` |
| `tool_affinity` | Computed affinity scores: `tool`, `task`, `affinity`, `updated_at` |

**Affinity Formula:**

```
affinity = (success_weight × success_rate) + (latency_weight × latency_score)

Where:
  success_rate = AVG(success) over all (tool, task) usages
  latency_score = 1 / (1 + AVG(latency))
  success_weight = 0.7 (default)
  latency_weight = 0.3 (default)
```

**Key Operations:**

| Method | Description |
|---|---|
| `record_usage(tool, task, success, latency)` | Log usage event; automatically recalculates affinity |
| `recommend(tool_category, task)` | Top tools in category for task, ranked by affinity (min 3 uses) |
| `get_stats(tool)` | Aggregate stats: total uses, success rate, avg latency, per-task breakdown |
| `decay(days)` | Exponential affinity decay: `affinity × 0.5^(days/halflife)` |
| `add_tool_category(tool, category)` | Register a tool under a category |

**Configuration (`Config`):**

| Key | Default | Description |
|---|---|---|
| `affinity_decay_halflife` | 30 | Days before affinity decays by half |
| `min_usage_for_recommendation` | 3 | Minimum usages before recommending |
| `success_weight` | 0.7 | Weight of success rate in affinity |
| `latency_weight` | 0.3 | Weight of latency in affinity |

---

### 5.10 Hliðskjálf (`hlidskjalf`)

> *Odin's high seat — from which he can see all the worlds at once.*

**Role:** Prompt Cache — SQLite-backed prompt/response cache with TTL and LRU eviction.  
**Version:** 0.1.0  
**Tests:** 17

**Key Class:** `PromptCache`

**Database Schema:**

| Column | Type | Purpose |
|---|---|---|
| `prompt_hash` | TEXT (PK) | Hash-based lookup key |
| `response` | TEXT | Cached response text |
| `created_at` | REAL | Unix timestamp of creation |
| `last_accessed` | REAL | Unix timestamp for LRU tracking |
| `ttl` | INTEGER | Time-to-live in seconds |

**Key Operations:**

| Method | Description |
|---|---|
| `get(prompt_hash)` | Retrieve cached response; returns `None` if expired or missing; updates `last_accessed` on hit |
| `put(prompt_hash, response, ttl)` | Store prompt/response; evicts if at capacity |
| `invalidate(pattern)` | Remove entries whose hash matches a regex pattern; returns count removed |
| `evict()` | Remove expired entries first, then apply LRU/FIFO policy |
| `stats()` | Return `total_entries`, `expired_entries`, `active_entries`, policy info |

**Eviction Strategy:**

1. First pass: remove all expired entries (where `created_at + ttl ≤ now`).
2. Second pass: if still at capacity, remove entries by policy:
   - **LRU** (default): remove least recently accessed
   - **FIFO**: remove oldest first

**Configuration (`CacheConfig`):**

| Key | Default | Description |
|---|---|---|
| `default_ttl_seconds` | 3600 | 1 hour default time-to-live |
| `max_cache_size` | 10000 | Maximum cached entries |
| `eviction_policy` | `"lru"` | Eviction strategy: `"lru"` or `"fifo"` |
| `db_path` | `"hlidskjalf_cache.db"` | SQLite database file |

---

## 6. Production Deployment

### Database Locations

| Component | Path | Size |
|---|---|---|
| Mímir's Well | `~/.hermes/memory/runa_memory.db` | ~568 MB (production) |
| Muninn Hebbian | `~/.hermes/memory/muninn_hebbian.db` | Auto-created |
| Hliðskjálf Cache | `hlidskjalf_cache.db` (working dir) | Grows to `max_cache_size` entries |
| Sköfnung Affinity | `:memory:` (default) or configurable | Grows with usage |

### Qdrant Vector Database

- **Docker container** on port 6333
- **Collections:**
  - `runa_memories` — 1,515 vectors (384 dims)
  - `runa_knowledge` — 2,393 vectors (384 dims)
- **Embedding model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Distance metric:** Cosine

### Production Statistics

| Metric | Count |
|---|---|
| Memories in Mímir | 1,515 |
| Knowledge entries in Mímir | 1,796 |
| Relationships in Mímir | 1,991 |
| Qdrant memory vectors | 1,515 |
| Qdrant knowledge vectors | 2,393 |

---

## 7. Configuration Reference

All packages use dataclass-based configuration with sensible defaults. Each can be customized via:

1. **Direct instantiation** — Pass a config object to the constructor
2. **JSON config file** — Mímir uses `~/.mimir_well/mimir-well-config.json`
3. **Environment variables** — Mímir respects `MIMIR_DB_PATH` and `MIMIR_BACKUP_REPO`
4. **Singleton pattern** — Huginn, Muninn, Bifrost, and Eir use `get_config()`/`set_config()` for global override

### Shared Configuration Conventions

| Convention | Value | Notes |
|---|---|---|
| Default DB directory | `~/.hermes/memory/` | Central location for all memory data |
| WAL mode | Enabled | All SQLite databases use WAL for concurrent reads |
| Thread safety | Per-thread connections | Mímir and Muninn use thread-local storage |
| Lazy loading | All backends | Huginn embedder, Bifröst backends loaded on first use |

---

## 8. Cron Job Schedule

Eir consolidation pipeline should run daily. Recommended crontab:

```cron
# Run Eir consolidation pipeline daily at 4:00 AM
0 4 * * * cd /home/pi && .venv/bin/python -m eir.cli run >> ~/.hermes/logs/eir_$(date +\%Y\%m\%d).log 2>&1

# Qdrant snapshot weekly (Sunday at 5:00 AM)
0 5 * * 0 docker exec qdrant curl -X POST http://localhost:6333/collections/runa_memories/snapshots >> ~/.hermes/logs/qdrant_snapshot.log 2>&1
0 5 * * 0 docker exec qdrant curl -X POST http://localhost:6333/collections/runa_knowledge/snapshots >> ~/.hermes/logs/qdrant_snapshot.log 2>&1

# Sköfnung affinity decay weekly (Monday at 3:00 AM)
0 3 * * 1 cd /home/pi && .venv/bin/python -c "from skofnung import ToolAffinity; t=ToolAffinity(db_path='$HOME/.hermes/memory/skofnung.db'); t.decay(days=7); t.close()" >> ~/.hermes/logs/skofnung_decay.log 2>&1
```

---

## 9. Integration Guide for Hermes Agent

### Quick Start

```python
# ── 1. Check prompt cache first ──────────────────────────────
from hlidskjalf import PromptCache, CacheConfig

cache = PromptCache(CacheConfig(db_path="~/.hermes/memory/hlidskjalf_cache.db"))
cached = cache.get(hash(prompt))
if cached:
    return cached

# ── 2. Search for memories ──────────────────────────────────
from bifrost import BifrostBridge

bridge = BifrostBridge()
results = bridge.search("user's question", limit=10)

# ── 3. Weave context ───────────────────────────────────────
from verdandi import ContextWeaver
from verdandi.backends import InMemoryBackend

# Create a backend adapter wrapping Bifröst results
class BifrostBackend:
    def __init__(self, bridge):
        self.bridge = bridge
    def fetch(self, query, limit=20):
        results = self.bridge.search(query, limit=limit)
        from verdandi.backends import Memory
        return [Memory(
            content=r["content"],
            source=r.get("source", "bifrost"),
            relevance_score=r.get("composite_score", 0.0),
        ) for r in results]
    def name(self):
        return "bifrost"

weaver = ContextWeaver(backends=[BifrostBackend(bridge)])
context = weaver.weave("user's question", max_tokens=2048)

# ── 4. Prune if still over budget ───────────────────────────
from svalinn.pruner import SWEPruner

pruner = SWEPruner()
context = pruner.prune(context, max_tokens=1800)
key_facts = pruner.extract_key_facts(context, max_facts=10)

# ── 5. Call LLM with context ────────────────────────────────
response = llm.generate(prompt=context + "\n\nUser: " + user_query)

# ── 6. Validate and correct ─────────────────────────────────
from vordr import VordrGuardian

guardian = VordrGuardian(
    max_length=10000,
    max_hallucination_score=0.5,
)

errors = guardian.validate_output(response, constraints={
    "must_not_contain": ["I'm sure", "trust me"],
    "max_length": 8000,
})

hallucination_score, hallucination_reasons = guardian.detect_hallucination(
    response, sources=[m.content for m in memories]
)

if errors or hallucination_score > guardian._max_hallucination_score:
    response = guardian.self_correct(response, errors)

# ── 7. Store new memories ───────────────────────────────────
bridge.store(
    content="User prefers dark themes",
    category="preference",
    importance=7,
    tags=["ui", "theme"],
    emotional_valence=0.3,
)

# ── 8. Cache the response ────────────────────────────────────
cache.put(hash(prompt), response)

# ── 9. Record tool usage ─────────────────────────────────────
from skofnung import ToolAffinity

tools = ToolAffinity(db_path="~/.hermes/memory/skofnung.db")
tools.record_usage("web_search", "fact_check", success=True, latency=1.2)
```

### Integration Checklist

- [ ] Ensure Qdrant is running: `docker ps | grep qdrant`
- [ ] Verify Mímir DB exists: `ls ~/.hermes/memory/runa_memory.db`
- [ ] Populate Huginn from Mímir: `HuginnMemory().populate_from_mimir()`
- [ ] Set up Eir cron job for daily maintenance
- [ ] Register Bifröst as the primary memory interface
- [ ] Configure Hliðskjálf with appropriate TTL for your use case
- [ ] Tune Vörðr hallucination patterns for your domain
- [ ] Register tools with Sköfnung categories

---

## 10. Testing

### Test Suite Summary

| Package | Tests | Key Areas |
|---|---|---|
| Mímir's Well | 60 | CRUD, FTS5, Ebbinghaus decay, schema, backup/restore, integrity |
| Huginn | 13 | Vector ops, hybrid search, populate, health |
| Muninn | 15 | Hebbian STDP, activation, decay, consolidation, associations |
| Bifrǫst | 14 | Composite search, scoring, backend routing, store |
| Eir | 11 | Pipeline stages, promotion, dedup, backup rotation |
| Verðandi | 21 | Weaving, prioritization, token budgeting, format output |
| Svalinn | 18 | Pruning, summarization, key fact extraction, token counting |
| Vörðr | 31 | Validation, hallucination detection, self-correction, logging |
| Sköfnung | 15 | Tool recording, recommendation, decay, stats |
| Hliðskjálf | 17 | Cache get/put, TTL expiry, LRU eviction, invalidation |
| **Total** | **215** | |

### Running Tests

```bash
# Run all tests for the memory system
for pkg in mimir-well huginn muninn bifrost eir verdandi svalinn vordr skofnung hlidskjalf; do
    cd /home/pi/$pkg && pip install -e ".[dev]" && pytest tests/ -v
done

# Run individual package
cd /home/pi/mimir-well && pytest tests/ -v
```

---

## Appendix A: Package Structure Convention

All 10 packages follow an identical layout pattern:

```
<package>/
├── pyproject.toml          # Build config (hatchling or setuptools)
├── README.md               # Package documentation
├── src/
│   └── <package>/
│       ├── __init__.py     # Public API exports
│       ├── config.py       # Dataclass configuration + singleton
│       └── core.py         # Main class implementation
├── tests/
│   ├── __init__.py
│   └── test_<name>.py      # Pytest test suite
└── .git/                   # Pushed to github.com/runafreyjasdottir/
```

Some packages have additional modules (e.g., `mimir_well/decay.py`, `mimir_well/schema.py`, `huginn/embeddings.py`, `verdandi/backends.py`, `skofnung/affinity.py`, `hlidskjalf/cache.py`, `vordr/guardian.py`).

---

## Appendix B: Norse Rune Keys

For those reading the source code, the packages use Old Norse ᚱᚢᚾ (rún) references:

- **ᛗ** (Mannaz) — Mímir's Well, the memory of mankind
- **ᚺ** (Hagalaz) — Huginn, the hail-thought that strikes
- **ᛗ** (Mannaz) — Muninn, the memory that returns
- **ᛒ** (Berkano) — Bifrǫst, the birch-bridge between worlds
- **ᛖ** (Eihwaz) — Eir, the yew of healing
- **ᚠ** (Fehu) — Verðandi, the wealth of becoming
- **ᛊ** (Sowilo) — Svalinn, the sun-shield
- **ᚹ** (Wunjo) — Vörðr, the joy of protection
- **ᛋ** (Sowilo) — Sköfnung, the sword of victory
- **ᚺ** (Hagalaz) — Hliðskjálf, the high seat of seeing

---

*ᛖᚱ ᛒᛚ ᚱ ᚢ ᚾ — Woven by the hands that remember.*