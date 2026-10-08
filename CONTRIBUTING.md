# Contributing to Capital Manifold

Thank you for your interest in contributing to **Capital Manifold** — the open-source planetary balance-sheet network dynamics, siphon forensics, and macro-financial graph engine.

We welcome contributions from financial engineers, computational economists, systems architects, quantitative researchers, and open-source developers committed to planetary financial transparency.

---

## Table of Contents
1. [Code of Conduct & Philosophy](#code-of-conduct--philosophy)
2. [Development Environment Setup](#development-environment-setup)
3. [Architecture Overview](#architecture-overview)
4. [Adding New Statutory Harvesters](#adding-new-statutory-harvesters)
5. [Adding Adversarial Audit Invariants](#adding-adversarial-audit-invariants)
6. [Extending the Procedural Graph Engine Bridge](#extending-the-procedural-graph-engine-bridge)
7. [Adding Siphon Forensics Corridors](#adding-siphon-forensics-corridors)
8. [Testing & Quality Standards](#testing--quality-standards)
9. [Pull Request Workflow](#pull-request-workflow)

---

## Code of Conduct & Philosophy

Capital Manifold is built as a **public-utility counter-intelligence platform** dedicated to radical transparency in global monetary mechanics. We adhere to these tenets:
* **Zero Fabrication:** Every baseline macro quantity must link to statutory, primary-source data (ECB, Banque de France, US Treasury DTS, NY Fed, SEC EDGAR, BIS, IMF) or calibrated empirical benchmarks.
* **Adversarial Rigor:** Invariants are adversarial by design. If a new corridor leaks balance-sheet capital, violates Kirchhoff flow conservation, or mixes temporal velocities without normalization, the test suite must catch it.
* **Clean Dimensional Separation:** Price/yield/spread metrics (basis points) must never be conflated with directional nominal fiat flows (USD/EUR).

---

## Development Environment Setup

### Prerequisites
* Python 3.10+ (tested on Python 3.12)
* Git
* Virtual environment (`venv` or `conda`)

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/ckupferberg/capital-manifold.git
cd capital-manifold

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install the package in editable mode with development dependencies
pip install -e .

# 4. Rebuild the DuckDB local cache from primary harvesters
python scripts/rebuild_manifold_db.py

# 5. Run the test suite to verify installation
pytest tests/
```

---

## Architecture Overview

```
src/capital_manifold/
├── core/                  # Core Pydantic schemas (FlowEvent, MacroStressSnapshot, SiphonAnomaly)
├── harvesters/            # Statutory primary data ingestors (ECB, BdF, DTS, SEC, NY Fed)
├── storage/               # DuckDB & Parquet persistence engine (ManifoldStore)
├── bridge/                # PGM Engine bridge (128d embeddings, landmark scaffolding, Dual-Frontier A*)
├── adversarial/           # SystemAuditor, SiphonHunter, and AdversarialSubstrate
├── simulation/            # StressGauntletEngine (Crisis regimes, failovers, zero-hallucination proofs)
├── pipeline/              # Autonomous CLI pipelines and traversals
├── web/                   # FastAPI backend & Cytoscape.js interactive dashboard
└── cli.py                 # Unified 'capital-manifold' CLI entrypoint
```

---

## Adding New Statutory Harvesters

All harvesters reside in `src/capital_manifold/harvesters/` and inherit from `BaseHarvester` (`src/capital_manifold/harvesters/base.py`).

### Implementation Steps

1. **Subclass `BaseHarvester`**:
   ```python
   from capital_manifold.harvesters.base import BaseHarvester
   from capital_manifold.core.schema import FlowEvent, FlowType

   class BankOfJapanHarvester(BaseHarvester):
       def __init__(self, cache_dir: Optional[Path] = None):
           super().__init__(name="boj_harvester", cache_dir=cache_dir)

       def harvest(self) -> List[FlowEvent]:
           events: List[FlowEvent] = []
           # Ingest primary data via HTTP or baseline fallback
           ...
           return events
   ```

2. **Enforce `FlowEvent` Invariants**:
   * `nominal_amount` must be $\ge 0.0$.
   * `amount_usd_normalized` must be $\ge 0.0$.
   * Spread or basis point metrics (e.g., `oat_bund_spread_bp`) must set `flow_type = FlowType.RISK_FRICTION`, `nominal_amount = 0.0`, and store scalar values strictly in `metric_value`.
   * Include exact statutory provenance in `data_source` and `source_line_item`.

3. **Register in `scripts/rebuild_manifold_db.py`**:
   Add your harvester to the master rebuild pipeline so new entities and events populate `data/cache/manifold.duckdb`.

4. **Add Unit Tests**:
   Create `tests/test_<name>_harvester.py` verifying parsing, network failure fallbacks, and schema validation.

---

## Adding Adversarial Audit Invariants

The `SystemAuditor` (`src/capital_manifold/adversarial/system_auditor.py`) executes 5 audit dimensions:
1. **Accounting Conservation** (Kirchhoff flow conservation: $\sum \text{Inflows} = \sum \text{Outflows} + \Delta \text{Reserves}$)
2. **Dimensional Integrity** (Yields vs. Fiat currencies, positive flow directions, FX rate bounds)
3. **Temporal Cadence** (Turnover velocity normalization: Daily vs. Monthly vs. Quarterly vs. Annual)
4. **Graph Topology** (Articulation points, weakly/strongly connected components, absorbing sinks)
5. **Macro Dark Matter** (Benchmarking against unmodeled OTC derivatives, basis trades, and shadow banking)

### Adding a New Invariant Check

To introduce a new invariant:
1. Identify the auditor class (`AccountingConservationAuditor`, `DimensionalIntegrityAuditor`, etc.).
2. Implement your validation method returning a structured anomaly dataclass.
3. Incorporate the finding into the category penalty score calculation.
4. Add corresponding assertions in `tests/test_system_auditor.py`.

---

## Extending the Procedural Graph Engine Bridge

The bridge (`src/capital_manifold/bridge/pgm_adapter.py`) translates macro-financial entities into the PGM Engine's `EntityNode` and `EdgeRelation` substrate.

### 1. Registering New Entities
Add the entity definition to `FINANCIAL_ENTITIES` with its statutory monetary tier:
```python
"new_entity_id": {
    "tier": MonetaryTier.TRANSMISSION,
    "name": "Official Entity Name",
    "sector": "central_bank | primary_dealer | sovereign_issuer | ...",
    "jurisdiction": "US | EU | JP | CN | GLOBAL",
    "description": "Functional description of balance-sheet operations.",
}
```

### 2. Synthesizing 128-Dimensional Financial Embeddings
When defining or updating vector construction, preserve the canonical dimensional partition:
* **Dims 0–3:** One-hot monetary tier (`GENESIS`, `TRANSMISSION`, `TRAVERSAL`, `SINK`)
* **Dims 4–11:** Institutional sector encoding
* **Dims 12–27:** Jurisdictional coordinates and currency block alignment
* **Dims 28–43:** Balance-sheet asset capacity and systemic scale ($\log_{10} \text{USD}$)
* **Dims 44–59:** Liquidity velocity and temporal turnover frequency
* **Dims 60–75:** Credit risk friction, sovereign spread, and haircut impedance
* **Dims 76–127:** Structural graph embeddings, bridge utility flags, and residual latent space

---

## Adding Siphon Forensics Corridors

The `SiphonHunter` (`src/capital_manifold/adversarial/siphon_hunter.py`) detects illicit, hidden, or structural capital extraction:

1. **Bilateral Mirror Trade Corridors:**
   Add new commodity corridors comparing Exporter FOB against Importer CIF with standard CIF/FOB margin reconciliation.
2. **Absorbing Dark Conduits:**
   Configure intermediate entities exhibiting trapped capital basins, freight margin skimming, or unrecorded retention.
3. **Custody Nominee Hubs:**
   Update `CUSTODIAN_NOMINEE_PROFILES` with official sovereign holdings, domestic absorption ceilings, and triangulated beneficial sovereign owners.
4. **IMF Net Errors & Omissions Vectors:**
   Calibrate dark shipping, informal remittance (USDT / Hawala), or offshore luxury asset allocations.

---

## Testing & Quality Standards

All pull requests must pass the complete test suite with **zero errors and zero regression failures**:

```bash
# Run the entire test suite
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=capital_manifold

# Run CLI verification
pytest tests/test_cli.py
```

### Mandatory Requirements
* **Zero Warnings:** Address all deprecation or runtime warnings.
* **Deterministic Execution:** Tests must not depend on live unauthenticated external networks; use fixtures or built-in statutory fallbacks.
* **Typing:** Use modern Python 3.10+ type annotations (`int | None`, `list[str]`, etc.).
* **Pydantic Validation:** All data mutations must pass strict Pydantic model validation.

---

## Pull Request Workflow

1. **Fork & Branch:** Create a feature branch with a descriptive name:
   ```bash
   git checkout -b feat/japan-carry-refinement
   # or
   git checkout -b fix/target2-drain-boundary
   ```
2. **Commit Conventions:** Follow Conventional Commits:
   * `feat: add Bank of England repo facility harvester`
   * `fix: correct CIF/FOB margin calculation in gold corridor`
   * `docs: update ARCHITECTURE.md 128d embedding specification`
   * `test: add adversarial test for custody nominee 50-sigma outlier`
3. **Verify Locally:**
   * Run `pytest tests/`
   * Test CLI commands (`capital-manifold audit`, `capital-manifold siphon`, `capital-manifold simulate`, `capital-manifold traverse`)
   * Run `python scripts/rebuild_manifold_db.py` to ensure clean database generation
4. **Submit PR:** Open a Pull Request against `main`. Provide a clear summary of changes, motivation, and test results.
