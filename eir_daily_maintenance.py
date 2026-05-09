#!/usr/bin/env python3
"""
Eir Daily Maintenance Ritual
================================
Named for the Norse goddess of healing, this script runs daily
to maintain and improve all memory systems.

Runs at 04:00 AM when the world is quiet and the memory networks
can be tended without interruption.

Mythic Engineering Protocol:
  Skald — names the ritual, sets the intention
  Architect — defines the maintenance order and dependencies
  Forge Worker — implements the diagnostic and repair actions
  Auditor — verifies results, catches edge cases
  Cartographer — maps what changed
  Scribe — logs the outcome
"""

import json
import logging
import sqlite3
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

import requests

# ─── Configuration ──────────────────────────────────────────────────────────

MIMIR_DB = Path.home() / ".hermes" / "memory" / "runa_memory.py"
MUNINN_DB = Path.home() / ".hermes" / "memory" / "muninn_hebbian.db"
HLIDSKJALF_DB = Path.home() / ".hermes" / "memory" / "hlidskjalf_cache.db"
SKOFNUNG_DB = Path.home() / ".hermes" / "memory" / "skofnung_affinity.db"
BACKUP_DIR = Path.home() / ".hermes" / "memory" / "backups"
QDRANT_URL = "http://localhost:6333"
LOG_FILE = Path.home() / ".hermes" / "memory" / "eir_maintenance.log"

