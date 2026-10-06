from __future__ import annotations
import sys
import logging
from pathlib import Path

# Add src to pythonpath
src_dir = Path(__file__).resolve().parent.parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from capital_manifold.harvesters.france import FranceMacroHarvester
from capital_manifold.storage.duckdb_store import ManifoldStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("run_france")

def main():
    print("=" * 80)
    print(" CAPITAL MANIFOLD: AUTONOMOUS FRANCE LIQUIDITY & DEBT INGESTION HARVESTER")
    print("=" * 80)

    store = ManifoldStore()
    with FranceMacroHarvester() as harvester:
        events = harvester.harvest()
        stress = harvester.compute_stress_snapshot()

    count = store.insert_flow_events(events)
    snap_id = store.insert_stress_snapshot(stress)
    store.export_parquet()

    print("\n" + "#" * 80)
    print(f" HARVEST SUMMARY: {count} FlowEvents Ingested to DuckDB & Parquet")
    print("#" * 80)
    print(f" * Jurisdiction:                     {stress.jurisdiction} (French Republic)")
    print(f" * French 10Y Benchmark (OAT Yield): {stress.oat_10y_yield:.2f}%")
    print(f" * German 10Y Benchmark (Bund):      {stress.bund_10y_yield:.3f}%")
    print(f" * OAT-Bund Spread (Risk Friction):  +{stress.oat_bund_spread_bp:.1f} basis points")
    print(f" * Banque de France TARGET2 Deficit: {stress.target2_net_position_eur / 1e9:,.2f} Billion EUR")
    print(f" * French Maastricht Gross Debt:     {stress.maastricht_debt_nominal_eur / 1e9:,.1f} Billion EUR ({stress.maastricht_debt_pct_gdp:.1f}% GDP)")
    print(f" * Monthly Trade Bleed (Deficit):    {stress.latest_monthly_trade_deficit_eur / 1e9:,.2f} Billion EUR / month")
    print(f" * Net Liquidity Pressure Score:     {stress.net_liquidity_pressure_score:.1f} / 100.0 (Elevated Sovereign Stress)")
    print("#" * 80)

    print("\nSample Flow Records in DuckDB:")
    df = store.query_df("SELECT period_label, instrument, nominal_amount, flow_type, data_source FROM flow_events ORDER BY timestamp DESC LIMIT 10")
    print(df.to_string(index=False))

    store.close()
    print("\n[OK] Pipeline completed successfully.")

if __name__ == "__main__":
    main()
