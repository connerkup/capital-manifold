"""Unit tests for the Systemic Shock Simulation Gauntlet.

Verifies:
1. Regime 1 (French OAT Crisis) dynamic failover to CA-CIB / Natixis secondary syndicate.
2. Regime 2 (Transatlantic Dollar Freeze) dynamic failover to FICC sponsored repo.
3. Regime 3 (Compound Super-Crisis) compound routing and anti-hallucination verification.
4. Integrated GauntletReport synthesis and JSON serialization.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from capital_manifold.simulation.stress_gauntlet import (
    StressGauntletEngine,
    GauntletRegimeResult,
    GauntletReport,
)
from capital_manifold.bridge.pgm_adapter import ManifoldPGMBridge


@pytest.fixture
def gauntlet_engine() -> StressGauntletEngine:
    return StressGauntletEngine()


def test_stress_gauntlet_engine_initialization(gauntlet_engine: StressGauntletEngine):
    """Verifies clean initialization and substrate cloning capability."""
    assert gauntlet_engine.bridge is not None
    assert gauntlet_engine.engine is not None
    assert gauntlet_engine.base_substrate is not None
    assert len(gauntlet_engine.base_substrate.entities) >= 40

    clone = gauntlet_engine._clone_substrate()
    assert len(clone.entities) == len(gauntlet_engine.base_substrate.entities)
    assert clone is not gauntlet_engine.base_substrate


def test_regime_1_sovereign_blowout_failover(gauntlet_engine: StressGauntletEngine):
    """Verifies that 75% SVT dealer constraint forces failover to Natixis syndicate."""
    regime = gauntlet_engine.run_regime_1_sovereign_blowout()

    assert regime.regime_id == "REGIME-01-OAT-CRISIS"
    assert regime.bypass_corridor_activation_pct == 100.0
    assert "ca_cib_natixis_dealer_syndicate" in regime.active_bypasses
    assert regime.avg_pct_cost_delta > 0.0

    # Route 1: Tresor -> TARGET2
    r_t2 = regime.routes["french_republic_tresor->eurosystem_target2_pool"]
    assert r_t2.baseline_success is True
    assert "svt_dealers_bnp_socgen" in r_t2.baseline_path
    assert r_t2.shocked_success is True
    assert "ca_cib_natixis_dealer_syndicate" in r_t2.shocked_path
    assert "svt_dealers_bnp_socgen" not in r_t2.shocked_path
    assert r_t2.cost_delta > 0.0

    # Route 2: Tresor -> Bund Anchor
    r_bund = regime.routes["french_republic_tresor->bund_risk_free_anchor"]
    assert r_bund.baseline_success is True
    assert r_bund.shocked_success is True
    assert "ca_cib_natixis_dealer_syndicate" in r_bund.shocked_path
    assert "bund_risk_free_anchor" == r_bund.shocked_path[-1]

    # Bottlenecks identified
    assert len(regime.bottleneck_nodes) > 0
    assert any("natixis" in b or "tresor" in b or "france" in b for b in regime.bottleneck_nodes)


def test_regime_2_dollar_repo_freeze_failover(gauntlet_engine: StressGauntletEngine):
    """Verifies that US Triparty repo collapse triggers dynamic failover to FICC sponsored repo."""
    regime = gauntlet_engine.run_regime_2_dollar_freeze()

    assert regime.regime_id == "REGIME-02-DOLLAR-FREEZE"
    assert regime.bypass_corridor_activation_pct == 100.0
    assert "ficc_sponsored_repo_clearing" in regime.active_bypasses

    # Carry desk funding route
    r_jp = regime.routes["japan_institutional_carry_desk->us_treasury_tga"]
    assert r_jp.baseline_success is True
    assert "us_triparty_repo_pool" in r_jp.baseline_path
    assert r_jp.shocked_success is True
    assert "ficc_sponsored_repo_clearing" in r_jp.shocked_path
    assert "us_triparty_repo_pool" not in r_jp.shocked_path
    assert "us_treasury_tga" == r_jp.shocked_path[-1]

    # European G-SIB funding route
    r_fx = regime.routes["offshore_fx_swap_desk->us_treasury_tga"]
    assert r_fx.baseline_success is True
    assert "us_triparty_repo_pool" in r_fx.baseline_path
    assert r_fx.shocked_success is True
    assert "ficc_sponsored_repo_clearing" in r_fx.shocked_path
    assert "us_triparty_repo_pool" not in r_fx.shocked_path

    # US Prime MMF cash repo route
    r_mmf = regime.routes["us_prime_mmf_basin->us_treasury_tga"]
    assert r_mmf.baseline_success is True
    assert r_mmf.shocked_success is True
    assert "ficc_sponsored_repo_clearing" in r_mmf.shocked_path


def test_regime_3_compound_super_crisis_and_anti_hallucination(gauntlet_engine: StressGauntletEngine):
    """Verifies compound crisis resilience and strict zero-hallucination guarantees on severed conduits."""
    regime = gauntlet_engine.run_regime_3_compound_super_crisis()

    assert regime.regime_id == "REGIME-03-COMPOUND-SUPER-CRISIS"
    assert regime.bypass_corridor_activation_pct == 100.0
    assert regime.zero_hallucinations_verified is True

    # 1. Active routes still successfully route via bypasses
    r_t2 = regime.routes["french_republic_tresor->eurosystem_target2_pool"]
    assert r_t2.shocked_success is True
    assert "ca_cib_natixis_dealer_syndicate" in r_t2.shocked_path

    r_jp = regime.routes["japan_institutional_carry_desk->us_treasury_tga"]
    assert r_jp.shocked_success is True
    assert "ficc_sponsored_repo_clearing" in r_jp.shocked_path

    # 2. Interdicted shadow tanker routes must return success=False with zero hallucinated edges
    r_energy_fr = regime.routes["bank_of_russia_cbr_vault->french_economy_importers"]
    assert r_energy_fr.baseline_success is True
    assert r_energy_fr.shocked_success is False
    assert len(r_energy_fr.shocked_path) == 0
    assert r_energy_fr.zero_hallucinations_passed is True

    r_energy_in = regime.routes["bank_of_russia_cbr_vault->reserve_bank_of_india_refining_hub"]
    assert r_energy_in.baseline_success is True
    assert r_energy_in.shocked_success is False
    assert len(r_energy_in.shocked_path) == 0
    assert r_energy_in.zero_hallucinations_passed is True


def test_full_gauntlet_synthesis_and_serialization(gauntlet_engine: StressGauntletEngine, tmp_path: Path):
    """Verifies that run_full_gauntlet synthesizes all 3 regimes and serializes cleanly."""
    report = gauntlet_engine.run_full_gauntlet()

    assert isinstance(report, GauntletReport)
    assert len(report.regimes) == 3
    assert "REGIME-01-OAT-CRISIS" in report.regimes
    assert "REGIME-02-DOLLAR-FREEZE" in report.regimes
    assert "REGIME-03-COMPOUND-SUPER-CRISIS" in report.regimes

    assert report.overall_resilience_score >= 85.0
    assert len(report.summary_insights) >= 4

    # JSON serialization check
    d = report.to_dict()
    assert isinstance(d, dict)
    serialized = json.dumps(d, indent=2)
    assert len(serialized) > 500

    out_file = tmp_path / "gauntlet_results.json"
    out_file.write_text(serialized, encoding="utf-8")
    assert out_file.exists()
    assert out_file.stat().st_size > 500
