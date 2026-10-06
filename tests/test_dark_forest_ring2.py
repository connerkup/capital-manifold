"""Unit tests verifying Dark Forest Ring 2: The QT Burn Chamber, Evaporating RRP Buffer & Offshore Sinks.

Tests:
1. Fed H.4.1 Balance Sheet & Treasury TIC Live/Fallback Harvester Ingestion.
2. Dark Forest Ring 2 Entity & Edge Registration in L3 Substrate.
3. Dual-Frontier A* Multi-Corridor Path Discovery:
   - Sovereign Debt -> Primary Dealers -> London Eurodollar -> Cayman Offshore Pool.
   - US Prime MMF -> US Treasury TGA -> Fed SOMA QT Burn Chamber.
   - French Sovereign Crisis -> Banque de France -> Fed/ECB Emergency Swap Line.
   - Prime MMF Cash Parking in Fed ON RRP Buffer.
4. RRP Buffer Exhaustion Simulation & Full Macro Traversal Invariants.
"""

from unittest.mock import MagicMock
import numpy as np
import pytest

from capital_manifold.bridge.pgm_adapter import (
    FINANCIAL_ENTITIES,
    ManifoldPGMBridge,
    MonetaryTier,
)
from capital_manifold.core.schema import FlowEvent, FlowType
from capital_manifold.harvesters.fed_dark_forest_ring2 import (
    CENTRAL_BANK_SWAPS_USD,
    CUMULATIVE_QT_BURN_USD,
    CURRENT_ON_RRP_USD,
    CURRENT_SOMA_ASSETS_USD,
    TIC_CAYMAN_HEDGE_USD,
    TIC_UK_EURODOLLAR_USD,
    TOTAL_US_PUBLIC_DEBT_USD,
    DarkForestRing2Harvester,
)


@pytest.fixture
def harvester() -> DarkForestRing2Harvester:
    return DarkForestRing2Harvester()


@pytest.fixture
def bridge() -> ManifoldPGMBridge:
    return ManifoldPGMBridge()


def test_dark_forest_ring2_harvester_api_and_fallback(harvester: DarkForestRing2Harvester):
    """Verifies harvesting and schema normalization of Fed H.4.1 QT and Treasury TIC data."""
    # 1. Standard execution
    h41_events, h41_meta = harvester.fetch_fed_h41_balance_sheet()
    assert len(h41_events) == 3
    assert "fed_soma_total_assets_usd" in h41_meta
    assert "fed_cumulative_qt_burn_usd" in h41_meta
    assert "fed_on_rrp_balance_usd" in h41_meta
    assert "central_bank_liquidity_swaps_usd" in h41_meta

    # Check QT burn event
    qt_ev = next(e for e in h41_events if "qt_burn" in e.event_id)
    assert qt_ev.flow_type == FlowType.QT_BURN
    assert qt_ev.source_entity == "federal_reserve_soma"
    assert qt_ev.target_entity == "fed_soma_qt_burn_chamber"
    assert qt_ev.nominal_amount >= 2.0e12  # Over $2 Trillion QT money destruction
    assert qt_ev.currency == "USD"

    # Check ON RRP buffer event
    rrp_ev = next(e for e in h41_events if "rrp_buffer" in e.event_id)
    assert rrp_ev.flow_type == FlowType.POOL_CONCENTRATION
    assert rrp_ev.source_entity == "us_prime_mmf_basin"
    assert rrp_ev.target_entity == "fed_on_rrp_buffer_sink"
    assert rrp_ev.nominal_amount == pytest.approx(CURRENT_ON_RRP_USD, rel=0.1)

    # Check Central Bank Swap Line event
    swap_ev = next(e for e in h41_events if "swap_line" in e.event_id)
    assert swap_ev.flow_type == FlowType.INTERBANK_TRANSFER
    assert swap_ev.target_entity == "fed_ecb_liquidity_swap_line"
    assert swap_ev.nominal_amount == pytest.approx(CENTRAL_BANK_SWAPS_USD, rel=0.1)

    # 2. Treasury TIC foreign holdings
    tic_events, tic_meta = harvester.fetch_treasury_tic_and_debt()
    assert len(tic_events) == 5
    assert tic_meta["total_us_public_debt_usd"] == TOTAL_US_PUBLIC_DEBT_USD

    uk_ev = next(e for e in tic_events if "uk" in e.event_id)
    assert uk_ev.source_entity == "london_eurodollar_pool"
    assert uk_ev.nominal_amount == TIC_UK_EURODOLLAR_USD

    cayman_ev = next(e for e in tic_events if "cayman" in e.event_id)
    assert cayman_ev.source_entity == "offshore_cayman_hedge_pool"
    assert cayman_ev.nominal_amount == TIC_CAYMAN_HEDGE_USD

    # 3. Network outage fallback verification
    mock_client = MagicMock()
    mock_client.get.side_effect = Exception("Simulated connection timeout")
    harvester.client = mock_client

    fb_events, fb_meta = harvester.fetch_fed_h41_balance_sheet()
    assert len(fb_events) == 3
    assert fb_meta["fed_soma_total_assets_usd"] == CURRENT_SOMA_ASSETS_USD
    assert fb_meta["fed_cumulative_qt_burn_usd"] == CUMULATIVE_QT_BURN_USD
    assert fb_meta["fed_on_rrp_balance_usd"] == CURRENT_ON_RRP_USD


