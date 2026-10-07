"""Comprehensive Unit & Regression Tests for Private Asset Portfolios & Principal Holdings.

Validates the downstream transmission of planetary macro liquidity into private
operational accounts under the Desk Master multi-domain governance hierarchy:
- Layer 0 (Apex Principal): conner_principal_vault
- Layer 1 (Operating Sister OpCos): launchfizz_treasury_vault, vesperspatial_actuarial_reserves, silvera_renewable_packaging
- Layer 2B (Distributed Scientific Fleet): scientific_fleet_compute_pool
- Private Assets & Property: valle_rd_asset_ledger

Invariants Enforced:
1. Double-Entry Conservation: Inflow == Outflow ($0.00 leak) across all private conduits.
2. Global System Integrity Score: >= 90.0 / 100.0, Conservation Score == 20.0 / 20.0.
3. Graph Topology: 0 unintended sink traps, circular feedback ensuring all private entities have in/out degree > 0.
4. Continuous Harmonic Geometry: All node embeddings d=128 (unit norm) and edge relations d=32.
"""

from __future__ import annotations

import duckdb
import numpy as np
import pytest

from capital_manifold.adversarial.adversarial_substrate import (
    AdversarialSubstrateBuilder,
    EntityCategory,
)
from capital_manifold.adversarial.system_auditor import (
    AccountingConservationAuditor,
    EntityRole,
    SystemAuditor,
    DEFAULT_DUCKDB_PATH,
)
from capital_manifold.bridge.pgm_adapter import (
    FINANCIAL_ENTITIES,
    ManifoldPGMBridge,
    MonetaryTier,
)
from capital_manifold.core.schema import FlowEvent, FlowType
from capital_manifold.harvesters.private_assets import (
    APPLE_COMPUTE_PROCEEDS_BURN_USD,
    COMMERCIAL_BANK_SYSTEMIC_LENDING_USD,
    CONNER_EQUITY_ENDOWMENT_USD,
    CONNER_MMF_YIELD_USD,
    LAUNCHFIZZ_CREDIT_LINE_USD,
    LAUNCHFIZZ_EQUITY_INJECTION_USD,
    LAUNCHFIZZ_PAYROLL_VENDORS_USD,
    LAUNCHFIZZ_SAAS_INFRA_USD,
    PRIME_MMF_YIELD_REPLENISHMENT_USD,
    REPORT_DATE,
    SCIENTIFIC_COMPUTE_ENDOWMENT_USD,
    SCIENTIFIC_COMPUTE_HARDWARE_USD,
    SILVERA_CAPEX_INJECTION_USD,
    SILVERA_FEEDSTOCK_TOOLING_USD,
    VALLE_RD_EQUITY_CUSHION_USD,
    VALLE_RD_ESCROW_EQUITY_USD,
    VALLE_RD_MORTGAGE_AMORTIZATION_USD,
    VESPERSPATIAL_COLLATERAL_ESCROW_USD,
    VESPERSPATIAL_UNDERWRITING_PREMIUMS_USD,
    PrivateAssetsHarvester,
)


PRIVATE_ENTITIES = [
    "conner_principal_vault",
    "launchfizz_treasury_vault",
    "vesperspatial_actuarial_reserves",
    "silvera_renewable_packaging",
    "scientific_fleet_compute_pool",
    "valle_rd_asset_ledger",
]


@pytest.fixture
def harvester() -> PrivateAssetsHarvester:
    return PrivateAssetsHarvester()


@pytest.fixture
def bridge() -> ManifoldPGMBridge:
    return ManifoldPGMBridge()


# -------------------------------------------------------------------------
# 1. Statutory Flow Ingestion Tests
# -------------------------------------------------------------------------

