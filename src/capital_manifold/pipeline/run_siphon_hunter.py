"""Executable CLI Pipeline: Automated Siphon & Structural Discrepancy Hunter.

Executes adversarial red-team scans across global macro flow infrastructure:
1. Bilateral Mirror Trade Discrepancies (Russian Urals crude, Swiss gold, US-China customs gap).
2. Absorbing Sinks & Dark Conduits (Russian trapped capital, shadow tanker freight margins).
3. Custody Nominee Triangulation (Euroclear, Clearstream, Swiss banks, Cayman SPVs).
4. IMF Net Errors & Omissions (NEO) Capital Flight Decomposition ($180B global residual).

Produces an institutional Bloomberg/Palantir-style terminal briefing and persists
structured machine-readable intelligence to data/processed/siphon_audit_report.json.
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

from capital_manifold.adversarial.siphon_hunter import (
    DEFAULT_CIF_FOB_MARGIN_PCT,
    DEFAULT_DUCKDB_PATH,
    DEFAULT_REPORT_PATH,
    SiphonAuditReport,
    SiphonHunter,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("run_siphon_hunter")

# Terminal Color Codes
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"


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


def print_siphon_report(report: SiphonAuditReport) -> None:
    """Renders high-density institutional terminal report."""
    sep = "=" * 102
    subsep = "-" * 102

    print("\n" + BOLD + CYAN + sep + RESET)
    print(BOLD + WHITE + "   CAPITAL MANIFOLD: AUTOMATED SIPHON & STRUCTURAL DISCREPANCY HUNTER" + RESET)
    print(DIM + "   Covert Flow Detection, Bilateral Mirror Trade Invoicing, Custody Nominees & Capital Flight" + RESET)
    print(BOLD + CYAN + sep + RESET)

    print(f"\n * Timestamp:                   {report.timestamp}")
    print(f" * Total Identified Siphons:    {BOLD}{RED}{format_usd(report.total_siphoned_volume_usd)}{RESET}")
    print(f" * Total Trade/Macro Gaps:      {BOLD}{YELLOW}{format_usd(report.total_discrepancy_volume_usd)}{RESET}")
    print(f" * Excess Nominee Custody:      {BOLD}{MAGENTA}{format_usd(report.summary_statistics['total_excess_custody_nominee_volume_usd'])}{RESET}")
    print(f" * Global IMF NEO Residual:     {BOLD}{WHITE}{format_usd(report.summary_statistics['global_neo_annual_discrepancy_usd'])}{RESET}")

    # -------------------------------------------------------------------------
    # 1. Bilateral Mirror Trade Discrepancies
    # -------------------------------------------------------------------------
    print("\n" + BOLD + subsep + RESET)
    print(BOLD + WHITE + " 1. BILATERAL MIRROR TRADE DISCREPANCY SCANNER (CIF/FOB ADJUSTED)" + RESET)
    print(BOLD + subsep + RESET)
    print(f" Discrepancies Found: {len(report.bilateral_discrepancies)}\n")

    for d in report.bilateral_discrepancies:
        badge = f"{RED}[CRITICAL]{RESET}" if d.severity == "CRITICAL" else f"{YELLOW}[HIGH]{RESET}"
        print(f" {badge} {BOLD}{d.corridor_id}{RESET} - {d.commodity}")
        print(f"     Route:                {d.exporter_country}  -->  {d.importer_country}")
        print(f"     Reported Export:      {format_usd(d.reported_export_fob_usd)} (FOB declared at port of origin)")
        print(f"     Reported Import:      {format_usd(d.reported_import_cif_usd)} (CIF declared at customs destination)")
        print(f"     Expected Import:      {format_usd(d.expected_import_cif_usd)} ({d.cif_fob_adjustment_pct:.1f}% CIF/FOB transportation margin)")
        print(f"     Raw Mirror Gap:       {BOLD}{format_usd(d.raw_discrepancy_usd)}{RESET}")
        print(f"     Adjusted Gap:         {BOLD}{format_usd(d.adjusted_discrepancy_usd)}{RESET}")
        print(f"     Classification:       {CYAN}{d.discrepancy_type}{RESET}")
        print(f"     Siphoned Volume:      {BOLD}{RED}{format_usd(d.suspected_siphoned_amount_usd)}{RESET}")
        print(f"     Suspected Entities:   {DIM}{', '.join(d.suspected_intermediaries)}{RESET}")
        print(f"     Audit Intelligence:   {d.methodology_notes}\n")

    # -------------------------------------------------------------------------
    # 2. Absorbing Sinks & Dark Conduits
    # -------------------------------------------------------------------------
    print(BOLD + subsep + RESET)
    print(BOLD + WHITE + " 2. ABSORBING SINK & DARK CONDUIT HUNTER (KIRCHHOFF CONSERVATION)" + RESET)
    print(BOLD + subsep + RESET)
    print(f" Absorbing Anomalies Identified: {len(report.absorbing_conduits)}\n")

    for c in report.absorbing_conduits:
        badge = f"{RED}[CRITICAL]{RESET}" if c.severity == "CRITICAL" else f"{YELLOW}[HIGH]{RESET}" if c.severity == "HIGH" else f"{BLUE}[MEDIUM]{RESET}"
        print(f" {badge} {BOLD}{c.entity_id}{RESET} [{c.jurisdiction}]")
        print(f"     Sector:               {c.sector}")
        print(f"     Total Inflow:         {format_usd(c.total_inflow_usd)}")
        print(f"     Total Outflow:        {format_usd(c.total_outflow_usd)}")
        print(f"     Siphoned / Trapped:   {BOLD}{RED}{format_usd(c.siphoned_volume_usd)}{RESET}")
        print(f"     Retention Ratio:      {BOLD}{c.retention_ratio_pct:.1f}%{RESET}")
        print(f"     Classification:       {CYAN}{c.anomaly_classification}{RESET}")
        print(f"     Counterparties:       {DIM}{', '.join(c.suspected_counterparties)}{RESET}")
        print(f"     Audit Intelligence:   {c.audit_narrative}\n")

    # -------------------------------------------------------------------------
    # 3. Custody Nominee Triangulation Scanner
    # -------------------------------------------------------------------------
    print(BOLD + subsep + RESET)
    print(BOLD + WHITE + " 3. CUSTODY NOMINEE TRIANGULATION SCANNER (BENEFICIAL SOVEREIGN LOOK-THROUGH)" + RESET)
    print(BOLD + subsep + RESET)
    print(f" Nominee Hubs Evaluated: {len(report.custody_nominees)}\n")

    for n in report.custody_nominees:
        badge = f"{RED}[CRITICAL]{RESET}" if n.severity == "CRITICAL" else f"{YELLOW}[HIGH]{RESET}"
        print(f" {badge} {BOLD}{n.custodian_name}{RESET} ({n.custodian_entity})")
        print(f"     Primary Depository:   {n.primary_fmi}")
        print(f"     Reported Holdings:    {BOLD}{format_usd(n.reported_treasury_holdings_usd)}{RESET}")
        print(f"     Domestic Capacity:    {format_usd(n.estimated_domestic_capacity_usd)} (Max sovereign investor absorption)")
        print(f"     Excess Nominee Vol:   {BOLD}{RED}{format_usd(n.excess_nominee_holdings_usd)}{RESET} ({n.nominee_intensity_ratio:.1f}x domestic capacity)")
        print(f"     Statistical Outlier:  {BOLD}{MAGENTA}{n.sigma_deviation:.1f}-sigma{RESET} above expected capacity")
        print("     Triangulated Beneficial Sovereign Owners:")
        for bo in n.triangulated_beneficial_owners:
            print(f"       -> {BOLD}{bo.beneficial_owner}{RESET}: {GREEN}{format_usd(bo.attributed_volume_usd)}{RESET} ({bo.attributed_pct:.1f}%)")
            print(f"          Motive: {DIM}{bo.strategic_motive}{RESET}")
        print(f"     Audit Intelligence:   {n.audit_narrative}\n")

    # -------------------------------------------------------------------------
    # 4. IMF Net Errors & Omissions (NEO) Capital Flight Allocator
    # -------------------------------------------------------------------------
    print(BOLD + subsep + RESET)
    print(BOLD + WHITE + " 4. IMF NET ERRORS & OMISSIONS (NEO) CAPITAL FLIGHT ALLOCATOR" + RESET)
    print(BOLD + subsep + RESET)
    neo = report.statistical_residual_allocation
    print(f" Global Annual BoP Discrepancy: {BOLD}{WHITE}{format_usd(neo.global_neo_annual_discrepancy_usd)}{RESET}")
    print(f" Modeled in Manifold Substrate:  {format_usd(neo.modeled_neo_in_manifold_usd)}")
    print(f" Unmodeled Gap:                 {format_usd(neo.unmodeled_neo_gap_usd)}\n")

    print(" Allocated Dark Vectors:")
    for v in neo.allocated_vectors:
        print(f"   [+] {BOLD}{v['vector_name']}{RESET}")
        print(f"       Allocation:              {BOLD}{GREEN}{format_usd(v['allocated_amount_usd'])}{RESET} ({v['allocation_pct']:.1f}% of global residual)")
        print(f"       Operational Mechanism:   {v['operational_mechanism']}")
        print(f"       Geographic Hotspots:     {', '.join(v['geographic_hotspots'])}")
        print(f"       Suspected Rails:         {DIM}{', '.join(v['suspected_settlement_rails'])}{RESET}\n")

    print(f" Flight Origins: {', '.join(neo.capital_flight_origin_jurisdictions)}")
    print(f" Offshore Sinks: {', '.join(neo.capital_flight_destination_sinks)}\n")

    # -------------------------------------------------------------------------
    # 5. Master Intelligence Summary & Actionable Recommendations
    # -------------------------------------------------------------------------
    print(BOLD + sep + RESET)
    print(BOLD + WHITE + " 5. MASTER INTELLIGENCE SUMMARY & TOP CRITICAL LEAKS" + RESET)
    print(BOLD + sep + RESET)

    print("\n Top Unmasked Covert Siphons & Trapped Capital Basins:")
    for idx, leak in enumerate(report.top_critical_leaks[:5], 1):
        print(f"  {idx}. {BOLD}{leak['id']}{RESET} [{leak['severity']}] - {RED}{format_usd(leak['volume_usd'])}{RESET}")
        print(f"     Entity:         {leak['entity']}")
        print(f"     Classification: {leak['classification']}")
        print(f"     Summary:        {leak['description']}")

    print("\n Actionable Regulatory & Financial Engineering Remediation:")
    for r in report.remediation_actions:
        print(f"  * [{BOLD}{r['area']}{RESET}]: {CYAN}{r['action']}{RESET}")
        print(f"    Details: {r['details']}")

    print("\n" + BOLD + CYAN + sep + RESET + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Automated Siphon & Structural Discrepancy Hunter Pipeline.")
    parser.add_argument(
        "--output-json",
        type=str,
        default=str(DEFAULT_REPORT_PATH),
        help=f"Destination path for structured JSON audit report (default: {DEFAULT_REPORT_PATH})",
    )
    parser.add_argument(
        "--duckdb",
        type=str,
        default=str(DEFAULT_DUCKDB_PATH),
        help=f"Path to DuckDB database (default: {DEFAULT_DUCKDB_PATH})",
    )
    parser.add_argument(
        "--cif-fob-pct",
        type=float,
        default=DEFAULT_CIF_FOB_MARGIN_PCT,
        help=f"Standard CIF/FOB margin percentage (default: {DEFAULT_CIF_FOB_MARGIN_PCT}%%)",
    )
    parser.add_argument(
        "--sigma-threshold",
        type=float,
        default=5.0,
        help="Outlier sigma threshold for custody nominee identification (default: 5.0)",
    )
    args = parser.parse_args()

    hunter = SiphonHunter(duckdb_path=args.duckdb)
    report = hunter.generate_siphon_report(output_path=args.output_json)
    print_siphon_report(report)
    logger.info(f"Report execution complete. Written to {args.output_json}")


if __name__ == "__main__":
    main()
