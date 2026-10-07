"""Unit tests verifying The Complete Planetary Monetary Manifold (7 Global Regions).

Tests:
1. Statutory Planetary Flow Ingestion across 7 global macro regions.
2. Planetary Node & Edge Registration in L3 Substrate (unit norm d=128, relations d=32).
3. Dual-Frontier A* Multi-Corridor Path Discovery:
   - Petro-Yuan Sino-Gulf Bilateral Energy Corridor.
   - Shadow Maritime Tanker Russian Crude Refining Loop (evading G7 price caps).
   - Pacific Hardware & Commodity Loop (Australia -> China -> Taiwan TSMC -> Apple Buyback).
   - African Mineral Debt Servicing & UAE Sovereign Wealth Placement.
4. Global De-Dollarization Shock Simulation & Full Macro Traversal Invariants.
"""

import numpy as np
import pytest

from capital_manifold.bridge.pgm_adapter import (
    FINANCIAL_ENTITIES,
    ManifoldPGMBridge,
    MonetaryTier,
)
from capital_manifold.core.schema import FlowEvent, FlowType
from capital_manifold.harvesters.planetary_macro import (
    AFRICA_MINERALS_DEBT_CONDUIT_USD,
    AUSTRALIA_COMMODITY_FAUCET_USD,
    BRAZIL_AGRI_EXPORT_SURPLUS_USD,
    CBR_PHYSICAL_GOLD_VAULT_USD,
    CBR_YUAN_RESERVES_USD,
    EUROCLEAR_FROZEN_RUSSIAN_ASSETS_USD,
    HONG_KONG_CNH_TURNOVER_USD,
    INDIA_RUSSIAN_CRUDE_REFINING_USD,
    PBOC_SAFE_RESERVES_USD,
    PETRO_YUAN_ENERGY_SETTLEMENT_USD,
    SAUDI_SAMA_PIF_ASSETS_USD,
    SHADOW_TANKER_CRUDE_ARBITRAGE_USD,
    TAIWAN_TSMC_HARDWARE_FLOW_USD,
    TIC_BRAZIL_TREASURIES_USD,
    TIC_CHINA_TREASURIES_USD,
    TIC_INDIA_TREASURIES_USD,
    TIC_TAIWAN_TREASURIES_USD,
    UAE_ADIA_MUBADALA_USD,
    PlanetaryMacroHarvester,
)


@pytest.fixture
def harvester() -> PlanetaryMacroHarvester:
    return PlanetaryMacroHarvester()


@pytest.fixture
def bridge() -> ManifoldPGMBridge:
    return ManifoldPGMBridge()