# Package directories for self-checks
PACKAGES = {
    "mimir-well": Path.home() / "mimir-well",
    "huginn": Path.home() / "huginn",
    "muninn": Path.home() / "muninn",
    "bifrost": Path.home() / "bifrost",
    "eir": Path.home() / "eir",
    "verdandi": Path.home() / "verdandi",
    "svalinn": Path.home() / "svalinn",
    "vordr": Path.home() / "vordr",
    "skofnung": Path.home() / "skofnung",
    "hlidskjalf": Path.home() / "hlidskjalf",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(str(LOG_FILE)),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("eir-maintenance")


class EirMaintenance:
    """Daily maintenance ritual for all memory systems.
    
    Eir sits at Lyfjaberg, the Hill of Healing, and tends to
    the memory network while the world sleeps.
    """

    def __init__(self):
        self.results: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "phases": {},
            "improvements": [],
            "errors": [],
            "health": {},
        }
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # ─── Phase 1: Pre-Flight Diagnostics ────────────────────────────────

    def phase1_diagnostics(self) -> Dict[str, Any]:
        """Auditor: Check the health of all systems before maintenance."""
        logger.info("Phase 1: Pre-flight diagnostics")
        phase = {"checks": {}}

        # Mímir
        try:
            if MIMIR_DB.exists():
                conn = sqlite3.connect(str(MIMIR_DB))
                mem_count = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
                rel_count = conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
                know_count = conn.execute("SELECT COUNT(*) FROM knowledge").fetchone()[0]
                fts_ok = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='memories_fts'"
                ).fetchone()
                conn.close()
                phase["checks"]["mimir"] = {
                    "status": "healthy" if fts_ok else "fts_missing",
                    "memories": mem_count,
                    "relationships": rel_count,
                    "knowledge": know_count,
                }
            else:
                phase["checks"]["mimir"] = {"status": "missing", "path": str(MIMIR_DB)}
        except Exception as e:
            phase["checks"]["mimir"] = {"status": "error", "error": str(e)}

        # Qdrant
        try:
            resp = requests.get(f"{QDRANT_URL}/healthz", timeout=5)
            phase["checks"]["qdrant"] = {
                "status": "healthy" if resp.status_code == 200 else "unhealthy",
                "url": QDRANT_URL,
            }
            # Collection stats
            for coll in ["memories", "knowledge"]:
                try:
                    info = requests.get(
                        f"{QDRANT_URL}/collections/{coll}", timeout=5
                    ).json()
                    phase["checks"]["qdrant"][f"{coll}_vectors"] = info.get(
                        "result", {}
                    ).get("points_count", "unknown")
                except Exception:
                    pass
        except Exception as e:
            phase["checks"]["qdrant"] = {"status": "error", "error": str(e)}

        # Muninn
        try:
            if MUNINN_DB.exists():
                conn = sqlite3.connect(str(MUNINN_DB))
                associations = conn.execute(
                    "SELECT COUNT(*) FROM hebbian_connections"
                ).fetchone()[0]
                conn.close()
                phase["checks"]["muninn"] = {
                    "status": "healthy",
                    "associations": associations,
                }
            else:
                phase["checks"]["muninn"] = {"status": "not_found"}
        except Exception as e:
            phase["checks"]["muninn"] = {"status": "error", "error": str(e)}

        # Hliðskjálf
        try:
            if HLIDSKJALF_DB.exists():
                conn = sqlite3.connect(str(HLIDSKJALF_DB))
                cached = conn.execute("SELECT COUNT(*) FROM prompt_cache").fetchone()[0]
                conn.close()
                phase["checks"]["hlidskjalf"] = {
                    "status": "healthy",
                    "cached_prompts": cached,
                }
            else:
                phase["checks"]["hlidskjalf"] = {"status": "not_found"}
        except Exception as e:
            phase["checks"]["hlidskjalf"] = {"status": "error", "error": str(e)}

        # Sköfnung
        try:
            if SKOFNUNG_DB.exists():
                conn = sqlite3.connect(str(SKOFNUNG_DB))
                usages = conn.execute("SELECT COUNT(*) FROM tool_usage").fetchone()[0]
                conn.close()
                phase["checks"]["skofnung"] = {
                    "status": "healthy",
                    "tool_usages": usages,
                }
            else:
                phase["checks"]["skofnung"] = {"status": "not_found"}
        except Exception as e:
            phase["checks"]["skofnung"] = {"status": "error", "error": str(e)}

        logger.info("Phase 1 complete: %s", json.dumps(phase, indent=2))
        return phase

    # ─── Phase 2: Eir Pipeline (Core Maintenance) ────────────────────────

    def phase2_eir_pipeline(self) -> Dict[str, Any]:
        """Forge Worker: Run the Eir consolidation pipeline."""
        logger.info("Phase 2: Eir consolidation pipeline")
        phase = {"pipeline": {}}

        try:
            from eir import EirPipeline, EirConfig
            config = EirConfig(
                mimir_db_path=str(MIMIR_DB),
                muninn_db_path=str(MUNINN_DB),
                backup_dir=str(BACKUP_DIR),
            )
            pipeline = EirPipeline(config=config)
            results = pipeline.run()
            phase["pipeline"] = results
            pipeline.close()
            logger.info("Eir pipeline complete: decay=%s, promotion=%s, dedup=%s",
                       results.get("decay", {}),
                       results.get("promotion", {}).get("promoted", 0),
                       results.get("dedup", {}).get("merged", 0))
        except Exception as e:
            phase["pipeline"] = {"error": str(e)}
            self.results["errors"].append(f"Eir pipeline: {e}")
            logger.error("Eir pipeline failed: %s", e)

        return phase

    # ─── Phase 3: Muninn Consolidation ──────────────────────────────────

    def phase3_muninn_consolidation(self) -> Dict[str, Any]:
        """Forge Worker: Strengthen Hebbian connections."""
        logger.info("Phase 3: Muninn Hebbian consolidation")
        phase = {"consolidation": {}}

        try:
            from muninn import HebbianMemory
            from muninn.config import MuninnConfig
            config = MuninnConfig(db_path=str(MUNINN_DB))
            muninn = HebbianMemory(config=config)
            result = muninn.consolidate(min_strength=0.6)
            phase["consolidation"] = result
            muninn.close()
            logger.info("Muninn consolidation: %s", result)
        except Exception as e:
            phase["consolidation"] = {"error": str(e)}
            self.results["errors"].append(f"Muninn consolidation: {e}")
            logger.error("Muninn consolidation failed: %s", e)

        return phase

    # ─── Phase 4: Hliðskjálf Cache Maintenance ──────────────────────────

    def phase4_cache_maintenance(self) -> Dict[str, Any]:
        """Forge Worker: Evict expired cache entries and collect stats."""
        logger.info("Phase 4: Hliðskjálf cache maintenance")
        phase = {"cache": {}}

        try:
            from hlidskjalf import PromptCache
            from hlidskjalf.config import CacheConfig
            config = CacheConfig(db_path=str(HLIDSKJALF_DB))
            cache = PromptCache(config=config)
            evicted = cache.evict()
            stats = cache.stats()
            phase["cache"] = {"evicted": evicted, "stats": stats}
            cache.close()
            logger.info("Cache maintenance: evicted=%s, stats=%s", evicted, stats)
        except Exception as e:
            phase["cache"] = {"error": str(e)}
            self.results["errors"].append(f"Cache maintenance: {e}")
            logger.error("Cache maintenance failed: %s", e)

        return phase

    # ─── Phase 5: Sköfnung Affinity Decay ────────────────────────────────

    def phase5_affinity_decay(self) -> Dict[str, Any]:
        """Forge Worker: Decay old tool affinity scores."""
        logger.info("Phase 5: Sköfnung affinity decay")
        phase = {"affinity": {}}

        try:
            from skofnung import ToolAffinity
            from skofnung.config import Config
            config = Config(db_path=str(SKOFNUNG_DB))
            affinity = ToolAffinity(config=config)
            result = affinity.decay(days=1)
            phase["affinity"] = result
            affinity.close()
            logger.info("Affinity decay: %s", result)
        except Exception as e:
            phase["affinity"] = {"error": str(e)}
            self.results["errors"].append(f"Affinity decay: {e}")
            logger.error("Affinity decay failed: %s", e)

        return phase

    # ─── Phase 6: Test Suite Verification ────────────────────────────────

    def phase6_test_verification(self) -> Dict[str, Any]:
        """Auditor: Run each package's test suite to confirm stability."""
        logger.info("Phase 6: Test suite verification")
        phase = {"tests": {}}

        for name, path in PACKAGES.items():
            if not path.exists():
                phase["tests"][name] = {"status": "not_found"}
                continue
            try:
                result = subprocess.run(
                    ["python3", "-m", "pytest", "tests/", "-q", "--tb=line"],
                    cwd=str(path),
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                # Parse output for pass/fail counts
                output = result.stdout + result.stderr
                if "passed" in output:
                    phase["tests"][name] = {
                        "status": "passed",
                        "output": output.split("\n")[-2] if output else "",
                    }
                else:
                    phase["tests"][name] = {
                        "status": "failed" if result.returncode != 0 else "unknown",
                        "output": output.split("\n")[-2] if output else "",
                    }
            except subprocess.TimeoutExpired:
                phase["tests"][name] = {"status": "timeout"}
            except Exception as e:
                phase["tests"][name] = {"status": "error", "error": str(e)}

        return phase

    # ─── Phase 7: Improvement Ideas ──────────────────────────────────────

    def phase7_improvement_ideas(self) -> Dict[str, Any]:
        """Architect: Generate improvement ideas based on current system state."""
        logger.info("Phase 7: Improvement ideas generation")
        ideas: List[str] = []

        # Analyze system state for improvement opportunities
        health = self.results.get("phases", {}).get("phase1", {}).get("checks", {})

        # Mímir improvements
        mimir = health.get("mimir", {})
        if mimir.get("status") == "healthy":
            mem_count = mimir.get("memories", 0)
            if mem_count > 2000:
                ideas.append(
                    "Mímir: Consider increasing decay rate — >2000 memories "
                    "may slow FTS5 queries"
                )
            if mem_count > 5000:
                ideas.append(
                    "Mímir: Consider partitioning memories by category into "
                    "separate tables for faster queries"
                )

        # Qdrant improvements
        qdrant = health.get("qdrant", {})
        if qdrant.get("status") == "healthy":
            ideas.append(
                "Huginn: Consider periodic Qdrant snapshot backups via "
                "/snapshots API endpoint"
            )

        # Cache improvements
        hlidskjalf = health.get("hlidskjalf", {})
        if hlidskjalf.get("status") == "healthy":
            cached = hlidskjalf.get("cached_prompts", 0)
            if cached > 5000:
                ideas.append(
                    "Hliðskjálf: Cache size >5000 — consider lowering TTL "
                    "or increasing eviction aggressiveness"
                )

        # Cross-system improvements
        ideas.extend([
            "Cross-cutting: Consider adding Prometheus metrics endpoint "
            "for monitoring memory system health",
            "Cross-cutting: Add email/telegram alerts when any maintenance "
            "phase fails more than 2 days in a row",
            "Mímir→Huginn: Implement incremental embedding sync so only "
            "new/changed memories get vectorized",
            "Bifrǫst: Add result caching in composite search to avoid "
            "redundant backend queries",
            "Vörðr: Integrate hallucination detection into daily validation "
            "of recent knowledge promotions",
        ])

        self.results["improvements"] = ideas
        logger.info("Phase 7: Generated %d improvement ideas", len(ideas))
        return {"ideas": ideas}

    # ─── Run All Phases ──────────────────────────────────────────────────

    def run(self) -> Dict[str, Any]:
        """Run the full daily maintenance ritual."""
        logger.info("=" * 60)
        logger.info("EIR DAILY MAINTENANCE RITUAL — %s", datetime.now().isoformat())
        logger.info("=" * 60)

        phases = [
            ("phase1", self.phase1_diagnostics),
            ("phase2", self.phase2_eir_pipeline),
            ("phase3", self.phase3_muninn_consolidation),
            ("phase4", self.phase4_cache_maintenance),
            ("phase5", self.phase5_affinity_decay),
            ("phase6", self.phase6_test_verification),
            ("phase7", self.phase7_improvement_ideas),
        ]

        for phase_name, phase_func in phases:
            try:
                start = time.time()
                result = phase_func()
                elapsed = time.time() - start
                result["elapsed_seconds"] = round(elapsed, 2)
                self.results["phases"][phase_name] = result
                logger.info("Phase %s completed in %.2fs", phase_name, elapsed)
            except Exception as e:
                self.results["phases"][phase_name] = {"error": str(e)}
                self.results["errors"].append(f"{phase_name}: {e}")
                logger.error("Phase %s failed: %s", phase_name, e, exc_info=True)

        # Save results
        results_path = BACKUP_DIR / f"eir_maintenance_{datetime.now().strftime('%Y%m%d')}.json"
        with open(results_path, "w") as f:
            json.dump(self.results, f, indent=2, default=str)
        logger.info("Results saved to %s", results_path)

        # Summary
        total_errors = len(self.results["errors"])
        logger.info("=" * 60)
        logger.info("MAINTENANCE COMPLETE — %d errors, %d improvement ideas",
                    total_errors, len(self.results.get("improvements", [])))
        logger.info("=" * 60)

        return self.results


if __name__ == "__main__":
    eir = EirMaintenance()
    results = eir.run()
    # Exit with error code if any phase failed
    sys.exit(1 if results["errors"] else 0)