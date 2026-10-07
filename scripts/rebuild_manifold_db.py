"""Rebuild and Refresh Capital Manifold DuckDB and Parquet Store.

Executes all 6 statutory harvesters:
1. FranceMacroHarvester
2. FedDarkForestRing2Harvester
3. TransatlanticHarvester
4. TranspacificCorporateHarvester
5. PlanetaryMacroHarvester
6. DarkMatterHarvester

Clears legacy tables, inserts all normalized FlowEvents and MacroStressSnapshots,
and exports clean Parquet files to data/processed/.
"""

import sys
import logging
from pathlib import Path

# Add src to sys.path
src_dir = Path(__file__).resolve().parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from capital_manifold.storage.duckdb_store import ManifoldStore
from capital_manifold.harvesters.france import FranceMacroHarvester
from capital_manifold.harvesters.fed_dark_forest_ring2 import DarkForestRing2Harvester
from capital_manifold.harvesters.us_transatlantic import TransatlanticMacroHarvester
from capital_manifold.harvesters.transpacific_corporate import TranspacificCorporateHarvester
from capital_manifold.harvesters.planetary_macro import PlanetaryMacroHarvester
from capital_manifold.harvesters.dark_matter import DarkMatterHarvester
from capital_manifold.harvesters.private_assets import PrivateAssetsHarvester

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("rebuild_db")


def main():
    store = ManifoldStore()
    logger.info("Dropping legacy tables in DuckDB to ensure zero schema or dimensional leakage...")
    store.conn.execute("DROP TABLE IF EXISTS flow_events;")
    store.conn.execute("DROP TABLE IF EXISTS macro_stress_snapshots;")
    store._init_tables()

    total_events = 0

    # 1. France Macro Harvester
    logger.info("Harvesting France Macro...")
    with FranceMacroHarvester() as h_fr:
        fr_events = h_fr.harvest()
        stress = h_fr.compute_stress_snapshot()
        c1 = store.insert_flow_events(fr_events)
        store.insert_stress_snapshot(stress)
        total_events += c1

    # 2. Transatlantic Harvester
    logger.info("Harvesting Transatlantic...")
    with TransatlanticMacroHarvester() as h_ta:
        ta_events = h_ta.harvest()
        c2 = store.insert_flow_events(ta_events)
        total_events += c2

    # 3. Fed Dark Forest Ring 2
    logger.info("Harvesting Fed Dark Forest Ring 2...")
    with DarkForestRing2Harvester() as h_df:
        df_events = h_df.harvest()
        c3 = store.insert_flow_events(df_events)
        total_events += c3

    # 4. Transpacific Corporate
    logger.info("Harvesting Transpacific Corporate...")
    with TranspacificCorporateHarvester() as h_tp:
        tp_events = h_tp.harvest()
        c4 = store.insert_flow_events(tp_events)
        total_events += c4

    # 5. Planetary Macro
    logger.info("Harvesting Planetary Macro...")
    with PlanetaryMacroHarvester() as h_pm:
        pm_events = h_pm.harvest()
        c5 = store.insert_flow_events(pm_events)
        total_events += c5

    # 6. Dark Matter
    logger.info("Harvesting Global Macro Dark Matter...")
    with DarkMatterHarvester() as h_dm:
        dm_events = h_dm.harvest()
        c6 = store.insert_flow_events(dm_events)
        total_events += c6

    # 7. Private Asset Portfolios & Principal Holdings
    logger.info("Harvesting Private Asset Portfolios & Principal Holdings...")
    with PrivateAssetsHarvester() as h_pa:
        pa_events = h_pa.harvest()
        c7 = store.insert_flow_events(pa_events)
        total_events += c7

    logger.info(f"Total FlowEvents inserted into DuckDB: {total_events}")

    # Export Parquet
    processed_dir = Path("/home/ubuntu/repos/capital-manifold/data/processed")
    store.export_parquet(output_dir=processed_dir)
    logger.info("Clean Parquet files exported successfully.")

    store.close()
    print(f"SUCCESS: Database rebuilt with {total_events} FlowEvents across 7 harvesters.")


if __name__ == "__main__":
    main()