def test_planetary_macro_harvester_ingestion(harvester: PlanetaryMacroHarvester):
    """Verifies statutory flow ingestion across all planetary macro jurisdictions (8 dark forest + Eurasia)."""
    events = harvester.harvest()
    assert len(events) == 48

    # 1. China & East Asia
    ev_china = next(e for e in events if "planetary_tic_pboc" in e.event_id)
    assert ev_china.nominal_amount == TIC_CHINA_TREASURIES_USD
    assert ev_china.source_entity == "pboc_safe_foreign_reserves"
    assert ev_china.target_entity == "us_treasuries_custody"

    ev_taiwan = next(e for e in events if "taiwan_tsmc_hardware" in e.event_id)
    assert ev_taiwan.nominal_amount == TAIWAN_TSMC_HARDWARE_FLOW_USD
    assert ev_taiwan.target_entity == "apple_bigtech_treasury_vault"

    # 2. Middle East & Petro-Yuan
    ev_py = next(e for e in events if "petro_yuan_energy" in e.event_id)
    assert ev_py.nominal_amount == PETRO_YUAN_ENERGY_SETTLEMENT_USD
    assert ev_py.source_entity == "saudi_sama_pif_nexus"
    assert ev_py.target_entity == "petro_yuan_bilateral_settlement_bridge"

    ev_uae = next(e for e in events if "uae_sovereign_wealth" in e.event_id)
    assert ev_uae.nominal_amount == UAE_ADIA_MUBADALA_USD
    assert ev_uae.target_entity == "uae_adia_mubadala_basin"

    # 3. Russia & Euroclear
    ev_frozen = next(e for e in events if "euroclear_frozen" in e.event_id)
    assert ev_frozen.nominal_amount == EUROCLEAR_FROZEN_RUSSIAN_ASSETS_USD
    assert ev_frozen.flow_type == FlowType.POOL_CONCENTRATION

    ev_gold = next(e for e in events if "cbr_gold_vault" in e.event_id)
    assert ev_gold.nominal_amount == CBR_PHYSICAL_GOLD_VAULT_USD

    ev_tanker = next(e for e in events if "shadow_tanker_crude" in e.event_id)
    assert ev_tanker.nominal_amount == SHADOW_TANKER_CRUDE_ARBITRAGE_USD

    # 4. India Refining Arbitrage
    ev_india = next(e for e in events if "india_refining_arbitrage" in e.event_id)
    assert ev_india.nominal_amount == INDIA_RUSSIAN_CRUDE_REFINING_USD
    assert ev_india.source_entity == "shadow_tanker_energy_arbitrage"
    assert ev_india.target_entity == "reserve_bank_of_india_refining_hub"

    # 5. Australia & Brazil Resources
    ev_aus = next(e for e in events if "australia_commodity" in e.event_id)
    assert ev_aus.nominal_amount == AUSTRALIA_COMMODITY_FAUCET_USD

    ev_br = next(e for e in events if "brazil_agri" in e.event_id)
    assert ev_br.nominal_amount == BRAZIL_AGRI_EXPORT_SURPLUS_USD

    # 6. Africa Minerals
    ev_afr = next(e for e in events if "africa_minerals" in e.event_id)
    assert ev_afr.nominal_amount == AFRICA_MINERALS_DEBT_CONDUIT_USD

    # 7. Dark Forest Regions Ingestion Assertions
    ev_norway = next(e for e in events if "norway_gpfg_global_allocation" in e.event_id)
    assert ev_norway.nominal_amount == 1750.0e9

    ev_snb = next(e for e in events if "snb_gsib_reserve_transmission" in e.event_id)
    assert ev_snb.nominal_amount == 500.0e9

    ev_mas = next(e for e in events if "mas_official_reserve_transfer" in e.event_id)
    assert ev_mas.nominal_amount == 400.0e9

    ev_bok = next(e for e in events if "bok_nps_fx_swap" in e.event_id)
    assert ev_bok.nominal_amount == 300.0e9

    ev_gilt = next(e for e in events if "uk_dmo_gilt_issuance" in e.event_id)
    assert ev_gilt.nominal_amount == 2600.0e9

    ev_maple = next(e for e in events if "boc_maple_pension_liquidity" in e.event_id)
    assert ev_maple.nominal_amount == 1500.0e9

    ev_mx = next(e for e in events if "banxico_nearshoring_facility" in e.event_id)
    assert ev_mx.nominal_amount == 500.0e9

    ev_sdr = next(e for e in events if "imf_sdr_bis_allocation" in e.event_id)
    assert ev_sdr.nominal_amount == 450.0e9

    ev_nwf = next(e for e in events if "nwf_oil_buffer_injection" in e.event_id)
    assert ev_nwf.nominal_amount == 155.0e9