def test_dark_forest_ring2_node_registration(bridge: ManifoldPGMBridge):
    """Verifies that all 5 Ring 2 nodes and transmission edges exist with valid embeddings."""
    sub = bridge.substrate
    ring2_nodes = [
        "fed_soma_qt_burn_chamber",
        "fed_on_rrp_buffer_sink",
        "offshore_cayman_hedge_pool",
        "london_eurodollar_pool",
        "fed_ecb_liquidity_swap_line",
    ]

    for nid in ring2_nodes:
        node = sub.get_entity(nid)
        assert node is not None, f"Ring 2 node {nid} missing from substrate"
        assert node.embedding.shape == (128,), f"Ring 2 node {nid} invalid shape"
        norm = np.linalg.norm(node.embedding)
        assert norm == pytest.approx(1.0, abs=1e-5), f"Ring 2 node {nid} not unit normalized"
        assert nid in FINANCIAL_ENTITIES
        assert node.metadata.get("sector") == FINANCIAL_ENTITIES[nid]["sector"]

    # Verify Ring 2 Relations and Dimensions (d=32)
    ring2_relations = [
        ("us_prime_mmf_basin", "fed_on_rrp_buffer_sink", "rrp_cash_parking"),
        ("us_triparty_repo_pool", "us_treasury_tga", "tga_debt_issuance_absorption"),
        ("us_treasury_tga", "fed_soma_qt_burn_chamber", "qt_redemption_money_burn"),
        ("offshore_fx_swap_desk", "london_eurodollar_pool", "eurodollar_syndication"),
        ("london_eurodollar_pool", "offshore_cayman_hedge_pool", "cayman_shadow_capital_flight"),
        ("banque_de_france", "fed_ecb_liquidity_swap_line", "emergency_fx_swap_activation"),
        ("fed_ecb_liquidity_swap_line", "offshore_fx_swap_desk", "central_bank_dollar_injection"),
    ]

    for src_id, tgt_id, rel_name in ring2_relations:
        targets = sub.adjacency.get(src_id, {})
        assert tgt_id in targets, f"Missing edge {src_id} -> {tgt_id}"
        edge_list = targets[tgt_id]
        matching = [e for e in edge_list if e.relation == rel_name]
        assert len(matching) >= 1, f"Missing relation {rel_name} on {src_id} -> {tgt_id}"
        edge = matching[0]
        assert edge.weight > 0.0
        assert edge.relation_embedding is not None
        assert edge.relation_embedding.shape == (32,)


