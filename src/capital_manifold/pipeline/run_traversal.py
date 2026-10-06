"""CLI Pipeline: Executes non-greedy macro-financial path traversal using PGM Engine.

Traces liquidity corridors from French sovereign debt expansion (OAT issuance)
to Eurosystem TARGET2 pool and German Bund safe-haven anchor.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Add src to pythonpath
src_dir = Path(__file__).resolve().parent.parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from capital_manifold.bridge.pgm_adapter import ManifoldPGMBridge, MonetaryTier

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("run_traversal")


def main() -> None:
    print("=" * 88)
    print("  CAPITAL MANIFOLD x PROCEDURAL GRAPH ENGINE (PGM-ENGINE)")
    print("  AUTONOMOUS MACRO-FINANCIAL LIQUIDITY PATH MATERIALIZER & TRAVERSAL CORRIDOR")
    print("=" * 88)

    # 1. Initialize Bridge
    logger.info("Initializing ManifoldPGMBridge...")
    bridge = ManifoldPGMBridge()

    stress = bridge.stress_snapshot
    print("\n" + "-" * 88)
    print(" 1. MACRO STRESS CONTEXT & IMPEDANCE PARAMETERS (Latest European Central Bank / Eurostat)")
    print("-" * 88)
    if stress:
        print(f" * Jurisdiction:                     {stress.jurisdiction} (French Republic)")
        print(f" * French 10Y Benchmark (OAT Yield): {stress.oat_10y_yield:.2f}%")
        print(f" * German 10Y Benchmark (Bund):      {stress.bund_10y_yield:.3f}%")
        print(f" * OAT-Bund Spread (Risk Friction):  +{stress.oat_bund_spread_bp:.1f} basis points")
        print(f" * BdF TARGET2 Net Liability Drain:  €{abs(stress.target2_net_position_eur) / 1e9:,.2f} Billion")
        print(f" * Maastricht Gross Debt:            €{stress.maastricht_debt_nominal_eur / 1e9:,.1f} Billion ({stress.maastricht_debt_pct_gdp:.1f}% GDP)")
        print(f" * Monthly Trade Balance Deficit:    €{abs(stress.latest_monthly_trade_deficit_eur) / 1e9:,.2f} Billion / month")
        print(f" * Composite Liquidity Stress Score: {stress.net_liquidity_pressure_score:.2f} / 100.0 (Elevated Friction)")

    # 2. Monetary Tiers & Landmark Graph
    lm = bridge.engine.landmark_graph
    print("\n" + "-" * 88)
    print(f" 2. GLOBAL LANDMARK CORRIDOR SCAFFOLDING ({lm.num_clusters} Clusters across 4 Monetary Tiers)")
    print("-" * 88)
    tier_labels = {
        MonetaryTier.GENESIS: "Tier 0 (Genesis: Sovereign Fiscal / Issuance)",
        MonetaryTier.TRANSMISSION: "Tier 1 (Transmission: Primary Dealers & Central Bank Reserves)",
        MonetaryTier.TRAVERSAL: "Tier 2 (Traversal: Interbank Settlement & Real Trade Deficit)",
        MonetaryTier.SINK: "Tier 3 (Sink: Safe-Haven Collateral Anchors & Foreign Bleed)",
    }
    for c_id in range(lm.num_clusters):
        entities_in_c = sorted(list(lm.cluster_to_entities.get(c_id, set())))
        tier_names = set(bridge.substrate.entities[e].metadata.get("tier") for e in entities_in_c if e in bridge.substrate.entities)
        tier_str = ", ".join(tier_labels.get(t, f"Tier {t}") for t in tier_names if t is not None)
        print(f" * Landmark Cluster C{c_id} [{tier_str}]:")
        for e in entities_in_c:
            print(f"     -> {e}")
    print(f" * Coarse Cluster Adjacency: {dict(lm.cluster_adjacency)}")

    # 3. Traversal Execution
    print("\n" + "-" * 88)
    print(" 3. NON-GREEDY DUAL-FRONTIER A* PATH DISCOVERY")
    print("-" * 88)

    traversal_results = bridge.execute_macro_traversal()

    # Traversal A: French Treasury -> TARGET2 Pool
    t2_res = traversal_results["paths"]["target2_drain"]
    print("\n [A] French Sovereign Debt Expansion -> Eurosystem TARGET2 Liability Drain:")
    print(f"     Status:           {'[SUCCESS]' if t2_res['success'] else '[FAILED]'}")
    print(f"     Discovered Path:  {' -> '.join(t2_res['nodes'])}")
    print(f"     Edge Relations:   {' -> '.join(t2_res['edges'])}")
    print(f"     Path Traversal Cost: {t2_res['total_cost']:.4f}")
    print(f"     Frontier Steps:   {t2_res['iterations']} iterations, {t2_res['expanded_nodes']} expanded nodes")

    # Traversal B: French Treasury -> German Bund Safe Haven Anchor
    bund_res = traversal_results["paths"]["bund_safe_haven_flight"]
    print("\n [B] French Sovereign Debt Issuance -> German Bund Risk-Free Anchor (Spread Gradient):")
    print(f"     Status:           {'[SUCCESS]' if bund_res['success'] else '[FAILED]'}")
    print(f"     Discovered Path:  {' -> '.join(bund_res['nodes'])}")
    print(f"     Edge Relations:   {' -> '.join(bund_res['edges'])}")
    print(f"     Path Traversal Cost: {bund_res['total_cost']:.4f}")
    print(f"     Frontier Steps:   {bund_res['iterations']} iterations, {bund_res['expanded_nodes']} expanded nodes")

    # Traversal C: French Treasury -> Foreign Trade Bleed
    trade_res = traversal_results["paths"]["foreign_trade_bleed"]
    print("\n [C] French Fiscal Deficit Expansion -> Real Economy Foreign Trade Bleed:")
    print(f"     Status:           {'[SUCCESS]' if trade_res['success'] else '[FAILED]'}")
    print(f"     Discovered Path:  {' -> '.join(trade_res['nodes'])}")
    print(f"     Edge Relations:   {' -> '.join(trade_res['edges'])}")
    print(f"     Path Traversal Cost: {trade_res['total_cost']:.4f}")
    print(f"     Frontier Steps:   {trade_res['iterations']} iterations, {trade_res['expanded_nodes']} expanded nodes")

    # 4. Bridge Entities and Resolution of Blindness
    print("\n" + "-" * 88)
    print(" 4. BRIDGE ENTITY BLINDNESS RESOLUTION")
    print("-" * 88)
    print(f" * Identified Intermediate Bridge Entities: {traversal_results['bridge_entities']}")
    print(" * Theoretical Mechanism:")
    print("   - Sovereign issuance ('french_republic_tresor') and safe-haven sinks ('bund_risk_free_anchor')")
    print("     reside in distant institutional tiers with low direct cosine similarity.")
    print("   - Naive 1-hop greedy search rejects intermediate clearing entities like 'svt_dealers_bnp_socgen'")
    print("     and 'banque_de_france' due to lack of immediate query overlap.")
    print("   - Landmark Scaffolding restricts the corridor to {Genesis -> Transmission -> Traversal -> Sink},")
    print("     while Dual-Frontier Bidirectional A* steps forward and backward concurrently.")
    print("   - Corridor-protected utility boosts (U >= 0.85) guarantee that clearing intermediaries")
    print("     are materialized into active L1/L2 memory rather than prematurely evicted.")

    # 5. Telemetry & Buffer Statistics
    telemetry = traversal_results["buffer_stats"]
    print("\n" + "-" * 88)
    print(" 5. ENGINE TELEMETRY & TIERED MEMORY BUFFER STATISTICS")
    print("-" * 88)
    print(f" * Active L1 Nodes:               {telemetry['active_l1_nodes']} / {bridge.max_nodes_k}")
    print(f" * Active L1 Edges:               {telemetry['active_l1_edges']} / {bridge.max_edges_m}")
    print(f" * Peak L1 Nodes Reached:         {telemetry['peak_l1_nodes']}")
    print(f" * Peak L1 Edges Reached:         {telemetry['peak_l1_edges']}")
    print(f" * L2 Host Graph Nodes:           {telemetry['l2_total_nodes']}")
    print(f" * L2 Host Graph Edges:           {telemetry['l2_total_edges']}")
    print(f" * Contractions Synthesized:      {telemetry['contractions_synthesized']}")
    print(f" * Search Iterations Completed:   {telemetry['iteration']}")
    print(f" * Invariant Verification Status: {'[VERIFIED PASS]' if traversal_results['invariants_verified'] else '[FAIL]'}")
    for inv_name, status in traversal_results["invariant_details"].items():
        print(f"     -> {inv_name}: {'PASS' if status else 'FAIL'}")
    print("=" * 88)
    print("[OK] Traversal pipeline completed successfully.")


if __name__ == "__main__":
    main()
