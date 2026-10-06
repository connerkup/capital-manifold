"""Unit tests verifying Transatlantic US Dollar Conduit and Dark Forest Ring 1 Bridge.

Tests:
1. Live/Fallback Harvester Ingestion: US Treasury DTS (TGA) & NY Fed Markets API (SOFR).
2. Dark Forest Ring 1 Entity & Edge Registration in L3 Substrate.
3. Dual-Frontier A* Multi-Hop Transatlantic Path Discovery to US Prime MMF Basin.
4. Macro Friction, OAT Haircut, and TGA Reserve Drain Dynamics.
"""

from unittest.mock import MagicMock
import numpy as np
import pytest

from capital_manifold.bridge.pgm_adapter import (
    FINANCIAL_ENTITIES,
    ManifoldPGMBridge,
    MonetaryTier,
)
from capital_manifold.core.schema import FlowEvent, FlowType, MacroStressSnapshot
from capital_manifold.harvesters.us_transatlantic import (
    FALLBACK_SOFR_RATE,
    FALLBACK_SOFR_VOLUME_USD,
    FALLBACK_TGA_CLOSING_USD,
    FALLBACK_TGA_NET_DRAIN_USD,
    FALLBACK_TGA_OPENING_USD,
    TransatlanticMacroHarvester,
)


@pytest.fixture
def harvester() -> TransatlanticMacroHarvester:
    """Fixture providing TransatlanticMacroHarvester."""
    return TransatlanticMacroHarvester()


@pytest.fixture
def bridge() -> ManifoldPGMBridge:
    """Fixture providing initialized ManifoldPGMBridge."""
    return ManifoldPGMBridge()


def test_transatlantic_harvester_api_and_fallback(harvester: TransatlanticMacroHarvester):
    """Verifies parsing of US Treasury DTS cash balances and NY Fed repo reference rates."""
    # 1. Standard execution (live endpoint or internal fallback if offline)
    tga_events, tga_meta = harvester.fetch_tga_cash_balance()
    assert len(tga_events) == 2
    assert "tga_closing_balance_usd" in tga_meta
    assert "tga_opening_balance_usd" in tga_meta
    assert "tga_net_liquidity_change_usd" in tga_meta
    assert tga_meta["tga_closing_balance_usd"] > 0
    assert isinstance(tga_meta["tga_net_liquidity_change_usd"], float)

    drain_ev = next(e for e in tga_events if "drain" in e.event_id)
    stock_ev = next(e for e in tga_events if "stock" in e.event_id)
    assert drain_ev.currency == "USD"
    assert drain_ev.target_entity == "us_treasury_tga"
    assert drain_ev.flow_type == FlowType.TAX_ABSORPTION
    assert stock_ev.nominal_amount == tga_meta["tga_closing_balance_usd"]

    sofr_events, sofr_meta = harvester.fetch_nyfed_reference_rates()
    assert len(sofr_events) == 1
    assert "sofr_rate" in sofr_meta
    assert "sofr_volume_billions_usd" in sofr_meta
    assert sofr_meta["sofr_rate"] > 0
    assert sofr_meta["sofr_volume_billions_usd"] >= 1000.0  # Multi-trillion market

    sofr_ev = sofr_events[0]
    assert sofr_ev.target_entity == "us_triparty_repo_pool"
    assert sofr_ev.source_entity == "us_prime_mmf_basin"
    assert sofr_ev.flow_type == FlowType.REPO_COLLATERAL
    assert sofr_ev.currency == "USD"
    assert sofr_ev.amount_usd_normalized >= 1e12

    # 2. Explicit network failure fallback test
    mock_client = MagicMock()
    mock_client.get.side_effect = Exception("Simulated network outage")
    harvester.client = mock_client

    fallback_tga_events, fallback_tga_meta = harvester.fetch_tga_cash_balance()
    assert len(fallback_tga_events) == 2
    assert fallback_tga_meta["tga_closing_balance_usd"] == FALLBACK_TGA_CLOSING_USD
    assert fallback_tga_meta["tga_opening_balance_usd"] == FALLBACK_TGA_OPENING_USD
    assert fallback_tga_meta["tga_net_liquidity_change_usd"] == FALLBACK_TGA_NET_DRAIN_USD
    assert fallback_tga_meta.get("fallback_applied") is True

    fallback_sofr_events, fallback_sofr_meta = harvester.fetch_nyfed_reference_rates()
    assert len(fallback_sofr_events) == 1
    assert fallback_sofr_meta["sofr_rate"] == FALLBACK_SOFR_RATE
    assert fallback_sofr_meta["sofr_volume_billions_usd"] == pytest.approx(FALLBACK_SOFR_VOLUME_USD / 1e9)


