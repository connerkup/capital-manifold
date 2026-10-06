"""Unit tests verifying The Global Liquidity Triangle & Cross-Border Spillover Nexus.

Tests:
1. SEC EDGAR Live/Fallback XBRL Ingestion, Japan TIC, and Gulf Petrodollar Harvester.
2. Global Liquidity Triangle Entity & Edge Registration in L3 Substrate.
3. Dual-Frontier A* Multi-Corridor Path Discovery:
   - Transpacific Yen Carry Faucet -> US Triparty Repo -> US Treasury TGA.
   - French Sovereign Stimulus -> Exporters -> Big Tech Vault -> Buyback Burn Chamber.
   - French Trade Bleed -> Exporters -> Gulf Sovereign Wealth Basin -> SVT Dealer Diversification.
4. Yen FX Intervention Shock Simulation & Full Macro Traversal Invariants.
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
from capital_manifold.harvesters.transpacific_corporate import (
    FALLBACK_APPLE_BUYBACKS_USD,
    FALLBACK_APPLE_CASH_USD,
    FALLBACK_APPLE_LIQUID_USD,
    FALLBACK_APPLE_SECURITIES_USD,
    GULF_PETRODOLLAR_RECYCLING_USD,
    JAPAN_TIC_TREASURY_HOLDING_USD,
    TranspacificCorporateHarvester,
)


@pytest.fixture
def harvester() -> TranspacificCorporateHarvester:
    return TranspacificCorporateHarvester()


@pytest.fixture
def bridge() -> ManifoldPGMBridge:
    return ManifoldPGMBridge()


def test_transpacific_corporate_harvester_api_and_fallback(harvester: TranspacificCorporateHarvester):
    """Verifies harvesting and schema normalization of SEC EDGAR facts and TIC/Petrodollar flows."""
    # 1. Apple SEC EDGAR Ingestion
    apple_events, apple_meta = harvester.fetch_apple_sec_edgar()
    assert len(apple_events) == 2
    assert "cik" in apple_meta
    assert apple_meta["cik"] == "0000320193"
    assert "total_liquid_hoard_usd" in apple_meta
    assert "payments_for_repurchase_of_common_stock_usd" in apple_meta

    # Check Apple Liquid Hoard Event
    ev_vault = next(e for e in apple_events if "apple_liquid_vault" in e.event_id)
    assert ev_vault.flow_type == FlowType.POOL_CONCENTRATION
    assert ev_vault.source_entity == "us_prime_mmf_basin"
    assert ev_vault.target_entity == "apple_bigtech_treasury_vault"
    assert ev_vault.nominal_amount >= 50.0e9  # Over $50 Billion liquid hoard
    assert ev_vault.currency == "USD"

    # Check Apple Buyback Burn Event
    ev_burn = next(e for e in apple_events if "apple_buyback_burn" in e.event_id)
    assert ev_burn.flow_type == FlowType.QT_BURN
    assert ev_burn.source_entity == "apple_bigtech_treasury_vault"
    assert ev_burn.target_entity == "corporate_share_buyback_burn_chamber"
    assert ev_burn.nominal_amount >= 50.0e9  # Over $50 Billion equity retirement
    assert ev_burn.currency == "USD"

    # 2. Japan TIC & Gulf Petrodollar Flows
    global_events, global_meta = harvester.fetch_japan_tic_and_petrodollar()
    assert len(global_events) == 2
    assert global_meta["japan_tic_treasury_holding_usd"] == JAPAN_TIC_TREASURY_HOLDING_USD
    assert global_meta["gulf_petrodollar_recycling_usd"] == GULF_PETRODOLLAR_RECYCLING_USD

    ev_japan = next(e for e in global_events if "japan_tic" in e.event_id)
    assert ev_japan.source_entity == "japan_mof_boj_carry_faucet"
    assert ev_japan.target_entity == "us_treasuries_custody"
    assert ev_japan.nominal_amount == JAPAN_TIC_TREASURY_HOLDING_USD
    assert ev_japan.nominal_amount > 1.0e12  # Over $1.1 Trillion

    ev_petro = next(e for e in global_events if "gulf_petrodollar" in e.event_id)
    assert ev_petro.source_entity == "foreign_export_economies"
    assert ev_petro.target_entity == "gulf_petrodollar_sovereign_wealth_basin"
    assert ev_petro.nominal_amount == GULF_PETRODOLLAR_RECYCLING_USD

    # 3. Network Outage Fallback Verification
    mock_client = MagicMock()
    mock_client.get.side_effect = Exception("Simulated SEC EDGAR downtime")
    harvester.client = mock_client

    fb_events, fb_meta = harvester.fetch_apple_sec_edgar()
    assert len(fb_events) == 2
    assert fb_meta["cash_and_cash_equivalents_usd"] == FALLBACK_APPLE_CASH_USD
    assert fb_meta["marketable_securities_current_usd"] == FALLBACK_APPLE_SECURITIES_USD
    assert fb_meta["total_liquid_hoard_usd"] == FALLBACK_APPLE_LIQUID_USD
    assert fb_meta["payments_for_repurchase_of_common_stock_usd"] == FALLBACK_APPLE_BUYBACKS_USD


def test_global_triangle_node_registration(bridge: ManifoldPGMBridge):
    """Verifies that all 5 Global Triangle nodes and transmission edges exist with valid embeddings."""
    sub = bridge.substrate
    triangle_nodes = [
        "japan_mof_boj_carry_faucet",
        "japan_institutional_carry_desk",
        "apple_bigtech_treasury_vault",
        "corporate_share_buyback_burn_chamber",
        "gulf_petrodollar_sovereign_wealth_basin",
    ]

    for nid in triangle_nodes:
        node = sub.get_entity(nid)
        assert node is not None, f"Global Triangle node {nid} missing from substrate"
        assert node.embedding.shape == (128,), f"Global Triangle node {nid} invalid shape"
        norm = np.linalg.norm(node.embedding)
        assert norm == pytest.approx(1.0, abs=1e-5), f"Global Triangle node {nid} not unit normalized"
        assert nid in FINANCIAL_ENTITIES
        assert node.metadata.get("sector") == FINANCIAL_ENTITIES[nid]["sector"]

    # Verify Global Triangle Relations and Dimensions (d=32)
    triangle_relations = [
        ("japan_mof_boj_carry_faucet", "japan_institutional_carry_desk", "jpy_zero_interest_liquidity_provision"),
        ("japan_institutional_carry_desk", "us_triparty_repo_pool", "yen_carry_dollar_treasury_absorption"),
        ("us_prime_mmf_basin", "apple_bigtech_treasury_vault", "corporate_commercial_paper_and_t_bill_placement"),
        ("foreign_export_economies", "apple_bigtech_treasury_vault", "global_enterprise_tech_inflow"),
        ("apple_bigtech_treasury_vault", "corporate_share_buyback_burn_chamber", "equity_share_retirement_buyback_burn"),
        ("foreign_export_economies", "gulf_petrodollar_sovereign_wealth_basin", "petrodollar_energy_surplus_accumulation"),
        ("gulf_petrodollar_sovereign_wealth_basin", "svt_dealers_bnp_socgen", "sovereign_wealth_oat_diversification"),
    ]

    for src_id, tgt_id, rel_name in triangle_relations:
        targets = sub.adjacency.get(src_id, {})
        assert tgt_id in targets, f"Missing edge {src_id} -> {tgt_id}"
        edge_list = targets[tgt_id]
        matching = [e for e in edge_list if e.relation == rel_name]
        assert len(matching) >= 1, f"Missing relation {rel_name} on {src_id} -> {tgt_id}"
        edge = matching[0]
        assert edge.weight > 0.0
        assert edge.relation_embedding is not None
        assert edge.relation_embedding.shape == (32,)


def test_dual_frontier_a_star_global_triangle_traversals(bridge: ManifoldPGMBridge):
    """Verifies Dual-Frontier A* path discovery across all 3 Global Liquidity Triangle transmission corridors."""
    # Corridor 1: Transpacific Yen Carry Corridor -> US Treasury TGA
    res1 = bridge.materialize_liquidity_path(
        source_id="japan_mof_boj_carry_faucet",
        target_id="us_treasury_tga",
    )
    assert res1.success is True
    assert res1.path_nodes == [
        "japan_mof_boj_carry_faucet",
        "japan_institutional_carry_desk",
        "us_triparty_repo_pool",
        "us_treasury_tga",
    ]
    assert [e.relation for e in res1.path_edges] == [
        "jpy_zero_interest_liquidity_provision",
        "yen_carry_dollar_treasury_absorption",
        "tga_debt_issuance_absorption",
    ]
    assert res1.total_cost > 0.0
    assert res1.iterations > 0

    # Corridor 2: French Sovereign Stimulus -> Big Tech Vault -> Buyback Burn Chamber
    res2 = bridge.materialize_liquidity_path(
        source_id="french_republic_tresor",
        target_id="corporate_share_buyback_burn_chamber",
    )
    assert res2.success is True
    assert res2.path_nodes == [
        "french_republic_tresor",
        "french_economy_importers",
        "foreign_export_economies",
        "apple_bigtech_treasury_vault",
        "corporate_share_buyback_burn_chamber",
    ]
    assert [e.relation for e in res2.path_edges] == [
        "fiscal_stimulus_import_demand",
        "trade_deficit_drain",
        "global_enterprise_tech_inflow",
        "equity_share_retirement_buyback_burn",
    ]
    assert res2.total_cost > 0.0

    # Corridor 3: French Trade Bleed -> Gulf Sovereign Wealth Basin
    res3 = bridge.materialize_liquidity_path(
        source_id="french_republic_tresor",
        target_id="gulf_petrodollar_sovereign_wealth_basin",
    )
    assert res3.success is True
    assert res3.path_nodes == [
        "french_republic_tresor",
        "french_economy_importers",
        "foreign_export_economies",
        "gulf_petrodollar_sovereign_wealth_basin",
    ]
    assert [e.relation for e in res3.path_edges] == [
        "fiscal_stimulus_import_demand",
        "trade_deficit_drain",
        "petrodollar_energy_surplus_accumulation",
    ]
    assert res3.total_cost > 0.0

    # Direct 1-hop Petrodollar Reinvestment into SVT Primary Dealers
    res_recycle = bridge.materialize_liquidity_path(
        source_id="gulf_petrodollar_sovereign_wealth_basin",
        target_id="svt_dealers_bnp_socgen",
    )
    assert res_recycle.success is True
    assert res_recycle.path_nodes == [
        "gulf_petrodollar_sovereign_wealth_basin",
        "svt_dealers_bnp_socgen",
    ]
    assert [e.relation for e in res_recycle.path_edges] == [
        "sovereign_wealth_oat_diversification",
    ]


def test_yen_shock_and_full_traversal_invariants(bridge: ManifoldPGMBridge):
    """Verifies full macroeconomic traversal summary and Yen FX Intervention shock dynamics."""
    summary = bridge.execute_macro_traversal()
    assert summary["invariants_verified"] is True
    assert summary["invariant_details"]["transpacific_carry_reachability"] is True
    assert summary["invariant_details"]["corporate_buyback_reachability"] is True
    assert summary["invariant_details"]["petrodollar_reachability"] is True

    paths = summary["paths"]
    assert "transpacific_yen_carry" in paths
    assert paths["transpacific_yen_carry"]["success"] is True
    assert "corporate_share_buyback_burn" in paths
    assert paths["corporate_share_buyback_burn"]["success"] is True
    assert "petrodollar_recycling_loop" in paths
    assert paths["petrodollar_recycling_loop"]["success"] is True

    # Sensitivity dynamics under Yen FX Intervention shock
    # Baseline vs $50B FX Intervention:
    # When BoJ/MoF intervenes to defend yen, carry trade volume contracts and friction spikes.
    w_carry_calm = bridge.compute_edge_weight(
        base_weight=1.05,
        flow_volume_eur=800.0e9,
        risk_friction=0.10,
        is_domestic_retention=False,
    )
    w_carry_shock = bridge.compute_edge_weight(
        base_weight=1.05,
        flow_volume_eur=750.0e9,
        risk_friction=1.20,
        is_domestic_retention=False,
    )
    assert w_carry_shock > w_carry_calm, "Yen FX intervention shock must increase carry transmission impedance"

    # SVT Dealer funding cost under cross-market contagion
    w_svt_calm = bridge.compute_edge_weight(
        base_weight=1.10,
        flow_volume_eur=40.0e9,
        risk_friction=0.815 * 1.5,
        is_domestic_retention=False,
    )
    w_svt_shock = bridge.compute_edge_weight(
        base_weight=1.10,
        flow_volume_eur=40.0e9,
        risk_friction=1.75 * 1.5,
        is_domestic_retention=False,
    )
    assert w_svt_shock > w_svt_calm, "Cross-market OAT spread widening must increase SVT dealer funding impedance"