def test_planetary_node_and_edge_registration(bridge: ManifoldPGMBridge):
    """Verifies that all Planetary Manifold and Dark Forest nodes and transmission relations exist with valid embeddings."""
    sub = bridge.substrate
    planetary_nodes = [
        # Original 13 planetary nodes
        "pboc_safe_foreign_reserves",
        "chinese_state_banks_fx_desk",
        "offshore_cnh_hong_kong_hub",
        "taiwan_central_bank_tsmc_semiconductor_sink",
        "saudi_sama_pif_nexus",
        "uae_adia_mubadala_basin",
        "petro_yuan_bilateral_settlement_bridge",
        "bank_of_russia_cbr_vault",
        "shadow_tanker_energy_arbitrage",
        "brazil_banco_central_agri_faucet",
        "reserve_bank_of_australia_commodity_faucet",
        "reserve_bank_of_india_refining_hub",
        "africa_critical_minerals_debt_conduit",
        # 16 Dark Forest entities
        "norway_norges_bank_gpfg_faucet",
        "norway_gpfg_global_equity_sink",
        "swiss_national_bank_snb_vault",
        "ubs_group_consolidated_gsib",
        "singapore_mas_reserve_faucet",
        "singapore_gic_temasek_sovereign_basin",
        "bank_of_korea_bok_vault",
        "korea_national_pension_service_nps",
        "bank_of_england_boe_vault",
        "uk_dmo_gilt_debt_market",
        "bank_of_canada_boc_vault",
        "canada_maple_pension_consortium",
        "banco_de_mexico_banxico_faucet",
        "usmca_nearshoring_trade_conduit",
        "imf_special_drawing_rights_sdr_pool",
        "bis_basel_banking_department",
        # 4 Eurasian upgrade entities
        "russia_national_wealth_fund_nwf",
        "russian_state_banking_credit_nexus",
        "gazprombank_energy_settlement_hub",
        "russia_offshore_shadow_capital_basin",
    ]

    for nid in planetary_nodes:
        node = sub.get_entity(nid)
        assert node is not None, f"Planetary node {nid} missing from substrate"
        assert node.embedding.shape == (128,), f"Planetary node {nid} invalid shape"
        norm = np.linalg.norm(node.embedding)
        assert norm == pytest.approx(1.0, abs=1e-5), f"Planetary node {nid} not unit normalized"
        assert nid in FINANCIAL_ENTITIES
        assert node.metadata.get("sector") == FINANCIAL_ENTITIES[nid]["sector"]

    # Verify Planetary Relations and Dimensions (d=32)
    planetary_relations = [
        ("saudi_sama_pif_nexus", "petro_yuan_bilateral_settlement_bridge", "petro_yuan_crude_invoicing"),
        ("petro_yuan_bilateral_settlement_bridge", "offshore_cnh_hong_kong_hub", "cnh_cross_border_liquidity_settlement"),
        ("offshore_cnh_hong_kong_hub", "chinese_state_banks_fx_desk", "onshore_offshore_cnh_repatriation"),
        ("chinese_state_banks_fx_desk", "pboc_safe_foreign_reserves", "sovereign_fx_reserve_accumulation"),
        ("petro_yuan_bilateral_settlement_bridge", "chinese_state_banks_fx_desk", "direct_petro_yuan_clearing"),
        ("bank_of_russia_cbr_vault", "shadow_tanker_energy_arbitrage", "shadow_tanker_crude_export"),
        ("shadow_tanker_energy_arbitrage", "reserve_bank_of_india_refining_hub", "discounted_crude_refining_intake"),
        ("reserve_bank_of_india_refining_hub", "french_economy_importers", "refined_diesel_european_reexport"),
        ("reserve_bank_of_australia_commodity_faucet", "chinese_state_banks_fx_desk", "australian_iron_ore_lng_settlement"),
        ("brazil_banco_central_agri_faucet", "chinese_state_banks_fx_desk", "brazilian_agri_resource_settlement"),
        ("chinese_state_banks_fx_desk", "taiwan_central_bank_tsmc_semiconductor_sink", "cross_strait_electronics_demand"),
        ("taiwan_central_bank_tsmc_semiconductor_sink", "apple_bigtech_treasury_vault", "advanced_semiconductor_hardware_shipment"),
        ("africa_critical_minerals_debt_conduit", "chinese_state_banks_fx_desk", "resource_concession_debt_servicing"),
        ("pboc_safe_foreign_reserves", "africa_critical_minerals_debt_conduit", "belt_and_road_infrastructure_lending"),
        ("uae_adia_mubadala_basin", "svt_dealers_bnp_socgen", "gulf_sovereign_euro_debt_placement"),
        ("saudi_sama_pif_nexus", "svt_dealers_bnp_socgen", "saudi_capital_diversification_oat"),
        ("bank_of_russia_cbr_vault", "eurosystem_target2_pool", "immobilized_euroclear_reserve_claim"),
    ]

    for src_id, tgt_id, rel_name in planetary_relations:
        targets = sub.adjacency.get(src_id, {})
        assert tgt_id in targets, f"Missing edge {src_id} -> {tgt_id}"
        edge_list = targets[tgt_id]
        matching = [e for e in edge_list if e.relation == rel_name]
        assert len(matching) >= 1, f"Missing relation {rel_name} on {src_id} -> {tgt_id}"
        edge = matching[0]
        assert edge.weight > 0.0
        assert edge.relation_embedding is not None
        assert edge.relation_embedding.shape == (32,)


