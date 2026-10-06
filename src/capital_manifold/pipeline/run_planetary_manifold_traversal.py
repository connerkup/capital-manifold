"""Planetary Monetary Manifold Traversal & Global De-Dollarization Simulation.

Traces:
[1] The Petro-Yuan Sino-Gulf Corridor:
    Saudi Energy (SAMA/PIF) -> Petro-Yuan Bridge -> Chinese State Banks -> PBOC SAFE Reserve Vault.
[2] The Shadow Energy Refining Loop:
    Bank of Russia (CBR) -> Shadow Tanker Fleet -> India Jamnagar Refining Hub -> French Economy Importers (evading G7 maritime price caps).
[3] The Pacific Hardware & Commodity Loop:
    Australia Resources (RBA) -> Chinese Industrial Banks -> Taiwan TSMC -> Apple Big Tech Vault -> Buyback Burn Chamber.
[4] Global De-Dollarization Simulation:
    Model a 20% shift in global crude and raw material pricing from USD to bilateral Petro-Yuan/Gold,
    measuring the resulting liquidity drain on US Triparty Repo and European SVT primary dealers.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Add src to pythonpath
src_dir = Path(__file__).resolve().parent.parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from capital_manifold.bridge.pgm_adapter import ManifoldPGMBridge
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

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("run_planetary_manifold_traversal")


def main() -> None:
    print("=" * 110)
    print("  CAPITAL MANIFOLD: THE COMPLETE PLANETARY MONETARY MANIFOLD")
    print("  7 Global Regions, Parallel Shadow Circuits & Global De-Dollarization Dynamics")
    print("=" * 110)

    # 1. Harvest & Display Telemetry across 7 Global Regions
    print("\n" + "-" * 110)
    print(" 1. STATUTORY PLANETARY HARVEST TELEMETRY (7 GLOBAL REGIONS)")
    print("-" * 110)

    with PlanetaryMacroHarvester() as harvester:
        all_events = harvester.harvest_and_store()

    print(f" * Harvested {len(all_events)} planetary flow events across all 7 macro jurisdictions:")
    print(f"   [1] China & East Asia:")
    print(f"         -> PBOC / SAFE Foreign Reserves:      ${PBOC_SAFE_RESERVES_USD / 1e12:.3f} Trillion (Global reserve anchor)")
    print(f"         -> TIC US Treasury Holdings:          ${TIC_CHINA_TREASURIES_USD / 1e9:,.1f} Billion (#2 foreign creditor)")
    print(f"         -> Hong Kong CNH Clearing Hub:         ${HONG_KONG_CNH_TURNOVER_USD / 1e9:,.1f} Billion / day turnover")
    print(f"         -> Taiwan TSMC Semiconductor Hardware: ${TAIWAN_TSMC_HARDWARE_FLOW_USD / 1e9:,.1f} Billion + ${TIC_TAIWAN_TREASURIES_USD / 1e9:,.1f}B TIC")
    print(f"   [2] Middle East & Gulf:")
    print(f"         -> Saudi SAMA Central Bank & PIF:     ${SAUDI_SAMA_PIF_ASSETS_USD / 1e9:,.1f} Billion sovereign wealth pool")
    print(f"         -> UAE ADIA & Mubadala Basin:         ${UAE_ADIA_MUBADALA_USD / 1e12:.3f} Trillion global assets")
    print(f"         -> Petro-Yuan Bilateral Energy Bridge: ${PETRO_YUAN_ENERGY_SETTLEMENT_USD / 1e9:,.1f} Billion / year non-USD settlement")
    print(f"   [3] Russia & Sanctioned Shadow Circuit:")
    print(f"         -> Euroclear Belgium Frozen Reserves: ${EUROCLEAR_FROZEN_RUSSIAN_ASSETS_USD / 1e9:,.1f} Billion (€210B immobilized)")
    print(f"         -> CBR Physical Gold Vault Pivot:     ${CBR_PHYSICAL_GOLD_VAULT_USD / 1e9:,.1f} Billion (2,332 metric tons)")
    print(f"         -> CBR Renminbi / CNY Reserves:       ${CBR_YUAN_RESERVES_USD / 1e9:,.1f} Billion liquid reserve pivot")
    print(f"         -> Shadow Tanker Seaborne Crude:      ${SHADOW_TANKER_CRUDE_ARBITRAGE_USD / 1e9:,.1f} Billion (evading G7 price cap)")
    print(f"   [4] Latin America / South America:")
    print(f"         -> Brazil BCB TIC US Treasuries:      ${TIC_BRAZIL_TREASURIES_USD / 1e9:,.1f} Billion")
    print(f"         -> Brazil Agri/Mineral Export Faucet: ${BRAZIL_AGRI_EXPORT_SURPLUS_USD / 1e9:,.1f} Billion surplus to Asia/Europe")
    print(f"   [5] Australia & Pacific Raw Materials:")
    print(f"         -> RBA Pacific Commodity Faucet:      ${AUSTRALIA_COMMODITY_FAUCET_USD / 1e9:,.1f} Billion (Iron ore, LNG, Met coal)")
    print(f"   [6] India & South Asia:")
    print(f"         -> RBI TIC US Treasuries:             ${TIC_INDIA_TREASURIES_USD / 1e9:,.1f} Billion")
    print(f"         -> Russian Crude Refining Arbitrage:  ${INDIA_RUSSIAN_CRUDE_REFINING_USD / 1e9:,.1f} Billion re-exported to Europe")
    print(f"   [7] Africa & Frontier Resources:")
    print(f"         -> Critical Minerals & Debt Conduit:  ${AFRICA_MINERALS_DEBT_CONDUIT_USD / 1e9:,.1f} Billion cobalt/copper debt service")

    # 2. Structural Analysis of the Parallel Shadow Circuit
    print("\n" + "-" * 110)
    print(" 2. STRUCTURAL ARCHITECTURE OF THE PARALLEL SHADOW CIRCUIT")
    print("-" * 110)
    print(" * The Petro-Yuan Bilateral Clearing Bridge:")
    print("     Gulf energy producers (Saudi Aramco / PIF) increasingly invoice crude deliveries to China directly")
    print("     in Renminbi (CNH) through the Shanghai Petroleum and Natural Gas Exchange. This completely bypasses")
    print("     New York Fedwire and SWIFT, settling directly through the PBOC's CIPS network into Chinese state banks.")
    print(" * The Shadow Maritime Energy Arbitrage Loop:")
    print("     Immobilization of $300B in Russian central bank reserves catalyzed a parallel maritime logistics loop:")
    print("     Urals crude is transported on 600+ dark fleet shadow tankers without Western maritime insurance,")
    print("     delivered to Indian coastal refineries (Jamnagar/Nayara) at discounted pricing, refined into diesel")
    print("     and jet fuel, and re-exported into European importers (including France) legally under transformed origin rules.")
    print(" * The Pacific Hardware & Commodity Loop:")
    print("     Australian iron ore and Brazilian resources feed Chinese industrial fabrication; Taiwan TSMC supplies")
    print("     monopolistic 3nm advanced silicon to Apple; Apple harvests enterprise cash hoards and executes share")
    print("     buybacks, creating a planetary circuit connecting Pacific mines to corporate capital retirement.")

    # 3. Non-Greedy Dual-Frontier A* Multi-Corridor Traversals
    print("\n" + "-" * 110)
    print(" 3. NON-GREEDY DUAL-FRONTIER A* PATH DISCOVERY (PLANETARY CORRIDORS)")
    print("-" * 110)

    bridge = ManifoldPGMBridge()

    # Corridor 1: Petro-Yuan Sino-Gulf Corridor
    res1 = bridge.materialize_liquidity_path(
        source_id="saudi_sama_pif_nexus",
        target_id="pboc_safe_foreign_reserves",
    )
    print(f" [CORRIDOR 1] The Petro-Yuan Sino-Gulf Corridor:")
    print(f"   * Status:        {'[SUCCESS]' if res1.success else '[FAILED]'}")
    print(f"   * Traversal:     {' -> '.join(res1.path_nodes)}")
    print(f"   * Transmission:  {' -> '.join(e.relation for e in res1.path_edges)}")
    print(f"   * Traversal Cost: {res1.total_cost:.4f} ({res1.iterations} iterations, {res1.expanded_nodes} nodes expanded)")

    # Corridor 2: Shadow Energy Refining Loop
    res2 = bridge.materialize_liquidity_path(
        source_id="bank_of_russia_cbr_vault",
        target_id="french_economy_importers",
    )
    print(f"\n [CORRIDOR 2] The Shadow Energy Refining Loop (Sanctions Arbitrage):")
    print(f"   * Status:        {'[SUCCESS]' if res2.success else '[FAILED]'}")
    print(f"   * Traversal:     {' -> '.join(res2.path_nodes)}")
    print(f"   * Transmission:  {' -> '.join(e.relation for e in res2.path_edges)}")
    print(f"   * Traversal Cost: {res2.total_cost:.4f} ({res2.iterations} iterations, {res2.expanded_nodes} nodes expanded)")

    # Corridor 3: Pacific Hardware & Commodity Loop
    res3 = bridge.materialize_liquidity_path(
        source_id="reserve_bank_of_australia_commodity_faucet",
        target_id="corporate_share_buyback_burn_chamber",
    )
    print(f"\n [CORRIDOR 3] The Pacific Hardware & Commodity Loop:")
    print(f"   * Status:        {'[SUCCESS]' if res3.success else '[FAILED]'}")
    print(f"   * Traversal:     {' -> '.join(res3.path_nodes)}")
    print(f"   * Transmission:  {' -> '.join(e.relation for e in res3.path_edges)}")
    print(f"   * Traversal Cost: {res3.total_cost:.4f} ({res3.iterations} iterations, {res3.expanded_nodes} nodes expanded)")

    # 4. Global De-Dollarization Simulation (20% Non-USD Commodity Shift)
    print("\n" + "-" * 110)
    print(" 4. SIMULATION: 20% GLOBAL COMMODITY DE-DOLLARIZATION & CROSS-MARKET CONTAGION")
    print("-" * 110)
    print(" Scenario: 20% of global oil and dry bulk raw material trades migrate from USD to bilateral Petro-Yuan/Gold.")
    print(" Measuring resulting collateral drain on US Triparty Repo and transmission impedance on European SVT dealers.")

    dedollarization_scenarios = [
        ("Baseline (USD Petrodollar Dominance)", 3007.0e9, 0.05, 65.0e9, 0.15, 81.5),
        ("Moderate De-Dollarization (10% Bilateral Shift)", 2706.0e9, 0.25, 95.0e9, 0.12, 105.0),
        ("Severe De-Dollarization (20% Bilateral Shift)", 2405.0e9, 0.45, 130.0e9, 0.08, 135.0),
    ]

    for label, repo_vol, repo_fric, py_vol, py_fric, oat_spread in dedollarization_scenarios:
        w_repo = bridge.compute_edge_weight(
            base_weight=1.05,
            flow_volume_eur=repo_vol,
            risk_friction=repo_fric,
            is_domestic_retention=False,
        )
        w_svt = bridge.compute_edge_weight(
            base_weight=1.10,
            flow_volume_eur=40.0e9,
            risk_friction=(oat_spread / 100.0) * 1.5,
            is_domestic_retention=False,
        )
        w_petroyuan = bridge.compute_edge_weight(
            base_weight=0.90,
            flow_volume_eur=py_vol,
            risk_friction=py_fric,
            is_domestic_retention=False,
        )
        step_cost_repo = 1.0 / (1.0 + w_repo)
        step_cost_svt = 1.0 / (1.0 + w_svt)
        step_cost_py = 1.0 / (1.0 + w_petroyuan)

        print(f"\n * {label}:")
        print(f"     -> US Triparty Repo Volume:      ${repo_vol/1e9:,.0f}B | Repo Spread Friction: {repo_fric:.2f}")
        print(f"     -> US Repo Financing Impedance:  {w_repo:.4f} (Step Cost: {step_cost_repo:.4f})")
        print(f"     -> European SVT Dealer Funding:  {w_svt:.4f} (Step Cost: {step_cost_svt:.4f}) [OAT Spread: +{oat_spread:5.1f} bp]")
        print(f"     -> Petro-Yuan Bilateral Clearing: {w_petroyuan:.4f} (Step Cost: {step_cost_py:.4f}) [Volume: ${py_vol/1e9:,.0f}B]")

    # 5. Graph Engine Telemetry
    telemetry = bridge.engine.get_telemetry()
    print("\n" + "-" * 110)
    print(" 5. PROCEDURAL GRAPH ENGINE TELEMETRY")
    print("-" * 110)
    print(f" * Active L1 Buffer Nodes:        {telemetry['active_l1_nodes']} / {bridge.max_nodes_k}")
    print(f" * Active L1 Buffer Edges:        {telemetry['active_l1_edges']} / {bridge.max_edges_m}")
    print(f" * Peak L1 Nodes Reached:         {telemetry['peak_l1_nodes']}")
    print(f" * Peak L1 Edges Reached:         {telemetry['peak_l1_edges']}")
    print(f" * L2 Host Graph Nodes:           {telemetry['l2_total_nodes']}")
    print(f" * L2 Host Graph Edges:           {telemetry['l2_total_edges']}")
    print(f" * Landmark Graph Clusters:       {bridge.engine.landmark_graph.num_clusters}")
    print("=" * 110)
    print("[OK] Complete Planetary Monetary Manifold traversal and De-Dollarization simulation completed successfully.")


if __name__ == "__main__":
    main()
