"""Dark Forest Ring 2 Traversal: The QT Burn Chamber, Evaporating RRP Buffer & Offshore Sinks.

Traces:
[1] French Sovereign Stress -> Primary Dealers -> London Eurodollar Pool -> Cayman Offshore Capital Pool.
[2] US Prime MMF -> US Treasury TGA -> Fed SOMA QT Burn Chamber (The literal money destruction).
[3] Emergency central bank swap line activation under simulated RRP exhaustion ($361B -> $0B).
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
from capital_manifold.core.schema import MacroStressSnapshot
from capital_manifold.harvesters.fed_dark_forest_ring2 import DarkForestRing2Harvester

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("run_dark_forest_ring2")


def main() -> None:
    print("=" * 96)
    print("  CAPITAL MANIFOLD: DARK FOREST RING 2 - THE QT BURN & OFFSHORE EURODOLLAR NEXUS")
    print("  Dual-Frontier A* Multi-Corridor Traversal & RRP Depletion Telemetry")
    print("=" * 96)

    # 1. Harvest Fed H.4.1 Balance Sheet & Treasury TIC
    print("\n" + "-" * 96)
    print(" 1. LIVE / CALIBRATED MACRO HARVEST: FED H.4.1 RELEASE & US TREASURY TIC")
    print("-" * 96)

    with DarkForestRing2Harvester() as harvester:
        h41_events, h41_meta = harvester.fetch_fed_h41_balance_sheet()
        tic_events, tic_meta = harvester.fetch_treasury_tic_and_debt()

    soma_assets_b = h41_meta.get("fed_soma_total_assets_usd", 0.0) / 1e9
    qt_burn_b = h41_meta.get("fed_cumulative_qt_burn_usd", 0.0) / 1e9
    rrp_bal_b = h41_meta.get("fed_on_rrp_balance_usd", 0.0) / 1e9
    rrp_drain_b = h41_meta.get("fed_on_rrp_evaporated_usd", 0.0) / 1e9
    reserves_b = h41_meta.get("fed_reserve_balances_usd", 0.0) / 1e9
    tga_b = h41_meta.get("fed_tga_balance_usd", 0.0) / 1e9
    swaps_m = h41_meta.get("central_bank_liquidity_swaps_usd", 0.0) / 1e6

    total_debt_t = tic_meta.get("total_us_public_debt_usd", 0.0) / 1e12
    uk_holding_b = tic_meta.get("tic_united_kingdom_usd", 0.0) / 1e9
    belgium_b = tic_meta.get("tic_belgium_euroclear_usd", 0.0) / 1e9
    lux_b = tic_meta.get("tic_luxembourg_ucits_usd", 0.0) / 1e9
    cayman_b = tic_meta.get("tic_cayman_islands_usd", 0.0) / 1e9

    print(f" * Fed SOMA Total Balance Sheet:    ${soma_assets_b:,.1f} Billion (${soma_assets_b/1000:.3f} Trillion)")
    print(f" * Cumulative QT Money Destruction: ${qt_burn_b:,.1f} Billion (${qt_burn_b/1000:.3f} Trillion burned from $8.9T peak)")
    print(f" * Overnight Reverse Repo (ON RRP): ${rrp_bal_b:,.1f} Billion (Depleted from $2.55T peak - ${rrp_drain_b/1000:.3f}T drained, -85.8%!)")
    print(f" * Commercial Bank Reserves at Fed: ${reserves_b:,.1f} Billion (${reserves_b/1000:.3f} Trillion)")
    print(f" * US Treasury General Account:     ${tga_b:,.1f} Billion (${tga_b/1000:.3f} Trillion)")
    print(f" * Central Bank Liquidity Swaps:    ${swaps_m:,.1f} Million (Dormant emergency dollar swap facility)")
    print(f" * Total US Public Debt Outstanding: ${total_debt_t:.2f} Trillion")
    print(f" * TIC Major Foreign Custody Hubs:  UK (London): ${uk_holding_b:.1f}B | Cayman: ${cayman_b:.1f}B | Belgium: ${belgium_b:.1f}B | Lux: ${lux_b:.1f}B")

    # 2. Economic Shadow Mechanics: The Evaporating $361.88B Buffer
    print("\n" + "-" * 96)
    print(" 2. MACROECONOMIC DYNAMICS: THE EVAPORATING RRP BUFFER & THE QT MONEY SINK")
    print("-" * 96)
    print(" * The Reverse Repo (ON RRP) Cushion:")
    print("     When ON RRP stood at $2.55 Trillion, massive US Treasury bill issuance and Fed quantitative")
    print("     tightening (QT) were absorbed almost entirely by Money Market Funds pulling cash out of the")
    print("     Fed's RRP facility. This shielded bank reserves and transatlantic interbank repo desks from")
    print("     liquidity strain.")
    print(f" * The Zero-Bound Cliff (Remaining Cushion: ${rrp_bal_b:.1f}B):")
    print(f"     With the RRP facility collapsed to ${rrp_bal_b:.1f}B (down 85.8%), this buffer is nearing complete")
    print("     exhaustion. Once ON RRP reaches $0, ongoing Fed QT ($60B+/month) and Treasury debt absorption")
    print("     must pull dollar-for-dollar from bank reserves, triggering sharp spikes in SOFR, cross-currency")
    print("     basis swap widening, and forced activation of central bank liquidity lines.")
    print(" * The QT Burn Chamber:")
    print(f"     The Fed has incinerated ${qt_burn_b/1000:.3f} Trillion in base money since 2022. Maturing Treasuries")
    print("     are not reinvested; principal received from the Treasury is permanently extinguished.")

    # 3. Dual-Frontier A* Multi-Corridor Traversals
    print("\n" + "-" * 96)
    print(" 3. NON-GREEDY DUAL-FRONTIER A* PATH DISCOVERY (3 DARK FOREST RING 2 CORRIDORS)")
    print("-" * 96)

    bridge = ManifoldPGMBridge()

    # Corridor 1: French Sovereign -> Primary Dealers -> London Eurodollar -> Cayman
    res1 = bridge.materialize_liquidity_path("french_republic_tresor", "offshore_cayman_hedge_pool")
    print(f" [CORRIDOR 1] French Sovereign Stress -> London Eurodollar -> Cayman Offshore Pool")
    print(f"   * Status:        {'[SUCCESS]' if res1.success else '[FAILED]'}")
    print(f"   * Traversal:     {' -> '.join(res1.path_nodes)}")
    print(f"   * Transmission:  {' -> '.join(e.relation for e in res1.path_edges)}")
    print(f"   * Traversal Cost: {res1.total_cost:.4f} ({res1.iterations} iterations, {res1.expanded_nodes} nodes expanded)")

    # Corridor 2: US Prime MMF -> US Treasury TGA -> Fed SOMA QT Burn Chamber
    res2 = bridge.materialize_liquidity_path("us_prime_mmf_basin", "fed_soma_qt_burn_chamber")
    print(f"\n [CORRIDOR 2] US Prime MMF Cash -> US Treasury TGA -> Fed SOMA QT Money Burn")
    print(f"   * Status:        {'[SUCCESS]' if res2.success else '[FAILED]'}")
    print(f"   * Traversal:     {' -> '.join(res2.path_nodes)}")
    print(f"   * Transmission:  {' -> '.join(e.relation for e in res2.path_edges)}")
    print(f"   * Traversal Cost: {res2.total_cost:.4f} ({res2.iterations} iterations, {res2.expanded_nodes} nodes expanded)")

    # Corridor 3: French Sovereign -> Banque de France -> Fed/ECB Emergency Swap Line
    res3 = bridge.materialize_liquidity_path("french_republic_tresor", "fed_ecb_liquidity_swap_line")
    print(f"\n [CORRIDOR 3] French Sovereign Crisis -> Banque de France -> Fed/ECB Emergency Swap Line")
    print(f"   * Status:        {'[SUCCESS]' if res3.success else '[FAILED]'}")
    print(f"   * Traversal:     {' -> '.join(res3.path_nodes)}")
    print(f"   * Transmission:  {' -> '.join(e.relation for e in res3.path_edges)}")
    print(f"   * Traversal Cost: {res3.total_cost:.4f} ({res3.iterations} iterations, {res3.expanded_nodes} nodes expanded)")

    # 4. Stress Simulation: RRP Buffer Depletion Sensitivity ($361.88B -> $0B)
    print("\n" + "-" * 96)
    print(" 4. SIMULATION: RRP BUFFER EXHAUSTION & EMERGENCY SWAP IMPEDANCE DYNAMICS")
    print("-" * 96)

    cases = [
        ("Current Buffer ($361.88B RRP Remaining)", 361.883e9, 81.5, 3.89),
        ("Late Buffer ($100.00B RRP Remaining)", 100.0e9, 120.0, 4.35),
        ("Exhaustion Cliff ($0.00B RRP Remaining - Reserve Drain Regime)", 0.0, 220.0, 5.75),
    ]

    for label, rrp_vol, spread_bp, sofr in cases:
        w_rrp = bridge.compute_edge_weight(
            base_weight=1.05,
            flow_volume_eur=max(1e6, rrp_vol),
            risk_friction=(spread_bp / 100.0) * 0.4,
            is_domestic_retention=False,
        )
        w_swap_act = bridge.compute_edge_weight(
            base_weight=1.30,
            flow_volume_eur=207e6 if rrp_vol > 0 else 50e9,  # Emergency surge if exhausted
            risk_friction=(spread_bp / 100.0) * 2.0,
            is_domestic_retention=False,
        )
        step_cost_rrp = 1.0 / (1.0 + w_rrp)
        step_cost_swap = 1.0 / (1.0 + w_swap_act)
        print(f" * {label}:")
        print(f"     -> Spread: +{spread_bp:5.1f} bp | SOFR: {sofr:.2f}%")
        print(f"     -> RRP Cash Parking Weight: {w_rrp:.4f} (Step Cost: {step_cost_rrp:.4f})")
        print(f"     -> Emergency FX Swap Weight: {w_swap_act:.4f} (Step Cost: {step_cost_swap:.4f})")

    # 5. Engine Telemetry & Invariant Telemetry
    telemetry = bridge.engine.get_telemetry()
    print("\n" + "-" * 96)
    print(" 5. PROCEDURAL GRAPH ENGINE TELEMETRY")
    print("-" * 96)
    print(f" * Active L1 Buffer Nodes:        {telemetry['active_l1_nodes']} / {bridge.max_nodes_k}")
    print(f" * Active L1 Buffer Edges:        {telemetry['active_l1_edges']} / {bridge.max_edges_m}")
    print(f" * Peak L1 Nodes Reached:         {telemetry['peak_l1_nodes']}")
    print(f" * Peak L1 Edges Reached:         {telemetry['peak_l1_edges']}")
    print(f" * L2 Host Graph Nodes:           {telemetry['l2_total_nodes']}")
    print(f" * L2 Host Graph Edges:           {telemetry['l2_total_edges']}")
    print(f" * Contractions Synthesized:      {telemetry['contractions_synthesized']}")
    print(f" * Global Landmark Clusters:      {bridge.engine.landmark_graph.num_clusters}")
    print("=" * 96)
    print("[OK] Dark Forest Ring 2 traversal and RRP depletion telemetry completed successfully.")


if __name__ == "__main__":
    main()
