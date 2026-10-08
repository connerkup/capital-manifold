"""Capital Manifold: Institutional Planetary Liquidity & Balance-Sheet Graph Engine CLI.

Provides unified entrypoints for:
- audit: Adversarial system integrity, double-entry accounting conservation, and dimensional checks.
- siphon: Automated siphon, dark conduit, custody nominee, and mirror trade discrepancy hunter.
- simulate: Systemic shock simulation gauntlet across extreme crisis regimes.
- serve: Institutional Cytoscape web dashboard and REST API server.
- traverse: Non-greedy dual-frontier A* liquidity path discovery across monetary tiers.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger("capital_manifold.cli")


def _cmd_audit(args: argparse.Namespace) -> int:
    from capital_manifold.adversarial.system_auditor import (
        DEFAULT_DUCKDB_PATH,
        SystemAuditor,
    )
    from capital_manifold.pipeline.run_system_audit import print_audit_report

    duckdb_path = args.duckdb_path or str(DEFAULT_DUCKDB_PATH)
    auditor = SystemAuditor(duckdb_path=duckdb_path)
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
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(summary_dict, f, indent=2)
        print(f"\n[+] Wrote audit scorecard summary JSON to: {out_path.resolve()}")

    return 0


def _cmd_siphon(args: argparse.Namespace) -> int:
    from capital_manifold.adversarial.siphon_hunter import (
        DEFAULT_CIF_FOB_MARGIN_PCT,
        DEFAULT_DUCKDB_PATH,
        DEFAULT_REPORT_PATH,
        SiphonHunter,
    )
    from capital_manifold.pipeline.run_siphon_hunter import print_siphon_report

    duckdb_path = args.duckdb or str(DEFAULT_DUCKDB_PATH)
    output_path = args.output_json or str(DEFAULT_REPORT_PATH)
    cif_fob = args.cif_fob_pct if args.cif_fob_pct is not None else DEFAULT_CIF_FOB_MARGIN_PCT

    hunter = SiphonHunter(duckdb_path=duckdb_path)
    report = hunter.generate_siphon_report(
        cif_fob_adjustment_pct=cif_fob,
        sigma_threshold=args.sigma_threshold,
        output_path=output_path,
    )
    print_siphon_report(report)
    print(f"\n[+] Siphon audit report successfully generated and saved to: {output_path}")
    return 0


def _cmd_simulate(args: argparse.Namespace) -> int:
    from capital_manifold.pipeline.run_simulation_gauntlet import (
        OUTPUT_PATH as DEFAULT_SIM_OUTPUT,
        run_pipeline,
    )
    from capital_manifold.simulation.stress_gauntlet import StressGauntletEngine

    if args.output_json:
        engine = StressGauntletEngine()
        report = engine.run_full_gauntlet()
        out_path = Path(args.output_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2)
        print(f"\n[+] Gauntlet simulation results successfully written to: {out_path.resolve()}")
    else:
        run_pipeline()
    return 0


def _cmd_serve(args: argparse.Namespace) -> int:
    import uvicorn

    print("=" * 80)
    print("  CAPITAL MANIFOLD: INSTITUTIONAL FINANCIAL ENGINEERING DASHBOARD")
    print(f"  Access URL: http://{args.host}:{args.port}")
    print(f"  API Docs:   http://{args.host}:{args.port}/docs")
    print("=" * 80)

    uvicorn.run(
        "capital_manifold.web.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )
    return 0


def _cmd_traverse(args: argparse.Namespace) -> int:
    mode = args.mode
    if mode == "macro":
        from capital_manifold.pipeline.run_traversal import main as macro_main
        macro_main()
    elif mode == "planetary":
        from capital_manifold.pipeline.run_planetary_manifold_traversal import main as planetary_main
        planetary_main()
    elif mode == "global":
        from capital_manifold.pipeline.run_global_triangle_traversal import main as global_main
        global_main()
    elif mode == "transatlantic":
        from capital_manifold.pipeline.run_transatlantic_traversal import main as transatlantic_main
        transatlantic_main()
    else:
        print(f"Unknown traversal mode: {mode}")
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="capital-manifold",
        description="Capital Manifold: Institutional Planetary Balance-Sheet Network Dynamics & Siphon Forensics Engine.",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # Subcommand: audit
    audit_parser = subparsers.add_parser(
        "audit",
        help="Run comprehensive adversarial system integrity & double-entry conservation audit",
    )
    audit_parser.add_argument(
        "--duckdb-path",
        type=str,
        default=None,
        help="Path to DuckDB database (default: data/cache/manifold.duckdb)",
    )
    audit_parser.add_argument(
        "--output-json",
        type=str,
        default=None,
        help="Optional path to output audit scorecard as JSON",
    )

    # Subcommand: siphon
    siphon_parser = subparsers.add_parser(
        "siphon",
        help="Run automated siphon & structural discrepancy hunter",
    )
    siphon_parser.add_argument(
        "--duckdb",
        type=str,
        default=None,
        help="Path to DuckDB database (default: data/cache/manifold.duckdb)",
    )
    siphon_parser.add_argument(
        "--output-json",
        type=str,
        default=None,
        help="Path to output structured JSON audit report",
    )
    siphon_parser.add_argument(
        "--cif-fob-pct",
        type=float,
        default=None,
        help="Standard CIF/FOB margin percentage (default: 6.0 percent)",
    )
    siphon_parser.add_argument(
        "--sigma-threshold",
        type=float,
        default=5.0,
        help="Outlier sigma threshold for custody nominee identification (default: 5.0)",
    )

    # Subcommand: simulate
    simulate_parser = subparsers.add_parser(
        "simulate",
        help="Execute systemic shock simulation gauntlet across crisis regimes",
    )
    simulate_parser.add_argument(
        "--output-json",
        type=str,
        default=None,
        help="Optional destination path for simulation report JSON",
    )

    # Subcommand: serve
    serve_parser = subparsers.add_parser(
        "serve",
        help="Launch interactive Cytoscape web dashboard and REST API server",
    )
    serve_parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host interface to bind (default: 127.0.0.1)",
    )
    serve_parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="Port to listen on (default: 8765)",
    )
    serve_parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development",
    )

    # Subcommand: traverse
    traverse_parser = subparsers.add_parser(
        "traverse",
        help="Execute non-greedy dual-frontier A* path discovery across monetary corridors",
    )
    traverse_parser.add_argument(
        "--mode",
        choices=["macro", "planetary", "global", "transatlantic"],
        default="macro",
        help="Monetary corridor to traverse: macro, planetary, global, transatlantic (default: macro)",
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.subcommand:
        parser.print_help()
        return 0

    handler_map = {
        "audit": _cmd_audit,
        "siphon": _cmd_siphon,
        "simulate": _cmd_simulate,
        "serve": _cmd_serve,
        "traverse": _cmd_traverse,
    }

    handler = handler_map.get(args.subcommand)
    if handler:
        return handler(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