def test_private_assets_harvester_ingestion(harvester: PrivateAssetsHarvester):
    """Verifies that all 18 private asset flows are generated with strict accounting invariants."""
    events = harvester.harvest()
    assert len(events) == 18

    # 1. Apex Principal Yield Transmission
    ev_yield = next(e for e in events if "private_yield_transmission_mmf" in e.event_id)
    assert ev_yield.source_entity == "us_prime_mmf_basin"
    assert ev_yield.target_entity == "conner_principal_vault"
    assert ev_yield.nominal_amount == CONNER_MMF_YIELD_USD
    assert ev_yield.flow_type == FlowType.POOL_CONCENTRATION

    # 2. Operating Sister OpCos: Launchfizz
    ev_lf_credit = next(e for e in events if "launchfizz_operating_credit_line" in e.event_id)
    assert ev_lf_credit.source_entity == "us_commercial_bank_credit_pool"
    assert ev_lf_credit.target_entity == "launchfizz_treasury_vault"
    assert ev_lf_credit.nominal_amount == LAUNCHFIZZ_CREDIT_LINE_USD

    ev_lf_equity = next(e for e in events if "launchfizz_equity_injection" in e.event_id)
    assert ev_lf_equity.source_entity == "conner_principal_vault"
    assert ev_lf_equity.target_entity == "launchfizz_treasury_vault"
    assert ev_lf_equity.nominal_amount == LAUNCHFIZZ_EQUITY_INJECTION_USD

    ev_lf_pay = next(e for e in events if "launchfizz_payroll_disbursements" in e.event_id)
    assert ev_lf_pay.source_entity == "launchfizz_treasury_vault"
    assert ev_lf_pay.target_entity == "agency_operating_payroll_and_vendors"
    assert ev_lf_pay.nominal_amount == LAUNCHFIZZ_PAYROLL_VENDORS_USD

    ev_lf_saas = next(e for e in events if "launchfizz_saas_disbursements" in e.event_id)
    assert ev_lf_saas.source_entity == "launchfizz_treasury_vault"
    assert ev_lf_saas.target_entity == "commercial_cloud_and_saas_vendors"
    assert ev_lf_saas.nominal_amount == LAUNCHFIZZ_SAAS_INFRA_USD

    # 3. Operating Sister OpCos: Vesperspatial (Delphi-1.0)
    ev_vs_prem = next(e for e in events if "vesperspatial_underwriting_premiums" in e.event_id)
    assert ev_vs_prem.source_entity == "catastrophe_reinsurance_cedants"
    assert ev_vs_prem.target_entity == "vesperspatial_actuarial_reserves"
    assert ev_vs_prem.nominal_amount == VESPERSPATIAL_UNDERWRITING_PREMIUMS_USD

    ev_vs_escrow = next(e for e in events if "vesperspatial_collateral_escrow" in e.event_id)
    assert ev_vs_escrow.source_entity == "vesperspatial_actuarial_reserves"
    assert ev_vs_escrow.target_entity == "us_treasuries_custody"
    assert ev_vs_escrow.nominal_amount == VESPERSPATIAL_COLLATERAL_ESCROW_USD

    # 4. Operating Sister OpCos: Silvera
    ev_silv_capex = next(e for e in events if "silvera_capex_injection" in e.event_id)
    assert ev_silv_capex.source_entity == "conner_principal_vault"
    assert ev_silv_capex.target_entity == "silvera_renewable_packaging"
    assert ev_silv_capex.nominal_amount == SILVERA_CAPEX_INJECTION_USD

    ev_silv_tool = next(e for e in events if "silvera_feedstock_tooling" in e.event_id)
    assert ev_silv_tool.source_entity == "silvera_renewable_packaging"
    assert ev_silv_tool.target_entity == "molded_fiber_tooling_and_feedstock_vendors"
    assert ev_silv_tool.nominal_amount == SILVERA_FEEDSTOCK_TOOLING_USD

    # 5. Distributed Scientific Fleet
    ev_comp_endow = next(e for e in events if "scientific_compute_endowment" in e.event_id)
    assert ev_comp_endow.source_entity == "conner_principal_vault"
    assert ev_comp_endow.target_entity == "scientific_fleet_compute_pool"
    assert ev_comp_endow.nominal_amount == SCIENTIFIC_COMPUTE_ENDOWMENT_USD

    ev_comp_hw = next(e for e in events if "compute_vendor_disbursements" in e.event_id)
    assert ev_comp_hw.source_entity == "scientific_fleet_compute_pool"
    assert ev_comp_hw.target_entity == "apple_bigtech_treasury_vault"
    assert ev_comp_hw.nominal_amount == SCIENTIFIC_COMPUTE_HARDWARE_USD

    # 6. Real Estate & Property
    ev_valle_eq = next(e for e in events if "valle_rd_equity_cushion" in e.event_id)
    assert ev_valle_eq.source_entity == "conner_principal_vault"
    assert ev_valle_eq.target_entity == "valle_rd_asset_ledger"
    assert ev_valle_eq.nominal_amount == VALLE_RD_EQUITY_CUSHION_USD

    ev_valle_mort = next(e for e in events if "valle_rd_mortgage_amortization" in e.event_id)
    assert ev_valle_mort.source_entity == "valle_rd_asset_ledger"
    assert ev_valle_mort.target_entity == "us_commercial_bank_credit_pool"
    assert ev_valle_mort.nominal_amount == VALLE_RD_MORTGAGE_AMORTIZATION_USD

    ev_valle_dist = next(e for e in events if "valle_rd_retained_equity_escrow" in e.event_id)
    assert ev_valle_dist.source_entity == "valle_rd_asset_ledger"
    assert ev_valle_dist.target_entity == "valle_rd_property_equity_escrow"
    assert ev_valle_dist.nominal_amount == VALLE_RD_ESCROW_EQUITY_USD


