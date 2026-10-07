"""Executable CLI Pipeline: Adversarial System Audit & Red-Team Scorecard.

Executes a comprehensive, quantitative audit across:
1. Accounting Conservation Invariants (Sources, Conduits, Sinks, Leaks, Orphans).
2. Dimensional & Unit Consistency (Yield spreads as fiat currency, signed nominal amounts, FX rates).
3. Temporal Cadence & Velocity Normalization (Daily vs Monthly vs Quarterly vs Annual, Stock vs Flow).
4. Graph Topology & Critical Node Resilience (117+ node substrate, articulation points, sink traps, node removals).
5. Global Macro Dark Matter Benchmarking (BIS OTC derivatives $600T, Basis trade $800B, Trade discrepancy $175B, PBOC swaps $550B).

Outputs a structured, quantitative scorecard with an Adversarial System Integrity Score (0-100),
detailed breakdowns, high-risk anomalies, and remediation recommendations.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# Add src to sys.path
src_dir = Path(__file__).resolve().parent.parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from capital_manifold.adversarial.system_auditor import (
    SystemAuditor,
    FullAuditScorecard,
    EntityRole,
    SinkType,
    TemporalCadence,
    DEFAULT_DUCKDB_PATH,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("run_system_audit")


def format_usd(val: float) -> str:
    """Format large USD values into human-readable strings."""
    abs_val = abs(val)
    sign = "-" if val < 0 else ""
    if abs_val >= 1e12:
        return f"{sign}${abs_val / 1e12:,.2f}T"
    elif abs_val >= 1e9:
        return f"{sign}${abs_val / 1e9:,.2f}B"
    elif abs_val >= 1e6:
        return f"{sign}${abs_val / 1e6:,.2f}M"
    elif abs_val >= 1e3:
        return f"{sign}${abs_val / 1e3:,.2f}K"
    else:
        return f"{sign}${abs_val:,.2f}"


def print_audit_report(scorecard: FullAuditScorecard) -> None:
    sep = "=" * 94
    subsep = "-" * 94

    print("\n" + sep)
    print("   CAPITAL MANIFOLD: ADVERSARIAL SYSTEM AUDITOR & RED-TEAM SCORECARD")
    print("   Comprehensive Audit of Schema, Conservation Laws, Topology, and Global Dark Matter")
    print(sep)

    # -------------------------------------------------------------
    # 1. Accounting Conservation Report
    # -------------------------------------------------------------
    cons = scorecard.conservation_report
    print("\n" + subsep)
    print(" 1. ACCOUNTING CONSERVATION & DOUBLE-ENTRY INVARIANTS AUDIT")
    print(subsep)
    print(f" * Total Entities Evaluated:   {cons.total_entities_evaluated}")
    print(f" * Source Entities (In=0):     {len(cons.source_entities)}")
    print(f" * Intermediate Conduits:      {len(cons.conduit_entities)}")
    print(f" * Sink Entities (Out=0):      {len(cons.sink_entities)}")
    print(f" * Orphan Nodes (In=0, Out=0): {len(cons.orphan_entities)}")
    print(f" * Total Detected Leaks:       {len(cons.detected_leaks)}")
    print(f" * Total Unaccounted Leakage:  {format_usd(cons.total_leakage_volume_usd)}")

    if cons.orphan_entities:
        print("\n   [!] Orphan Entities Identified (Registered in System, Zero Inflows / Outflows):")
        for o in cons.orphan_entities[:8]:
            print(f"       - {o}")
        if len(cons.orphan_entities) > 8:
            print(f"       ... and {len(cons.orphan_entities) - 8} more orphan entities.")

    if cons.detected_leaks:
        print("\n   [!] Critical Double-Entry Conservation Leaks Flagged:")
        for leak in cons.detected_leaks:
            print(f"       -> Entity: {leak['entity_id']}")
            print(f"          Inflow:  {format_usd(leak['inflow_usd'])}")
            print(f"          Outflow: {format_usd(leak['outflow_usd'])}")
            print(f"          Leakage: {format_usd(leak['leak_amount_usd'])} ({leak['description']})")

    # -------------------------------------------------------------
    # 2. Dimensional Integrity Report
    # -------------------------------------------------------------
    dim = scorecard.dimensional_report
    print("\n" + subsep)
    print(" 2. DIMENSIONAL INTEGRITY & UNIT CONSISTENCY AUDIT")
    print(subsep)
    print(f" * Total Flow Events Audited:      {dim.total_events_audited}")
    print(f" * Unit / Dimensional Mismatches:  {dim.unit_mismatches_count}")
    print(f" * Signed Amount Violations (<0):  {dim.signed_amount_violations_count}")
    print(f" * FX Normalization Anomalies:     {dim.fx_anomalies_count}")
    print(f" * Dimensionally Sound:            {'YES' if dim.is_dimensionally_sound else 'NO (VIOLATIONS DETECTED)'}")

    if dim.errors:
        print("\n   [!] Dimensional Violations Detected:")
        for err in dim.errors[:6]:
            print(f"       -> [{err.severity}] {err.error_type} in '{err.event_id}' ({err.instrument})")
            print(f"          Nominal: {err.nominal_amount} {err.currency} -> USD: ${err.amount_usd_normalized:,.2f}")
            print(f"          Detail:  {err.description}")
        if len(dim.errors) > 6:
            print(f"       ... and {len(dim.errors) - 6} additional dimensional errors.")

    # -------------------------------------------------------------
    # 3. Temporal Cadence Report
    # -------------------------------------------------------------
    temp = scorecard.temporal_report
    print("\n" + subsep)
    print(" 3. TEMPORAL CADENCE & VELOCITY NORMALIZATION AUDIT")
    print(subsep)
    print(f" * Total Flow Events Analyzed:    {temp.total_events}")
    print(f"     -> High-Frequency Daily:     {temp.daily_events_count} (Turnover <= 1 day)")
    print(f"     -> Monthly Periodic:         {temp.monthly_events_count} (Turnover ~30 days)")
    print(f"     -> Quarterly Periodic:       {temp.quarterly_events_count} (Turnover ~90 days)")
    print(f"     -> Annual / Static Stock:    {temp.annual_static_events_count} (Turnover > 120 days or static)")
    print(f" * Stock vs. Flow Confusions:     {len(temp.stock_flow_confusions)}")
    print(f" * Path Cadence Mismatches:       {len(temp.path_cadence_mismatches)}")

    print("\n   [*] Annualized Rate Equivalents vs. Static Stocks:")
    print("       - SOFR Triparty Repo:      $3.007T/day  -> Annualized Flow: $757.764 Trillion/year (252 days)")
    print("       - TGA Net Reserve Drain:   $12.154B/day -> Annualized Flow: $3.063 Trillion/year")
    print("       - Apple Share Buyback:     $62.094B/qtr -> Annualized Flow: $248.376 Billion/year")
    print("       - US Public Debt Stock:    $40.250 Trillion (Static State Variable S, NOT Flow dS/dt)")
    print("       - French Maastricht Debt:  $3.536 Trillion (Static State Variable S, NOT Flow dS/dt)")

    if temp.path_cadence_mismatches:
        print("\n   [!] Path Temporal Cadence Jumps (>10x Velocity Mismatch):")
        for m in temp.path_cadence_mismatches:
            print(f"       -> Path: {' -> '.join(m['path'])}")
            print(f"          From: {m['source_cadence']} to {m['target_cadence']}")
            print(f"          Velocity Ratio Jump: {m['velocity_ratio']:.1f}x (Annualized Ratio: {m['annualized_rate_jump_ratio']:.1f}x)")
            print(f"          Issue: {m['issue']}")

    # -------------------------------------------------------------
    # 4. Graph Topology Report
    # -------------------------------------------------------------
    topo = scorecard.topology_report
    print("\n" + subsep)
    print(" 4. GRAPH TOPOLOGY & CRITICAL NODE RESILIENCE AUDIT (117+ NODE SUBSTRATE)")
    print(subsep)
    print(f" * Total Substrate Entities:      {topo.total_nodes}")
    print(f" * Total Substrate Edges:         {topo.total_edges}")
    print(f" * Directed Graph Density:        {topo.graph_density:.4f}")
    print(f" * Weakly Connected Components:   {topo.weakly_connected_components}")
    print(f" * Strongly Connected Components: {topo.strongly_connected_components}")
    print(f" * Articulation Points (Cut Vertices): {len(topo.articulation_points)}")
    print(f" * Absorbing Sinks (Out=0, In>0): {len(topo.absorbing_sinks)}")
    print(f"     -> Legitimate Monetary Burns: {len(topo.legitimate_burn_sinks)} (QT burn, share buybacks, RRP buffer, Bund anchor)")
    print(f"     -> Unintended Dead-End Traps: {len(topo.unintended_sink_traps)} (Decoy consumer fintechs & municipal terminals)")

    print("\n   [*] Top Articulation Points (Single Points of Failure):")
    for ap in topo.articulation_points[:6]:
        print(f"       - {ap}")

    print("\n   [*] Critical Node Removal & Route Stability Stress Tests:")
    for node_name, impact in topo.critical_node_removals.items():
        print(f"       -> Node: '{node_name}' ({impact.get('node_role', '')})")
        print(f"          Severed Routes: {impact.get('severed_routes', [])}")
        print(f"          Route Disruption: {impact.get('disruption_pct', 0.0):.1f}%")
        if "systemic_impact" in impact:
            print(f"          Systemic Impact: {impact['systemic_impact']}")

    # -------------------------------------------------------------
    # 5. Global Macro Dark Matter Report
    # -------------------------------------------------------------
    dm = scorecard.unmodeled_risk_report
    print("\n" + subsep)
    print(" 5. GLOBAL MACRO 'DARK MATTER' & UNMODELED RISK AUDIT")
    print(subsep)
    print(f" * Total Modeled Explicit Assets:     {format_usd(dm.modeled_total_explicit_usd)} (US & French Sovereign Debt)")
    print(f" * Total Modeled Daily Repo Volume:   {format_usd(dm.modeled_daily_repo_volume_usd)}")
    print(f" * Total Unmodeled Dark Matter:       {format_usd(dm.total_unmodeled_dark_matter_usd)} Notional")
    print(f" * Global Manifold Coverage Ratio:    {dm.overall_coverage_ratio_pct:.2f}% Modeled / {100.0 - dm.overall_coverage_ratio_pct:.2f}% Dark Matter")
    print(f" * Dark Matter Risk Multiplier:       {dm.dark_matter_multiplier:.1f}x Unmodeled Commitments per Sovereign Debt")
    print(f" * Systemic Blindspot Score:          {dm.systemic_blindspot_score:.1f} / 100.0 (Tail Risk Severity)")
    print(f" * ISDA Netted At-Risk Commitments:   {format_usd(dm.at_risk_economic_commitments_usd)} ($25T GMV + $67T Shadow + $1.7T PC + Debt + Repo)")
    print(f" * Modeled At-Risk Commitments:       {format_usd(dm.modeled_at_risk_commitments_usd)} ({dm.at_risk_coverage_ratio_pct:.1f}% At-Risk Coverage)")

    print("\n   [*] Dark Matter Pillars Breakdown:")
    for b in dm.benchmarks:
        print(f"       -> {b.domain_name}:")
        print(f"          Real-World Scale: {b.real_world_metric_label}")
        print(f"          Modeled Amount:   {format_usd(b.modeled_notional_usd)} ({b.coverage_ratio_pct:.3f}% coverage)")
        print(f"          Unmodeled Gap:    {format_usd(b.gap_usd)}")
        print(f"          Risk Mechanism:   {b.primary_risk_mechanism}")

    # -------------------------------------------------------------
    # 6. Final Scorecard & Remediation
    # -------------------------------------------------------------
    print("\n" + sep)
    print("   ADVERSARIAL SYSTEM INTEGRITY SCORECARD")
    print(sep)
    print(f"   OVERALL SYSTEM INTEGRITY SCORE:    {scorecard.system_integrity_score:.1f} / 100.0")
    print(f"   ------------------------------------------------------------------")
    print(f"   [1] Accounting Conservation Score: {scorecard.conservation_score:.1f} / 20.0")
    print(f"   [2] Dimensional Integrity Score:   {scorecard.dimensional_score:.1f} / 20.0")
    print(f"   [3] Temporal Cadence Score:        {scorecard.temporal_score:.1f} / 20.0")
    print(f"   [4] Graph Topology Score:          {scorecard.topology_score:.1f} / 20.0")
    print(f"   [5] Macro Dark Matter Score:       {scorecard.dark_matter_score:.1f} / 20.0")
    print(sep)

    print("\n" + subsep)
    print(" 7. HIGH-RISK ANOMALIES & SYSTEMIC DEFICIENCIES")
    print(subsep)
    for a in scorecard.high_risk_anomalies:
        print(f" * [{a['severity']}] {a['id']}: {a['dimension']} - {a['entity']}")
        print(f"   Description: {a['description']}")
        print(f"   Impact:      {a['impact']}\n")

    print(subsep)
    print(" 8. REMEDIATION RECOMMENDATIONS")
    print(subsep)
    for r in scorecard.remediation_recommendations:
        print(f" * {r['id']} [{r['area']}]: {r['action']}")
        print(f"   Details: {r['details']}\n")
    print(sep)


def main() -> None:
    parser = argparse.ArgumentParser(description="Capital Manifold Adversarial System Auditor CLI")
    parser.add_argument(
        "--duckdb-path",
        type=str,
        default=str(DEFAULT_DUCKDB_PATH),
        help="Path to DuckDB database (default: data/cache/manifold.duckdb)",
    )
    parser.add_argument(
        "--output-json",
        type=str,
        default=None,
        help="Optional path to output audit scorecard as JSON",
    )
    args = parser.parse_args()

    auditor = SystemAuditor(duckdb_path=args.duckdb_path)
    scorecard = auditor.run_full_audit()

    print_audit_report(scorecard)

    if args.output_json:
        out_path = Path(args.output_json)
        summary_dict = {
            "system_integrity_score": scorecard.system_integrity_score,
            "category_scores": {
                "conservation": scorecard.conservation_score,
                "dimensional": scorecard.dimensional_score,
                "temporal": scorecard.temporal_score,
                "topology": scorecard.topology_score,
                "dark_matter": scorecard.dark_matter_score,
            },
            "total_leakage_usd": scorecard.conservation_report.total_leakage_volume_usd,
            "conduit_leaks_count": len(scorecard.conservation_report.detected_leaks),
            "unit_errors_count": scorecard.dimensional_report.unit_mismatches_count,
            "unmodeled_dark_matter_usd": scorecard.unmodeled_risk_report.total_unmodeled_dark_matter_usd,
            "at_risk_economic_commitments_usd": scorecard.unmodeled_risk_report.at_risk_economic_commitments_usd,
            "modeled_at_risk_commitments_usd": scorecard.unmodeled_risk_report.modeled_at_risk_commitments_usd,
            "at_risk_coverage_ratio_pct": scorecard.unmodeled_risk_report.at_risk_coverage_ratio_pct,
            "coverage_ratio_pct": scorecard.unmodeled_risk_report.overall_coverage_ratio_pct,
            "high_risk_anomalies": scorecard.high_risk_anomalies,
            "remediation_recommendations": scorecard.remediation_recommendations,
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(summary_dict, f, indent=2)
        print(f"\n[+] Wrote audit scorecard summary JSON to: {out_path.resolve()}")


if __name__ == "__main__":
    main()