def test_dark_forest_ring1_node_registration(bridge: ManifoldPGMBridge):
    """Verifies that Dark Forest Ring 1 nodes and transmission edges are properly registered."""
    sub = bridge.substrate
    dark_forest_nodes = [
        "offshore_fx_swap_desk",
        "us_triparty_repo_pool",
        "us_prime_mmf_basin",
        "us_treasury_tga",
    ]

    for nid in dark_forest_nodes:
        node = sub.get_entity(nid)
        assert node is not None, f"Dark Forest node {nid} missing from substrate"
        assert node.embedding.shape == (128,), f"Dark Forest node {nid} has invalid dimension"
        norm = np.linalg.norm(node.embedding)
        assert norm == pytest.approx(1.0, abs=1e-5), f"Dark Forest node {nid} embedding not unit normalized"
        assert nid in FINANCIAL_ENTITIES
        assert node.metadata.get("sector") == FINANCIAL_ENTITIES[nid]["sector"]

    # Verify SVT Dealer -> Offshore FX Swap Desk edge
    targets_svt = sub.adjacency.get("svt_dealers_bnp_socgen", {})
    assert "offshore_fx_swap_desk" in targets_svt
    fx_edges = targets_svt["offshore_fx_swap_desk"]
    assert len(fx_edges) >= 1
    assert fx_edges[0].relation == "synthetic_usd_fx_swap"
    assert fx_edges[0].weight > 0
    assert fx_edges[0].relation_embedding.shape == (32,)

    # Verify Offshore FX Swap Desk -> US Triparty Repo Pool edge
    targets_fx = sub.adjacency.get("offshore_fx_swap_desk", {})
    assert "us_triparty_repo_pool" in targets_fx
    repo_edges = targets_fx["us_triparty_repo_pool"]
    assert repo_edges[0].relation == "repo_dollar_financing"
    assert repo_edges[0].metadata.get("daily_volume_usd") == 3007e9

    # Verify Triparty Repo Pool <-> Prime MMF Basin bidirectional edges
    targets_repo = sub.adjacency.get("us_triparty_repo_pool", {})
    assert "us_prime_mmf_basin" in targets_repo
    drain_edges = targets_repo["us_prime_mmf_basin"]
    assert drain_edges[0].relation == "repo_liquidity_absorption"

    targets_mmf = sub.adjacency.get("us_prime_mmf_basin", {})
    assert "us_triparty_repo_pool" in targets_mmf
    lending_edges = targets_mmf["us_triparty_repo_pool"]
    assert lending_edges[0].relation == "mmf_cash_repo_lending"

    # Verify US Treasury TGA -> US Triparty Repo Pool edge
    targets_tga = sub.adjacency.get("us_treasury_tga", {})
    assert "us_triparty_repo_pool" in targets_tga
    tga_edges = targets_tga["us_triparty_repo_pool"]
    assert tga_edges[0].relation == "tga_reserve_absorption_drain"


def test_transatlantic_corridor_path_discovery(bridge: ManifoldPGMBridge):
    """Verifies Dual-Frontier A* path discovery from French Treasury to US Prime MMF Basin."""
    res = bridge.materialize_liquidity_path(
        source_id="french_republic_tresor",
        target_id="us_prime_mmf_basin",
    )
    assert res.success is True, f"Failed to materialize transatlantic path: {res}"
    expected_path = [
        "french_republic_tresor",
        "svt_dealers_bnp_socgen",
        "offshore_fx_swap_desk",
        "us_triparty_repo_pool",
        "us_prime_mmf_basin",
    ]
    assert res.path_nodes == expected_path

    expected_relations = [
        "oat_primary_issuance",
        "synthetic_usd_fx_swap",
        "repo_dollar_financing",
        "repo_liquidity_absorption",
    ]
    actual_relations = [e.relation for e in res.path_edges]
    assert actual_relations == expected_relations

    assert res.total_cost > 0.0
    assert res.iterations > 0
    assert res.expanded_nodes > 0

    # Ensure intermediate and sink Dark Forest nodes are admitted to L1 buffer and L2 host graph
    assert "offshore_fx_swap_desk" in bridge.engine.l1_buffer.entity_to_slot
    assert "us_triparty_repo_pool" in bridge.engine.l1_buffer.entity_to_slot
    assert "us_prime_mmf_basin" in bridge.engine.l1_buffer.entity_to_slot
    assert bridge.engine.l2_graph.has_node("offshore_fx_swap_desk")
    assert bridge.engine.l2_graph.has_node("us_triparty_repo_pool")
    assert bridge.engine.l2_graph.has_node("us_prime_mmf_basin")

    # Verify full macroeconomic traversal summary includes transatlantic conduit
    summary = bridge.execute_macro_traversal()
    assert summary["invariants_verified"] is True
    assert summary["invariant_details"]["transatlantic_mmf_reachability"] is True
    assert "transatlantic_dollar_conduit" in summary["paths"]
    assert summary["paths"]["transatlantic_dollar_conduit"]["success"] is True
    assert summary["paths"]["transatlantic_dollar_conduit"]["nodes"] == expected_path


def test_tga_drain_and_oat_haircut_impedance_dynamics(bridge: ManifoldPGMBridge):
    """Verifies that OAT-Bund spread widening and TGA cash drain increase traversal impedance."""
    # 1. Spread widening friction on synthetic USD FX swap
    w_swap_calm = bridge.compute_edge_weight(
        base_weight=1.10,
        flow_volume_eur=70e9,
        risk_friction=0.30,  # +30 bps spread
        is_domestic_retention=False,
    )
    w_swap_stress = bridge.compute_edge_weight(
        base_weight=1.10,
        flow_volume_eur=70e9,
        risk_friction=1.60,  # +160 bps spread
        is_domestic_retention=False,
    )
    assert w_swap_stress > w_swap_calm

    # 2. Daily volume sensitivity on repo financing
    w_repo_huge_vol = bridge.compute_edge_weight(
        base_weight=1.05,
        flow_volume_eur=3007e9,  # $3.007 Trillion SOFR volume
        risk_friction=0.80,
        is_domestic_retention=False,
    )
    w_repo_small_vol = bridge.compute_edge_weight(
        base_weight=1.05,
        flow_volume_eur=50e9,
        risk_friction=0.80,
        is_domestic_retention=False,
    )
    assert w_repo_huge_vol < w_repo_small_vol

    # 3. TGA reserve absorption impedance
    w_tga = bridge.compute_edge_weight(
        base_weight=1.35,
        flow_volume_eur=12.154e9,
        risk_friction=0.80 * 1.8,
        is_domestic_retention=True,
    )
    assert w_tga > 1.35