# -------------------------------------------------------------------------
# 2. DuckDB Persistence & Storage Invariants
# -------------------------------------------------------------------------

def test_private_assets_duckdb_store():
    """Verifies that the DuckDB store contains all 115 flows and all 6 private entities."""
    assert DEFAULT_DUCKDB_PATH.exists(), f"DuckDB not found at {DEFAULT_DUCKDB_PATH}"
    con = duckdb.connect(str(DEFAULT_DUCKDB_PATH), read_only=True)
    try:
        count = con.execute("SELECT count(*) FROM flow_events").fetchone()[0]
        assert count == 115

        # Check all 6 private entities are referenced as source or target
        for pe in PRIVATE_ENTITIES:
            pe_count = con.execute(
                "SELECT count(*) FROM flow_events WHERE source_entity = ? OR target_entity = ?",
                [pe, pe]
            ).fetchone()[0]
            assert pe_count > 0, f"Private entity {pe} not found in DuckDB flow_events"
    finally:
        con.close()


# -------------------------------------------------------------------------
# 3. Double-Entry Conservation & Zero-Leak Invariants
# -------------------------------------------------------------------------

def test_private_assets_double_entry_conservation():
    """Verifies zero double-entry leaks across all 6 private entities and macro counterparties."""
    auditor = AccountingConservationAuditor(duckdb_path=DEFAULT_DUCKDB_PATH)
    report = auditor.audit()

    # Verify zero conduit leaks across the entire manifold
    assert len(report.detected_leaks) == 0
    assert report.total_leakage_volume_usd == pytest.approx(0.0, abs=1e-3)

    # Verify each private asset entity is a perfectly conserved conduit
    expected_flows = {
        "conner_principal_vault": 1_730_000.0,
        "launchfizz_treasury_vault": 2_100_000.0,
        "vesperspatial_actuarial_reserves": 2_500_000.0,
        "silvera_renewable_packaging": 350_000.0,
        "scientific_fleet_compute_pool": 480_000.0,
        "valle_rd_asset_ledger": 650_000.0,
    }

    for pe, expected_usd in expected_flows.items():
        assert pe in report.conduit_entities, f"{pe} not categorized as intermediate conduit"
        s = report.summaries[pe]
        assert s.role == EntityRole.INTERMEDIATE_CONDUIT
        assert s.is_conduit is True
        assert s.is_leak is False
        assert s.leak_amount_usd == pytest.approx(0.0, abs=1e-3)
        assert s.total_inflow_usd == pytest.approx(expected_usd, rel=1e-3)
        assert s.total_outflow_usd == pytest.approx(expected_usd, rel=1e-3)

    # Verify systemic macro counterparties remain balanced
    apple_s = report.summaries["apple_bigtech_treasury_vault"]
    assert apple_s.is_leak is False
    assert apple_s.leak_amount_usd == pytest.approx(0.0, abs=1e-3)

    mmf_s = report.summaries["us_prime_mmf_basin"]
    assert mmf_s.is_leak is False
    assert mmf_s.leak_amount_usd == pytest.approx(0.0, abs=1e-3)


# -------------------------------------------------------------------------
# 4. Financial Registry & PGM Bridge Integration
# -------------------------------------------------------------------------

def test_private_assets_entity_registration():
    """Verifies that all private entities and counterparties are registered in FINANCIAL_ENTITIES."""
    for pe in PRIVATE_ENTITIES:
        assert pe in FINANCIAL_ENTITIES, f"{pe} missing from FINANCIAL_ENTITIES registry"
        entry = FINANCIAL_ENTITIES[pe]
        assert isinstance(entry["tier"], MonetaryTier)
        assert entry["jurisdiction"] == "US"
        assert len(entry["description"]) > 0

    # Counterparty entities
    assert "agency_operating_payroll_and_vendors" in FINANCIAL_ENTITIES
    assert "commercial_cloud_and_saas_vendors" in FINANCIAL_ENTITIES
    assert "molded_fiber_tooling_and_feedstock_vendors" in FINANCIAL_ENTITIES
    assert "valle_rd_property_equity_escrow" in FINANCIAL_ENTITIES
    assert "us_corporate_and_household_borrowers" in FINANCIAL_ENTITIES
    assert "us_commercial_bank_credit_pool" in FINANCIAL_ENTITIES
    assert "family_office_principal_endowment" in FINANCIAL_ENTITIES
    assert "catastrophe_reinsurance_cedants" in FINANCIAL_ENTITIES
    assert "us_treasuries_custody" in FINANCIAL_ENTITIES


