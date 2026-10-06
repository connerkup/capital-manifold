"""Global Liquidity Triangle Traversal Pipeline.

Traces:
[1] Transpacific Yen Carry Corridor: Japan Carry Faucet -> Institutional Desk -> US Triparty Repo -> US Treasury TGA.
[2] Corporate Buyback Burn Corridor: French Trade Bleed -> Global Exporters -> Big Tech Cash Hoard -> Share Buyback Burn.
[3] Petrodollar Recycling Loop: French Trade Bleed -> Exporters -> Gulf Sovereign Wealth Basin -> SVT Dealer Diversification.
[4] Simulation: $50B Yen FX Intervention shock (BoJ/MoF selling US Treasuries) & transatlantic repo/dealer spillover.
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
from capital_manifold.harvesters.transpacific_corporate import TranspacificCorporateHarvester

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("run_global_triangle_traversal")


def main() -> None:
    print("=" * 100)
    print("  CAPITAL MANIFOLD: THE GLOBAL LIQUIDITY TRIANGLE & CROSS-BORDER SPILLOVER NEXUS")
    print("  Transpacific Yen Carry Faucet, Corporate Buyback Burn Chamber & Petrodollar Loop")
    print("=" * 100)

    # 1. Harvest Live / Baseline Data (Apple SEC EDGAR, Japan TIC, Petrodollars)
    print("\n" + "-" * 100)
    print(" 1. HARVEST TELEMETRY: SEC EDGAR LIVE XBRL & US TREASURY TIC CAPITAL FLOWS")
    print("-" * 100)

    with TranspacificCorporateHarvester() as harvester:
        apple_events, apple_meta = harvester.fetch_apple_sec_edgar()
        global_events, global_meta = harvester.fetch_japan_tic_and_petrodollar()

    cash_b = apple_meta.get("cash_and_cash_equivalents_usd", 0.0) / 1e9
    sec_b = apple_meta.get("marketable_securities_current_usd", 0.0) / 1e9
    liquid_b = apple_meta.get("total_liquid_hoard_usd", 0.0) / 1e9
    buyback_b = apple_meta.get("payments_for_repurchase_of_common_stock_usd", 0.0) / 1e9
    edgar_date = apple_meta.get("record_date", "Latest")

    japan_tic_b = global_meta.get("japan_tic_treasury_holding_usd", 0.0) / 1e9
    petro_b = global_meta.get("gulf_petrodollar_recycling_usd", 0.0) / 1e9

    print(f" * Apple Inc. SEC EDGAR Live Facts (CIK 0000320193, Period: {edgar_date}):")
    print(f"     -> Cash & Cash Equivalents:            ${cash_b:,.2f} Billion")
    print(f"     -> Marketable Securities (Current):     ${sec_b:,.2f} Billion")
    print(f"     -> Total Liquid Treasury/Cash Vault:   ${liquid_b:,.2f} Billion")
    print(f"     -> Share Buyback Equity Retirement:    ${buyback_b:,.2f} Billion (Extinguished from circulation!)")
    print(f" * Japan TIC US Treasury Anchor:             ${japan_tic_b:,.1f} Billion (${japan_tic_b/1000:.3f} Trillion #1 Global Creditor)")
    print(f" * Gulf GCC Petrodollar Recycling Basin:    ${petro_b:,.1f} Billion / year recycled into Western sovereigns")

    # 2. Institutional Mechanics & Triangular Architecture
    print("\n" + "-" * 100)
    print(" 2. MACROECONOMIC DYNAMICS OF THE GLOBAL LIQUIDITY TRIANGLE")
    print("-" * 100)
    print(" * The Transpacific Yen Carry Faucet:")
    print("     The Bank of Japan's ultra-low policy anchors trillions in JPY financing. Japanese institutional")
    print("     giants (Norinchukin, Japan Post, lifers) borrow yen, execute cross-currency swaps into USD,")
    print("     and fund $1.104T in US Treasuries and triparty repo assets, acting as the global liquidity anchor.")
    print(" * The Corporate Buyback Burn Chamber:")
    print("     Global commerce channels trade revenues into US mega-cap tech monopolies. Rather than funding")
    print("     capex or dividends, Apple and peers incinerate over $62 Billion quarterly through share buybacks,")
    print("     permanently extinguishing private monetary velocity and concentrating equity ownership.")
    print(" * The Petrodollar Recycling Loop:")
    print("     European and Asian real economy trade deficits transfer cash to Gulf energy exporters (GCC SWFs).")
    print("     These sovereign wealth funds diversify petrodollar surpluses back into European sovereign debt (OATs)")
    print("     via Paris/London primary dealers, completing the macroeconomic feedback loop.")

    # 3. Dual-Frontier A* Multi-Corridor Traversals
    print("\n" + "-" * 100)
    print(" 3. NON-GREEDY DUAL-FRONTIER A* PATH DISCOVERY (THE 3 TRIANGULAR CORRIDORS)")
    print("-" * 100)

    bridge = ManifoldPGMBridge()

    # Corridor 1: Japan Carry Faucet -> TGA
    res1 = bridge.materialize_liquidity_path("japan_mof_boj_carry_faucet", "us_treasury_tga")
    print(f" [CORRIDOR 1] Transpacific Yen Carry Corridor:")
    print(f"   * Status:        {'[SUCCESS]' if res1.success else '[FAILED]'}")
    print(f"   * Traversal:     {' -> '.join(res1.path_nodes)}")
    print(f"   * Transmission:  {' -> '.join(e.relation for e in res1.path_edges)}")
    print(f"   * Traversal Cost: {res1.total_cost:.4f} ({res1.iterations} iterations, {res1.expanded_nodes} nodes expanded)")

    # Corridor 2: French Trade Bleed -> Apple Buyback Burn
    res2 = bridge.materialize_liquidity_path("french_republic_tresor", "corporate_share_buyback_burn_chamber")
    print(f"\n [CORRIDOR 2] French Sovereign Stimulus -> Big Tech -> Corporate Share Buyback Burn:")
    print(f"   * Status:        {'[SUCCESS]' if res2.success else '[FAILED]'}")
    print(f"   * Traversal:     {' -> '.join(res2.path_nodes)}")
    print(f"   * Transmission:  {' -> '.join(e.relation for e in res2.path_edges)}")
    print(f"   * Traversal Cost: {res2.total_cost:.4f} ({res2.iterations} iterations, {res2.expanded_nodes} nodes expanded)")

    # Corridor 3: Petrodollar Recycling Loop -> SVT Dealers
    res3 = bridge.materialize_liquidity_path("french_republic_tresor", "gulf_petrodollar_sovereign_wealth_basin")
    print(f"\n [CORRIDOR 3] Petrodollar Energy Recycling Basin:")
    print(f"   * Status:        {'[SUCCESS]' if res3.success else '[FAILED]'}")
    print(f"   * Traversal:     {' -> '.join(res3.path_nodes)}")
    print(f"   * Transmission:  {' -> '.join(e.relation for e in res3.path_edges)}")
    print(f"   * Traversal Cost: {res3.total_cost:.4f} ({res3.iterations} iterations, {res3.expanded_nodes} nodes expanded)")

    # 4. Stress Simulation: $50B Yen FX Intervention Shock
    print("\n" + "-" * 100)
    print(" 4. SIMULATION: $50B YEN FX INTERVENTION SHOCK & CROSS-MARKET CONTAGION")
    print("-" * 100)

    intervention_scenarios = [
        ("Baseline (Calm Transpacific Carry)", 800.0e9, 0.10, 81.5),
        ("Moderate FX Defense ($20B Treasuries Liquidated)", 780.0e9, 0.45, 110.0),
        ("Severe Yen Shock ($50B Treasuries Liquidated - Carry Unwind)", 750.0e9, 1.20, 175.0),
    ]

    for label, carry_vol, jpy_friction, oat_spread in intervention_scenarios:
        w_carry = bridge.compute_edge_weight(
            base_weight=1.05,
            flow_volume_eur=carry_vol,
            risk_friction=jpy_friction,
            is_domestic_retention=False,
        )
        w_svt_dealers = bridge.compute_edge_weight(
            base_weight=1.10,
            flow_volume_eur=40.0e9,
            risk_friction=(oat_spread / 100.0) * 1.5,
            is_domestic_retention=False,
        )
        step_cost_carry = 1.0 / (1.0 + w_carry)
        step_cost_svt = 1.0 / (1.0 + w_svt_dealers)
        print(f" * {label}:")
        print(f"     -> JPY Risk Friction: {jpy_friction:.2f} | OAT-Bund Spread: +{oat_spread:5.1f} bp")
        print(f"     -> Yen Carry Absorption Weight: {w_carry:.4f} (Step Cost: {step_cost_carry:.4f})")
        print(f"     -> European SVT Dealer Funding Weight: {w_svt_dealers:.4f} (Step Cost: {step_cost_svt:.4f})")

    # 5. Engine Telemetry
    telemetry = bridge.engine.get_telemetry()
    print("\n" + "-" * 100)
    print(" 5. PROCEDURAL GRAPH ENGINE TELEMETRY")
    print("-" * 100)
    print(f" * Active L1 Buffer Nodes:        {telemetry['active_l1_nodes']} / {bridge.max_nodes_k}")
    print(f" * Active L1 Buffer Edges:        {telemetry['active_l1_edges']} / {bridge.max_edges_m}")
    print(f" * Peak L1 Nodes Reached:         {telemetry['peak_l1_nodes']}")
    print(f" * Peak L1 Edges Reached:         {telemetry['peak_l1_edges']}")
    print(f" * L2 Host Graph Nodes:           {telemetry['l2_total_nodes']}")
    print(f" * L2 Host Graph Edges:           {telemetry['l2_total_edges']}")
    print(f" * Landmark Graph Clusters:       {bridge.engine.landmark_graph.num_clusters}")
    print("=" * 100)
    print("[OK] Global Liquidity Triangle traversal and Yen FX shock simulation completed successfully.")


if __name__ == "__main__":
    main()
