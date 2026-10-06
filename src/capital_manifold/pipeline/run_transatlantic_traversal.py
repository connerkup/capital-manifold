"""Transatlantic Dollar Conduit & Offshore FX Swap / Repo Traversal Pipeline.

Traces the Dark Forest liquidity corridor from French sovereign debt issuance
through European G-SIB primary dealers, offshore synthetic USD FX swap desks,
the $3.007T/day US triparty repo pool, and into the US Prime MMF cash basin.
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
from capital_manifold.harvesters.us_transatlantic import TransatlanticMacroHarvester

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("run_transatlantic_traversal")


def main() -> None:
    print("=" * 92)
    print("  CAPITAL MANIFOLD: THE TRANSATLANTIC DOLLAR CONDUIT & SHADOW REPO NEXUS")
    print("  Dark Forest Ring 1: Dual-Frontier A* Liquidity Path Materializer")
    print("=" * 92)

    # 1. Harvest Live US Transatlantic Signals
    print("\n" + "-" * 92)
    print(" 1. LIVE TRANSATLANTIC LIQUIDITY HARVEST (US Treasury DTS & NY Fed Markets API)")
    print("-" * 92)
    with TransatlanticMacroHarvester() as harvester:
        tga_events, tga_meta = harvester.fetch_tga_cash_balance()
        sofr_events, sofr_meta = harvester.fetch_nyfed_reference_rates()

    tga_close_b = tga_meta.get("tga_closing_balance_usd", 0.0) / 1e9
    tga_change_b = tga_meta.get("tga_net_liquidity_change_usd", 0.0) / 1e9
    tga_date = tga_meta.get("record_date", "Latest")

    sofr_rate = sofr_meta.get("sofr_rate", 3.89)
    sofr_vol_b = sofr_meta.get("sofr_volume_billions_usd", 3007.0)
    sofr_date = sofr_meta.get("effective_date", "Latest")

    print(f" * US Treasury Cash Vault (TGA Closing):  ${tga_close_b:,.2f} Billion ({tga_date})")
    print(f" * TGA Net Liquidity Drain (Daily Change): {tga_change_b:+,.2f} Billion USD/day (Reserves Absorbed into Fed Vault)")
    print(f" * NY Fed SOFR Overnight Financing Rate:   {sofr_rate:.2f}% ({sofr_date})")
    print(f" * SOFR Daily Triparty Repo Turnover:     ${sofr_vol_b:,.1f} Billion / day (${sofr_vol_b/1000:.3f} Trillion/day)")
    print(f" * Broader Triparty Aggregate (BGCR/TGCR): ${sofr_meta.get('bgcr_volume_billions_usd', 1209):,.1f}B / ${sofr_meta.get('tgcr_volume_billions_usd', 1168):,.1f}B")

    # 2. Institutional Mechanics & Dark Forest Ring 1
    print("\n" + "-" * 92)
    print(" 2. INSTITUTIONAL MECHANICS & SHADOW BANKING TOPOLOGY")
    print("-" * 92)
    print(" * Synthetic USD Inflow Mechanism:")
    print("     European G-SIBs (BNP Paribas, Société Générale) cannot fund US dollar balance sheets")
    print("     via domestic ECB deposit reserves. They take down French OAT sovereign debt, pledge it")
    print("     as collateral in London/NY cross-currency basis swaps ('offshore_fx_swap_desk'), generating")
    print("     synthetic USD liabilities to access the $3.007T US triparty repo pool.")
    print(" * Shadow Outflow / Haircut Friction:")
    print("     When French sovereign stress widens (OAT-Bund spread), cross-border counterparties impose")
    print("     steeper collateral haircuts, widening the negative EUR/USD basis swap spread.")
    print(" * TGA Liquidity Absorption Friction:")
    print(f"     The US Treasury's ${tga_close_b:.1f}B cash hoard ({tga_change_b:+.2f}B/day drain) pulls reserves directly")
    print("     out of US clearing bank repo desks, tightening collateral capacity for foreign borrowers.")

    # 3. Path Discovery via Dual-Frontier A*
    print("\n" + "-" * 92)
    print(" 3. NON-GREEDY DUAL-FRONTIER A* PATH DISCOVERY (SOVEREIGN -> PRIME MMF BASIN)")
    print("-" * 92)

    bridge = ManifoldPGMBridge()
    src_id = "french_republic_tresor"
    tgt_id = "us_prime_mmf_basin"

    res = bridge.materialize_liquidity_path(src_id, tgt_id)
    print(f" * Target:               US Prime Money Market Fund Cash Basin ('{tgt_id}')")
    print(f" * Search Status:        {'[SUCCESS]' if res.success else '[FAILED]'}")
    print(f" * Discovered Path:      {' -> '.join(res.path_nodes)}")
    print(f" * Edge Relations:       {' -> '.join(e.relation for e in res.path_edges)}")
    print(f" * Total Traversal Cost: {res.total_cost:.4f}")
    print(f" * Search Iterations:    {res.iterations} steps, {res.expanded_nodes} nodes expanded")

    # 4. Comparative Stress Scenarios
    print("\n" + "-" * 92)
    print(" 4. COMPARATIVE STRESS SCENARIO ANALYSIS (SYNTHETIC USD IMPEDANCE)")
    print("-" * 92)

    scenarios = [
        ("Normal Transatlantic Conditions", 30.0, 0.0, 3.89),
        ("Current Stressed Regime", bridge.stress_snapshot.oat_bund_spread_bp if bridge.stress_snapshot else 81.5, tga_change_b, sofr_rate),
        ("Acute Transatlantic Crunch", 160.0, 35.0, 5.25),
    ]

    for label, spread_bp, tga_drain, s_rate in scenarios:
        w_swap = bridge.compute_edge_weight(
            base_weight=1.10,
            flow_volume_eur=70e9,
            risk_friction=(spread_bp / 100.0) * 1.5,
            is_domestic_retention=False,
        )
        w_repo = bridge.compute_edge_weight(
            base_weight=1.05,
            flow_volume_eur=3007e9,
            risk_friction=spread_bp / 100.0,
            is_domestic_retention=False,
        )
        w_mmf = bridge.compute_edge_weight(
            base_weight=0.95,
            flow_volume_eur=2500e9,
            risk_friction=(spread_bp / 100.0) * 0.5,
            is_domestic_retention=False,
        )
        # Cost = sum(1 / (1 + w))
        step_cost_swap = 1.0 / (1.0 + w_swap)
        step_cost_repo = 1.0 / (1.0 + w_repo)
        step_cost_mmf = 1.0 / (1.0 + w_mmf)
        total_shadow_cost = step_cost_swap + step_cost_repo + step_cost_mmf
        print(f" * {label:35s} (Spread: +{spread_bp:5.1f}bp, TGA Drain: ${tga_drain:+5.1f}B/day, SOFR: {s_rate:.2f}%):")
        print(f"     -> FX Swap Weight: {w_swap:.4f} | Repo Weight: {w_repo:.4f} | MMF Weight: {w_mmf:.4f}")
        print(f"     -> Aggregate Transatlantic Traversal Impedance: {total_shadow_cost:.4f}")

    # 5. Buffer Statistics and Invariant Telemetry
    telemetry = bridge.engine.get_telemetry()
    print("\n" + "-" * 92)
    print(" 5. ENGINE TELEMETRY & TIERED MEMORY BUFFER STATISTICS")
    print("-" * 92)
    print(f" * Active L1 Nodes:               {telemetry['active_l1_nodes']} / {bridge.max_nodes_k}")
    print(f" * Active L1 Edges:               {telemetry['active_l1_edges']} / {bridge.max_edges_m}")
    print(f" * Peak L1 Nodes Reached:         {telemetry['peak_l1_nodes']}")
    print(f" * Peak L1 Edges Reached:         {telemetry['peak_l1_edges']}")
    print(f" * L2 Host Graph Nodes:           {telemetry['l2_total_nodes']}")
    print(f" * L2 Host Graph Edges:           {telemetry['l2_total_edges']}")
    print(f" * Contractions Synthesized:      {telemetry['contractions_synthesized']}")
    print(f" * Search Iterations Completed:   {telemetry['iteration']}")
    print("=" * 92)
    print("[OK] Transatlantic dollar conduit traversal pipeline completed successfully.")


if __name__ == "__main__":
    main()