# -------------------------------------------------------------------------
# 5. Adversarial Substrate & Graph Topology Invariants
# -------------------------------------------------------------------------

def test_private_assets_adversarial_substrate_topology():
    """Verifies embedding geometry, edge gating, and absence of absorbing sink traps."""
    builder = AdversarialSubstrateBuilder()
    _, sub = builder.build_adversarial_engine(
        max_nodes_k=128,
        max_edges_m=512,
        num_landmark_clusters=8,
        latent_epsilon=0.10,
    )

    # Verify all 6 private entities are in the substrate with unit-norm d=128 embeddings
    for pe in PRIVATE_ENTITIES:
        node = sub.get_entity(pe)
        assert node is not None, f"Node {pe} missing from adversarial substrate"
        assert node.embedding.shape == (128,)
        norm = np.linalg.norm(node.embedding)
        assert norm == pytest.approx(1.0, abs=1e-5), f"Node {pe} embedding not unit normalized"
        assert builder.entity_categories[pe] == EntityCategory.PRIVATE_ASSETS

    # Verify circular feedback: in-degree > 0 and out-degree > 0 for all private entities
    for pe in PRIVATE_ENTITIES:
        out_edges = sub.adjacency.get(pe, {})
        assert len(out_edges) > 0, f"Entity {pe} has out-degree 0 (absorbing sink trap)"

        # Check in-degree by finding references across all source nodes
        in_count = sum(
            1 for src_id, targets in sub.adjacency.items()
            if pe in targets and len(targets[pe]) > 0
        )
        assert in_count > 0, f"Entity {pe} has in-degree 0 (unreachable orphan)"

    # Verify specific transmission relations exist with d=32 relation embeddings
    private_relations = [
        ("us_prime_mmf_basin", "conner_principal_vault", "private_yield_transmission"),
        ("us_commercial_bank_credit_pool", "launchfizz_treasury_vault", "commercial_credit_line"),
        ("conner_principal_vault", "launchfizz_treasury_vault", "venture_capital_allocation"),
        ("conner_principal_vault", "vesperspatial_actuarial_reserves", "underwriting_collateral_escrow"),
        ("conner_principal_vault", "scientific_fleet_compute_pool", "scientific_compute_endowment"),
        ("scientific_fleet_compute_pool", "apple_bigtech_treasury_vault", "compute_vendor_disbursements"),
        ("conner_principal_vault", "silvera_renewable_packaging", "clean_packaging_capex"),
        ("conner_principal_vault", "valle_rd_asset_ledger", "real_estate_equity_cushion"),
        ("valle_rd_asset_ledger", "us_commercial_bank_credit_pool", "mortgage_debt_service"),
        ("launchfizz_treasury_vault", "conner_principal_vault", "commercial_dividend_distribution"),
        ("silvera_renewable_packaging", "conner_principal_vault", "operating_cashflow_sweep"),
        ("vesperspatial_actuarial_reserves", "conner_principal_vault", "underwriting_profit_distribution"),
        ("valle_rd_asset_ledger", "conner_principal_vault", "property_equity_distribution"),
    ]

    for src_id, tgt_id, rel_name in private_relations:
        targets = sub.adjacency.get(src_id, {})
        assert tgt_id in targets, f"Missing edge {src_id} -> {tgt_id}"
        edge_list = targets[tgt_id]
        matching = [e for e in edge_list if e.relation == rel_name]
        assert len(matching) >= 1, f"Missing relation {rel_name} on {src_id} -> {tgt_id}"
        edge = matching[0]
        assert edge.weight > 0.0
        assert edge.relation_embedding is not None
        assert edge.relation_embedding.shape == (32,)


# -------------------------------------------------------------------------
# 6. Master System Scorecard Integrity
# -------------------------------------------------------------------------

def test_system_scorecard_integrity():
    """Verifies that the Master System Scorecard maintains >= 90.0 integrity and 20.0 conservation."""
    auditor = SystemAuditor()
    scorecard = auditor.run_full_audit()

    assert scorecard.system_integrity_score >= 90.0, f"Integrity score {scorecard.system_integrity_score} < 90.0"
    assert scorecard.conservation_score == 20.0, f"Conservation score {scorecard.conservation_score} != 20.0"
    assert scorecard.dimensional_score == 20.0, f"Dimensional score {scorecard.dimensional_score} != 20.0"
    assert len(scorecard.conservation_report.detected_leaks) == 0, "Double-entry leaks detected"
    assert scorecard.conservation_report.total_leakage_volume_usd == pytest.approx(0.0, abs=1e-3)
    assert len(scorecard.topology_report.unintended_sink_traps) == 0, "Unintended sink traps detected"