def test_dual_frontier_a_star_planetary_traversals(bridge: ManifoldPGMBridge):
    """Verifies Dual-Frontier A* path discovery across all 3 major Planetary Monetary Manifold corridors."""
    # Corridor 1: The Petro-Yuan Sino-Gulf Corridor
    res1 = bridge.materialize_liquidity_path(
        source_id="saudi_sama_pif_nexus",
        target_id="pboc_safe_foreign_reserves",
    )
    assert res1.success is True
    assert res1.path_nodes == [
        "saudi_sama_pif_nexus",
        "petro_yuan_bilateral_settlement_bridge",
        "chinese_state_banks_fx_desk",
        "pboc_safe_foreign_reserves",
    ]
    assert [e.relation for e in res1.path_edges] == [
        "petro_yuan_crude_invoicing",
        "direct_petro_yuan_clearing",
        "sovereign_fx_reserve_accumulation",
    ]
    assert res1.total_cost > 0.0
    assert res1.iterations > 0

    # Corridor 2: The Shadow Energy Refining Loop (Sanctions Arbitrage)
    res2 = bridge.materialize_liquidity_path(
        source_id="bank_of_russia_cbr_vault",
        target_id="french_economy_importers",
    )
    assert res2.success is True
    assert res2.path_nodes == [
        "bank_of_russia_cbr_vault",
        "shadow_tanker_energy_arbitrage",
        "reserve_bank_of_india_refining_hub",
        "french_economy_importers",
    ]
    assert [e.relation for e in res2.path_edges] == [
        "shadow_tanker_crude_export",
        "discounted_crude_refining_intake",
        "refined_diesel_european_reexport",
    ]
    assert res2.total_cost > 0.0

    # Corridor 3: The Pacific Hardware & Commodity Loop
    res3 = bridge.materialize_liquidity_path(
        source_id="reserve_bank_of_australia_commodity_faucet",
        target_id="corporate_share_buyback_burn_chamber",
    )
    assert res3.success is True
    assert res3.path_nodes == [
        "reserve_bank_of_australia_commodity_faucet",
        "chinese_state_banks_fx_desk",
        "taiwan_central_bank_tsmc_semiconductor_sink",
        "apple_bigtech_treasury_vault",
        "corporate_share_buyback_burn_chamber",
    ]
    assert [e.relation for e in res3.path_edges] == [
        "australian_iron_ore_lng_settlement",
        "cross_strait_electronics_demand",
        "advanced_semiconductor_hardware_shipment",
        "equity_share_retirement_buyback_burn",
    ]
    assert res3.total_cost > 0.0

    # Direct 1-hop: Petro-Yuan Bridge -> Offshore CNH Hong Kong Hub
    res_cnh = bridge.materialize_liquidity_path(
        source_id="petro_yuan_bilateral_settlement_bridge",
        target_id="offshore_cnh_hong_kong_hub",
    )
    assert res_cnh.success is True
    assert res_cnh.path_nodes == ["petro_yuan_bilateral_settlement_bridge", "offshore_cnh_hong_kong_hub"]

    # Direct 1-hop: UAE Wealth -> SVT Primary Dealers
    res_uae = bridge.materialize_liquidity_path(
        source_id="uae_adia_mubadala_basin",
        target_id="svt_dealers_bnp_socgen",
    )
    assert res_uae.success is True
    assert res_uae.path_nodes == ["uae_adia_mubadala_basin", "svt_dealers_bnp_socgen"]

    # Direct 1-hop: Africa Concession -> Chinese State Banks
    res_afr = bridge.materialize_liquidity_path(
        source_id="africa_critical_minerals_debt_conduit",
        target_id="chinese_state_banks_fx_desk",
    )
    assert res_afr.success is True
    assert res_afr.path_nodes == ["africa_critical_minerals_debt_conduit", "chinese_state_banks_fx_desk"]