def test_dual_frontier_a_star_ring2_traversals(bridge: ManifoldPGMBridge):
    """Verifies Dual-Frontier A* path discovery across all 3 Dark Forest Ring 2 transmission corridors."""
    # Corridor 1: French Sovereign -> Primary Dealers -> London Eurodollar -> Cayman
    res1 = bridge.materialize_liquidity_path(
        source_id="french_republic_tresor",
        target_id="offshore_cayman_hedge_pool",
    )
    assert res1.success is True
    assert res1.path_nodes == [
        "french_republic_tresor",
        "svt_dealers_bnp_socgen",
        "offshore_fx_swap_desk",
        "london_eurodollar_pool",
        "offshore_cayman_hedge_pool",
    ]
    assert [e.relation for e in res1.path_edges] == [
        "oat_primary_issuance",
        "synthetic_usd_fx_swap",
        "eurodollar_syndication",
        "cayman_shadow_capital_flight",
    ]
    assert res1.total_cost > 0.0
    assert res1.iterations > 0

    # Corridor 2: US Prime MMF -> US Triparty Repo -> US Treasury TGA -> Fed SOMA QT Burn Chamber
    res2 = bridge.materialize_liquidity_path(
        source_id="us_prime_mmf_basin",
        target_id="fed_soma_qt_burn_chamber",
    )
    assert res2.success is True
    assert res2.path_nodes == [
        "us_prime_mmf_basin",
        "us_triparty_repo_pool",
        "us_treasury_tga",
        "fed_soma_qt_burn_chamber",
    ]
    assert [e.relation for e in res2.path_edges] == [
        "mmf_cash_repo_lending",
        "tga_debt_issuance_absorption",
        "qt_redemption_money_burn",
    ]
    assert res2.total_cost > 0.0

    # Corridor 3: French Sovereign Crisis -> Banque de France -> Fed/ECB Emergency Swap Line
    res3 = bridge.materialize_liquidity_path(
        source_id="french_republic_tresor",
        target_id="fed_ecb_liquidity_swap_line",
    )
    assert res3.success is True
    assert res3.path_nodes == [
        "french_republic_tresor",
        "svt_dealers_bnp_socgen",
        "banque_de_france",
        "fed_ecb_liquidity_swap_line",
    ]
    assert [e.relation for e in res3.path_edges] == [
        "oat_primary_issuance",
        "dealer_reserve_clearing",
        "emergency_fx_swap_activation",
    ]
    assert res3.total_cost > 0.0

    # Direct 1-hop: US Prime MMF -> Fed ON RRP Buffer Sink
    res_rrp = bridge.materialize_liquidity_path(
        source_id="us_prime_mmf_basin",
        target_id="fed_on_rrp_buffer_sink",
    )
    assert res_rrp.success is True
    assert res_rrp.path_nodes == ["us_prime_mmf_basin", "fed_on_rrp_buffer_sink"]
    assert [e.relation for e in res_rrp.path_edges] == ["rrp_cash_parking"]


def test_rrp_exhaustion_simulation_and_full_traversal(bridge: ManifoldPGMBridge):
    """Verifies full macroeconomic traversal summary and RRP buffer exhaustion dynamics."""
    summary = bridge.execute_macro_traversal()
    assert summary["invariants_verified"] is True
    assert summary["invariant_details"]["cayman_capital_flight_reachability"] is True
    assert summary["invariant_details"]["qt_money_burn_reachability"] is True

    paths = summary["paths"]
    assert "cayman_offshore_capital_flight" in paths
    assert paths["cayman_offshore_capital_flight"]["success"] is True
    assert "fed_soma_qt_money_burn" in paths
    assert paths["fed_soma_qt_money_burn"]["success"] is True

    # RRP Depletion Sensitivity Dynamics
    # When RRP facility empties ($361B -> $1B), impedance to non-bank parking increases
    w_rrp_current = bridge.compute_edge_weight(
        base_weight=1.05,
        flow_volume_eur=361.883e9,
        risk_friction=0.30,
        is_domestic_retention=False,
    )
    w_rrp_depleted = bridge.compute_edge_weight(
        base_weight=1.05,
        flow_volume_eur=1.0e9,
        risk_friction=0.30,
        is_domestic_retention=False,
    )
    assert w_rrp_depleted > w_rrp_current, "Depleted RRP buffer must impose higher impedance on cash parking"

    # Spread widening friction on emergency central bank swap line
    w_swap_calm = bridge.compute_edge_weight(
        base_weight=1.30,
        flow_volume_eur=207e6,
        risk_friction=0.40,
        is_domestic_retention=False,
    )
    w_swap_crisis = bridge.compute_edge_weight(
        base_weight=1.30,
        flow_volume_eur=207e6,
        risk_friction=2.20,
        is_domestic_retention=False,
    )
    assert w_swap_crisis > w_swap_calm, "Crisis spread widening must increase emergency swap friction"