def test_dedollarization_simulation_and_full_traversal_invariants(bridge: ManifoldPGMBridge):
    """Verifies full macroeconomic traversal summary and 20% De-Dollarization shock dynamics."""
    summary = bridge.execute_macro_traversal()
    assert summary["invariants_verified"] is True
    assert summary["invariant_details"]["petro_yuan_sino_gulf_reachability"] is True
    assert summary["invariant_details"]["shadow_energy_refining_reachability"] is True
    assert summary["invariant_details"]["pacific_hardware_commodity_reachability"] is True

    paths = summary["paths"]
    assert "petro_yuan_sino_gulf" in paths
    assert paths["petro_yuan_sino_gulf"]["success"] is True
    assert "shadow_energy_refining_loop" in paths
    assert paths["shadow_energy_refining_loop"]["success"] is True
    assert "pacific_hardware_commodity_loop" in paths
    assert paths["pacific_hardware_commodity_loop"]["success"] is True

    # De-Dollarization Sensitivity Dynamics
    # When 20% of commodity trades shift from USD to bilateral Petro-Yuan:
    # 1. US Triparty Repo volume contracts ($3,007B -> $2,405B) and friction rises
    w_repo_calm = bridge.compute_edge_weight(
        base_weight=1.05,
        flow_volume_eur=3007.0e9,
        risk_friction=0.05,
        is_domestic_retention=False,
    )
    w_repo_shock = bridge.compute_edge_weight(
        base_weight=1.05,
        flow_volume_eur=2405.0e9,
        risk_friction=0.45,
        is_domestic_retention=False,
    )
    assert w_repo_shock > w_repo_calm, "Commodity de-dollarization must increase US repo financing impedance"

    # 2. European SVT Dealer funding faces wider spread friction
    w_svt_calm = bridge.compute_edge_weight(
        base_weight=1.10,
        flow_volume_eur=40.0e9,
        risk_friction=(81.5 / 100.0) * 1.5,
        is_domestic_retention=False,
    )
    w_svt_shock = bridge.compute_edge_weight(
        base_weight=1.10,
        flow_volume_eur=40.0e9,
        risk_friction=(135.0 / 100.0) * 1.5,
        is_domestic_retention=False,
    )
    assert w_svt_shock > w_svt_calm, "De-dollarization contagion must widen European SVT funding spread"

    # 3. Petro-Yuan bilateral clearing volume doubles ($65B -> $130B) and friction falls
    w_py_calm = bridge.compute_edge_weight(
        base_weight=0.90,
        flow_volume_eur=65.0e9,
        risk_friction=0.15,
        is_domestic_retention=False,
    )
    w_py_expanded = bridge.compute_edge_weight(
        base_weight=0.90,
        flow_volume_eur=130.0e9,
        risk_friction=0.08,
        is_domestic_retention=False,
    )
    assert w_py_expanded < w_py_calm, "Expanding Petro-Yuan clearing must lower transmission impedance"
